"""Fase 4 – Generación de código objeto: registro normalizado + instrucción SQL parametrizada."""


def generar_registro(guia) -> dict:
    codigo = guia.codigo_normalizado
    sede, anio, correlativo = guia.sede.lexema, int(guia.anio.lexema), int(guia.correlativo.lexema)
    return {
        "codigo": codigo,
        "prefijo": guia.prefijo.lexema,
        "sede": sede,
        "anio": anio,
        "correlativo": correlativo,
        "instruccion_sql": "INSERT INTO guias_emitidas (codigo, sede, anio, correlativo) VALUES (?, ?, ?, ?)",
        "parametros": [codigo, sede, anio, correlativo],
    }
