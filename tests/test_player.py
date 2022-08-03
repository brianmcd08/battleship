from battleship.coordinate import Coordinate
from battleship.ship import ShipType


def test_player_creation(player1, player2):
    assert len(player1.get_name()) > 0
    assert len(player2.get_name()) > 0
    assert player1.get_fleet().get_ships_count() == 0
    assert player2.get_fleet().get_ships_count() == 0


def test_place_ship(player1, carrier):
    assert player1.place_ship(carrier)
    assert player1.get_fleet().get_ships_count() == 1
    assert player1.get_fleet().get_ships().pop().get_type() == ShipType.CARRIER


def test_sink_ship(player1, battleship):
    assert player1.place_ship(battleship)
    assert player1.get_fleet().get_count_ships_afloat() == 1
    assert player1.register_shot(Coordinate(1, 2))
    assert player1.get_fleet().get_count_ships_afloat() == 1
    assert player1.register_shot(Coordinate(2, 2))
    assert player1.get_fleet().get_count_ships_afloat() == 1
    assert player1.register_shot(Coordinate(3, 2))
    assert player1.get_fleet().get_count_ships_afloat() == 1
    assert player1.register_shot(Coordinate(4, 2))
    assert player1.get_fleet().get_count_ships_afloat() == 0
