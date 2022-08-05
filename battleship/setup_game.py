from typing import List, Set

import pygame

from battleship.board import BoardPerspective
from battleship.constants import BLACK, BOARD_SIZE, CELL_WIDTH, CELL_MARGIN, CELL_HEIGHT
from battleship.coordinate import Coordinate
from battleship.graphics import draw_rect
from battleship.player import Player
from battleship.ship import ShipType, Ship
from battleship.square import SquareStatus


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
                    temp_coordinates = coordinates.copy()
                    temp_coordinates.add(Coordinate(row, column))
                    if Ship.is_horizontal_or_vertical(temp_coordinates) and len(temp_coordinates) <= ship_length:
                        grid[row][column] = SquareStatus.NEW
                        coordinates.add(Coordinate(row, column))
                    if len(temp_coordinates) == ship_length:
                        pygame_done = True
    return coordinates
