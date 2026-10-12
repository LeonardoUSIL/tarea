"""Controlador (MVC): conecta las rutas con el servicio y las vistas."""
from flask import Response, abort, current_app, jsonify, render_template, request, session

from app.forms import GuiaForm
from app.patterns.factory import ExportadorFactory
from app.patterns.strategy import MODOS
from app.services.compiler import gramatica_texto
from app.services.compiler.dfa import AFD
from app.utils.security import generar_token_csrf, validar_token_csrf

EJEMPLOS = [
    "GR-LIM-2026-000123",
    "GR-CAL-2026-000045",
    "GR-LIM-26-000123",
    "GR-XYZ-2026-000010",
    "GR-ATE-2026-00012A",
    "GR-LIM2026-000123",
    "gr-lim-2026-000123",
    "GR-LIM-2026-000000",
]


def _ctx():
    return current_app.extensions["translog"]


def _form_desde(datos):
    return GuiaForm.desde_dict(
        datos,
        max_longitud=current_app.config["MAX_LONGITUD_CODIGO"],
        max_lote=current_app.config["MAX_CODIGOS_POR_LOTE"],
    )


def _render_index(form, resultados=None, errores=None):
    return render_template(
        "index.html", form=form, resultados=resultados, errores=errores or [],
        modos=MODOS, ejemplos=EJEMPLOS, csrf=generar_token_csrf(session),
        resumen=_resumen(resultados))


def _resumen(resultados):
    if not resultados:
        return None
    validos = sum(1 for r in resultados if r.valido)
    return {"total": len(resultados), "validos": validos, "invalidos": len(resultados) - validos}


def index():
    return _render_index(GuiaForm())


def validar():
    if not validar_token_csrf(session, request.form.get("csrf")):
        abort(400, "Token CSRF inválido o ausente.")
    form = _form_desde(request.form)
    if not form.es_valido():
        return _render_index(form, errores=form.errores), 400
    resultados = _ctx()["servicio"].procesar(form.codigos, form.modo, form.autorizar)
    return _render_index(form, resultados)


def api_validar():
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        return jsonify(error="Se esperaba un cuerpo JSON (objeto)."), 400
    codigos = datos.get("codigos", datos.get("codigo", ""))
    if isinstance(codigos, list):
        codigos = "\n".join(str(c) for c in codigos)
    form = _form_desde({"codigos": str(codigos), "modo": datos.get("modo", "estricto"),
                        "autorizar": datos.get("autorizar", False)})
    if not form.es_valido():
        return jsonify(error=" ".join(form.errores)), 400
    resultados = _ctx()["servicio"].procesar(form.codigos, form.modo, form.autorizar)
    return jsonify(resultados=[r.to_dict() for r in resultados], resumen=_resumen(resultados))


def historial():
    repo = _ctx()["historial"]
    return render_template("historial.html", filas=repo.listar(100), stats=repo.estadisticas())


def reporte(formato):
    try:
        exportador = ExportadorFactory.crear(formato)
    except ValueError:
        abort(404)
    contenido = exportador.exportar(_ctx()["historial"].listar(1000))
    return Response(contenido, mimetype=exportador.mime,
                    headers={"Content-Disposition": f"attachment; filename=reporte_validaciones.{exportador.extension}"})


def gramatica():
    columnas, filas = AFD.tabla()
    return render_template(
        "gramatica.html", producciones=gramatica_texto(), columnas=columnas, filas_afd=filas,
        sedes=_ctx()["catalogo"].todas(), anio_min=current_app.config["ANIO_MINIMO"])
