"""Patrón Observer: cada validación notifica a los observadores (RF6: historial de auditoría)."""
from abc import ABC, abstractmethod

from app.utils.helpers import ahora_iso
from app.utils.security import limpiar_linea


class Observador(ABC):
    @abstractmethod
    def actualizar(self, evento: dict) -> None: ...


class SujetoAuditoria:
    def __init__(self):
        self._observadores = []

    def suscribir(self, observador: Observador):
        self._observadores.append(observador)

    def notificar(self, evento: dict):
        for obs in self._observadores:
            try:
                obs.actualizar(evento)
            except Exception:  # la auditoría nunca debe tumbar la validación
                pass


class ObservadorHistorialBD(Observador):
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def actualizar(self, evento):
        self.repositorio.registrar(evento)


class ObservadorLogArchivo(Observador):
    def __init__(self, ruta_log):
        self.ruta_log = ruta_log

    def actualizar(self, evento):
        estado = "VALIDO" if evento["valido"] else f"INVALIDO[{evento['fase_error']}]"
        linea = f"{ahora_iso()} | {estado} | {limpiar_linea(evento['entrada'])[:80]} | {limpiar_linea(evento['motivo'])[:200]}\n"
        with open(self.ruta_log, "a", encoding="utf-8") as f:
            f.write(linea)
