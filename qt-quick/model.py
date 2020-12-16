# This Python file uses the following encoding: utf-8

from PySide2.QtCore import QObject, Property, Signal, Slot
from dataclasses import dataclass

from typing import List, NewType, Tuple, Union, cast

import itertools
import random

Card = NewType('Card', List[str])

CARD_RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '8', '10', 'J', 'Q', 'K')
CARD_SUIT = ('C', 'D', 'H', 'S')

BUSTS: int = 21
CASINO_STOP: int = 17


def new_deck() -> List[Card]:
    all_cards = [cast(Card, list(card))
                 for card in itertools.product(CARD_RANKS, CARD_SUIT)]
    random.shuffle(all_cards)
    return all_cards


def cards_values(cards: List[Card]) -> List[int]:
    values: List[int] = [0]
    for card in cards:
        rank = card[0]
        if ((rank >= '2' and rank <= '9') or rank == '10'):
            values = [value + int(rank) for value in values]
        elif rank in ('J', 'Q', 'K'):
            values = [value + 10 for value in values]
        else:  # rank == 'A'
            new_values = []
            for value in values:
                new_values.append(value + 1)
                new_values.append(value + 11)
            values = new_values

    return values


def best_value(values: List[int]):
    not_busts = [value for value in values if value <= BUSTS]
    return max(not_busts) if not_busts else min(values)


class Model(QObject):
    _player_points: int
    _casino_points: int
    _player_cards: List[Card]
    _casino_cards: List[Card]

    _player_turn: bool

    _curr_deck: List[Card]

    player_points_changed = Signal()
    casino_points_changed = Signal()
    player_cards_changed = Signal()
    casino_cards_changed = Signal()
    player_turn_changed = Signal()

    def __init__(self):
        super().__init__()
        self._player_points = 0
        self._casino_points = 0
        self._player_cards = []
        self._casino_cards = []

        self.set_player_turn(False)
        self._init_new_hand()
        self.set_player_turn(True)

    def _init_new_hand(self):
        self.set_player_cards([])
        self.set_casino_cards([])

        self._curr_deck = new_deck()
        self._add_card_for_player()
        self._add_card_for_casino()

    def _add_card_for_player(self) -> None:
        self._player_cards.append(self._curr_deck.pop())
        self.player_cards_changed.emit()

    def _add_card_for_casino(self) -> None:
        self._casino_cards.append(self._curr_deck.pop())
        self.casino_cards_changed.emit()

    def set_player_points(self, points: int) -> None:
        self._player_points = points
        self.player_points_changed.emit()

    def set_casino_points(self, points: int) -> None:
        self._casino_points = points
        self.casino_points_changed.emit()

    def read_player_points(self) -> int:
        return self._player_points

    def read_casino_points(self) -> int:
        return self._casino_points

    def read_player_cards(self) -> List[Card]:
        return self._player_cards

    def set_player_cards(self, player_cards: List[Card]) -> None:
        self._player_cards = player_cards
        self.player_cards_changed.emit()

    def read_casino_cards(self) -> List[Card]:
        return self._casino_cards

    def set_casino_cards(self, casino_cards: List[Card]) -> None:
        self._casino_cards = casino_cards
        self.casino_cards_changed.emit()

    def read_player_turn(self) -> bool:
        return self._player_turn

    def set_player_turn(self, player_turn: bool) -> None:
        self._player_turn = player_turn
        self.player_turn_changed.emit()

    player_turn = Property(bool, read_player_turn,
                           set_player_turn, notify=player_turn_changed)

    player_points = Property(int, read_player_points,
                             set_player_points, notify=player_points_changed)
    casino_points = Property(int, read_casino_points,
                             set_casino_points, notify=casino_points_changed)

    player_cards = Property(list, read_player_cards,
                            set_player_cards, notify=player_cards_changed)
    casino_cards = Property(list, read_casino_cards,
                            set_casino_cards, notify=casino_cards_changed)

    @Slot()
    def hit(self):
        self.set_player_turn(False)
        self._add_card_for_player()

        if min(cards_values(self._player_cards)) > BUSTS:
            self._casino_win()
            self._init_new_hand()

        self.set_player_turn(True)

    @Slot()
    def stand(self):
        self.set_player_turn(False)

        self._casino_play()
        self._choose_winner()
        self._init_new_hand()

        self.set_player_turn(True)

    def _casino_play(self):
        while max(cards_values(self._casino_cards)) < CASINO_STOP:
            self._add_card_for_casino()

    def _choose_winner(self) -> None:
        player_win = min(cards_values(self._casino_cards)) > BUSTS or best_value(
            cards_values(self._player_cards)) > best_value(cards_values(self._casino_cards))
        casino_win = min(cards_values(self._player_cards)) > BUSTS or best_value(
            cards_values(self._player_cards)) < best_value(cards_values(self._casino_cards))

        if player_win:
            self._player_win()
        if casino_win:
            self._casino_win()

    def _player_win(self):
        self.set_player_points(self._player_points + 1)
        print('You Win :)')
        print(self._state())

    def _casino_win(self):
        self.set_casino_points(self._casino_points + 1)
        print('You Lose :(')
        print(self._state())

    def _state(self) -> str:
        return f'''Points: {self._player_points} vs {self._casino_points}
Values: {cards_values(self._player_cards)} vs {cards_values(self._casino_cards)}
Cards: {self._player_cards} vs {self._casino_cards}'''


if __name__ == '__main__':
    pass
