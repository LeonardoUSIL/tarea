"""Resultado completo de compilar (validar) un código de guía de remisión."""
from dataclasses import dataclass, field
from typing import List, Optional

from .ast_nodes import GuiaNode, NodoDerivacion
from .errores import ErrorCompilacion
from .token import Token


@dataclass
class ResultadoCompilacion:
    entrada: str
    entrada_original: str = ""
    tokens: List[Token] = field(default_factory=list)
    errores: List[ErrorCompilacion] = field(default_factory=list)
    arbol: Optional[NodoDerivacion] = None
    guia: Optional[GuiaNode] = None
    registro: Optional[dict] = None
    advertencias: List[str] = field(default_factory=list)
    modo: str = "estricto"
    autorizado: bool = False
    tiempo_ms: float = 0.0
    cumple_rnf1: bool = True  # RNF1: respuesta <= 1 segundo

    @property
    def valido(self) -> bool:
        return not self.errores

    @property
    def fase_error(self) -> Optional[str]:
        return self.errores[0].fase.value if self.errores else None

    @property
    def motivo(self) -> str:
        return "; ".join(e.mensaje for e in self.errores) if self.errores else "Código válido"

    def indicador(self) -> str:
        """Línea con '^' alineada bajo la primera posición de error."""
        for e in self.errores:
            if e.posicion:
                return " " * (e.posicion - 1) + "^"
        return ""

    def to_dict(self) -> dict:
        return {
            "entrada": self.entrada_original or self.entrada,
            "entrada_procesada": self.entrada,
            "valido": self.valido,
            "fase_error": self.fase_error,
            "motivo": self.motivo,
            "errores": [e.to_dict() for e in self.errores],
            "tokens": [t.to_dict() for t in self.tokens],
            "arbol": self.arbol.to_dict() if self.arbol else None,
            "registro": self.registro,
            "advertencias": self.advertencias,
            "modo": self.modo,
            "autorizado": self.autorizado,
            "tiempo_ms": self.tiempo_ms,
            "cumple_rnf1": self.cumple_rnf1,
        }
