"""
Módulo para validación de URLs y otros inputs
"""

from urllib.parse import urlparse
from typing import Optional

def validate_url(url: str) -> str:
    """
    Valida y normaliza una URL, asegurando que tenga el formato correcto.
    
    Args:
        url: La URL a validar
        
    Returns:
        La URL validada y normalizada
        
    Raises:
        ValueError: Si la URL no es válida
    """
    if not url:
        raise ValueError("URL no puede estar vacía")
    
    if not isinstance(url, str):
        raise ValueError("URL debe ser una cadena de texto")
    
    # Añadir esquema si no está presente
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    parsed = urlparse(url)
    
    if not parsed.netloc:
        raise ValueError("URL inválida - falta dominio o es incorrecto")
    
    # Normalizar la URL eliminando fragmentos y parámetros de consulta si es necesario
    normalized_url = parsed._replace(
        query="", 
        fragment="", 
        path=parsed.path.rstrip('/')
    ).geturl()
    
    return normalized_url

def is_excluded_url(url: str, exclude_patterns: list) -> bool:
    """
    Determina si una URL debe ser excluida del escaneo.
    
    Args:
        url: La URL a verificar
        exclude_patterns: Lista de patrones a excluir
        
    Returns:
        True si la URL debe ser excluida, False en caso contrario
    """
    excluded_ext = ['.jpg', '.jpeg', '.png', '.gif', '.css', '.js', '.pdf', '.svg']
    excluded_schemes = ['javascript:', 'mailto:', 'tel:', '#', 'data:']
    
    if any(pattern in url for pattern in exclude_patterns):
        return True
        
    if any(url.endswith(ext) for ext in excluded_ext):
        return True
        
    if any(url.startswith(scheme) for scheme in excluded_schemes):
        return True
        
    return False
