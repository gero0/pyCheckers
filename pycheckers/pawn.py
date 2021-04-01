import pygame
from pycheckers.player_color import PlayerColor


class EmptySquare:
    """Class representing an empty square on the board"""
    def __init__(self, coordinates):
        self.coordinates = coordinates


class Pawn:
    """Class representing a regular piece"""
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

    def get_possible_moves(self, board):
        """Returns all possible moves that can be made by this piece. This excludes jumps (captures of opponnent's pieces)."""
        possibleMoves = []

        (x, y) = self.coordinates

        square = board.get_square((x + 1, y + 1 * self.direction))
        # Check if field is empty
        if isinstance(square, EmptySquare):
            possibleMoves.append((x + 1, y + 1 * self.direction))

        square = board.get_square((x - 1, y + 1 * self.direction))
        if isinstance(square, EmptySquare):
            possibleMoves.append((x - 1, y + 1 * self.direction))

        return possibleMoves

    def get_possible_jumps(self, board):
        """A recursive algorithm searching for all possible jumps that can be made by the piece.
        Returns a list of tuples, that contain the position piece can jump to, and a list of pieces it captures along the way."""
        return Pawn.possible_jumps(self, board, self.direction, self.color, [])

    def possible_jumps(square, board, direction, color, captures):
        (x, y) = square.coordinates
        possibleJumps = []

        right_square = board.get_square((x + 1, y + 1 * direction))

        if isinstance(right_square, Pawn) and right_square.get_color() != color:
            square_behind_opponent = board.get_square(
                (x + 2, y + 2 * direction))

            if isinstance(square_behind_opponent, EmptySquare):
                # captures.append(right_square)
                jumps = Pawn.possible_jumps(
                    square_behind_opponent, board, direction, color, captures + [right_square])
                # check if array empty
                if not jumps:
                    possibleJumps.append(
                        ((x + 2, y + 2 * direction), captures + [right_square]))
                else:
                    for jump in jumps:
                        possibleJumps.append(jump)

        left_square = board.get_square((x - 1, y + 1 * direction))

        if isinstance(left_square, Pawn) and left_square.get_color() != color:
            square_behind_opponent = board.get_square(
                (x - 2, y + 2 * direction))

            if isinstance(square_behind_opponent, EmptySquare):
                jumps = Pawn.possible_jumps(
                    square_behind_opponent, board, direction, color, captures + [left_square])
                if not jumps:
                    possibleJumps.append(
                        ((x - 2, y + 2 * direction), captures + [left_square]))
                else:
                    for jump in jumps:
                        possibleJumps.append(jump)

        return possibleJumps

    def move(self, coordinates):
        # Set own coordinates to
        self.coordinates = coordinates

    def draw(self, display):
        (x, y) = self.coordinates
        display.blit(self.img, (x * self.square_size, y * self.square_size))

    def get_coordinates(self):
        return self.coordinates


class Queen(Pawn):
    def get_possible_moves(self, board):
        """Returns all possible moves that can be made by this piece. This excludes jumps (captures of opponnent's pieces)."""
        possibleMoves = []

        # Queen can move in any direction
        self.direction = 1
        moves = Pawn.get_possible_moves(self, board)

        self.direction = -1
        inverted_moves = Pawn.get_possible_moves(self, board)

        possibleMoves = moves + inverted_moves

        return possibleMoves

    def get_possible_jumps(self, board):
        """A recursive algorithm searching for all possible jumps that can be made by the piece.
        Returns a list of tuples, that contain the position piece can jump to, and a list of pieces it captures along the way."""
        return Queen.possible_jumps(self, board, self.color, [], self)

    def possible_jumps(square, board, color, captures, previous_square):
        (x, y) = square.coordinates
        possibleJumps = []

        right_square = board.get_square((x + 1, y + 1))

        if isinstance(right_square, Pawn) and right_square.get_color() != color:
            square_behind_opponent = board.get_square(
                (x + 2, y + 2))

            # previous_square is required so we don't go back to square we already visited. This prevents endless recursion
            if isinstance(square_behind_opponent, EmptySquare) and square_behind_opponent != previous_square:
                # captures.append(right_square)
                jumps = Queen.possible_jumps(
                    square_behind_opponent, board, color, captures + [right_square], square)
                # check if array empty
                if not jumps:
                    possibleJumps.append(
                        ((x + 2, y + 2), captures + [right_square]))
                else:
                    for jump in jumps:
                        possibleJumps.append(jump)

        left_square = board.get_square((x - 1, y + 1))

        if isinstance(left_square, Pawn) and left_square.get_color() != color:
            square_behind_opponent = board.get_square(
                (x - 2, y + 2))

            if isinstance(square_behind_opponent, EmptySquare) and square_behind_opponent != previous_square:
                jumps = Queen.possible_jumps(
                    square_behind_opponent, board, color, captures + [left_square], square)
                if not jumps:
                    possibleJumps.append(
                        ((x - 2, y + 2), captures + [left_square]))
                else:
                    for jump in jumps:
                        possibleJumps.append(jump)

        bottom_right_square = board.get_square((x + 1, y - 1))

        if isinstance(bottom_right_square, Pawn) and bottom_right_square.get_color() != color:
            square_behind_opponent = board.get_square(
                (x + 2, y - 2))

            if isinstance(square_behind_opponent, EmptySquare) and square_behind_opponent != previous_square:
                # captures.append(right_square)
                jumps = Queen.possible_jumps(
                    square_behind_opponent, board, color, captures + [bottom_right_square], square)
                # check if array empty
                if not jumps:
                    possibleJumps.append(
                        ((x + 2, y - 2), captures + [bottom_right_square]))
                else:
                    for jump in jumps:
                        possibleJumps.append(jump)

        bottom_left_square = board.get_square((x - 1, y - 1))

        if isinstance(bottom_left_square, Pawn) and bottom_left_square.get_color() != color:
            square_behind_opponent = board.get_square(
                (x - 2, y - 2))

            if isinstance(square_behind_opponent, EmptySquare) and square_behind_opponent != previous_square:
                jumps = Queen.possible_jumps(
                    square_behind_opponent, board, color, captures + [bottom_left_square], square)
                if not jumps:
                    possibleJumps.append(
                        ((x - 2, y - 2), captures + [bottom_left_square]))
                else:
                    for jump in jumps:
                        possibleJumps.append(jump)

        return possibleJumps

    def draw(self, display):
        (x, y) = self.coordinates
        display.blit(self.img, (x * self.square_size, y * self.square_size))
        display.blit(self.crown_img,
                     (x * self.square_size, y * self.square_size))
