from battleship.board import BoardPerspective
from battleship.coordinate import Coordinate
from battleship.square import SquareStatus
from battleship.constants import BOARD_SIZE


def test_create_board(board):
    assert len(board.get_raw_board()) == BOARD_SIZE
    assert len(board.get_raw_board()[0]) == BOARD_SIZE
    assert board.get_status(Coordinate(2, 3)) == SquareStatus.NOTHING


def test_add_ship_to_board(board, cruiser):
    board.add_ship(cruiser)
    assert board.get_status(Coordinate(1, 2)) == SquareStatus.OCCUPIED


def test_register_hit(board, cruiser):
    board.add_ship(cruiser)
    board.register_shot(Coordinate(1, 2))
    assert board.get_status(Coordinate(1, 2)) == SquareStatus.HIT


def test_register_miss(board, cruiser):
    board.add_ship(cruiser)
    board.register_shot(Coordinate(7, 5))
    assert board.get_status(Coordinate(7, 5)) == SquareStatus.MISS


def test_grid_perspectives(board, cruiser):
    board.add_ship(cruiser)
    board.register_shot(Coordinate(7, 5))
    board.register_shot(Coordinate(2, 2))
    player_grid = board.get_board()

    assert player_grid[7][5] == SquareStatus.NOTHING
    assert player_grid[1][2] == SquareStatus.OCCUPIED
    assert player_grid[2][2] == SquareStatus.HIT

    opponent_grid = board.get_board(BoardPerspective.OPPONENT)
    assert opponent_grid[7][5] == SquareStatus.MISS
    assert opponent_grid[1][2] == SquareStatus.NOTHING
    assert opponent_grid[2][2] == SquareStatus.HIT
