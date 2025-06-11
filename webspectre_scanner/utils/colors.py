"""
Módulo para manejar colores y efectos visuales
"""

import sys
from typing import NamedTuple

class Color(NamedTuple):
    red: int
    green: int
    blue: int

    @staticmethod
    def from_hex(hex_color: str):
        """Crea un color desde un código hexadecimal."""
        hex_color = hex_color.lstrip("#")
        return Color(int(hex_color[:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16))

    @staticmethod
    def lerp(start, end, alpha: float):
        """Interpola entre dos colores."""
        return Color(
            int(start.red + (end.red - start.red) * alpha),
            int(start.green + (end.green - start.green) * alpha),
            int(start.blue + (end.blue - start.blue) * alpha),
        )

def print_shaded_text(text, start_color=None, end_color=None):
    """Imprime texto con degradado entre start_color y end_color."""
    start_color = start_color or Color(0, 80, 0)    # Verde oscuro
    end_color = end_color or Color(0, 255, 127)     # Verde claro
    
    for index, char in enumerate(text):
        alpha = index / max(len(text) - 1, 1)
        color = Color.lerp(start_color, end_color, alpha)
        color_code = f"\033[38;2;{color.red};{color.green};{color.blue}m"
        sys.stdout.write(f"{color_code}{char}\033[0m")
    sys.stdout.write("\n")
