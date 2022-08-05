"""This represents a ship in the battleship game."""
from enum import Enum
from typing import Set

from battleship.coordinate import Coordinate
from battleship.constants import BOARD_SIZE


class ShipStatus(Enum):
    INTACT = 0
    HIT = 1
    SUNK = 2


class ShipType(Enum):
    DESTROYER = 1
    # SUBMARINE = 2
    # CRUISER = 3
    # BATTLESHIP = 4
    # CARRIER = 5


class Ship:
    SHIP_SIZE = {
        ShipType.DESTROYER: 2,
        # ShipType.SUBMARINE: 3,
        # ShipType.CRUISER: 3,
        # ShipType.BATTLESHIP: 4,
        # ShipType.CARRIER: 5,
    }

    SHIP_DESCRIPTION = {
        ShipType.DESTROYER: 'Destroyer',
        # ShipType.SUBMARINE: 'Submarine',
        # ShipType.CRUISER: 'Cruiser',
        # ShipType.BATTLESHIP: 'battleship',
        # ShipType.CARRIER: 'Carrier',
    }

    def __init__(self, ship_type: ShipType, coordinates: Set[Coordinate]):
        if (
            not len(coordinates) == Ship.SHIP_SIZE.get(ship_type) or
            not Ship.on_board(coordinates) or
            not Ship.is_horizontal_or_vertical(coordinates)
        ):
            raise ValueError('Invalid coordinates. Ship not created.')

        self._location = coordinates
        self._ship_type = ship_type
        self._hit_count = 0
        self._max_hit_count = len(coordinates)
        self._status = ShipStatus.INTACT

    def get_status(self) -> ShipStatus:
        return self._status

    def get_type(self) -> ShipType:
        return self._ship_type

    def get_location(self) -> Set[Coordinate]:
        return self._location

    def get_hit_count(self) -> int:
        return self._hit_count

    def get_max_hit_count(self) -> int:
        return self._max_hit_count

    def register_attack(self):
        if self.get_status() == ShipStatus.SUNK:
            raise RuntimeError('Internal error. Ship is already sunk.')
        self._hit_count += 1
        if self.get_hit_count() == self.get_max_hit_count():
            self._status = ShipStatus.SUNK
        else:
            self._status = ShipStatus.HIT

    @staticmethod
    def on_board(coordinates: Set[Coordinate]) -> bool:
        for coordinate in coordinates:
            if coordinate.x > BOARD_SIZE - 1 or coordinate.y > BOARD_SIZE - 1:
                return False
        return True

    @staticmethod
    def is_horizontal_or_vertical(coordinates: Set[Coordinate]) -> bool:
        x_coordinates = set([coordinate.x for coordinate in coordinates])
        y_coordinates = set([coordinate.y for coordinate in coordinates])
        if len(x_coordinates) == 1:
            # horizontal
            coordinates_to_check = sorted(list(y_coordinates))
        elif len(y_coordinates) == 1:
            # vertical
            coordinates_to_check = sorted(list(x_coordinates))
        else:
            return False

        current = coordinates_to_check[0]
        for index in range(1, len(coordinates_to_check)):
            if not coordinates_to_check[index] == current + 1:
                return False
            current = coordinates_to_check[index]

        return True
