"""Guías de remisión emitidas (sirve para detectar correlativos duplicados)."""
import sqlite3

from app.utils.helpers import ahora_iso
from .base import BaseRepository


class GuiaRepository(BaseRepository):
    def existe(self, codigo: str) -> bool:
        with self._conexion() as c:
            return c.execute("SELECT 1 FROM guias_emitidas WHERE codigo = ?", (codigo,)).fetchone() is not None

    def registrar(self, codigo, sede, anio, correlativo) -> bool:
        """False si el código ya existía (la restricción UNIQUE evita carreras)."""
        try:
            with self._conexion() as c:
                c.execute(
                    "INSERT INTO guias_emitidas (codigo, sede, anio, correlativo, fecha_hora) VALUES (?, ?, ?, ?, ?)",
                    (codigo, sede, anio, correlativo, ahora_iso()))
            return True
        except sqlite3.IntegrityError:
            return False
