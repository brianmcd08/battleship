from battleship.coordinate import Coordinate
from battleship.ship import Ship, ShipStatus, ShipType


def test_submarine_horizontal(submarine_horizontal):
    assert submarine_horizontal.get_type() == ShipType.SUBMARINE
    assert submarine_horizontal.get_max_hit_count() == 3
    assert submarine_horizontal.get_hit_count() == 0
    assert submarine_horizontal.get_status() == ShipStatus.INTACT


def test_submarine_vertical(submarine_vertical):
    assert submarine_vertical.get_type() == ShipType.SUBMARINE
    assert submarine_vertical.get_max_hit_count() == 3
    assert submarine_vertical.get_hit_count() == 0
    assert submarine_vertical.get_status() == ShipStatus.INTACT


def test_cruiser(cruiser):
    assert cruiser.get_type() == ShipType.CRUISER
    assert cruiser.get_max_hit_count() == 3
    assert cruiser.get_hit_count() == 0
    assert cruiser.get_status() == ShipStatus.INTACT


def test_destroyer(destroyer):
    assert destroyer.get_type() == ShipType.DESTROYER
    assert destroyer.get_max_hit_count() == 2
    assert destroyer.get_hit_count() == 0
    assert destroyer.get_status() == ShipStatus.INTACT


def test_battleship(battleship):
    assert battleship.get_type() == ShipType.BATTLESHIP
    assert battleship.get_max_hit_count() == 4
    assert battleship.get_hit_count() == 0
    assert battleship.get_status() == ShipStatus.INTACT


def test_carrier(carrier):
    assert carrier.get_type() == ShipType.CARRIER
    assert carrier.get_max_hit_count() == 5
    assert carrier.get_hit_count() == 0
    assert carrier.get_status() == ShipStatus.INTACT


def test_hit(battleship):
    before_hits = battleship.get_hit_count()
    assert before_hits == 0
    battleship.register_attack()
    assert battleship.get_status() == ShipStatus.HIT
    assert battleship.get_hit_count() == before_hits + 1


def test_sink_ship(destroyer):
    destroyer.register_attack()
    destroyer.register_attack()
    assert destroyer.get_status() == ShipStatus.SUNK


def test_not_vertical_or_horizontal():
    try:
        _ = Ship(ShipType.DESTROYER, {Coordinate(1, 2), Coordinate(2, 3)})
    except ValueError:
        assert True
    else:
        assert False


def test_horizontally_off_board():
    try:
        _ = Ship(ShipType.DESTROYER, {Coordinate(1, 7), Coordinate(1, 8)})
    except ValueError:
        assert True
    else:
        assert False


def test_vertically_off_board():
    try:
        _ = Ship(ShipType.DESTROYER, {Coordinate(7, 1), Coordinate(8, 1)})
    except ValueError:
        assert True
    else:
        assert False
