import pygame
from pawn import EmptySquare, Pawn, Queen
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
                        self.board[(column, row)] = Pawn(
                            PlayerColor.WHITE, square_size, (column, row))
                    elif row > 4:
                        self.board[(column, row)] = Pawn(
                            PlayerColor.BLACK, square_size, (column, row))
                    else:
                        self.board[(column, row)] = EmptySquare((column, row))
                else:
                    self.board[(column, row)] = EmptySquare((column, row))

    def get_square(self, coordinates):
        if coordinates in self.board:
            return self.board[coordinates]

    def get_board(self):
        return self.__board

    def move_piece(self, piece, coordinates):
        (_, y) = coordinates
        self.board[coordinates] = piece
        self.board[piece.coordinates] = EmptySquare(piece.coordinates)
        piece.move(coordinates)

        if y == 7 or y == 0:
            self.promote_piece(piece)

    def capture_piece(self, piece):
        self.board[piece.coordinates] = EmptySquare(piece.coordinates)

    def promote_piece(self, piece):
        color = piece.color
        self.board[piece.coordinates] = Queen(
            color, self.square_size, piece.coordinates)

    def pieces_left(self, color):
        counter = 0
        for row in range(8):
            for column in range(8):
                square = self.board[(column, row)]
                if not isinstance(square, EmptySquare) and square.get_color() == color:
                    counter += 1
        return counter

    def draw(self, display):
        display.fill((255, 255, 255))
        display.blit(self.boardImg, (0, 0))

        for row in range(8):
            for column in range(8):
                t = isinstance(self.board[(column, row)], EmptySquare)
                if not t:
                    self.board[(column, row)].draw(display)

    def any_moves_and_jumps(self, player):
        for row in range(8):
            for column in range(8):
                square = self.board[(column, row)]
                if not isinstance(square, EmptySquare) and square.get_color() == player:
                    jumps = square.get_possible_jumps(self)
                    moves = square.get_possible_moves(self)

                    if len(jumps) != 0 or len(moves) != 0:
                        return True

        return False

    def any_jumps(self, player):
        for row in range(8):
            for column in range(8):
                square = self.board[(column, row)]
                if not isinstance(square, EmptySquare) and square.get_color() == player:
                    jumps = square.get_possible_jumps(self)

                    if len(jumps) != 0:
                        return True

        return False
