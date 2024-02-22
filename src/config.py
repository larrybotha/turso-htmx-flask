import os
from typing import NamedTuple

from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import Engine, create_engine

load_dotenv()


class _Config(NamedTuple):
    app: Flask
    db_engine: Engine


def init_config() -> _Config:

    TURSO_DB_URL = os.getenv("TURSO_DB_URL", "")
    TURSO_DB_AUTH_TOKEN = os.getenv("TURSO_DB_AUTH_TOKEN", "")

    db_url = f"sqlite+{TURSO_DB_URL}/?authToken={TURSO_DB_AUTH_TOKEN}"
    db_engine = create_engine(
        db_url,
        connect_args={"check_same_thread": False},
        echo=True,
    )
    app = Flask(import_name="app", static_folder="src/static")

    app_config = _Config(app=app, db_engine=db_engine)

    return app_config


config = init_config()
