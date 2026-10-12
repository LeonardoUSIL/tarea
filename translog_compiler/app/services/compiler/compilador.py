"""Pipeline completo del minicompilador: léxico -> sintáctico -> semántico -> código objeto."""
from app.models import GuiaNode, ResultadoCompilacion
from app.patterns.decorator import medir_tiempo
from .codegen import generar_registro
from .lexer import AnalizadorLexico
from .parser import AnalizadorSintactico
from .semantic import AnalizadorSemantico


class Compilador:
    def __init__(self, catalogo, repositorio_guias, anio_min=2020, anio_max=None):
        self.lexico = AnalizadorLexico()
        self.semantico = AnalizadorSemantico(catalogo, repositorio_guias, anio_min, anio_max)

    @medir_tiempo(limite_ms=1000)
    def compilar(self, texto: str) -> ResultadoCompilacion:
        res = ResultadoCompilacion(entrada=texto, entrada_original=texto)

        tokens, errores = self.lexico.analizar(texto)
        res.tokens = tokens
        if errores:
            res.errores = errores
            return res

        arbol, errores = AnalizadorSintactico(tokens).analizar()
        if errores:
            res.errores = errores
            return res
        res.arbol = arbol
        res.guia = GuiaNode.desde_arbol(arbol)

        errores = self.semantico.analizar(res.guia)
        if errores:
            res.errores = errores
            return res

        res.registro = generar_registro(res.guia)
        return res
