"""This represents a point on the grid."""
from enum import Enum

from battleship.ship import Ship


class SquareStatus(Enum):
    NOTHING = 0
    OCCUPIED = 1
    MISS = 2
    HIT = 3
    NEW = 4


class Square:
    def __init__(self) -> None:
        self._status = SquareStatus.NOTHING
        self._ship = None

    def get_status(self) -> SquareStatus:
        return self._status

    def already_hit(self) -> bool:
        return self._status == SquareStatus.HIT

    def add_ship_to_square(self, ship: Ship):
        self._ship = ship
        self._status = SquareStatus.OCCUPIED

    def get_ship(self) -> Ship:
        return self._ship

    def register_shot(self) -> SquareStatus:
        if self.already_hit():
            raise RuntimeError('Internal error. ' +
                               'Player should not be allowed to fire at the same square multiple times.')
        if not self._ship:
            self._status = SquareStatus.MISS
        else:
            self._status = SquareStatus.HIT
            self.get_ship().register_attack()
        return self._status
