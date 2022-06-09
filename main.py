import tkinter as t

from internals import Internals
from minimax import *


def open_rules():
    rules_text = t.Text(font="courier", wrap="word")
    rules_text.insert(1.0, RULES)
    rules_text.grid(row=3, column=0, columnspan=4)


def get_cor_from_mouse(cor):
    xcor, ycor = cor
    row = int(ycor / 100)
    column = int(xcor / 100)
    return row, column


def play(difficulty):
    window = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Checkers")

    # Removes the main_menu window to leave only the game board.
    main_menu.destroy()
    clock = pygame.time.Clock()
    game = Internals(window)

    while not game.game_over:
        clock.tick(60)

        if game.playing == WHITE:
            # Half as second delay after the user plays their move until the AI plays.
            pygame.time.delay(500)

            # Minimax function called for the AI's moves.
            # The difficulty argument relates to the depth at which the search is carried out.
            minmax, new_board = minimax(game.get_board(), difficulty, WHITE)

            # The new_board parameter is used to replace the current board representation with the new board
            # after the AI makes its move.
            game.ai_move(new_board)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # When user clicks on a piece, it selects the piece, and when the user clicks on an empty green square
            # (legal move), the piece is moved to that square.
            if event.type == pygame.MOUSEBUTTONDOWN:
                cor = pygame.mouse.get_pos()
                row, column = get_cor_from_mouse(cor)
                game.select_piece(row, column)

            # There is also drag & drop functionality. Users can drag and drop pieces.
            if event.type == pygame.MOUSEBUTTONUP:
                cor = pygame.mouse.get_pos()
                row, column = get_cor_from_mouse(cor)
                game.move(row, column)

        # After each move is made, the display updates.
        game.update()


main_menu = t.Tk()
main_menu.title('Checkers')
canvas = t.Canvas()
logo = t.Label()
logo.config(font=("courier", 60, "normal"), text="CHECKERS")

rules = t.Button(text="Rules", width=10, command=open_rules)

# The difficulty is passed into the minimax algorithm as the depth of search.
easy = t.Button(text="Easy", width=10, command=lambda: play(2))
medium = t.Button(text="Medium", width=10, command=lambda: play(3))
hard = t.Button(text="Hard", width=10, command=lambda: play(4))

logo.grid(row=0, column=1, rowspan=2, columnspan=2)

rules.grid(row=2, column=0)
easy.grid(row=2, column=1)
medium.grid(row=2, column=2)
hard.grid(row=2, column=3)

# Ensures the main menu remains open while the user selects their difficulty.
main_menu.mainloop()
