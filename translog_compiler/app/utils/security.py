"""Funciones de seguridad: limpieza de entrada, CSRF y exportación segura a CSV."""
import hmac
import secrets


def limpiar_linea(linea: str) -> str:
    """Elimina caracteres de control (evita inyección en logs y consola)."""
    return "".join(c for c in linea if c.isprintable())


def generar_token_csrf(sesion) -> str:
    if "csrf" not in sesion:
        sesion["csrf"] = secrets.token_hex(16)
    return sesion["csrf"]


def validar_token_csrf(sesion, token_recibido: str) -> bool:
    esperado = sesion.get("csrf", "")
    return bool(esperado) and hmac.compare_digest(esperado, token_recibido or "")


def neutralizar_csv(valor):
    """Previene 'CSV injection' al abrir el reporte en Excel."""
    if isinstance(valor, str) and valor[:1] in ("=", "+", "-", "@", "\t", "\r"):
        return "'" + valor
    return valor
