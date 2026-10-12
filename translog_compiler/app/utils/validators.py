"""Validaciones de entrada previas a la compilación (no confundir con el análisis léxico-sintáctico)."""


def longitud_valida(texto: str, maximo: int) -> bool:
    return len(texto) <= maximo


def lote_valido(codigos: list, maximo: int) -> bool:
    return 0 < len(codigos) <= maximo
