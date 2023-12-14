import pathlib
import orjson

from dataclasses import dataclass

from .objects.service import Service


@dataclass
class Config:
    DEBUG = False
    SERVICES: list[Service]

    @classmethod
    def load_from_file(cls, path: str | pathlib.Path) -> "Config":
        with open(path, "r") as f:
            data = orjson.loads(f.read())

            return cls(**data)
