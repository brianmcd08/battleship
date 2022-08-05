"""This is a 2-d representation of a player's game-board"""
from enum import Enum
from typing import List

from battleship.coordinate import Coordinate
from battleship.ship import Ship
from battleship.square import Square, SquareStatus
from battleship.constants import BOARD_SIZE


class BoardPerspective(Enum):
    CURRENT = 0
    OPPONENT = 1


class Board:
    def __init__(self):
        self._grid = [[Square() for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]

    def __str__(self):
        return self.get_board()

    def __repr__(self):
        return self.get_raw_board()

    def get_status(self, coordinate: Coordinate) -> SquareStatus:
        return self._grid[coordinate.x][coordinate.y].get_status()

    def add_ship(self, ship: Ship):
        for coordinate in ship.get_location():
            self._grid[coordinate.x][coordinate.y].add_ship_to_square(ship)

    def register_shot(self, coordinate: Coordinate) -> SquareStatus:
        return self._grid[coordinate.x][coordinate.y].register_shot()

    def get_raw_board(self) -> List[List[Square]]:
        return self._grid

    def get_board(self, board_perspective: BoardPerspective = BoardPerspective.CURRENT) -> List[List[SquareStatus]]:
        result_grid = []
        for x in range(BOARD_SIZE):
            row = []
            for y in range(BOARD_SIZE):
                status = self.get_status(Coordinate(x, y))
                if (board_perspective == BoardPerspective.CURRENT and
                        status == SquareStatus.MISS):
                    status = SquareStatus.NOTHING
                elif (board_perspective == BoardPerspective.OPPONENT and
                      status == SquareStatus.OCCUPIED):
                    status = SquareStatus.NOTHING
                row.append(status)
            result_grid.append(row)

        return result_grid
