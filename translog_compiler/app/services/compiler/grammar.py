"""Gramática libre de contexto (GLC) de la guía de remisión.

    GUIA     -> CABECERA GUION CUERPO
    CABECERA -> PREFIJO GUION SEDE
    CUERPO   -> ANIO GUION CORRELATIVO

Terminales: PREFIJO GUION SEDE ANIO CORRELATIVO (los tokens del lexer).
Es LL(1): cada no terminal tiene una única producción.
Lenguaje equivalente (regex):  ^GR-[A-Z]{3}-[0-9]{4}-[0-9]{6}$
"""
SIMBOLO_INICIAL = "GUIA"

PRODUCCIONES = {
    "GUIA": ["CABECERA", "GUION", "CUERPO"],
    "CABECERA": ["PREFIJO", "GUION", "SEDE"],
    "CUERPO": ["ANIO", "GUION", "CORRELATIVO"],
}

TERMINALES = ["PREFIJO", "GUION", "SEDE", "ANIO", "CORRELATIVO"]

DESCRIPCION_TERMINAL = {
    "PREFIJO": "el prefijo 'GR'",
    "GUION": "un guion '-'",
    "SEDE": "el código de sede (3 letras)",
    "ANIO": "el año (4 dígitos)",
    "CORRELATIVO": "el correlativo (6 dígitos)",
}


def gramatica_texto() -> list:
    return [f"{nt} → {' '.join(prod)}" for nt, prod in PRODUCCIONES.items()]
