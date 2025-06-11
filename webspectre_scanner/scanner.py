"""
Módulo principal que contiene la lógica del escáner
"""

import os
import time
import random
from typing import NamedTuple, Set, Dict, List
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from bs4 import BeautifulSoup
from bs4 import XMLParsedAsHTMLWarning
import warnings

from colorama import Fore, Back, Style
from rich.console import Console

from webspectre_scanner.utils.colors import print_shaded_text
from webspectre_scanner.utils.validator import validate_url, is_excluded_url
from webspectre_scanner.reports.generator import generate_report
from datetime import datetime

from typing import NamedTuple

class Color(NamedTuple):
    """Representación de un color RGB"""
    red: int
    green: int
    blue: int

    @staticmethod
    def from_hex(hex_color: str) -> 'Color':
        """Crea un color desde un código hexadecimal"""
        hex_color = hex_color.lstrip("#")
        return Color(
            int(hex_color[:2], 16),
            int(hex_color[2:4], 16),
            int(hex_color[4:6], 16)
        )

    @staticmethod
    def lerp(start: 'Color', end: 'Color', alpha: float) -> 'Color':
        """Interpola linealmente entre dos colores"""
        return Color(
            int(start.red + (end.red - start.red) * alpha),
            int(start.green + (end.green - start.green) * alpha),
            int(start.blue + (end.blue - start.blue) * alpha),
        )

# Configuración inicial
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

class WebSpectreScanner:
    def __init__(self, args):
        self.args = args
        self.visited: Set[str] = set()
        self.valid_links: Set[str] = set()
        self.invalid_links: Set[str] = set()
        self.errors: List[str] = []
        self.url_status_cache: Dict[str, tuple] = {}
        self.start_time = None
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5'
        })
        
        self.settings = {
            'max_pages_per_section': args.max_pages,
            'exclude_paths': ['wp-json', 'feed', 'wp-admin', 'xmlrpc.php', 'oembed'],
            'trust_categories': True,
            'verify_ssl': not args.no_verify
        }
        
        if args.fast_scan:
            self.settings.update({
                'max_pages_per_section': 10,
                'trust_categories': True,
                'exclude_paths': self.settings['exclude_paths'] + ['api', 'ajax']
            })

    def print_banner(self):
        """Muestra el banner de la herramienta con efecto degradado"""
        # Definir colores para el degradado (verde oscuro a verde claro)
        start_color = Color(0, 80, 0)    # Verde oscuro
        end_color = Color(0, 255, 127)   # Verde claro
        
        banner_lines = [
"▄▄▌ ▐ ▄▌▄▄▄ .▄▄▄▄· .▄▄ ·  ▄▄▄·▄▄▄ . ▄▄· ▄▄▄▄▄▄▄▄  ▄▄▄ .",
"██· █▌▐█▀▄.▀·▐█ ▀█▪▐█ ▀. ▐█ ▄█▀▄.▀·▐█ ▌▪•██  ▀▄ █·▀▄.▀·",
"██▪▐█▐▐▌▐▀▀▪▄▐█▀▀█▄▄▀▀▀█▄ ██▀·▐▀▀▪▄██ ▄▄ ▐█.▪▐▀▀▄ ▐▀▀▪▄",
"▐█▌██▐█▌▐█▄▄▌██▄▪▐█▐█▄▪▐█▐█▪·•▐█▄▄▌▐███▌ ▐█▌·▐█•█▌▐█▄▄▌",
" ▀▀▀▀ ▀▪ ▀▀▀ ·▀▀▀▀  ▀▀▀▀ .▀    ▀▀▀ ·▀▀▀  ▀▀▀ .▀  ▀ ▀▀▀"
#"The Silent WebSpectre Scanner - By: Jey Zeta & Frank Prime,
        ]
        
        # Imprimir cada línea del banner con degradado
        for line in banner_lines:
            print_shaded_text(line, start_color, end_color)
            
        credits_text = "The Silent WebSpectre Scanner - By: Jey Zeta & Frank Prime"
        print_shaded_text(credits_text, start_color, end_color)
        
        from rich.console import Console
        console = Console()
        texto = f"[blink]{' ' * 15}🔥 hackunderway.com 🔥[/]"
        console.print(texto, style="bold red")
        
        #credits_text = "The Silent WebSpectre Scanner - By: Jey Zeta & Frank Prime"
        #print_shaded_text(credits_text, start_color=Color(0, 80, 0), end_color=Color(0, 255, 127))
        
        # La última línea con estilo especial
        #print(f"{banner_lines[-1]}\n")
	
    def run_scan(self):
        """Ejecuta el escaneo completo"""
        self.print_banner()
        
        target_url = self.args.url if self.args.url else input("\n[ 🌐] Enter URL (e.g., https://example.com): ")
        validated_url = validate_url(target_url)
        
        print("\n[*] Configuración:")
        print(f"  - URL: {validated_url}")
        print(f"  - Profundidad: {self.args.depth}")
        print(f"  - Páginas máx/sección: {self.settings['max_pages_per_section']}")
        print(f"  - Modo rápido: {'Sí' if self.args.fast_scan else 'No'}")
        print(f"  - Verificar SSL: {'No' if self.args.no_verify else 'Sí'}")
        
        print("\n[~] Iniciando escaneo...")
        self.start_time = time.time()
        self.scan_site(validated_url, max_depth=self.args.depth)
        
        report = generate_report(
            visited=self.visited,
            valid_links=self.valid_links,
            invalid_links=self.invalid_links,
            errors=self.errors,
            start_time=self.start_time,
            args=self.args
        )
        
        if self.args.output:
            os.makedirs(self.args.output, exist_ok=True)
        
        report.save(self.args.output)
        
        print("\n[+] === Resumen del Escaneo ===")
        print(f"  - URLs válidas encontradas: {report.stats['valid_urls']}")
        print(f"  - URLs inválidas detectadas: {report.stats['invalid_urls']}")
        print(f"  - Errores: {report.stats['error_count']}")
        print(f"  - Duración: {report.metadata['duration_sec']} segundos")
        print(f"  - Reporte JSON: {report.filename}")
        pdf_path = report.filename.replace('.json', '.pdf')
        print(f"  - Reporte PDF:  {pdf_path}")

    def scan_site(self, start_url, max_depth=2):
        """Escaneo principal del sitio con BFS optimizado"""
        queue = [(start_url, 0)]
        self.visited.add(start_url)
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = {}
            
            while queue or futures:
                while queue and len(futures) < 3:
                    current_url, depth = queue.pop(0)
                    
                    if '/page/' in current_url:
                        page_num = int(current_url.split('/page/')[1].split('/')[0])
                        if page_num > self.settings['max_pages_per_section']:
                            continue
                    
                    futures[executor.submit(self.scan_page, current_url)] = (current_url, depth)
                
                for future in as_completed(futures):
                    current_url, depth = futures.pop(future)
                    new_links = future.result()
                    
                    for link in new_links:
                        if link not in self.visited:
                            self.visited.add(link)
                            is_valid, status = self.check_url_status(link)
                            
                            if is_valid:
                                self.valid_links.add(link)
                                if depth + 1 <= max_depth:
                                    queue.append((link, depth + 1))
                            else:
                                self.invalid_links.add(link)
                    
                    time.sleep(random.uniform(1, 3))

    def scan_page(self, url):
        """Escanea una página individual en busca de enlaces"""
        try:
            is_valid, status = self.check_url_status(url)
            if not is_valid:
                self.invalid_links.add(url)
                return []

            self.valid_links.add(url)
            print(f"\n[+] Escaneando: {url}", flush=True)

            response = self.session.get(url, timeout=15)
            soup = BeautifulSoup(response.text, 'html.parser')
            found_links = []
            
            tags_map = {
                'a': ['href'],
                'link': ['href'],
                'script': ['src'],
                'iframe': ['src']
            }
            
            for tag, attrs in tags_map.items():
                for element in soup.find_all(tag):
                    for attr in attrs:
                        if element.has_attr(attr):
                            new_url = self.process_link(url, element[attr])
                            if new_url:
                                found_links.append(new_url)
            
            return found_links

        except Exception as e:
            error_msg = f"\n[!] Error en {url}: {str(e)}"
            print(error_msg, flush=True)
            self.errors.append(error_msg)
            return []

    def process_link(self, base_url, link):
        """Procesa y normaliza un enlace encontrado"""
        if not link or is_excluded_url(link, self.settings['exclude_paths']):
            return None
            
        new_url = urljoin(base_url, link)
        parsed = urlparse(new_url)
        new_url = parsed._replace(query="", fragment="").geturl()
        
        if parsed.netloc == urlparse(base_url).netloc and new_url not in self.visited:
            return new_url
        return None

    def check_url_status(self, url):
        """Verifica el estado de una URL con caching"""
        if url in self.url_status_cache:
            return self.url_status_cache[url]
        
        if self.settings['trust_categories'] and ('/category/' in url or '/page/' in url):
            return (True, 200)
            
        try:
            response = self.session.head(
                url, 
                timeout=10,
                allow_redirects=True,
                verify=self.settings['verify_ssl']
            )
            is_valid = response.status_code < 400
            self.url_status_cache[url] = (is_valid, response.status_code)
            return (is_valid, response.status_code)
        except Exception as e:
            print(f"\n[!] Error al verificar {url}: {str(e)}", flush=True)
            self.url_status_cache[url] = (False, 0)
            return (False, 0)

    def handle_interrupt(self):
        """Maneja la interrupción por teclado"""
        print("\n[!] Escaneo interrumpido. Generando reporte parcial...")
        report = generate_report(
            visited=self.visited,
            valid_links=self.valid_links,
            invalid_links=self.invalid_links,
            errors=self.errors,
            start_time=self.start_time,
            args=self.args
        )
        partial_name = f"partial_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        if self.args.output:
            partial_name = os.path.join(self.args.output, partial_name)
        with open(partial_name, 'w') as f:
            json.dump(report.to_dict(), f, indent=2)
        print(f"\n[!] Reporte parcial guardado como: {partial_name}")

    def handle_error(self, error):
        """Maneja errores durante el escaneo"""
        print(f"\n[!] Error crítico: {str(error)}")
        self.errors.append(str(error))

    def cleanup(self):
        """Limpia recursos y cierra la sesión"""
        self.session.close()
        print("\n[+] Limpieza completada. Sesión cerrada.")
