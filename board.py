from constants import *
from pieces import Pieces


class Board:
    def __init__(self):
        """Initialises the board class. Setting the number of each colour's starting pieces to 12 and kings to 0."""
        self.whites = 12
        self.blacks = 12
        self.white_kings = 0
        self.black_kings = 0
        self.board = []
        self.create_board()
        self.selected_piece = None
        # ^ Creates the board representation and displays the interactive board. Sets the selected piece to none.

    def create_board(self):
        """Creates the state representation, a 2-dimensional list, to represent the board."""
        # Each square on the board is given an x and y co-ordinate. The pieces are then added to this 2D list, where a 0
        # symbolises an empty square, and an occupied square is shown as the colour of the piece in that square.

        for row in range(8):
            # Creates a representation for each row in the self.board list
            self.board.append([])
            # Loops through all the black squares on the board to insert pieces, where applicable.
            for column in range(8):
                if column % 2 == ((row + 1) % 2):

                    # Inserts the starting pieces into the first three rows of each player's side of the board.
                    if row <= 2:
                        self.board[row].append(Pieces(WHITE, row, column))
                    elif row >= 5:
                        self.board[row].append(Pieces(BLACK, row, column))

                    # Sets each square in the two middle rows to be 0s, as none of these squares contain pieces.
                    else:
                        self.board[row].append(0)

                # Any red square on the board is allocated a 0.
                else:
                    self.board[row].append(0)

    def draw_black_row(self, window, row):
        """Draws a row with a black square in the leftmost space."""
        for column in range(8):
            if column % 2 == 0:
                # Every other square is filled in white.
                pygame.draw.rect(window, WHITE, (row * 100, column * 100, 100, 100))
            else:
                pygame.draw.rect(window, BLACK, (row * 100, column * 100, 100, 100))

    def draw_white_row(self, window, row):
        """Draws a row with a white square in the leftmost space."""
        for column in range(8):
            if column % 2 == 0:
                # Every other square is filled in black.
                pygame.draw.rect(window, BLACK, (row * 100, column * 100, 100, 100))
            else:
                pygame.draw.rect(window, WHITE, (row * 100, column * 100, 100, 100))

    def draw_board(self, window):
        """Draws the entire by calling the previous two functions"""
        for row in range(8):
            # Every other row has a black square in the corner.
            if row % 2 == 0:
                self.draw_black_row(window, row)
            else:
                self.draw_white_row(window, row)

        # The pieces are drawn onto the board.
        self.add_pieces(window)

    def add_pieces(self, window):
        """Draws the piece onto the board. Uses the board matrix"""
        # Loops through each square and inserts a piece if the item in the 2D list is allocated to a colour (not 0).
        for row in range(8):
            for column in range(8):
                piece = self.board[row][column]
                if piece != 0:
                    piece.draw(window)

    def get_piece(self, row, column):
        """Returns the row and column coordinates of the desired piece."""
        return self.board[row][column]

    def move(self, row, column, piece):
        """Moves a piece on the board and in the 2D list."""
        # Swaps the coordinates for the selected piece and the target square.
        self.board[piece.row][piece.column], self.board[row][column] = \
            self.board[row][column], self.board[piece.row][piece.column]
        piece.move(row, column)

        # If a piece reaches the opposite end of the board, that piece gets turned into a king.
        if row == 0 or row == 7:
            piece.crown()
            if piece.colour == BLACK:
                self.black_kings += 1
            else:
                self.white_kings += 1

    def get_legal_moves(self, selected_piece):
        """Calculates the legal moves that can be made by the current player."""
        legal_moves = {}
        left_column = selected_piece.column - 1
        right_column = selected_piece.column + 1
        row = selected_piece.row

        # Adds the applicable left and right forward moves to the legal moves list.
        if selected_piece.colour == BLACK:
            legal_moves.update(self.move_left(selected_piece.colour, -1, left_column, row - 1, max(row - 3, -1)))
            legal_moves.update(self.move_right(selected_piece.colour, -1, right_column, row - 1, max(row - 3, -1)))

        # Adds the applicable left and right forward moves to the legal moves list.
        if selected_piece.colour == WHITE:
            legal_moves.update(self.move_left(selected_piece.colour, 1, left_column, row + 1, min(row + 3, 8)))
            legal_moves.update(self.move_right(selected_piece.colour, 1, right_column, row + 1, min(row + 3, 8)))

        # Adds all applicable moves to the legal moves list (when piece is a king it can move in all 4 directions.)
        if selected_piece.king:
            legal_moves.update(self.move_left(selected_piece.colour, -1, left_column, row - 1, max(row - 3, -1)))
            legal_moves.update(self.move_right(selected_piece.colour, -1, right_column, row - 1, max(row - 3, -1)))
            legal_moves.update(self.move_left(selected_piece.colour, 1, left_column, row + 1, min(row + 3, 8)))
            legal_moves.update(self.move_right(selected_piece.colour, 1, right_column, row + 1, min(row + 3, 8)))

        return legal_moves

    def move_left(self, colour, direction, column, start, finish, captured=[]):
        """Moves the selected piece diagonally left."""
        legal_moves = {}
        last = []
        # If the piece is already in the leftmost column, it cannot move left, hence the loop is broken and that move
        # is not added to the legal moves list.
        for i in range(start, finish, direction):
            if column < 0:
                break
            selected_square = self.board[i][column]
            # Checks that the target square is empty.
            if selected_square == 0:
                # Checks if a piece has been captured and there are no other pieces that can be taken from that move.
                if captured and not last:
                    break
                # If a piece was captured, checks if another piece can be captured from the same move.
                elif captured:
                    legal_moves[(i, column)] = last + captured
                # If nothing can be skipped, legal_moves is updated with just the player move (no captures).
                else:
                    legal_moves[(i, column)] = last
                # If the target square is empty and the piece has already captured another piece, the following block
                # of code checks to see if multi-leg moves can be made, by recursively calling the move_left and
                # move_right methods.
                if last:
                    if direction == 1:
                        row = min(i + 3, 8)
                    else:
                        row = max(i - 3, 0)
                    legal_moves.update(self.move_left(colour, direction, column - 1, i + direction, row, captured=last))
                    legal_moves.update(
                        self.move_right(colour, direction, column + 1, i + direction, row, captured=last))
                break
            # If the square is occupied by a piece of the playing colour, the moving piece is blocked. Hence, the loop
            # is broken and no moves are added to legal moves
            elif selected_square.colour == colour:
                break
            # If there is a piece of the opposing colour in that square, the piece can be jumped over and captured.
            else:
                last = [selected_square]
            column -= 1

        return legal_moves

    def move_right(self, colour, direction, column, start, finish, captured=[]):
        """Moves the selected piece diagonally right."""
        legal_moves = {}
        last = []
        for i in range(start, finish, direction):
            # If the piece is already in the leftmost column, it cannot move left, hence it is not added to the legal
            # moves list.
            if column > 7:
                break
            selected_square = self.board[i][column]
            # Checks that the target square is empty.
            if selected_square == 0:
                # Checks if a piece has been captured and there are no other pieces that can be taken from that move.
                if captured and not last:
                    break
                # If a piece was captured, checks if another piece can be captured from the same move.
                elif captured:
                    legal_moves[(i, column)] = last + captured
                # If nothing can be skipped, legal_moves is updated with just the player move (no captures).
                else:
                    legal_moves[(i, column)] = last
                # If the target square is empty and the piece has already captured another piece, the following block
                # of code checks to see if multi-leg moves can be made, by recursively calling the move_left and
                # move_right methods.
                if last:
                    if direction == 1:
                        row = min(i + 3, 8)
                    else:
                        row = max(i - 3, 0)
                    legal_moves.update(self.move_left(colour, direction, column - 1, i + direction, row, captured=last))
                    legal_moves.update(
                        self.move_right(colour, direction, column + 1, i + direction, row, captured=last))
                break
            # If the square is occupied by a piece of the playing colour, the moving piece is blocked. Hence, the loop
            # is broken and no moves are added to legal moves
            elif selected_square.colour == colour:
                break
            # If there is a piece of the opposing colour in that square, the piece can be jumped over and captured.
            else:
                last = [selected_square]
            column += 1

        return legal_moves

    def remove_piece(self, pieces):
        """Removes desired number of pieces from the board and decreases class attribute for that colour's pieces"""
        # Captured pieces list is passed into this method, and the list is looped through
        for piece in pieces:
            # The 2D list is updated so that the piece is replaced with a 0
            self.board[piece.row][piece.column] = 0

            # Decreases the piece count for the corresponding colour
            if piece.colour == WHITE:
                self.whites -= 1
            else:
                self.blacks -= 1

    def check_regicide(self, pieces):
        """Checks whether captured piece was a king. If so, the capturing piece becomes a king."""
        # Loops through each piece in the list of captured pieces to check if any are kings
        for piece in pieces:
            if piece.king:
                return True
            else:
                return False

    def evaluate(self):
        """Evaluation function. Evaluates the state of the game from the white player's perspective."""
        # Evaluation function determines how strong a position the AI is in. Heuristic is used here, where kings are
        # weighted more than standard pieces, hence the AI aims to get king pieces.
        return self.whites - self.blacks + (self.white_kings * 2 - self.black_kings * 2)

    def return_pieces(self, colour):
        """Creates a list of all the corresponding colour's pieces."""
        pieces = []
        # Loops through each square in the board, and checks if it contains a piece of the corresponding colour.
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.colour == colour:
                    pieces.append(piece)

        return pieces
