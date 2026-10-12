import unittest

from app.services.compiler.lexer import AnalizadorLexico
from app.services.compiler.parser import AnalizadorSintactico


def sintaxis(texto):
    tokens, errores = AnalizadorLexico().analizar(texto)
    assert not errores, errores
    return AnalizadorSintactico(tokens).analizar()


class TestParser(unittest.TestCase):
    def test_valido_construye_arbol(self):
        arbol, errores = sintaxis("GR-LIM-2026-000123")
        self.assertEqual(errores, [])
        self.assertEqual(arbol.simbolo, "GUIA")
        self.assertEqual([h.simbolo for h in arbol.hijos], ["CABECERA", "GUION", "CUERPO"])

    def test_falta_guion(self):
        _, errores = sintaxis("GR-LIM2026-000123")
        self.assertEqual(errores[0].codigo, "SIN001")
        self.assertIn("guion", errores[0].mensaje)

    def test_codigo_vacio(self):
        _, errores = sintaxis("")
        self.assertIn("fin del código", errores[0].mensaje)

    def test_incompleto(self):
        _, errores = sintaxis("GR-LIM-2026")
        self.assertIn("fin del código", errores[0].mensaje)

    def test_sobrantes(self):
        _, errores = sintaxis("GR-LIM-2026-000123-001234")
        self.assertEqual(errores[0].codigo, "SIN002")

    def test_orden_incorrecto(self):
        _, errores = sintaxis("LIM-GR-2026-000123")
        self.assertEqual(errores[0].codigo, "SIN001")


if __name__ == "__main__":
    unittest.main()
