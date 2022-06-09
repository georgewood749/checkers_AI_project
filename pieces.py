from constants import *


class Pieces:
    def __init__(self, colour, row, column):
        self.colour = colour
        self.row = row
        self.column = column
        self.xcor = 0
        self.ycor = 0
        self.king = False
        self.get_square()

    def draw(self, window):
        """Draws piece onto board."""
        if self.colour == WHITE:
            window.blit(WHITE_PIECE, (self.xcor - 50, self.ycor - 50))
        else:
            window.blit(BLACK_PIECE, (self.xcor - 50, self.ycor - 50))

        if self.colour == WHITE and self.king:
            window.blit(WHITE_KING, (self.xcor - 50, self.ycor - 50))
        if self.colour == BLACK and self.king:
            window.blit(BLACK_KING, (self.xcor - 50, self.ycor - 50))

    def get_square(self):
        """Calculates the x and y co-ordinates of the center of the square."""
        self.xcor = (self.column * 100) + 50
        self.ycor = (self.row * 100) + 50

    def move(self, row, column):
        """Changes the square co-ordinates of a piece. """
        self.row = row
        self.column = column
        self.get_square()

    def crown(self):
        """Changes a piece into a king. Called when a piece reaches the opposite side of the board."""
        self.king = True
