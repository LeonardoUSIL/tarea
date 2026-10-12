import re
import unittest

from tests.helpers import crear_app_prueba


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = crear_app_prueba()
        self.cliente = self.app.test_client()

    def servicio(self):
        return self.app.extensions["translog"]["servicio"]

    def test_paginas_cargan(self):
        for ruta in ("/", "/historial", "/gramatica"):
            self.assertEqual(self.cliente.get(ruta).status_code, 200, ruta)

    def test_api_lote_y_historial(self):
        r = self.cliente.post("/api/validar", json={"codigos": ["GR-LIM-2026-000123", "GR-LIM-26-000123"]})
        datos = r.get_json()
        self.assertEqual(datos["resumen"], {"total": 2, "validos": 1, "invalidos": 1})
        stats = self.app.extensions["translog"]["historial"].estadisticas()
        self.assertEqual((stats["total"], stats["validos"], stats["invalidos"]), (2, 1, 1))
        self.assertEqual(stats["por_fase"], {"LÉXICO": 1})

    def test_duplicado_al_autorizar(self):
        s = self.servicio()
        primero = s.procesar(["GR-CAL-2026-000050"], autorizar=True)[0]
        segundo = s.procesar(["GR-CAL-2026-000050"], autorizar=True)[0]
        self.assertTrue(primero.valido and primero.autorizado)
        self.assertFalse(segundo.valido)
        self.assertEqual(segundo.errores[0].codigo, "SEM004")

    def test_sin_autorizar_no_registra(self):
        s = self.servicio()
        s.procesar(["GR-CAL-2026-000060"], autorizar=False)
        self.assertTrue(s.procesar(["GR-CAL-2026-000060"], autorizar=False)[0].valido)

    def test_modo_tolerante(self):
        r = self.servicio().procesar([" gr-lim-2026-000777 "], modo="tolerante")[0]
        self.assertTrue(r.valido)
        self.assertEqual(len(r.advertencias), 2)
        self.assertFalse(self.servicio().procesar([" gr-lim-2026-000777 "], modo="estricto")[0].valido)

    def test_api_rechaza_json_invalido_y_lote_vacio(self):
        self.assertEqual(self.cliente.post("/api/validar", data="no json").status_code, 400)
        self.assertEqual(self.cliente.post("/api/validar", json={"codigos": []}).status_code, 400)

    def test_formulario_exige_csrf(self):
        self.assertEqual(self.cliente.post("/validar", data={"codigos": "GR-LIM-2026-000123"}).status_code, 400)
        html = self.cliente.get("/").get_data(as_text=True)
        token = re.search(r'name="csrf" value="([0-9a-f]+)"', html).group(1)
        r = self.cliente.post("/validar", data={"codigos": "GR-LIM-26-000123", "modo": "estricto", "csrf": token})
        self.assertEqual(r.status_code, 200)
        self.assertIn("Año incompleto", r.get_data(as_text=True))

    def test_reportes(self):
        self.servicio().procesar(["-GR-LIM-2026-000123"])
        csv = self.cliente.get("/reporte/csv")
        self.assertEqual(csv.status_code, 200)
        self.assertIn("'-GR-LIM-2026-000123", csv.get_data(as_text=True))  # CSV injection neutralizada
        self.assertEqual(self.cliente.get("/reporte/json").status_code, 200)
        self.assertEqual(self.cliente.get("/reporte/xml").status_code, 404)

    def test_log_de_auditoria(self):
        self.servicio().procesar(["GR-LIM-2026-000123"])
        with open(self.app.config["LOG_FILE"], encoding="utf-8") as f:
            contenido = f.read()
        self.assertIn("VALIDO", contenido)


if __name__ == "__main__":
    unittest.main()
