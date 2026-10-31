import re

import requests

from sources.common import extract_cards_from_payload


CARD_LIST_ID_PATTERN = re.compile(r"/decks/([^/?#]+)")
API_URL = "https://api2.moxfield.com/v3/decks/all/{deck_id}"


def fetch_cards(url: str, session: requests.Session, include_sideboard: bool = True) -> list[tuple[str, int]]:
    match = CARD_LIST_ID_PATTERN.search(url)
    if not match:
        raise ValueError(f"No se pudo identificar la lista de cartas de Moxfield: {url}")

    response = session.get(API_URL.format(deck_id=match.group(1)), timeout=30)
    response.raise_for_status()
    payload = response.json()
    # El objeto raíz también tiene un campo `name` con el nombre del mazo;
    # las cartas están dentro de `boards`.
    return extract_cards_from_payload(payload.get("boards", payload), include_sideboard)
