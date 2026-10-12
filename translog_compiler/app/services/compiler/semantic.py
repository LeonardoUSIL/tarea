"""Fase 3 – Análisis semántico: reglas de negocio sobre el AST (sede, año, correlativo, duplicado)."""
from datetime import datetime

from app.models import ErrorCompilacion, Fase


class AnalizadorSemantico:
    def __init__(self, catalogo, repositorio_guias, anio_min=2020, anio_max=None):
        self.catalogo = catalogo
        self.guias = repositorio_guias
        self.anio_min = anio_min
        self._anio_max = anio_max

    @property
    def anio_max(self):
        return self._anio_max or datetime.now().year

    def analizar(self, guia):
        errores = []
        sede, anio, corr = guia.sede, guia.anio, guia.correlativo
        if not self.catalogo.existe(sede.lexema):
            errores.append(self._err("SEM001", f"La sede '{sede.lexema}' no existe en el catálogo ({', '.join(self.catalogo.codigos())}).", sede))
        if not (self.anio_min <= int(anio.lexema) <= self.anio_max):
            errores.append(self._err("SEM002", f"El año {anio.lexema} está fuera del rango permitido ({self.anio_min}–{self.anio_max}).", anio))
        if int(corr.lexema) == 0:
            errores.append(self._err("SEM003", "El correlativo 000000 no es válido: debe empezar en 000001.", corr))
        if not errores and self.guias.existe(guia.codigo_normalizado):
            errores.append(self._err("SEM004", f"Correlativo duplicado: la guía {guia.codigo_normalizado} ya fue emitida.", corr))
        return errores

    @staticmethod
    def _err(codigo, mensaje, token):
        return ErrorCompilacion(Fase.SEMANTICO, codigo, mensaje, token.posicion, token.lexema)
