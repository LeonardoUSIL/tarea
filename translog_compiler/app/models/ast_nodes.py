"""Árbol de derivación y nodo AST de la guía de remisión."""
from dataclasses import dataclass, field
from typing import List, Optional

from .token import Token, TipoToken


@dataclass
class NodoDerivacion:
    simbolo: str
    token: Optional[Token] = None
    hijos: List["NodoDerivacion"] = field(default_factory=list)

    def hojas(self) -> List[Token]:
        if self.token is not None:
            return [self.token]
        return [t for h in self.hijos for t in h.hojas()]

    def to_dict(self):
        return {
            "simbolo": self.simbolo,
            "lexema": self.token.lexema if self.token else None,
            "hijos": [h.to_dict() for h in self.hijos],
        }

    def a_texto(self, prefijo: str = "", ultimo: bool = True, raiz: bool = True) -> str:
        etiqueta = self.simbolo if self.token is None else f"{self.simbolo} → '{self.token.lexema}'"
        if raiz:
            lineas, nuevo_prefijo = [etiqueta], ""
        else:
            lineas = [prefijo + ("└── " if ultimo else "├── ") + etiqueta]
            nuevo_prefijo = prefijo + ("    " if ultimo else "│   ")
        for i, hijo in enumerate(self.hijos):
            lineas.append(hijo.a_texto(nuevo_prefijo, i == len(self.hijos) - 1, False))
        return "\n".join(lineas)


@dataclass
class GuiaNode:
    prefijo: Token
    sede: Token
    anio: Token
    correlativo: Token

    @property
    def codigo_normalizado(self) -> str:
        return f"{self.prefijo.lexema}-{self.sede.lexema}-{self.anio.lexema}-{self.correlativo.lexema}"

    @classmethod
    def desde_arbol(cls, arbol: NodoDerivacion) -> "GuiaNode":
        por_tipo = {t.tipo: t for t in arbol.hojas() if t.tipo != TipoToken.GUION}
        return cls(
            prefijo=por_tipo[TipoToken.PREFIJO],
            sede=por_tipo[TipoToken.SEDE],
            anio=por_tipo[TipoToken.ANIO],
            correlativo=por_tipo[TipoToken.CORRELATIVO],
        )
