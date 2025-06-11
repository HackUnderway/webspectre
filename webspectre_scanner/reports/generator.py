"""
Módulo para generar reportes de escaneo
"""

import json
import os
import time
from datetime import datetime
from dataclasses import dataclass
from urllib.parse import urlparse

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


@dataclass
class ScanReport:
    metadata: dict
    stats: dict
    valid_links: list
    errors: list
    filename: str = None

    def to_dict(self):
        """Convierte el reporte a diccionario"""
        return {
            "metadata": self.metadata,
            "stats": self.stats,
            "valid_links": sorted(self.valid_links),
            "errors": self.errors
        }

    def save(self, output_dir=None):
        """Guarda el reporte en un archivo JSON y PDF"""
        report_data = self.to_dict()
        
        target = self.metadata['target']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        json_name = f"scan_{target}_{timestamp}.json"
        pdf_name = f"scan_{target}_{timestamp}.pdf"

        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            json_path = os.path.join(output_dir, json_name)
            pdf_path = os.path.join(output_dir, pdf_name)
        else:
            json_path = json_name
            pdf_path = pdf_name

        self.filename = json_path

        # Guardar JSON
        with open(json_path, 'w') as f:
            json.dump(report_data, f, indent=2)

        # Guardar PDF
        self._save_pdf(pdf_path)

        return self.filename

    def _save_pdf(self, pdf_path):
        """Guarda el reporte como un archivo PDF"""
        c = canvas.Canvas(pdf_path, pagesize=letter)
        width, height = letter
        y = height - 40

        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, y, f"WebSpectre Report - {self.metadata['target']}")
        y -= 30

        c.setFont("Helvetica", 12)
        c.drawString(30, y, f"Fecha de escaneo: {self.metadata['scan_date']}")
        y -= 20
        c.drawString(30, y, f"Duración: {self.metadata['duration_sec']} segundos")
        y -= 20
        c.drawString(30, y, f"URLs válidas: {self.stats['valid_urls']}")
        y -= 20
        c.drawString(30, y, f"URLs inválidas: {self.stats['invalid_urls']}")
        y -= 20
        c.drawString(30, y, f"Errores: {self.stats['error_count']}")
        y -= 30

        c.setFont("Helvetica-Bold", 12)
        c.drawString(30, y, "URLs válidas:")
        y -= 20
        c.setFont("Helvetica", 10)
        for link in self.valid_links[:30]:  # Limita a 30 para evitar desbordes
            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - 40
            c.drawString(40, y, link)
            y -= 15

        if len(self.valid_links) > 30:
            c.drawString(40, y, "... (más URLs no mostradas)")
            y -= 20

        if y < 80:
            c.showPage()
            y = height - 40

        c.setFont("Helvetica-Bold", 12)
        c.drawString(30, y, "Errores encontrados:")
        y -= 20
        c.setFont("Helvetica", 10)
        for err in self.errors[:15]:  # También limitar
            if y < 40:
                c.showPage()
                c.setFont("Helvetica", 10)
                y = height - 40
            c.drawString(40, y, err[:90])  # Acortar texto
            y -= 15

        c.save()


def generate_report(visited, valid_links, invalid_links, errors, start_time, args):
    """Genera un reporte estructurado del escaneo"""
    elapsed = time.time() - start_time
    target = urlparse(next(iter(visited))).netloc if visited else "unknown"
    
    return ScanReport(
        metadata={
            "target": target,
            "scan_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration_sec": round(elapsed, 2),
            "config": {
                "max_depth": args.depth,
                "max_pages": args.max_pages,
                "excluded_paths": ['wp-json', 'feed', 'wp-admin', 'xmlrpc.php', 'oembed']
            }
        },
        stats={
            "valid_urls": len(valid_links),
            "invalid_urls": len(invalid_links),
            "error_count": len(errors)
        },
        valid_links=list(valid_links),
        errors=errors
    )
