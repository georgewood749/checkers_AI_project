import copy
from constants import *


def minimax(board, depth, max_player):
    if depth == 0:
        return board.evaluate(), board

    if max_player:
        best_move = None
        max_value = NEG_INF
        for move in return_moves(board, WHITE):
            evaluation = minimax(move, depth - 1, False)[0]
            if evaluation > max_value:
                max_value = evaluation

            if evaluation == max_value:
                best_move = move

        return max_value, best_move

    else:
        best_move = None
        min_value = INF
        for move in return_moves(board, BLACK):
            evaluation = minimax(move, depth - 1, True)[0]
            if evaluation < min_value:
                min_value = evaluation

            if evaluation == min_value:
                best_move = move

        return min_value, best_move


def ab_minimax(board, depth, a, b, max_player):
    if depth == 0:
        return board.evaluate(), board

    if max_player:
        best_move = None
        max_value = NEG_INF
        # Max value always starts as negative infinity.
        for move in return_moves(board, WHITE):
            evaluation = ab_minimax(move, depth - 1, a, b, False)[0]

            # Any score higher than negative infinity replaces the current max value.
            if evaluation > max_value:
                max_value = evaluation
            a = max(a, max_value)
            # Alpha-Beta pruning
            if a >= b:
                break

            best_move = move

        return max_value, best_move

    else:
        best_move = None
        min_value = INF
        for move in return_moves(board, BLACK):
            evaluation = ab_minimax(move, depth - 1, a, b, True)[0]

            # Any score lower than infinity replaces the current min value.
            if evaluation < min_value:
                min_value = evaluation
            b = min(b, min_value)
            # Alpha-Beta pruning
            if a >= b:
                break

            best_move = move

        return min_value, best_move


def sim_move(piece, move, board, captured):
    """To be called in return_moves function. Simulates the possible moves on the temporary board to evaluate score."""
    # Moves the chosen piece on the temporary board.
    board.move(move[0], move[1], piece)
    # If the simulated move captures a piece, the captured piece is removed from the temporary board.
    if captured:
        board.remove_piece(captured)
        # A regicide check is run on the captured piece.
        # If the captured piece was a king, the capturing piece instantly becomes a king.
        if check_ai_regicide(captured):
            piece.crown()

    # Returns the temporary board for the return_moves function to work with.
    return board


def return_moves(board, colour):
    """Returns the legal moves for each piece in the list."""
    moves = []
    # Gets the legal moves for each of the pieces in the list.
    for piece in board.return_pieces(colour):
        legal_moves = board.get_legal_moves(piece)
        # A new temporary board is created to simulate the possible moves for each piece.
        # Each possible move is added to the moves list as a new board.
        for move, captured in legal_moves.items():
            temporary_board = copy.deepcopy(board)
            temporary_piece = temporary_board.get_piece(piece.row, piece.column)
            new_board = sim_move(temporary_piece, move, temporary_board, captured)
            moves.append(new_board)

    return moves


def check_ai_regicide(pieces):
    """Checks whether captured piece was a king. If so, the capturing piece becomes a king."""
    # Loops through any captured pieces
    for piece in pieces:
        # Checks is any of the captured pieces were kings
        if piece.king:
            # Returns true if the captured piece was a king (hence the capturing piece will become a king)
            return True
        else:
            # Returns false if the captured pieces did not have a king among them (capturing piece remains non-king)
            return False
