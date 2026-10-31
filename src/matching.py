from collections import Counter
import re
import unicodedata


def normalize_card_name(name: str) -> str:
    """Normaliza un nombre para comparar cartas entre plataformas."""
    without_accents = "".join(
        character
        for character in unicodedata.normalize("NFKD", name)
        if not unicodedata.combining(character)
    )
    return re.sub(r"\s+", " ", without_accents).strip().casefold()


def aggregate_cards(card_counts: list[tuple[str, int]]) -> Counter[str]:
    cards: Counter[str] = Counter()
    for name, quantity in card_counts:
        normalized = normalize_card_name(name)
        if normalized and quantity > 0:
            cards[normalized] += quantity
    return cards


def find_matches(
    wanted_cards: list[tuple[str, int]], sale_cards: list[tuple[str, int]]
) -> list[dict[str, object]]:
    """Devuelve las cartas buscadas que también están disponibles para comprar."""
    wanted_totals = aggregate_cards(wanted_cards)
    sale_totals = aggregate_cards(sale_cards)

    display_names: dict[str, str] = {}
    for name, _ in wanted_cards + sale_cards:
        display_names.setdefault(normalize_card_name(name), name.strip())

    return [
        {
            "card": display_names[name],
            "wanted_quantity": wanted_totals[name],
            "available_quantity": sale_totals[name],
        }
        for name in sorted(wanted_totals.keys() & sale_totals.keys())
    ]
