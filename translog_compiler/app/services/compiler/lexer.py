"""Fase 1 – Análisis léxico: cadena -> tokens (usa el AFD) con recuperación de errores."""
from app.models import ErrorCompilacion, Fase, TipoToken, Token
from .dfa import AFD

PREFIJO_VALIDO = "GR"
LONG_PREFIJO, LONG_SEDE, LONG_ANIO, LONG_CORRELATIVO = 2, 3, 4, 6


class AnalizadorLexico:
    def __init__(self, afd: AFD = None):
        self.afd = afd or AFD()

    def analizar(self, texto: str):
        tokens, errores, pos = [], [], 0
        while pos < len(texto):
            categoria, fin = self.afd.reconocer(texto, pos)
            if categoria is None:
                errores.append(self._error_caracter(texto[pos], pos + 1))
                pos += 1
                continue
            lexema = texto[pos:fin]
            token, error = self._clasificar(categoria, lexema, pos + 1)
            if error:
                errores.append(error)
            else:
                tokens.append(token)
            pos = fin
        tokens.append(Token(TipoToken.EOF, "", len(texto) + 1))
        return tokens, errores

    # -- clasificación de lexemas en tokens -------------------------------------------
    def _clasificar(self, categoria, lexema, col):
        n = len(lexema)
        if categoria == "GUION":
            return Token(TipoToken.GUION, lexema, col), None
        if categoria == "LETRAS":
            if n == LONG_PREFIJO:
                if lexema == PREFIJO_VALIDO:
                    return Token(TipoToken.PREFIJO, lexema, col), None
                return None, self._err("LEX002", f"Prefijo '{lexema}' inválido: se esperaba '{PREFIJO_VALIDO}'.", col, lexema)
            if n == LONG_SEDE:
                return Token(TipoToken.SEDE, lexema, col), None
            return None, self._err(
                "LEX003", f"El bloque de letras '{lexema}' tiene {n} caracteres: el prefijo lleva {LONG_PREFIJO} y la sede {LONG_SEDE}.", col, lexema)
        # DIGITOS
        if n == LONG_ANIO:
            return Token(TipoToken.ANIO, lexema, col), None
        if n == LONG_CORRELATIVO:
            return Token(TipoToken.CORRELATIVO, lexema, col), None
        if n < LONG_ANIO:
            return None, self._err("LEX004", f"Año incompleto: '{lexema}' tiene {n} dígito(s), se esperaban {LONG_ANIO}.", col, lexema)
        if n == LONG_ANIO + 1:
            return None, self._err("LEX005", f"Correlativo incompleto: '{lexema}' tiene {n} dígitos, se esperaban {LONG_CORRELATIVO}.", col, lexema)
        return None, self._err("LEX006", f"Bloque numérico '{lexema}' demasiado largo ({n} dígitos, máximo {LONG_CORRELATIVO}).", col, lexema)

    def _error_caracter(self, c, col):
        if c.isspace():
            msg = "Espacio en blanco no permitido dentro del código."
        elif "a" <= c <= "z":
            msg = f"Letra minúscula '{c}': el código solo admite MAYÚSCULAS."
        else:
            msg = f"Carácter '{c}' no permitido (solo A-Z, 0-9 y '-')."
        return self._err("LEX001", msg, col, c)

    @staticmethod
    def _err(codigo, mensaje, col, lexema):
        return ErrorCompilacion(Fase.LEXICO, codigo, mensaje, col, lexema)
