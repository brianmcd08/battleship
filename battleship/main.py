"""Battleship game"""
from time import sleep
from typing import Optional, List

import pygame

from battleship.board import BoardPerspective
from battleship.constants import BLACK, CELL_WIDTH, CELL_HEIGHT, CELL_MARGIN, WINDOW_SIZE
from battleship.constants import BOARD_SIZE
from battleship.coordinate import Coordinate
from battleship.graphics import display_message, draw_separator, draw_rect
from battleship.player import Player
from battleship.setup_game import get_players, setup_board
from battleship.square import SquareStatus


def main():
    players = get_players()
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    setup_board(screen, players)
    screen = pygame.display.set_mode((WINDOW_SIZE * 2 + 42, WINDOW_SIZE))
    play(screen, players)


def get_attack(screen: pygame.Surface, player: Player, opponent: Player) -> SquareStatus:
    pygame.display.set_caption(f'{player.get_name()}, take your shot!')
    pygame_done = False
    while not pygame_done:
        screen.fill(BLACK)
        grid: List[List[SquareStatus]] = opponent.get_board(BoardPerspective.OPPONENT)
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                draw_rect(screen, grid, row, column)

        # draw line in-between
        for row in range(BOARD_SIZE):
            draw_separator(screen, row, BOARD_SIZE)

        # Draw "read-only" grid
        grid2: List[List[SquareStatus]] = player.get_board(BoardPerspective.CURRENT)
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE+1, BOARD_SIZE*2+1):
                draw_rect(screen, grid2, row, column)
        pygame.display.flip()

        for event in pygame.event.get():  # User did something
            # If user clicked close
            if event.type == pygame.QUIT:
                pygame_done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos: tuple[int, int] = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (CELL_WIDTH + CELL_MARGIN)
                if column > BOARD_SIZE - 1:
                    # click is on the "non-clickable" board
                    continue
                row = pos[1] // (CELL_HEIGHT + CELL_MARGIN)
                grid[row][column] = opponent.register_shot(Coordinate(row, column))

                if grid[row][column] == SquareStatus.HIT:
                    display_message(screen, 'Hit!')
                else:
                    display_message(screen, 'Miss!')

                draw_rect(screen, grid, row, column)
                pygame.display.flip()
                sleep(1)
                return grid[row][column]


def play(screen: pygame.Surface, players: list[Player]):
    winner: Optional[Player] = None
    done: bool = False

    while not done:
        done = take_player_turn(screen, players[0], players[1])
        if done:
            winner = players[0]
            continue
        done = take_player_turn(screen, players[1], players[0])
        if done:
            winner = players[1]

    print(f'{winner.get_name()} wins!')


def take_player_turn(screen: pygame.Surface, player1: Player, player2: Player) -> bool:
    status: SquareStatus = get_attack(screen, player1, player2)
    if status == SquareStatus.HIT and player2.get_fleet().get_count_ships_afloat() == 0:
        return True
    return False


if __name__ == "__main__":
    main()
