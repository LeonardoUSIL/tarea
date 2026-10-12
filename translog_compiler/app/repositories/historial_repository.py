"""Historial de auditoría de validaciones (RF6)."""
from app.utils.helpers import ahora_iso
from .base import BaseRepository


class HistorialRepository(BaseRepository):
    def registrar(self, evento: dict):
        with self._conexion() as c:
            c.execute(
                "INSERT INTO historial_validaciones (fecha_hora, codigo, valido, fase_error, motivo, tiempo_ms, modo) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (ahora_iso(), evento["entrada"][:200], int(evento["valido"]), evento["fase_error"],
                 evento["motivo"][:500], evento["tiempo_ms"], evento["modo"]),
            )

    def listar(self, limite: int = 100) -> list:
        with self._conexion() as c:
            filas = c.execute(
                "SELECT fecha_hora, codigo, valido, fase_error, motivo, tiempo_ms, modo "
                "FROM historial_validaciones ORDER BY id DESC LIMIT ?", (limite,)).fetchall()
        return [dict(f) | {"valido": bool(f["valido"])} for f in filas]

    def estadisticas(self) -> dict:
        with self._conexion() as c:
            total, validos = c.execute(
                "SELECT COUNT(*), COALESCE(SUM(valido), 0) FROM historial_validaciones").fetchone()
            por_fase = c.execute(
                "SELECT fase_error, COUNT(*) n FROM historial_validaciones "
                "WHERE valido = 0 GROUP BY fase_error").fetchall()
        invalidos = total - validos
        return {
            "total": total,
            "validos": validos,
            "invalidos": invalidos,
            "tasa_error": round(100 * invalidos / total, 1) if total else 0.0,
            "por_fase": {f["fase_error"]: f["n"] for f in por_fase},
        }
