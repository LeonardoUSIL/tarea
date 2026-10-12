import tempfile
from pathlib import Path

from app import create_app
from app.config import Config

TMP = Path(tempfile.gettempdir())


class VercelConfig(Config):
    # En Vercel solo se puede escribir en /tmp
    DATABASE_PATH = TMP / "app.db"
    LOG_FILE = TMP / "logs.txt"
    LOG_DIR = TMP / "logs"


app = create_app(VercelConfig)
