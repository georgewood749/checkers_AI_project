import pygame

# colours (RGB)
WHITE = (230, 220, 200)
BLACK = (50, 50, 50)
GREEN = (75, 200, 5)

# pieces
BLACK_PIECE = pygame.transform.scale(pygame.image.load('images/black_piece.png'), (100, 100))
WHITE_PIECE = pygame.transform.scale(pygame.image.load('images/white_piece.png'), (100, 100))

# kings
BLACK_KING = pygame.transform.scale(pygame.image.load('images/black_king.png'), (100, 100))
WHITE_KING = pygame.transform.scale(pygame.image.load('images/white_king.png'), (100, 100))

INF = float('inf')
NEG_INF = float('-inf')
ALPHA = float('-inf')
BETA = float('inf')


RULES = "RULES OF CHECKERS \n" \
        "\nThe rules below form a general basis for your coursework implementation of checkers. Note that the marking "\
        "criteria for the assignment specify additional features and rules to those outlined here. So, please make " \
        "sure you pay attention to the details given in the assignment guidelines.\n" \
        "\n" \
        "\nSETUP YOUR CHECKERBOARD\n" \
        "\nCheckers is played on a board made up of squares. The squares are laid out in eight columns and eight rows.\n"\
        "\nCheckers is a game for two players. Each player receives twelve, flat disk-like pieces which are placed on " \
        "the black squares of the first 3 rows of each end of the board. Be sure that a light-coloured square " \
        "appears in the lower right-hand corner of the board.\n" \
        "\nThe darker- coloured checkers are usually designated " \
        "black, and the lighter colour is designated white. Black always moves first.\n" \
        "\n" \
        "\nGENERAL RULES FOR CHECKERS\n" \
        "\nNow that you have set up the board, you are ready to begin play. First, determine who is to be 'black'. You " \
        "can use any method for this you wish, flip a coin, alternate, etc. However, the most common method in " \
        "amateur play is for one of the players to take one colour checker in each hand and hold out his hands before "\
        "him. The other player chooses a hand, the colour checker in that hand determines the colour with which he " \
        "plays.\n" \
        "\nThe object is to eliminate all opposing checkers or to create a situation in which it is impossible for your"\
        "opponent to make any move. Normally, the victory will be due to complete elimination.\n" \
        "\nBlack moves first and play proceeds alternately. From their initial positions, checkers may only move " \
        "forward. There are two types of moves that can be made, capturing moves and non- capturing moves. " \
        "Non-capturing moves are simply a diagonal move forward from one square to an adjacent square. (Note that the "\
        "white squares are never used.) Capturing moves occur when a player 'jumps' an opposing piece. This is also " \
        "done on the diagonal and can only happen when the square behind (on the same diagonal) is also open. This " \
        "means that you may not jump an opposing piece around a corner.\n" \
        "\nOn a capturing move, a piece may make multiple jumps. If after a jump a player is in a position to make " \
        "another jump then he may do so. This means that a player may make several jumps in succession, " \
        "capturing several pieces on a single turn.\n" \
        "\n" \
        "\nCROWNING KINGS IN CHECKERS\n" \
        "\nWhen a checker achieves the opponent's edge of the board (called the 'king row') it is crowned with another " \
        "checker. This signifies that the checker has been made a king. The king now gains an added ability to move " \
        "backward. The king may now also jump in either direction or even in both directions in one turn (if he makes "\
        "multiple jumps).\n" \
        "\nA similar idea in the game of chess occurs when a pawn reaches the opponent's end of the board it becomes a "\
        "queen. There is a practical reason for these piece promotions. Without it, a piece which can only move in " \
        "one direction becomes worthless. Interestingly enough, it also has some social significance in that it " \
        "signifies that royalty and power should not be simply endowed at birth. Nobility is something that can be " \
        "and should be earned.\n" \
        "\nIf the player gets an uncrowned checker on the king's row because of a capturing move then he must stop to "\
        "be crowned even if another capture seems to be available. He may then use his new king on his next move.\n" \
        "\n" \
        "\nCHECKERS STRATEGY\n" \
        "\nCheckers is a straight-forward game in many ways. Yet, play can unfold in intricate layers. Every move opens "\
        "untold possibilities and closes down untold more. Thus, it is well to keep a few strategies in mind when " \
        "playing, even when it is just for fun.\n" \
        "\nFirst, always keep in mind the possibility of using the forced capture rule to maneuver your opponent into a "\
        "position where he gives up two pieces for one of your own. Often a one piece advantage can make all the " \
        "difference in the end game.\n" \
        "\nSecond, always try to keep the lanes to your own king's row blocked to your opponent. Once either side gets " \
        "a king, any uncrowned checker in the open is highly vulnerable.\n" \
        "\nThird, move between your own pieces and your opponent in order to move adjacent to an opposing checker " \
        "without loss.\n" \
        "\nOf course, these are elementary ideas to the tournament player. To move beyond the beginner stage, " \
        "a player will want to acquire a book on checkers and checker strategy. An excellent place to begin is Fred " \
        "Reinfeld's book, How to win at Checkers. "
