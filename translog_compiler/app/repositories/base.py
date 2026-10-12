"""Acceso base a SQLite (una conexión por operación: seguro con hilos de Flask)."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path


class BaseRepository:
    def __init__(self, ruta_bd):
        self.ruta_bd = str(ruta_bd)

    @contextmanager
    def _conexion(self):
        conn = sqlite3.connect(self.ruta_bd)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()


def aplicar_migraciones(ruta_bd, directorio):
    """Ejecuta database/migrations/*.sql en orden (son idempotentes)."""
    conn = sqlite3.connect(str(ruta_bd))
    try:
        for archivo in sorted(Path(directorio).glob("*.sql")):
            conn.executescript(archivo.read_text(encoding="utf-8"))
        conn.commit()
    finally:
        conn.close()
