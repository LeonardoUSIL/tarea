"""Rutas principales del sistema."""
from flask import Blueprint

from app.controllers import guia_controller as c

bp = Blueprint("main", __name__)

bp.add_url_rule("/", "index", c.index)
bp.add_url_rule("/validar", "validar", c.validar, methods=["POST"])
bp.add_url_rule("/historial", "historial", c.historial)
bp.add_url_rule("/gramatica", "gramatica", c.gramatica)
bp.add_url_rule("/reporte/<formato>", "reporte", c.reporte)
bp.add_url_rule("/api/validar", "api_validar", c.api_validar, methods=["POST"])
