"""Fase 2 – Análisis sintáctico: descenso recursivo dirigido por la gramática (grammar.py)."""
from app.models import ErrorCompilacion, Fase, NodoDerivacion, TipoToken
from .grammar import DESCRIPCION_TERMINAL, PRODUCCIONES, SIMBOLO_INICIAL


class _ErrorSintactico(Exception):
    def __init__(self, error):
        self.error = error


class AnalizadorSintactico:
    def __init__(self, tokens, producciones=None, inicial=SIMBOLO_INICIAL):
        self.tokens = tokens
        self.producciones = producciones or PRODUCCIONES
        self.inicial = inicial
        self.i = 0

    def analizar(self):
        """Devuelve (arbol, errores). Modo pánico: se detiene en el primer error."""
        try:
            arbol = self._derivar(self.inicial)
            actual = self.tokens[self.i]
            if actual.tipo != TipoToken.EOF:
                raise _ErrorSintactico(ErrorCompilacion(
                    Fase.SINTACTICO, "SIN002",
                    f"Sobran caracteres después del correlativo: {self._describir(actual)}.",
                    actual.posicion, actual.lexema))
            return arbol, []
        except _ErrorSintactico as e:
            return None, [e.error]

    def _derivar(self, simbolo):
        if simbolo in self.producciones:
            nodo = NodoDerivacion(simbolo)
            for s in self.producciones[simbolo]:
                nodo.hijos.append(self._derivar(s))
            return nodo
        actual = self.tokens[self.i]
        if actual.tipo.value != simbolo:
            previo = f" después de '{self.tokens[self.i - 1].lexema}'" if self.i > 0 else ""
            raise _ErrorSintactico(ErrorCompilacion(
                Fase.SINTACTICO, "SIN001",
                f"Se esperaba {DESCRIPCION_TERMINAL[simbolo]}{previo} pero se encontró {self._describir(actual)}.",
                actual.posicion, actual.lexema))
        self.i += 1
        return NodoDerivacion(simbolo, token=actual)

    @staticmethod
    def _describir(token):
        if token.tipo == TipoToken.EOF:
            return "el fin del código"
        nombre = {"ANIO": "año", "SEDE": "sede", "PREFIJO": "prefijo", "GUION": "guion", "CORRELATIVO": "correlativo"}
        return f"{nombre[token.tipo.value]} '{token.lexema}'"
