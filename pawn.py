import pygame
from player_color import PlayerColor

class Pawn:
    def __init__(self, color, square_size, coordinates):
        self.square_size = square_size
        self.color = color
        self.coordinates = coordinates
        self.direction = 1

        self.crown_img = pygame.image.load('img/crown.png')

        if self.color == PlayerColor.WHITE:
            self.direction = 1
            self.img = pygame.image.load('img/white.png')
        else:
            self.direction = -1
            self.img = pygame.image.load('img/black.png')

    def get_color(self):
        return self.color

    def getPossibleMoves(self, board):
        possibleMoves = []

        (x, y) = self.coordinates

        field = board.get_field((x + 1, y + 1 * self.direction))
        # Check if field is empty
        if field is None:
            possibleMoves += ((x + 1, y + 1 * self.direction), None)

        # if not, check if we can capture a piece
        elif field is Pawn and field.get_color() != self.color:
            field_behind_opponent = board.get_field(
                (x + 2, y + 2 * self.direction))

            if field_behind_opponent is None:
                possibleMoves += ((x + 2, y + 2 * self.direction), field)

        field = board.get_field((x - 1, y + 1 * self.direction))
        if field is None:
            possibleMoves += ((x - 1, y + 1 * self.direction), None)

        elif field is Pawn and field.get_color() != self.color:
            field_behind_opponent = board.get_field(
                (x - 2, y + 2 * self.direction))

            if field_behind_opponent is None:
                possibleMoves += ((x - 2, y + 2 * self.direction), field)

        return possibleMoves

    def move(self, coordinates):
        # Set own coordinates to
        self.coordinates = coordinates

    def draw(self, display):
        (x, y) = self.coordinates
        display.blit(self.img, (x * self.square_size, y * self.square_size))


class Queen(Pawn):
    def getPossibleMoves(self, coordinates):
        possibleMoves = []

        # Queen can move in any direction
        moves = Pawn.getPossibleMoves(self)
        inverted_moves = Pawn.getPossibleMoves(self)

        possibleMoves = moves + inverted_moves

        return possibleMoves

    def draw(self, display):
        (x, y) = self.coordinates
        display.blit(self.img, (x * self.square_size, y * self.square_size))
        display.blit(self.crown_img,
                     (x * self.square_size, y * self.square_size))
