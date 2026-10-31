from collections.abc import Iterator
from typing import Any


def extract_cards_from_payload(payload: Any, include_sideboard: bool = True) -> list[tuple[str, int]]:
    """Extrae entradas de cartas de las estructuras JSON habituales de los sitios."""
    cards: list[tuple[str, int]] = []
    excluded_sections = {"maybeboard", "considering", "not_in_deck"}
    if not include_sideboard:
        excluded_sections.add("sideboard")

    def walk(value: Any, section: str = "") -> Iterator[tuple[str, int]]:
        if isinstance(value, dict):
            normalized_section = section.casefold().replace("-", "_")
            if normalized_section in excluded_sections:
                return

            card = value.get("card")
            card_data = card if isinstance(card, dict) else value
            name = card_data.get("name") if isinstance(card_data, dict) else None
            quantity = value.get("quantity", value.get("count", 1))
            if isinstance(name, str) and name.strip() and isinstance(quantity, (int, float)):
                yield name.strip(), int(quantity)
                return

            for key, child in value.items():
                if key not in {"id", "uuid", "updatedAt", "createdAt"}:
                    yield from walk(child, key)
        elif isinstance(value, list):
            for child in value:
                yield from walk(child, section)

    cards.extend(walk(payload))
    return cards
