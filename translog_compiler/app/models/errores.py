"""Errores de compilación, clasificados por fase (RF5: indicar el motivo del error)."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Fase(str, Enum):
    LEXICO = "LÉXICO"
    SINTACTICO = "SINTÁCTICO"
    SEMANTICO = "SEMÁNTICO"


@dataclass(frozen=True)
class ErrorCompilacion:
    fase: Fase
    codigo: str
    mensaje: str
    posicion: Optional[int] = None
    lexema: str = ""

    def to_dict(self):
        return {
            "fase": self.fase.value,
            "codigo": self.codigo,
            "mensaje": self.mensaje,
            "posicion": self.posicion,
            "lexema": self.lexema,
        }
