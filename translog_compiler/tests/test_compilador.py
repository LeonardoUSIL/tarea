"""Pruebas del pipeline completo + matriz de casos (Objetivo específico 5: exactitud >= 95 %)."""
import unittest

from app.services.compiler import Compilador
from tests.helpers import CatalogoFalso, GuiasFalso

# (código, ¿debe ser válido?)
CASOS = [
    ("GR-LIM-2026-000123", True), ("GR-CAL-2025-000001", True), ("GR-ATE-2020-999999", True),
    ("GR-LIM-2026-000001", False),  # duplicado
    ("GR-LIM-2026-000000", False), ("GR-XYZ-2026-000123", False), ("GR-LIM-2019-000123", False),
    ("GR-LIM-2027-000123", False), ("GR-LIM-26-000123", False), ("GR-LIM-202-000123", False),
    ("GR-LIM-2026-12345", False), ("GR-LIM-2026-1234567", False), ("GR-LIM-2026-00012A", False),
    ("GR-LIM-2026-", False), ("GR-LIM-2026", False), ("GR-LIM", False), ("GR", False), ("", False),
    ("gr-lim-2026-000123", False), ("GR-lim-2026-000123", False), ("GR LIM 2026 000123", False),
    ("GR_LIM_2026_000123", False), ("GR-LIM2026-000123", False), ("GRLIM-2026-000123", False),
    ("GR--LIM-2026-000123", False), ("-GR-LIM-2026-000123", False), ("GR-LIM-2026-000123-", False),
    ("GR-LIM-2026-000123 ", False), (" GR-LIM-2026-000123", False), ("GX-LIM-2026-000123", False),
    ("GRR-LIM-2026-000123", False), ("GR-LI-2026-000123", False), ("GR-LIMA-2026-000123", False),
    ("LIM-GR-2026-000123", False), ("GR-2026-LIM-000123", False), ("2026-GR-LIM-000123", False),
    ("GR-LIM-2026-000123-000124", False), ("GR-LIM-2026-00 123", False), ("GR-LIM-20Z6-000123", False),
    ("GR-LÍM-2026-000123", False),
]


class TestCompilador(unittest.TestCase):
    def setUp(self):
        self.c = Compilador(CatalogoFalso(), GuiasFalso({"GR-LIM-2026-000001"}), anio_min=2020, anio_max=2026)

    def test_matriz_de_casos_exactitud(self):
        fallos = [(cod, esp) for cod, esp in CASOS if self.c.compilar(cod).valido != esp]
        exactitud = 1 - len(fallos) / len(CASOS)
        self.assertGreaterEqual(exactitud, 0.95, f"Fallos: {fallos}")
        self.assertEqual(fallos, [])  # en realidad esperamos 100 %

    def test_fases_de_error(self):
        self.assertEqual(self.c.compilar("GR-LIM-26-000123").fase_error, "LÉXICO")
        self.assertEqual(self.c.compilar("GR-LIM2026-000123").fase_error, "SINTÁCTICO")
        self.assertEqual(self.c.compilar("GR-XYZ-2026-000123").fase_error, "SEMÁNTICO")

    def test_registro_objeto(self):
        r = self.c.compilar("GR-ATE-2024-000045")
        self.assertTrue(r.valido)
        self.assertEqual(r.registro["parametros"], ["GR-ATE-2024-000045", "ATE", 2024, 45])

    def test_rnf1_tiempo(self):
        r = self.c.compilar("GR-LIM-2026-000123")
        self.assertTrue(r.cumple_rnf1)
        self.assertLess(r.tiempo_ms, 1000)

    def test_semantica_reporta_todos_los_errores(self):
        r = self.c.compilar("GR-XYZ-2031-000000")
        self.assertEqual([e.codigo for e in r.errores], ["SEM001", "SEM002", "SEM003"])


if __name__ == "__main__":
    unittest.main()
