import tkinter as tk
from board import Board

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


def display_about_window(root):
    new_window = tk.Toplevel(root)
    new_window.grab_set()
    new_window.title("About")
    new_window.iconbitmap("./assets/icon.ico")
    new_window.resizable(False, False)
    new_window.transient(root)
    new_window.geometry("450x460")
    new_window.focus_force()
    title = tk.Label(new_window, text="Othello v1.0", justify=tk.LEFT, anchor=tk.W)
    developer = tk.Label(new_window, text="Nader AbdAlGhani — nader_abdelghani@hotmail.com",
                         justify=tk.LEFT, anchor=tk.W)
    rules_title = tk.Label(new_window, text="RULES:", font='Helvetica 12 bold', justify=tk.LEFT, anchor=tk.W)
    rules = tk.Label(new_window, text=RULES, wraplength=420, justify=tk.CENTER, anchor=tk.W)
    label_padding = 10
    title.pack(side="top", fill="both", padx=label_padding, pady=label_padding)
    developer.pack(side="top", fill="both", padx=label_padding, pady=label_padding)
    rules_title.pack(side="top", fill="both", padx=label_padding, pady=label_padding)
    rules.pack(side="top", fill="both", padx=label_padding, pady=label_padding/2)


def main():
    root = tk.Tk()
    root.title("Othello")
    root.iconbitmap("./assets/icon.ico")
    # add menu bar
    menu_bar = tk.Menu(root)
    game_menu = tk.Menu(menu_bar, tearoff=0)
    game_menu.add_command(label="New Game")
    game_menu.add_command(label="Settings")
    game_menu.add_separator()
    game_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="Game", menu=game_menu)
    menu_bar.add_command(label="About", command=lambda: display_about_window(root))
    root.config(menu=menu_bar)
    board = Board(root, n=8)
    board.pack(side="top", padx=4, pady=4)
    root.mainloop()


if __name__ == "__main__":
    main()
