import json
import re
from typing import Any

import requests
from bs4 import BeautifulSoup

from sources.common import extract_cards_from_payload


def _find_json_payloads(html: str) -> list[Any]:
    soup = BeautifulSoup(html, "html.parser")
    payloads: list[Any] = []
    for script in soup.find_all("script"):
        text = script.string or script.get_text()
        if not text.strip():
            continue
        if script.get("type") == "application/json" or "deck" in text.casefold():
            try:
                payloads.append(json.loads(text))
            except json.JSONDecodeError:
                continue
    return payloads


def _find_html_cards(html: str) -> list[tuple[str, int]]:
    soup = BeautifulSoup(html, "html.parser")
    cards: list[tuple[str, int]] = []

    # ManaBox renders a desktop and a mobile row; usamos solo la variante desktop
    # para no duplicar cada carta.
    for container in soup.find_all(
        lambda tag: tag.name == "div"
        and "hidden" in tag.get("class", [])
        and "md:block" in tag.get("class", [])
    ):
        quantity_element = container.find(
            lambda tag: tag.name == "div" and "font-semibold" in tag.get("class", [])
        )
        name_element = container.find(
            lambda tag: tag.name == "div" and "font-medium" in tag.get("class", [])
        )
        if not quantity_element or not name_element:
            continue
        try:
            quantity = int(quantity_element.get_text(strip=True))
        except ValueError:
            continue
        name = name_element.get_text(" ", strip=True)
        if name and quantity > 0:
            cards.append((name, quantity))
    return cards


def fetch_cards(url: str, session: requests.Session, include_sideboard: bool = True) -> list[tuple[str, int]]:
    response = session.get(url, timeout=30)
    response.raise_for_status()

    html_cards = _find_html_cards(response.text)
    if html_cards:
        return html_cards

    for payload in _find_json_payloads(response.text):
        cards = extract_cards_from_payload(payload, include_sideboard)
        if cards:
            return cards

    # Algunas versiones de ManaBox exponen datos serializados dentro de una variable JS.
    for match in re.finditer(r"(?:deck|cards)\s*[:=]\s*(\{.*?\}|\[.*?\])", response.text, re.DOTALL):
        try:
            payload = json.loads(match.group(1))
        except json.JSONDecodeError:
            continue
        cards = extract_cards_from_payload(payload, include_sideboard)
        if cards:
            return cards

    raise ValueError(
        f"No se encontró una lista de cartas en ManaBox: {url}. "
        "La página puede requerir un adaptador actualizado."
    )
