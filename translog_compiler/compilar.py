"""Uso por consola (sin servidor web):

    python compilar.py GR-LIM-2026-000123 GR-LIM-26-000123
    python compilar.py --modo tolerante --arbol " gr-LIM-2026-000200 "
    python compilar.py --autorizar GR-CAL-2026-000001
"""
import argparse

from app import create_app


def main():
    ap = argparse.ArgumentParser(description="Minicompilador de guías de remisión – TransLog Perú S.A.C.")
    ap.add_argument("codigos", nargs="+")
    ap.add_argument("--modo", choices=["estricto", "tolerante"], default="estricto")
    ap.add_argument("--autorizar", action="store_true", help="registra el correlativo si el código es válido")
    ap.add_argument("--arbol", action="store_true", help="muestra el árbol de derivación")
    args = ap.parse_args()

    servicio = create_app().extensions["translog"]["servicio"]
    for r in servicio.procesar(args.codigos, args.modo, args.autorizar):
        estado = "VÁLIDO  " if r.valido else f"INVÁLIDO ({r.fase_error})"
        print(f"{estado:<22} {r.entrada_original!r}  [{r.tiempo_ms} ms]")
        if not r.valido:
            print(f"    {r.entrada}\n    {r.indicador()}\n    → {r.motivo}")
        for adv in r.advertencias:
            print(f"    ⚠ {adv}")
        if r.valido and r.autorizado:
            print("    ✔ correlativo registrado")
        if args.arbol and r.arbol:
            print("    " + r.arbol.a_texto().replace("\n", "\n    "))


if __name__ == "__main__":
    main()
