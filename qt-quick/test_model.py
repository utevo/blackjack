
from model import cards_values
import pytest


@pytest.mark.parametrize("cards, expected_values", [
    [[['A', 'S'], ['2', 'S']], {3, 13}],
    [[['A', 'S'], ['A', 'C'], ['A', 'D'], ['A', 'H']], {4, 14, 24, 34, 44}],
])
def test_cards_values(cards, expected_values):
    assert set(cards_values(cards)) == expected_values
