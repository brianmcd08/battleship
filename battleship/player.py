"""This represents a player in the battleship game."""
from typing import List

from battleship.board import Board, BoardPerspective
from battleship.coordinate import Coordinate
from battleship.fleet import Fleet
from battleship.ship import Ship
from battleship.square import SquareStatus, Square


class Player:
    def __init__(self, name: str):
        self._name = name
        self._board = Board()
        self._fleet = Fleet()

    def get_name(self) -> str:
        return self._name

    def get_raw_board(self) -> List[List[Square]]:
        return self._board.get_raw_board()

    def get_board(self, perspective: BoardPerspective) -> List[List[SquareStatus]]:
        return self._board.get_board(perspective)

    def get_fleet(self) -> Fleet:
        return self._fleet

    def place_ship(self, ship: Ship) -> bool:
        if not self._fleet.add_ship(ship):
            return False
        self._board.add_ship(ship)
        return True

    def register_shot(self, coordinate: Coordinate) -> SquareStatus:
        return self._board.register_shot(coordinate)
