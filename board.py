from tkinter import *
import numpy as np
import PIL.Image
import PIL.ImageTk
import math
from othello import Othello, simple_evaluation_fn, advanced_evaluation_fn
from agent import Agent

WHITE = 1
BLACK = 2
VALID_MOVE = 3
WHITE_IMG = "./assets/white_disk.png"
BLACK_IMG = "./assets/black_disk.png"
NEXT_MOVE_IMG = "./assets/next_move_disk.png"


class Board(Frame):
    def __init__(self,
                 parent,
                 n,
                 size,
                 color,
                 black_player_type,
                 white_player_type,
                 black_hints,
                 white_hints,
                 black_depth,
                 white_depth,
                 black_evaluation_fn,
                 white_evaluation_fn,
                 black_move_ordering,
                 white_move_ordering):

        self.black = Agent(BLACK,
                           black_player_type,
                           black_hints,
                           black_depth,
                           (simple_evaluation_fn if black_evaluation_fn == "simple" else advanced_evaluation_fn),
                           black_move_ordering)

        self.white = Agent(WHITE,
                           white_player_type,
                           white_hints,
                           white_depth,
                           (simple_evaluation_fn if white_evaluation_fn == "simple" else advanced_evaluation_fn),
                           white_move_ordering)
        self.current_player = self.black
        n = 2 ** math.ceil(math.log2(n))
        self.rows = n
        self.columns = n
        self.size = size
        self.color = color
        self.game = Othello(n)
        self.image_size = math.floor(size * 0.75)
        image = PIL.Image.open(WHITE_IMG)
        image = image.resize((self.image_size, self.image_size))
        self.white_img = PIL.ImageTk.PhotoImage(image)
        image = PIL.Image.open(BLACK_IMG)
        image = image.resize((self.image_size, self.image_size))
        self.black_img = PIL.ImageTk.PhotoImage(image)
        image = PIL.Image.open(NEXT_MOVE_IMG)
        image = image.resize((self.image_size, self.image_size))
        self.next_move_img = PIL.ImageTk.PhotoImage(image)

        Frame.__init__(self, parent)
        self.canvas = Canvas(self, borderwidth=0, highlightthickness=0,
                             width=n * size, height=n * size)
        self.canvas.pack(side="top", fill="both", expand=True, padx=4, pady=4)

        self.canvas.bind("<Configure>", self.refresh)
        self.moves_btns = []
        self.run_player_move()

    def run_player_move(self, move=None):
        if self.current_player.agent_type == "human" and move is not None:
            self.game.apply_move(self.current_player.identifier, move)
            self.current_player = self.black if self.current_player.identifier == WHITE else self.white
            for btn in self.moves_btns:
                btn.destroy()
            self.moves_btns = []
            self.refresh()
        elif self.current_player.agent_type == "computer":
            possible_moves = self.game.move_generator(self.current_player.identifier)
            player_move = self.current_player.get_move(possible_moves)
            self.game.apply_move(self.current_player.identifier, player_move)
            self.current_player = self.black if self.current_player.identifier == WHITE else self.white
            self.canvas.update()

    def add_piece(self, kind, row, column):
        x0 = (column * self.size) + int(self.size / 2)
        y0 = (row * self.size) + int(self.size / 2)
        if kind == WHITE:
            self.canvas.create_image(x0, y0, image=self.white_img, tags="piece", anchor=CENTER)
        elif kind == BLACK:
            self.canvas.create_image(x0, y0, image=self.black_img, tags="piece", anchor=CENTER)
        elif kind == VALID_MOVE:
            move_btn = Button(self, image=self.next_move_img,
                              command=lambda: self.run_player_move([row, column]), anchor=CENTER)
            move_btn.configure(bg=self.color, activebackground=self.color, relief=FLAT, overrelief=FLAT)
            self.moves_btns.append(move_btn)
            self.canvas.create_window(x0, y0, anchor=CENTER, window=move_btn, height=self.size - 1, width=self.size - 1)

    def update_images(self):
        self.image_size = math.floor(self.size * 0.75)
        image = PIL.Image.open(WHITE_IMG)
        image = image.resize((self.image_size, self.image_size))
        self.white_img = PIL.ImageTk.PhotoImage(image)
        image = PIL.Image.open(BLACK_IMG)
        image = image.resize((self.image_size, self.image_size))
        self.black_img = PIL.ImageTk.PhotoImage(image)
        image = PIL.Image.open(NEXT_MOVE_IMG)
        image = image.resize((self.image_size, self.image_size))
        self.next_move_img = PIL.ImageTk.PhotoImage(image)

    def refresh(self, event=None):
        if event is not None:
            x_size = int(event.width / self.columns)
            y_size = int(event.height / self.rows)
            self.size = min(x_size, y_size)
            self.update_images()
        color = self.color
        self.canvas.delete("square")
        self.canvas.delete("piece")
        for btn in self.moves_btns:
            btn.destroy()
        self.moves_btns = []
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
        white_pieces_indices = np.argwhere(self.game.state == WHITE)
        black_pieces_indices = np.argwhere(self.game.state == BLACK)
        next_move_indices = np.argwhere(self.game.state == VALID_MOVE)
        for index in white_pieces_indices:
            self.add_piece(WHITE, index[0], index[1])
        for index in black_pieces_indices:
            self.add_piece(BLACK, index[0], index[1])
        show_hints = (self.current_player == self.black and self.black.agent_type == "human" and self.black.hints) or \
                     (self.current_player == self.white and self.white.agent_type == "human" and self.white.hints)
        if show_hints:
            for index in next_move_indices:
                self.add_piece(VALID_MOVE, index[0], index[1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")
