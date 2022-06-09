from board import Board
from constants import *
import pygame.freetype


class Internals:
    def __init__(self, window):
        self.window = window
        self.board = Board()
        self.playing = BLACK
        self.selected = None
        self.game_over = False
        self.legal_moves = {}

    def update(self):
        """Updates the display and performs a win check, to be called after every move."""
        # self.board is set to None when one player has no pieces remaining.
        if self.board is None:
            if self.playing is WHITE:
                pygame.time.delay(5000)
                print("AI wins.")
                self.game_over = True
                # ^ The game loop is terminated.

            if self.playing is BLACK:
                pygame.time.delay(5000)
                print("You win!")
                self.game_over = True
                # ^ The game loop is terminated.

        else:
            # Board is redrawn to reflect current condition of the board.
            self.board.draw_board(self.window)
            # The legal moves are redrawn onto the board.
            self.draw_legal_moves(self.legal_moves)
            pygame.display.update()

    def select_piece(self, row, column):
        """Selects a piece, and calculates the legal moves that can be made by that piece."""
        selected_piece = self.board.get_piece(row, column)

        # Checks to see if the square has on of the player's pieces in it.
        if selected_piece != 0 and selected_piece.colour == self.playing:
            self.selected = selected_piece
            # Calculates the legal moves for the selected piece and updates the legal_moves dictionary.
            self.legal_moves = self.board.get_legal_moves(selected_piece)
            return True

        return False

    def draw_legal_moves(self, legal_moves):
        """Colours any the square of legal moves green."""
        # Loops through each move in the legal moves list, gets co-ords for each and colours those squares green.
        for i in legal_moves:
            row, column = i
            pygame.draw.rect(self.window, GREEN, ((column * 100), (row * 100), 100, 100))

    def move(self, row, column):
        """Moves a piece's co-ordinates within the 2D list, board.board.
        If a piece is captured, the piece is removed from the list and from the board."""
        # Sets the target square to be moved to.
        chosen_piece = self.board.get_piece(row, column)

        # Checks if the user has selected a piece to be moved, if the target square is empty, and if the target
        # square is in the list of legal moves. If all three conditions are met, the piece is moved to the target.
        if self.selected and chosen_piece == 0 and (row, column) in self.legal_moves:
            self.board.move(row, column, self.selected)
            # Checks to see if any pieces were captured from the move . Any captured pieces are added to a list.
            captured = self.legal_moves[(row, column)]
            if captured:
                # Any pieces that have been captured are removed from the board.
                self.board.remove_piece(captured)

                # Calls the regicide check. This checks if one of the captured pieces was a king.
                # If so the capturing piece immediately becomes a king and the turn ends.
                if self.board.check_regicide(captured):
                    self.selected.crown()

            self.switch_player()
        else:
            return False

        return True

    def switch_player(self):
        """Once a player has finished their turn, this method is called and the turn is transferred."""
        # Resets the legal_moves dictionary for the get_legal_moves to be called again for the other player.
        self.legal_moves = {}
        if self.playing == WHITE:
            self.playing = BLACK
        else:
            self.playing = WHITE

    def get_board(self):
        """Returns the board for use in the minimax function."""
        return self.board

    def ai_move(self, board):
        """Plays the AI's move, and passes the turn back to the player"""
        # Updates the board representation to the new board created when the AI makes a move.
        self.board = board
        # Turn is passed back to player when the AI move has been made and the board now reflects that move.
        self.switch_player()
