from typing import List

import pygame

from battleship.constants import BOARD_SIZE, RED, WHITE, BLACK, BLUE, GREEN, GRAY, CELL_WIDTH, CELL_HEIGHT, CELL_MARGIN
from battleship.square import SquareStatus


def display_message(screen: pygame.Surface, message: str):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(message, True, RED, WHITE)
    textRect = text.get_rect()
    textRect.center = (256, 256)
    screen.blit(text, textRect)


def draw_separator(screen: pygame.Surface, row: int, column: int):
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
