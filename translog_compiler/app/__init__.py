"""Inicializa la aplicación Flask, construye las dependencias y registra las rutas."""
import logging
from pathlib import Path

from flask import Flask

from .config import Config
from .patterns.observer import ObservadorHistorialBD, ObservadorLogArchivo, SujetoAuditoria
from .patterns.singleton import CatalogoSedes
from .repositories import GuiaRepository, HistorialRepository, aplicar_migraciones
from .services.compilador_service import CompiladorService
from .services.compiler import Compilador


def create_app(config_class=Config):
    app = Flask(__name__, template_folder="views/templates", static_folder="views/static")
    app.config.from_object(config_class)

    for ruta in (app.config["DATABASE_PATH"], app.config["LOG_FILE"]):
        Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    Path(app.config["LOG_DIR"]).mkdir(parents=True, exist_ok=True)
    logging.basicConfig(filename=Path(app.config["LOG_DIR"]) / "app.log", level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")

    aplicar_migraciones(app.config["DATABASE_PATH"], app.config["MIGRATIONS_DIR"])
    historial = HistorialRepository(app.config["DATABASE_PATH"])
    guias = GuiaRepository(app.config["DATABASE_PATH"])
    catalogo = CatalogoSedes(app.config["SEDES_PATH"])

    sujeto = SujetoAuditoria()
    sujeto.suscribir(ObservadorHistorialBD(historial))
    sujeto.suscribir(ObservadorLogArchivo(app.config["LOG_FILE"]))

    compilador = Compilador(catalogo, guias, app.config["ANIO_MINIMO"], app.config["ANIO_MAXIMO"])
    app.extensions["translog"] = {
        "servicio": CompiladorService(compilador, guias, sujeto),
        "historial": historial,
        "catalogo": catalogo,
    }

    from .routes import bp
    app.register_blueprint(bp)
    return app
