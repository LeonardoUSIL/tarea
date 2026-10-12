# Minicompilador de guías de remisión · TransLog Perú S.A.C.

Proyecto final de **Teoría de Computación** (USIL): *Automatización léxico-sintáctica para reducir errores
de validación de guías de remisión en una empresa logística de Lima.*

El sistema recibe uno o varios códigos de guía y los **compila** en 4 fases (ciclo Waterfall: análisis → diseño → desarrollo → pruebas):

| Fase | Archivo | Qué hace |
|------|---------|----------|
| 1. Léxica | `app/services/compiler/dfa.py`, `lexer.py` | AFD + tabla de transiciones → tokens (`PREFIJO`, `SEDE`, `ANIO`, `CORRELATIVO`, `GUION`) |
| 2. Sintáctica | `grammar.py`, `parser.py` | Gramática libre de contexto LL(1), descenso recursivo → árbol de derivación |
| 3. Semántica | `semantic.py` | Sede existente, año en rango, correlativo ≠ 000000, correlativo no duplicado |
| 4. Código objeto | `codegen.py` | Registro normalizado + `INSERT` SQL parametrizado |

## Lenguaje formal (supuesto de formato)

```
Código:  GR-LIM-2026-000123        Regex:  ^GR-[A-Z]{3}-[0-9]{4}-[0-9]{6}$
GUIA     → CABECERA GUION CUERPO
CABECERA → PREFIJO GUION SEDE
CUERPO   → ANIO GUION CORRELATIVO
```

> El PDF solo indica que el código tiene *prefijo, sede, año y correlativo*; el formato exacto (`GR`, sedes de 3 letras,
> año de 4 y correlativo de 6 dígitos) y el catálogo de sedes (`database/seeds/sedes.json`) son **supuestos** que
> debes ajustar a lo que definas en tu documento (RNF3: agregar una sede = una línea en el JSON, sin tocar autómata ni gramática).

## Ejecutar

```bash
python -m venv venv && venv\Scripts\activate      # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
python run.py                                     # http://127.0.0.1:5000
python compilar.py GR-LIM-2026-000123 GR-LIM-26-000123 --arbol   # sin servidor web
python -m unittest discover -s tests -t .         # pruebas
```

API: `POST /api/validar` con `{"codigos": ["GR-LIM-2026-000123"], "modo": "estricto", "autorizar": false}`.

## Estructura (según el documento "Estructura de Proyecto en Python", patrón MVC)

```
app/
  __init__.py  config.py  routes.py
  controllers/   guia_controller.py            (C)
  models/        token, errores, ast_nodes, resultado   (M)
  views/         templates/  static/{css,js,img,plugins}  (V)
  forms/         guia_form.py
  services/      compilador_service.py  compiler/{dfa,lexer,grammar,parser,semantic,codegen,compilador}.py
  repositories/  historial_repository.py  guia_repository.py
  patterns/      singleton/ (CatalogoSedes)   factory/ (exportadores CSV/JSON)
                 observer/ (auditoría BD + log)   strategy/ (modo estricto/tolerante)
                 decorator/ (medir_tiempo → RNF1)
  utils/         helpers.py  validators.py  security.py
database/        migrations/  seeds/  backups/  (app.db se crea al iniciar)
storage/ logs/ tests/  requirements.txt  .env  run.py  Dockerfile  .gitignore
```

## Trazabilidad con el proyecto

- **RF1–RF2–RF3**: `form` + `lexer` (lexemas y tokens) · **RF4**: `parser` · **RF5**: errores con fase, código, columna y motivo
- **RF6**: historial en SQLite (`/historial`) + `storage/logs.txt` (patrón Observer)
- **RNF1** (≤ 1 s): decorador `medir_tiempo` (cada validación toma ~1 ms) · **RNF2**: interfaz web simple
- **RNF3**: sedes en catálogo externo · **OE5** (exactitud ≥ 95 %): `tests/test_compilador.py` evalúa 40 casos válidos/inválidos

## Notas

- `forms/` usa una clase ligera (sin Flask-WTF) y el CSRF se valida en el controlador; puedes migrarlo a Flask-WTF.
- `usuarios.txt` del documento de estructura no se incluyó: este sistema no maneja usuarios.
- Con **Autorizar despacho** activo, un código válido se registra y el siguiente intento igual se rechaza como duplicado.
