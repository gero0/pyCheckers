from pawn import EmptySquare
from player_color import PlayerColor
from board import Board
from constants import *
import pygame


class Game:
    def __init__(self, player_color):
        self.selected_piece = None
        self.board = Board(SQUARE_SIZE)
        self.turn = PlayerColor.WHITE
        self.player_color = player_color
        self.valid_jumps = []
        self.valid_moves = []
        self.move_img = pygame.image.load('img/green.png')

    def update(self):
        self.board.draw(WINDOW)

        for jump in self.valid_jumps:
            coordinates = jump[0]
            (x, y) = coordinates
            WINDOW.blit(self.move_img,
                        (x * SQUARE_SIZE, y * SQUARE_SIZE))

        for moves in self.valid_moves:
            (x, y) = moves
            WINDOW.blit(self.move_img,
                        (x * SQUARE_SIZE, y * SQUARE_SIZE))

    def select_square(self, coordinates):
        # We can only select squares during out turn
        if self.turn != self.player_color:
            return

        square = self.board.get_square(coordinates)

        if not isinstance(square, EmptySquare) and square is not None:
            if square.get_color() == self.player_color:
                self.selected_piece = square
                self.valid_jumps = self.selected_piece.get_possible_jumps(self.board)
                self.valid_moves = []

                if len(self.valid_jumps) == 0:
                    self.valid_moves = self.selected_piece.get_possible_moves(self.board)
        else:
            if self.selected_piece is not None:

                for jump in self.valid_jumps:
                    (coords, captures) = jump
                    if coordinates == coords:
                        self.board.move_piece(self.selected_piece, coordinates)
                        for capture in captures:
                            self.board.capture_piece(capture)
                        self.end_turn()
                        return

                if coordinates in self.valid_moves:
                    self.board.move_piece(self.selected_piece, coordinates)
                    self.end_turn()

    def end_turn(self):
        self.valid_moves = []
        self.valid_jumps = []
        self.selected_piece = None

        if self.turn == PlayerColor.WHITE:
            self.turn = PlayerColor.BLACK
        else:
            self.turn = PlayerColor.WHITE

        #DELETE LATER
        self.player_color = self.turn
