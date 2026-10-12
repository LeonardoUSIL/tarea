"""Patrón Factory: crea el exportador de reportes según el formato pedido."""
import csv
import io
import json
from abc import ABC, abstractmethod

from app.utils.security import neutralizar_csv

COLUMNAS = ["fecha_hora", "codigo", "valido", "fase_error", "motivo", "tiempo_ms", "modo"]


class Exportador(ABC):
    mime = "text/plain"
    extension = "txt"

    @abstractmethod
    def exportar(self, filas: list) -> str: ...


class ExportadorCSV(Exportador):
    mime = "text/csv; charset=utf-8"
    extension = "csv"

    def exportar(self, filas):
        salida = io.StringIO()
        escritor = csv.DictWriter(salida, fieldnames=COLUMNAS, extrasaction="ignore")
        escritor.writeheader()
        for fila in filas:
            escritor.writerow({k: neutralizar_csv(fila.get(k)) for k in COLUMNAS})
        return salida.getvalue()


class ExportadorJSON(Exportador):
    mime = "application/json"
    extension = "json"

    def exportar(self, filas):
        return json.dumps(filas, ensure_ascii=False, indent=2)


class ExportadorFactory:
    _registro = {"csv": ExportadorCSV, "json": ExportadorJSON}

    @classmethod
    def crear(cls, formato: str) -> Exportador:
        try:
            return cls._registro[formato.lower()]()
        except KeyError:
            raise ValueError(f"Formato de reporte no soportado: {formato}")
