"""Battleship game"""
from time import sleep

import pygame
from typing import Set, List
from battleship.board import BoardPerspective
from battleship.coordinate import Coordinate
from battleship.player import Player
from battleship.ship import Ship, ShipType
from battleship.square import SquareStatus
from config import BOARD_SIZE

# Constants
BLACK = pygame.Color('black')
WHITE = pygame.Color('white')
GREEN = pygame.Color('green')
GRAY = pygame.Color('gray')
RED = pygame.Color('red')
BLUE = pygame.Color('blue')
CELL_WIDTH = 50
CELL_HEIGHT = 50
CELL_MARGIN = 12


def main():
    # Initialize pygame
    pygame.init()
    players = get_players()
    WINDOW_SIZE = (1024, 512)
    screen = pygame.display.set_mode(WINDOW_SIZE)
    setup_board(screen, players)
    # print_boards(players)
    play(screen, players)


def get_players() -> List[Player]:
    # set up players
    players = []
    for index in range(2):
        name = input(f'Enter name of player {index + 1}:>')
        players.append(Player(name))
    return players


def setup_board(screen: pygame.Surface, players: List[Player]):
    # get all ships for each player
    for player in players:
        for ship_type in ShipType:
            length = Ship.SHIP_SIZE.get(ship_type)
            description = Ship.SHIP_DESCRIPTION.get(ship_type)
            valid_ship = False
            while not valid_ship:
                coordinates = get_ship_coordinates(screen, player, length, description)
                try:
                    ship = Ship(ship_type, coordinates)
                    player.place_ship(ship)
                    valid_ship = True
                except ValueError:
                    print('There was a problem adding the ship. Please try again.')


def display_message(screen: pygame.Surface, message: str):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(message, True, RED, WHITE)
    textRect = text.get_rect()
    textRect.center = (256, 256)
    screen.blit(text, textRect)


def get_attack(screen: pygame.Surface, player: Player, opponent: Player) -> None:
    pygame.display.set_caption(f'{player.get_name()}, take your shot!')
    pygame_done = False
    while not pygame_done:
        # Set the screen background
        screen.fill(BLACK)
        # Draw the grid
        grid = opponent.get_board(BoardPerspective.OPPONENT)
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                draw_rect(screen, grid, row, column)

        # draw line in-between
        for row in range(BOARD_SIZE):
            draw_separator(screen, row, BOARD_SIZE)

        # Draw "read-only" grid
        grid2 = player.get_board(BoardPerspective.CURRENT)
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
                pos = pygame.mouse.get_pos()
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
                pygame_done = True


def draw_separator(screen: pygame.Surface, row: int, column: int):
    print("Separator", row, column)
    color = BLACK
    pygame.draw.rect(screen,
                     color,
                     [(CELL_MARGIN + CELL_WIDTH) * column + CELL_MARGIN,
                      (CELL_MARGIN + CELL_HEIGHT) * row + CELL_MARGIN,
                      CELL_WIDTH,
                      CELL_HEIGHT])


def draw_rect(screen: pygame.Surface, grid: List[List[SquareStatus]], row: int, column: int):
    if column > BOARD_SIZE:
        square = grid[row][column - BOARD_SIZE - 1]
    else:
        square = grid[row][column]

    match square:
        case SquareStatus.OCCUPIED:
            color = BLUE
        case SquareStatus.NEW:
            color = GREEN
        case SquareStatus.HIT:
            color = RED
        case SquareStatus.MISS:
            color = GRAY
        case _:
            color = WHITE

    pygame.draw.rect(screen,
                     color,
                     [(CELL_MARGIN + CELL_WIDTH) * column + CELL_MARGIN,
                      (CELL_MARGIN + CELL_HEIGHT) * row + CELL_MARGIN,
                      CELL_WIDTH,
                      CELL_HEIGHT])


def get_ship_coordinates(screen: pygame.Surface, player: Player,
                         ship_length: int, ship_description: ShipType
                         ) -> Set[Coordinate]:
    # draw board with submit button, title for the type of ship, on_submit -> add_ship
    # on clicking a square, convert the square to a coordinate and add to list of coordinates
    pygame.display.set_caption(f'{player.get_name()}, place your {ship_description}')
    pygame_done = False
    grid = player.get_board(BoardPerspective.CURRENT)
    coordinates = set()

    # Set the screen background
    screen.fill(BLACK)
    while not pygame_done:
        # Draw the grid
        for row in range(BOARD_SIZE):
            for column in range(BOARD_SIZE):
                draw_rect(screen, grid, row, column)
        pygame.display.flip()

        for event in pygame.event.get():  # User did something
            # If user clicked close
            if (event.type == pygame.QUIT and
                    len(coordinates) == ship_length):
                pygame_done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # User clicks the mouse. Get the position
                pos = pygame.mouse.get_pos()
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (CELL_WIDTH + CELL_MARGIN)
                row = pos[1] // (CELL_HEIGHT + CELL_MARGIN)

                if grid[row][column] == SquareStatus.NEW:
                    grid[row][column] = SquareStatus.NOTHING
                    coordinates.remove(Coordinate(row, column))
                elif grid[row][column] == SquareStatus.NOTHING:
                    grid[row][column] = SquareStatus.NEW
                    coordinates.add(Coordinate(row, column))
    return coordinates


def play(screen: pygame.Surface, players: list[Player]):
    winner = None
    done = False

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
    # done = False
    for _ in range(3):
        get_attack(screen, player1, player2)
        get_attack(screen, player2, player1)

    return True


if __name__ == "__main__":
    main()
