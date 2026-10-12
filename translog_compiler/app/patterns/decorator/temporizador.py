"""Patrón Decorator: mide el tiempo de compilación y verifica el RNF1 (<= 1 s por código)."""
import functools
import time


def medir_tiempo(limite_ms: float = 1000.0):
    def decorador(funcion):
        @functools.wraps(funcion)
        def envoltura(*args, **kwargs):
            inicio = time.perf_counter()
            resultado = funcion(*args, **kwargs)
            resultado.tiempo_ms = round((time.perf_counter() - inicio) * 1000, 3)
            resultado.cumple_rnf1 = resultado.tiempo_ms <= limite_ms
            return resultado
        return envoltura
    return decorador
