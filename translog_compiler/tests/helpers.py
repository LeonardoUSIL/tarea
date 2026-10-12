"""Utilidades compartidas por las pruebas."""
import tempfile
from pathlib import Path

from app import create_app
from app.config import Config


class CatalogoFalso:
    def existe(self, c):
        return c in {"LIM", "CAL", "ATE"}

    def codigos(self):
        return ["ATE", "CAL", "LIM"]


class GuiasFalso:
    def __init__(self, existentes=()):
        self.existentes = set(existentes)

    def existe(self, codigo):
        return codigo in self.existentes


def crear_app_prueba():
    tmp = Path(tempfile.mkdtemp())

    class ConfigPrueba(Config):
        TESTING = True
        SECRET_KEY = "prueba"
        DATABASE_PATH = tmp / "prueba.db"
        LOG_FILE = tmp / "logs.txt"
        LOG_DIR = tmp / "logs"
        ANIO_MAXIMO = 2026

    return create_app(ConfigPrueba)
