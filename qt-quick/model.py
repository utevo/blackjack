# This Python file uses the following encoding: utf-8

from PySide2.QtCore import QObject, Property, Signal, Slot
from dataclasses import dataclass

from typing import List, NewType, Tuple, Union

from enum import Enum


class Model(QObject):
    _player_points: int
    _casino_points: int
    _player_cards: List[List[str]]
    _casino_cards: List[List[str]]

    def __init__(self):
        super().__init__()
        self._player_points = 0
        self._casino_points = 0
        self._player_cards = []
        self._casino_cards = []
        self._init_hand()

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

    @Signal
    def player_points_changed(self) -> None:
        pass

    @Signal
    def casino_points_changed(self) -> None:
        pass

    def read_player_cards(self) -> List[List[str]]:
        return self._player_cards

    def set_player_cards(self, player_cards: List[List[str]]) -> None:
        self._player_cards = player_cards
        self.player_cards_changed.emit()

    @Signal
    def player_cards_changed(self) -> None:
        pass

    def read_casino_cards(self) -> List[List[str]]:
        return self._casino_cards

    def set_casino_cards(self, casino_cards: List[List[str]]) -> None:
        self._casino_cards = casino_cards
        self.casino_cards_changed.emit()

    @Signal
    def casino_cards_changed(self) -> None:
        pass

    player_points = Property(int, read_player_points, set_player_points, notify=player_points_changed)
    casino_points = Property(int, read_casino_points, set_casino_points, notify=casino_points_changed)

    player_cards = Property(list, read_player_cards, set_player_cards, notify=player_cards_changed)
    casino_cards = Property(list, read_casino_cards, set_casino_cards, notify=casino_cards_changed)

    @Slot()
    def hit(self):
        print('hit')

    @Slot()
    def stand(self):
        print('stand')

