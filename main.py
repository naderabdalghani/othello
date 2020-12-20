import tkinter as tk
from board import Board

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Othello")
    root.iconbitmap("./assets/icon.ico")
    board = Board(root, n=8)
    board.pack(side="top", fill="both", expand=True, padx=4, pady=4)
    root.mainloop()
