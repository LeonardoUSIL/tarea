"""Catálogo de sedes (Singleton). Se carga una vez desde database/seeds/sedes.json.

RNF3: agregar una sede nueva = agregar una línea al JSON; el autómata y la gramática no cambian.
"""
from pathlib import Path

from app.utils.helpers import leer_json
from .singleton import Singleton


class CatalogoSedes(metaclass=Singleton):
    def __init__(self, ruta):
        datos = leer_json(Path(ruta))
        self._sedes = {s["codigo"]: s["nombre"] for s in datos["sedes"]}

    def existe(self, codigo: str) -> bool:
        return codigo in self._sedes

    def codigos(self):
        return sorted(self._sedes)

    def todas(self) -> dict:
        return dict(self._sedes)
