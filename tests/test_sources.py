import unittest

from src.sources.common import extract_cards_from_payload


class SourceParsingTests(unittest.TestCase):
    def test_extracts_moxfield_board_entries(self) -> None:
        payload = {
            "mainboard": {
                "count": 2,
                "cards": {
                    "one": {"quantity": 2, "card": {"name": "Sol Ring"}},
                },
            },
            "sideboard": {
                "count": 1,
                "cards": {
                    "two": {"quantity": 1, "card": {"name": "Negate"}},
                },
            },
            "maybeboard": {
                "count": 1,
                "cards": {
                    "three": {"quantity": 1, "card": {"name": "Island"}},
                },
            },
        }
        self.assertEqual(
            extract_cards_from_payload(payload),
            [("Sol Ring", 2), ("Negate", 1)],
        )
        self.assertEqual(
            extract_cards_from_payload(payload, include_sideboard=False),
            [("Sol Ring", 2)],
        )


if __name__ == "__main__":
    unittest.main()
