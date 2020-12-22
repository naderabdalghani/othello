from tkinter import *
import numpy as np
import PIL.Image
import PIL.ImageTk
import math
from othello import Othello, simple_evaluation_fn, advanced_evaluation_fn
from agent import Agent

WHITE = 1
BLACK = 2
NEXT_MOVE = 3
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

        self.black = Agent(black_player_type,
                           black_hints,
                           black_depth,
                           (simple_evaluation_fn if black_evaluation_fn == "simple" else advanced_evaluation_fn),
                           black_move_ordering)

        self.white = Agent(white_player_type,
                           white_hints,
                           white_depth,
                           (simple_evaluation_fn if white_evaluation_fn == "simple" else advanced_evaluation_fn),
                           white_move_ordering)
        self.player_turn = BLACK
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

        canvas_width = n * size
        canvas_height = n * size

        Frame.__init__(self, parent)
        self.canvas = Canvas(self, borderwidth=0, highlightthickness=0,
                             width=canvas_width, height=canvas_height)
        self.canvas.pack(side="top", fill="both", expand=True, padx=4, pady=4)
        self.canvas.bind("<Configure>", self.refresh)

    def add_piece(self, kind, row, column):
        x0 = (column * self.size) + int(self.size / 2)
        y0 = (row * self.size) + int(self.size / 2)
        if kind == 1:
            self.canvas.create_image(x0, y0, image=self.white_img, tags="piece", anchor=CENTER)
        elif kind == 2:
            self.canvas.create_image(x0, y0, image=self.black_img, tags="piece", anchor=CENTER)
        elif kind == 3:
            self.canvas.create_image(x0, y0, image=self.next_move_img, tags="piece", anchor=CENTER)

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

    def refresh(self, event):
        x_size = int(event.width / self.columns)
        y_size = int(event.height / self.rows)
        color = self.color
        self.size = min(x_size, y_size)
        self.update_images()
        self.canvas.delete("square")
        self.canvas.delete("piece")
        for row in range(self.rows):
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
        white_pieces_indices = np.argwhere(self.game.state == WHITE)
        black_pieces_indices = np.argwhere(self.game.state == BLACK)
        next_move_indices = np.argwhere(self.game.state == NEXT_MOVE)
        for index in white_pieces_indices:
            self.add_piece(WHITE, index[0], index[1])
        for index in black_pieces_indices:
            self.add_piece(BLACK, index[0], index[1])
        show_hints = (self.player_turn == BLACK and self.black.agent_type == "human" and self.black.hints) or \
                     (self.player_turn == WHITE and self.white.agent_type == "human" and self.white.hints)
        if show_hints:
            for index in next_move_indices:
                self.add_piece(NEXT_MOVE, index[0], index[1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")
