"""Funciones de apoyo del sistema."""
import json
from datetime import datetime
from pathlib import Path


def ahora_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def leer_json(ruta) -> dict:
    return json.loads(Path(ruta).read_text(encoding="utf-8"))
