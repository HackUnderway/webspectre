"""
Módulo para manejar la interfaz de línea de comandos
"""

import argparse

def parse_arguments():
    """Configura y parsea los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        prog='python -m webspectre_scanner',
        usage='python -m webspectre_scanner [url] [-h] [-d DEPTH] [-o OUTPUT] [--fast-scan] [--max-pages MAX_PAGES] [--no-verify]',
        description="WebSpectre Scanner - Escáner web avanzado con verificación de URLs",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Ejemplos de uso:
  Escaneo básico: python -m webspectre_scanner https://example.com
  Escaneo profundo: python -m webspectre_scanner https://example.com -d 3 -o reportes
  Escaneo rápido: python -m webspectre_scanner https://example.com --fast-scan"""
    )

    parser.add_argument(
        'url',
        nargs='?',
        help='URL objetivo a escanear (ej. https://example.com)'
    )
    parser.add_argument(
        '-d', '--depth',
        type=int,
        default=2,
        help='Profundidad máxima de escaneo (predeterminado: 2)'
    )
    parser.add_argument(
        '-o', '--output',
        help='Directorio para guardar reportes (se creará si no existe)'
    )
    parser.add_argument(
        '--fast-scan',
        action='store_true',
        help='Modo rápido (limita páginas por sección y excluye APIs)'
    )
    parser.add_argument(
        '--max-pages',
        type=int,
        default=20,
        help='Límite de páginas por sección (predeterminado: 20)'
    )
    parser.add_argument(
        '--no-verify',
        action='store_true',
        help='Deshabilitar verificación SSL'
    )

    return parser.parse_args()
