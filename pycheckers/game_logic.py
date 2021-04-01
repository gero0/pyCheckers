from pycheckers.pawn import EmptySquare
from pycheckers.player_color import PlayerColor
from pycheckers.board import Board
from pycheckers.constants import *
import pygame
import asyncio
import json


class Game:
    def __init__(self, player_color, socket):
        self.selected_piece = None
        self.board = Board(SQUARE_SIZE)
        self.turn = PlayerColor.WHITE
        self.player_color = player_color
        self.valid_jumps = []
        self.valid_moves = []
        self.move_img = pygame.image.load('img/green.png')
        self.winner = None
        self.font = pygame.font.Font('ArialCE.ttf', 24)
        self.socket = socket

    def update(self):
        self.board.draw(WINDOW)

        if self.winner is not None:
            img1 = self.font.render(
                "Winner: " + Game.player_color_string(self.winner), False, (0, 0, 0))
            WINDOW.blit(img1, (820, 0))
            pygame.display.update()
            return

        you_img = self.font.render(
            "You're playing as: " + Game.player_color_string(self.player_color), False, (0, 0, 0))
        turn_img = self.font.render(
            "Turn: " + Game.player_color_string(self.turn), False, (0, 0, 0))

        WINDOW.blit(you_img, (820, 50))
        WINDOW.blit(turn_img, (820, 100))

        for jump in self.valid_jumps:
            coordinates = jump[0]
            (x, y) = coordinates
            WINDOW.blit(self.move_img,
                        (x * SQUARE_SIZE, y * SQUARE_SIZE))

        for moves in self.valid_moves:
            (x, y) = moves
            WINDOW.blit(self.move_img,
                        (x * SQUARE_SIZE, y * SQUARE_SIZE))

        pygame.display.update()

        if self.player_color != self.turn and self.winner is None:
            self.wait_for_opponent()

    def select_square(self, coordinates):
        # We can only select squares during out turn
        if self.turn != self.player_color:
            return

        square = self.board.get_square(coordinates)

        if not isinstance(square, EmptySquare) and square is not None:
            if square.get_color() == self.player_color:
                self.selected_piece = square
                self.valid_jumps = self.selected_piece.get_possible_jumps(
                    self.board)
                self.valid_moves = []

                if len(self.valid_jumps) == 0:
                    self.valid_moves = self.selected_piece.get_possible_moves(
                        self.board)
        else:
            if self.selected_piece is not None:

                for jump in self.valid_jumps:
                    (coords, captures) = jump
                    if coordinates == coords:
                        move = (self.selected_piece.get_coordinates(),
                                coordinates)
                        self.board.move_piece(self.selected_piece, coordinates)
                        for capture in captures:
                            self.board.capture_piece(capture)

                        self.send_move(move, captures)
                        self.end_turn()

                        return

                if coordinates in self.valid_moves:
                    move = (self.selected_piece.get_coordinates(), coordinates)
                    self.board.move_piece(self.selected_piece, coordinates)
                    self.send_move(move, [])
                    self.end_turn()

    def end_turn(self):
        self.valid_moves = []
        self.valid_jumps = []
        self.selected_piece = None

        if self.turn == PlayerColor.WHITE:
            self.turn = PlayerColor.BLACK
        else:
            self.turn = PlayerColor.WHITE

        self.check_lose()

    def end_game(self, winner):
        self.winner = winner
        print("Winner: ", winner)

    def player_color_string(color):
        if color == PlayerColor.WHITE:
            return "White"
        elif color == PlayerColor.BLACK:
            return "Black"

    def check_lose(self):
        player = self.turn
        if self.board.pieces_left(player) == 0 or self.board.any_moves_and_jumps(player) == False:
            if player == PlayerColor.WHITE:
                self.end_game(PlayerColor.BLACK)
            else:
                self.end_game(PlayerColor.WHITE)

    def send_move(self, move, captures):
        caps = []
        if captures is not None:
            caps = [capture.get_coordinates() for capture in captures]
        j = json.dumps({"move": move, "captures": caps})

        self.socket.sendall(j.encode())

    def wait_for_opponent(self):
        data = self.socket.recv(1024)
        j = json.loads(data)
        self.process_move(j)

    def process_move(self, json):
        move = json["move"]
        captures = []
        try:  # in case there's' no captures
            captures = json["captures"]
        except:
            pass

        (current, dest) = move
        piece = self.board.get_square(tuple(current))
        self.board.move_piece(piece, tuple(dest))

        for capture in captures:
            piece = self.board.get_square(tuple(capture))
            self.board.capture_piece(piece)

        self.end_turn()
