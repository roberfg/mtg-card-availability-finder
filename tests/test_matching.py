import unittest

from src.matching import find_matches, normalize_card_name


class MatchingTests(unittest.TestCase):
    def test_normalizes_case_accents_and_whitespace(self) -> None:
        self.assertEqual(normalize_card_name("  Élite de Serra "), "elite de serra")

    def test_finds_matches_and_aggregates_quantities(self) -> None:
        matches = find_matches(
            [("Lightning Bolt", 4), ("Counterspell", 2)],
            [("lightning bolt", 1), ("Sol Ring", 1)],
        )
        self.assertEqual(
            matches,
            [{"card": "Lightning Bolt", "wanted_quantity": 4, "available_quantity": 1}],
        )


if __name__ == "__main__":
    unittest.main()
