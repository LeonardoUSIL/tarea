"""Modelo de Token: unidad mínima con significado producida por el analizador léxico."""
from dataclasses import dataclass
from enum import Enum


class TipoToken(Enum):
    PREFIJO = "PREFIJO"          # GR
    SEDE = "SEDE"                # LIM, CAL, ATE...
    ANIO = "ANIO"                # 4 dígitos
    CORRELATIVO = "CORRELATIVO"  # 6 dígitos
    GUION = "GUION"              # -
    EOF = "EOF"                  # fin de la cadena


@dataclass(frozen=True)
class Token:
    tipo: TipoToken
    lexema: str
    posicion: int  # columna (base 1) donde empieza el lexema

    def to_dict(self):
        return {"tipo": self.tipo.value, "lexema": self.lexema, "posicion": self.posicion}
