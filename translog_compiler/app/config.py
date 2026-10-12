"""Configuraciones generales del proyecto (lee variables de entorno y, si existe, el archivo .env)."""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def _cargar_env():
    env = BASE_DIR / ".env"
    if env.exists():
        for linea in env.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if linea and not linea.startswith("#") and "=" in linea:
                k, v = linea.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


_cargar_env()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "cambiar-en-produccion")
    DATABASE_PATH = Path(os.getenv("DATABASE_PATH", BASE_DIR / "database" / "app.db"))
    MIGRATIONS_DIR = BASE_DIR / "database" / "migrations"
    SEDES_PATH = BASE_DIR / "database" / "seeds" / "sedes.json"
    LOG_FILE = BASE_DIR / "storage" / "logs.txt"
    LOG_DIR = BASE_DIR / "logs"

    # Reglas de negocio de la guía de remisión
    ANIO_MINIMO = int(os.getenv("ANIO_MINIMO", 2020))
    ANIO_MAXIMO = int(os.getenv("ANIO_MAXIMO", 0)) or None  # None = año actual

    # Límites de entrada
    MAX_LONGITUD_CODIGO = 64
    MAX_CODIGOS_POR_LOTE = 200
    MAX_CONTENT_LENGTH = 64 * 1024
