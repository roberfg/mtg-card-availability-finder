import argparse
from pathlib import Path
from urllib.parse import urlparse

import requests
import yaml

from config import load_card_list_config
from matching import find_matches, normalize_card_name
from sources import manabox, moxfield


def fetch_card_list_cards(
    url: str, session: requests.Session, include_sideboard: bool
) -> list[tuple[str, int]]:
    host = urlparse(url).netloc.casefold()
    if "moxfield.com" in host:
        return moxfield.fetch_cards(url, session, include_sideboard)
    if "manabox.app" in host:
        return manabox.fetch_cards(url, session, include_sideboard)
    raise ValueError(f"Fuente no soportada para la URL: {url}")


def collect_cards_by_list_url(
    urls: list[str], session: requests.Session, include_sideboard: bool
) -> dict[str, list[tuple[str, int]]]:
    cards_by_url: dict[str, list[tuple[str, int]]] = {}
    for url in urls:
        print(f"Procesando: {url}")
        cards_by_url[url] = fetch_card_list_cards(url, session, include_sideboard)
    return cards_by_url


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Busca cartas disponibles entre listas de MTG.")
    parser.add_argument("--wanted-config", type=Path, default=Path("config/wanted-card-lists.yaml"))
    parser.add_argument("--sale-config", type=Path, default=Path("config/sale-card-lists.yaml"))
    parser.add_argument("--output", type=Path, default=Path("output/card-matches.yaml"))
    parser.add_argument("--without-sideboard", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    wanted_config = load_card_list_config(args.wanted_config)
    sale_config = load_card_list_config(args.sale_config)
    session = requests.Session()
    session.headers.update({"User-Agent": "mtg-card-match-finder/0.1"})

    include_sideboard = not args.without_sideboard
    wanted_cards_by_url = collect_cards_by_list_url(wanted_config.urls, session, include_sideboard)
    sale_cards_by_url = collect_cards_by_list_url(sale_config.urls, session, include_sideboard)
    wanted_cards = [card for cards in wanted_cards_by_url.values() for card in cards]
    sale_cards = [card for cards in sale_cards_by_url.values() for card in cards]
    matches = find_matches(wanted_cards, sale_cards)

    for match in matches:
        card_name = normalize_card_name(str(match["card"]))
        match["sale_links"] = [
            url
            for url, cards in sale_cards_by_url.items()
            if any(normalize_card_name(name) == card_name for name, _ in cards)
        ]

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump({"matches": matches}, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"Coincidencias encontradas: {len(matches)}")
    print(f"Resultado: {args.output}")


if __name__ == "__main__":
    main()
