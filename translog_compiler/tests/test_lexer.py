import unittest

from app.models import TipoToken
from app.services.compiler.lexer import AnalizadorLexico


class TestLexer(unittest.TestCase):
    def setUp(self):
        self.lex = AnalizadorLexico()

    def tipos(self, texto):
        tokens, errores = self.lex.analizar(texto)
        return [t.tipo for t in tokens], errores

    def test_codigo_valido_genera_7_tokens_mas_eof(self):
        tipos, errores = self.tipos("GR-LIM-2026-000123")
        self.assertEqual(errores, [])
        self.assertEqual(tipos, [TipoToken.PREFIJO, TipoToken.GUION, TipoToken.SEDE, TipoToken.GUION,
                                 TipoToken.ANIO, TipoToken.GUION, TipoToken.CORRELATIVO, TipoToken.EOF])

    def test_minuscula(self):
        _, errores = self.tipos("gr-LIM-2026-000123")
        self.assertEqual({e.codigo for e in errores}, {"LEX001"})

    def test_prefijo_invalido(self):
        _, errores = self.tipos("GX-LIM-2026-000123")
        self.assertEqual(errores[0].codigo, "LEX002")

    def test_anio_incompleto(self):
        _, errores = self.tipos("GR-LIM-26-000123")
        self.assertEqual(errores[0].codigo, "LEX004")

    def test_correlativo_incompleto_y_largo(self):
        self.assertEqual(self.tipos("GR-LIM-2026-12345")[1][0].codigo, "LEX005")
        self.assertEqual(self.tipos("GR-LIM-2026-1234567")[1][0].codigo, "LEX006")

    def test_caracter_invalido_con_posicion(self):
        _, errores = self.tipos("GR-LIM-2026-000123#")
        self.assertEqual([(e.codigo, e.posicion) for e in errores], [("LEX001", 19)])

    def test_espacio_interno(self):
        _, errores = self.tipos("GR-LIM -2026-000123")
        self.assertIn("Espacio", errores[0].mensaje)


if __name__ == "__main__":
    unittest.main()
