"""Lógica de negocio: orquesta estrategia de entrada, compilador, autorización y auditoría."""
from app.models import ErrorCompilacion, Fase
from app.patterns.strategy import MODOS


class CompiladorService:
    def __init__(self, compilador, repositorio_guias, sujeto_auditoria):
        self.compilador = compilador
        self.guias = repositorio_guias
        self.sujeto = sujeto_auditoria

    def procesar(self, codigos: list, modo: str = "estricto", autorizar: bool = False) -> list:
        estrategia = MODOS.get(modo, MODOS["estricto"])
        return [self._procesar_uno(c, estrategia, autorizar) for c in codigos]

    def _procesar_uno(self, bruto, estrategia, autorizar):
        texto, advertencias = estrategia.preparar(bruto)
        res = self.compilador.compilar(texto)
        res.entrada_original = bruto
        res.advertencias = advertencias
        res.modo = estrategia.nombre

        if res.valido and autorizar:
            r = res.registro
            if self.guias.registrar(r["codigo"], r["sede"], r["anio"], r["correlativo"]):
                res.autorizado = True
            else:  # otro proceso la emitió entre la verificación y el registro
                res.errores.append(ErrorCompilacion(
                    Fase.SEMANTICO, "SEM004",
                    f"Correlativo duplicado: la guía {r['codigo']} ya fue emitida.", res.guia.correlativo.posicion,
                    res.guia.correlativo.lexema))
                res.registro = None

        self.sujeto.notificar({
            "entrada": bruto, "valido": res.valido, "fase_error": res.fase_error,
            "motivo": res.motivo, "tiempo_ms": res.tiempo_ms, "modo": res.modo,
        })
        return res
