from battleship.ship import ShipStatus
from battleship.square import SquareStatus


def test_create_square(square_without_ship):
    assert square_without_ship.get_status() == SquareStatus.NOTHING
    assert square_without_ship.get_ship() is None


def test_miss(square_without_ship):
    square_without_ship.register_shot()
    assert square_without_ship.get_status() == SquareStatus.MISS
    assert square_without_ship.get_ship() is None


def test_hit(square_with_ship):
    assert square_with_ship.get_ship().get_status() == ShipStatus.INTACT
    square_with_ship.register_shot()
    assert square_with_ship.get_status() == SquareStatus.HIT
    assert square_with_ship.get_ship().get_status() == ShipStatus.HIT
