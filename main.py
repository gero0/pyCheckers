import pygame
from player_color import PlayerColor
from board import Board
from pawn import Pawn

BOARD_WIDTH, BOARD_HEIGHT = 800, 800
ROWS, COLUMNS = 8, 8
SQUARE_SIZE = BOARD_WIDTH // COLUMNS

WINDOW = pygame.display.set_mode((1200, 800))

FPS = 60


def get_coords_from_mouse(position):
    (x, y) = position
    
    if x > BOARD_WIDTH:
        return None

    return (x // SQUARE_SIZE, y // SQUARE_SIZE)


def main():
    pygame.display.set_caption("pyCheckers")

    run = True
    clock = pygame.time.Clock()

    board = Board(SQUARE_SIZE)

    while run:
        clock.tick(FPS)
        board.draw(WINDOW)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                pass


if __name__ == "__main__":
    main()
