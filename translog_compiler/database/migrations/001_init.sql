CREATE TABLE IF NOT EXISTS historial_validaciones (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha_hora  TEXT    NOT NULL,
    codigo      TEXT    NOT NULL,
    valido      INTEGER NOT NULL,
    fase_error  TEXT,
    motivo      TEXT,
    tiempo_ms   REAL,
    modo        TEXT
);

CREATE TABLE IF NOT EXISTS guias_emitidas (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    codigo      TEXT    NOT NULL UNIQUE,
    sede        TEXT    NOT NULL,
    anio        INTEGER NOT NULL,
    correlativo INTEGER NOT NULL,
    fecha_hora  TEXT    NOT NULL
);
