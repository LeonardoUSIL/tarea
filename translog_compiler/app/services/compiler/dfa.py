"""AFD (autómata finito determinista) del analizador léxico.

Alfabeto de entrada (clases de caracteres): LETRA (A-Z), DIGITO (0-9), GUION (-).

Estados:   q0 (inicial) | q_letras* | q_digitos* | q_guion*      (* = aceptación)

                 LETRA      DIGITO     GUION
    q0         q_letras   q_digitos   q_guion
    q_letras   q_letras      -          -
    q_digitos     -       q_digitos     -
    q_guion       -          -          -

Cualquier transición no definida lleva implícitamente al estado trampa (error).
Equivale a las expresiones regulares:  [A-Z]+   |   [0-9]+   |   -
"""
LETRA, DIGITO, GUION, OTRO = "LETRA", "DIGITO", "GUION", "OTRO"

ESTADO_INICIAL = "q0"
ACEPTACION = {"q_letras": "LETRAS", "q_digitos": "DIGITOS", "q_guion": "GUION"}
TRANSICIONES = {
    ("q0", LETRA): "q_letras",
    ("q_letras", LETRA): "q_letras",
    ("q0", DIGITO): "q_digitos",
    ("q_digitos", DIGITO): "q_digitos",
    ("q0", GUION): "q_guion",
}


def clasificar_caracter(c: str) -> str:
    if "A" <= c <= "Z":
        return LETRA
    if "0" <= c <= "9":
        return DIGITO
    if c == "-":
        return GUION
    return OTRO


class AFD:
    def reconocer(self, texto: str, inicio: int):
        """Máxima coincidencia desde `inicio`. Devuelve (categoria, fin) o (None, inicio)."""
        estado, i, ultimo = ESTADO_INICIAL, inicio, (None, inicio)
        while i < len(texto):
            siguiente = TRANSICIONES.get((estado, clasificar_caracter(texto[i])))
            if siguiente is None:
                break
            estado, i = siguiente, i + 1
            if estado in ACEPTACION:
                ultimo = (ACEPTACION[estado], i)
        return ultimo

    @staticmethod
    def tabla():
        """Tabla de transiciones lista para mostrarse (filas = estados, columnas = clases)."""
        estados = [ESTADO_INICIAL, "q_letras", "q_digitos", "q_guion"]
        columnas = [LETRA, DIGITO, GUION]
        filas = []
        for e in estados:
            celdas = [TRANSICIONES.get((e, c), "—") for c in columnas]
            marca = "*" if e in ACEPTACION else ""
            filas.append({"estado": e + marca, "celdas": celdas})
        return columnas, filas
