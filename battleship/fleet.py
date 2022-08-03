"""This represents a fleet of ships belonging to a single player."""
from typing import Set
from battleship.ship import Ship, ShipStatus


class Fleet:
    def __init__(self):
        self._ships = set()

    def get_count_ships_afloat(self) -> int:
        count = 0
        for ship in self._ships:
            if not ship.get_status() == ShipStatus.SUNK:
                count += 1
        return count

    def add_ship(self, ship: Ship) -> bool:
        if not (
            self.is_unique_type(ship) and
            self.is_not_overlapping(ship)
        ):
            return False
        self._ships.add(ship)
        return True

    def get_ships_count(self) -> int:
        return len(self._ships)

    def get_ships(self) -> Set[Ship]:
        return self._ships

    def is_unique_type(self, new_ship: Ship) -> bool:
        ship_type = new_ship.get_type()
        for ship in self._ships:
            if ship.get_type() == ship_type:
                return False
        return True

    def is_not_overlapping(self, new_ship: Ship) -> bool:
        new_ship_location = new_ship.get_location()
        for ship in self._ships:
            if new_ship_location.intersection(ship.get_location()):
                return False
        return True
