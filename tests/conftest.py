import pytest

from battleship.board import Board
from battleship.coordinate import Coordinate
# from battleship.player import Player
from battleship.player import Player
from battleship.ship import Ship, ShipType
from battleship.square import Square


@pytest.fixture
def destroyer():
    return Ship(ShipType.DESTROYER, {Coordinate(1, 2), Coordinate(2, 2)})


@pytest.fixture
def submarine_vertical():
    return Ship(ShipType.SUBMARINE, {Coordinate(2, 2), Coordinate(3, 2), Coordinate(4, 2)})


@pytest.fixture
def submarine_horizontal():
    return Ship(ShipType.SUBMARINE, {Coordinate(1, 2), Coordinate(1, 3), Coordinate(1, 4)})


@pytest.fixture
def cruiser():
    return Ship(ShipType.CRUISER, {Coordinate(1, 2), Coordinate(2, 2), Coordinate(3, 2)})


@pytest.fixture
def battleship():
    return Ship(ShipType.BATTLESHIP, {Coordinate(1, 2), Coordinate(2, 2), Coordinate(3, 2), Coordinate(4, 2)})


@pytest.fixture
def carrier():
    return Ship(ShipType.CARRIER, {Coordinate(1, 2), Coordinate(2, 2), Coordinate(3, 2), Coordinate(4, 2),
                                   Coordinate(5, 2)})


@pytest.fixture
def square_without_ship():
    return Square()


@pytest.fixture
def square_with_ship():
    square = Square()
    ship = Ship(ShipType.CRUISER, {Coordinate(1, 2), Coordinate(2, 2), Coordinate(3, 2)})
    square.add_ship_to_square(ship)
    return square


@pytest.fixture
def board():
    return Board()


@pytest.fixture
def player1():
    return Player('Player1')


@pytest.fixture
def player2():
    return Player('Player2')
