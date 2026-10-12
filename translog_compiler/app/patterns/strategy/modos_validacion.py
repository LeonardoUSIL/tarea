"""Patrón Strategy: modos intercambiables de preparar la entrada antes de compilar.

- estricto:   el código se compila tal cual (como lo exigiría el sistema de facturación).
- tolerante:  recorta espacios y pasa a MAYÚSCULAS, avisando de cada corrección.
"""
from abc import ABC, abstractmethod


class EstrategiaEntrada(ABC):
    nombre = ""
    descripcion = ""

    @abstractmethod
    def preparar(self, texto: str):
        """Devuelve (texto_a_compilar, advertencias)."""


class ModoEstricto(EstrategiaEntrada):
    nombre = "estricto"
    descripcion = "Valida el código exactamente como fue digitado."

    def preparar(self, texto):
        return texto, []


class ModoTolerante(EstrategiaEntrada):
    nombre = "tolerante"
    descripcion = "Recorta espacios y convierte a mayúsculas antes de validar."

    def preparar(self, texto):
        advertencias = []
        limpio = texto.strip()
        if limpio != texto:
            advertencias.append("Se eliminaron espacios al inicio/fin del código.")
        mayus = limpio.upper()
        if mayus != limpio:
            advertencias.append("Se convirtieron minúsculas a MAYÚSCULAS.")
        return mayus, advertencias


MODOS = {m.nombre: m() for m in (ModoEstricto, ModoTolerante)}
