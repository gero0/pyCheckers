from game_logic import Game
import pygame
from constants import *
from player_color import PlayerColor

def get_coords_from_mouse(position):
    (x, y) = position

    if x > BOARD_WIDTH:
        return None

    return (x // SQUARE_SIZE, y // SQUARE_SIZE)


def main():
    pygame.display.set_caption("pyCheckers")

    run = True
    clock = pygame.time.Clock()
    game = Game(PlayerColor.WHITE)

    while run:
        clock.tick(FPS)
        
        game.update()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                coords = get_coords_from_mouse(event.pos)
                game.select_square(coords)
                pass


if __name__ == "__main__":
    main()
