EMPTY = 0
WHITE = 1
BLACK = 2
MAXIMIZING_PLAYER = WHITE
VALID_MOVE = 3
GAME_IN_PROGRESS = 0
DRAW = 1
BLACK_WON = 2
WHITE_WON = 3
WHITE_IMG = "./assets/white_disk.png"
BLACK_IMG = "./assets/black_disk.png"
NEXT_MOVE_IMG = "./assets/next_move_disk.png"
BLACK_TURN_TEXT = "BLACK'S TURN"
WHITE_TURN_TEXT = "WHITE'S TURN"
BLACK_WON_TEXT = "BLACK WON!"
WHITE_WON_TEXT = "WHITE WON!"
DRAW_TEXT = "IT'S A DRAW"
BLACK_LOADING_TEXT = "BLACK'S THINKING..."
WHITE_LOADING_TEXT = "WHITE'S THINKING..."
CELL_SIZE = 64
BOARD_SIZE_VALUES = [8, 16, 32, 64]
DEPTH_MIN = 1
DEPTH_MAX = 20
EVALUATION_FNS = [
    "simple",
    "advanced"
]
DIRECTIONS = [
    "north",
    "south",
    "west",
    "east",
    "north_west",
    "north_east",
    "south_west",
    "south_east"
]
RULES = \
    "Othello (or Reversi) is a strategic board game that involves two players on a (2^k)*(2^k) (usually 8*8) " \
    "square grid with pieces that have two distinct sides (white and black). Each of the two sides corresponds to " \
    "one player; they are referred to here as White and Black. The game begins with four markers placed in a " \
    "square in the middle of the grid, two facing white-up, two pieces with the black side up. Black makes the " \
    "first move. Black must place a piece with the black side up on the board, in such a position that there " \
    "exists at least one straight (horizontal, vertical, or diagonal) line between the new piece and another " \
    "black piece, with one or more contiguous white pieces between them. After placing the piece, Black turns " \
    "over (flips or captures) all the white pieces lying on a straight line between the new piece and any " \
    "anchoring black pieces. All reversed pieces now show the black side, and Black can use them in later moves " \
    "-- unless White has reversed them back in the meantime. Now White plays. This player operates under the same " \
    "rules, with the roles reversed: White lays down a white piece, causing one or more black pieces to flip. " \
    "Players take alternate turns. If one player cannot make a valid move, the play is passed back to the other " \
    "player. When neither player can move, the game ends. This occurs when the grid has filled up, or when one " \
    "player has no more pieces on the board, or when neither player can legally place a piece in any of the " \
    "remaining squares. The player with more pieces on the board at the end wins. "
