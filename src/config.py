from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class CardListConfig:
    urls: list[str]


def load_card_list_config(path: Path) -> CardListConfig:
    """Carga y valida un archivo YAML con una lista de URLs de cartas."""
    try:
        data: Any = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ValueError(f"No existe el archivo de configuración: {path}") from error
    except yaml.YAMLError as error:
        raise ValueError(f"YAML inválido en {path}: {error}") from error

    if not isinstance(data, dict) or not isinstance(data.get("lists"), list):
        raise ValueError(f"{path} debe contener una clave 'lists' con una lista")

    urls = data["lists"]
    if not all(isinstance(url, str) and url.strip() for url in urls):
        raise ValueError(f"Todas las entradas de 'lists' en {path} deben ser URLs de texto")

    return CardListConfig(urls=[url.strip() for url in urls])
