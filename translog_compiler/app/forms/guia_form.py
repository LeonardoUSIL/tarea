"""Formulario de validación de guías (RF1). Versión ligera sin dependencias;
puede migrarse a Flask-WTF si se desea (el CSRF ya se controla en el controlador)."""
from app.patterns.strategy import MODOS
from app.utils.security import limpiar_linea
from app.utils.validators import longitud_valida, lote_valido


class GuiaForm:
    def __init__(self, texto="", modo="estricto", autorizar=False, max_longitud=64, max_lote=200):
        self.texto = texto or ""
        self.modo = modo
        self.autorizar = autorizar
        self.max_longitud = max_longitud
        self.max_lote = max_lote
        self.errores = []
        self.codigos = []

    @classmethod
    def desde_dict(cls, datos, **limites):
        return cls(texto=datos.get("codigos", ""), modo=datos.get("modo", "estricto"),
                   autorizar=str(datos.get("autorizar", "")).lower() in ("1", "true", "on", "si", "sí"), **limites)

    def es_valido(self) -> bool:
        self.errores, self.codigos = [], []
        if self.modo not in MODOS:
            self.errores.append("Modo de validación no reconocido.")
        lineas = [limpiar_linea(l) for l in self.texto.splitlines()]
        self.codigos = [l for l in lineas if l.strip() != ""]
        if not lote_valido(self.codigos, self.max_lote):
            self.errores.append(f"Ingrese entre 1 y {self.max_lote} códigos (uno por línea).")
        elif any(not longitud_valida(c, self.max_longitud) for c in self.codigos):
            self.errores.append(f"Cada código debe tener como máximo {self.max_longitud} caracteres.")
        return not self.errores
