<h1 align="center">WebSpectre 🔎</h1>

<p align="center">
  Escáner web avanzado que permite detectar enlaces válidos de sitios y generar reportes en múltiples formatos.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11+-blue.svg" alt="Python version">
  <img src="https://img.shields.io/badge/Estado-En%20Desarrollo-yellow.svg" alt="Estado">
  <img src="https://img.shields.io/badge/Reportes-PDF%20%7C%20JSON-green.svg" alt="Formatos de reporte">
</p>

---

## 🧠 Descripción

**WebSpectre** es una herramienta de escaneo web desarrollada en Python. Realiza análisis profundos o rápidos de sitios web, identificando enlaces válidos y generando reportes automáticos en JSON y PDF. Ideal para análisis de seguridad básicos o auditorías web.

---

## ⚙️ Instalación

Clona el repositorio:

```bash
git clone https://github.com/HackUnderway/webspectre.git
```
```bash
cd webspectre
```
```bash
pip install -r requirements.txt
```
```bash
python -m webspectre_scanner -h
```
```bash
usage: python -m webspectre_scanner [url] [-h] [-d DEPTH] [-o OUTPUT] [--fast-scan] [--max-pages MAX_PAGES] [--no-verify]

WebSpectre Scanner - Escáner web avanzado con verificación de URLs

positional arguments:
  url                   URL objetivo a escanear (ej. https://example.com)

options:
  -h, --help            show this help message and exit
  -d, --depth DEPTH     Profundidad máxima de escaneo (predeterminado: 2)
  -o, --output OUTPUT   Directorio para guardar reportes (se creará si no existe)
  --fast-scan           Modo rápido (limita páginas por sección y excluye APIs)
  --max-pages MAX_PAGES
                        Límite de páginas por sección (predeterminado: 20)
  --no-verify           Deshabilitar verificación SSL

Ejemplos de uso:
  Escaneo básico: python -m webspectre_scanner https://example.com
  Escaneo profundo: python -m webspectre_scanner https://example.com -d 3 -o reportes
  Escaneo rápido: python -m webspectre_scanner https://example.com --fast-scan
```
## 🚀 Uso
##### Escaneo básico
python -m webspectre_scanner https://example.com

##### Escaneo profundo con reportes
python -m webspectre_scanner https://example.com -d 3 -o reportes

##### Escaneo rápido
python -m webspectre_scanner https://example.com --fast-scan

<p align="center">
  <img src="assets/WebSpectre.png" alt="WebSpectre" width="600"/>
</p>

> **El proyecto está abierto a colaboradores.**

# DISTRIBUCIONES SOPORTADAS
|Distribución | Versión verificada | 	¿Soportado? | 	Estado |
|--------------|--------------------|------|-------|
|Kali Linux| 2025.1| si| funcionando   |
|Parrot Security OS| 6.2| si | funcionando   |
|Windows| 11 | si | funcionando   |
|BackBox| 9 | si | funcionando   |
|Arch Linux| 2024.12.01 | si | funcionando   |

# SOPORTE
Preguntas, errores o sugerencias: info@hackunderway.com

# LICENSE
- [x] WebSpectre tiene licencia.
- [x] Consulta el archivo [LICENSE](https://github.com/HackUnderway/webspectre#MIT-1-ov-file) para más información.

# CYBERSECURITY RESEARCHER

* [Victor Bancayan](https://www.offsec.com/bug-bounty-program/) - (**CEO at [Hack Underway](https://www.instagram.com/hackunderway/)**) 

## 🔗 ENLACES
[![PATREON](https://img.shields.io/badge/patreon-000000?style=for-the-badge&logo=Patreon&logoColor=white)](https://www.patreon.com/c/HackUnderway)
```
Fanpage: https://www.facebook.com/HackUnderway
X: https://x.com/JeyZetaOficial
Web site: https://hackunderway.com
Youtube: https://www.youtube.com/@JeyZetaOficial
```
## 🌞 Suscripciones
Afíliate:

- [Jey Zeta](https://www.facebook.com/JeyZetaOficial/subscribe/)

[![Kali Linux Badge](https://img.shields.io/badge/Kali%20Linux-1793D1?logo=kalilinux&logoColor=fff&style=plastic)](https://www.kali.org/)

from <img src="https://i.imgur.com/ngJCbSI.png" title="Perú"> made in <img src="https://i.imgur.com/NNfy2o6.png" title="Python"> with <img src="https://i.imgur.com/S86RzPA.png" title="Love"> by: <font color="red">Victor Bancayan</font>, if you want Donate <a href="https://www.buymeacoffee.com/HackUnderway"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=HackUnderway&button_colour=40DCA5&font_colour=ffffff&font_family=Comic&outline_colour=000000&coffee_colour=FFDD00" /></a>

© 2025

