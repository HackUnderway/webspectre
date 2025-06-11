#!/usr/bin/env python3
"""
Punto de entrada principal para WebSpectre Scanner
"""

from webspectre_scanner.cli import parse_arguments
from webspectre_scanner.scanner import WebSpectreScanner

def main():
    """Función principal que orquesta el escaneo"""
    args = parse_arguments()
    scanner = WebSpectreScanner(args)
    
    try:
        scanner.run_scan()
    except KeyboardInterrupt:
        scanner.handle_interrupt()
    except Exception as e:
        scanner.handle_error(e)
    finally:
        scanner.cleanup()

if __name__ == "__main__":
    main()
