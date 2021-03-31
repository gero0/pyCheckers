from pawn import Pawn
import pygame
from player_color import PlayerColor


class Board:
    def __init__(self, square_size):
        self.square_size = square_size
        self.board = {}
        # load images
        self.boardImg = pygame.image.load('img/board.png')

        # initialize board
        for row in range(8):
            for column in range(8):
                if (column % 2 == 0 and row % 2 == 0) or (column % 2 != 0 and row % 2 != 0):
                    if row < 3:
                        self.board[(row, column)] = Pawn(
                            PlayerColor.WHITE, square_size, (column, row))
                    elif row > 4:
                        self.board[(row, column)] = Pawn(
                            PlayerColor.BLACK, square_size, (column, row))
                    else:
                        self.board[(row, column)] = None
                else:
                    self.board[(row, column)] = None

    def get_square(self, coordinates):
        if coordinates in self.__board:
            return self.board[coordinates]

    def get_board(self):
        return self.__board

    def draw(self, display):
        display.fill((255, 255, 255))
        display.blit(self.boardImg, (0, 0))

        for row in range(8):
            for column in range(8):
                if self.board[(row, column)] is not None:
                    self.board[(row, column)].draw(display)
