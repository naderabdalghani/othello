from tkinter import *
import numpy as np
import PIL.Image
import PIL.ImageTk
import math
from othello import Othello, simple_evaluation_fn, advanced_evaluation_fn
from agent import Agent
from constants import WHITE, BLACK, VALID_MOVE, WHITE_IMG, BLACK_IMG, NEXT_MOVE_IMG, BLACK_TURN_TEXT, WHITE_TURN_TEXT,\
    BLACK_WON_TEXT, WHITE_WON_TEXT, DRAW_TEXT, BLACK_LOADING_TEXT, WHITE_LOADING_TEXT, GAME_IN_PROGRESS, BLACK_WON,\
    WHITE_WON, DRAW


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

        Frame.__init__(self, parent, bg="gray")
        self.black_score_var = IntVar(value=self.game.black_score)
        self.white_score_var = IntVar(value=self.game.white_score)
        self.game_info_var = StringVar(value=BLACK_TURN_TEXT)
        self.canvas = Canvas(self, borderwidth=0, highlightthickness=0,
                             width=n * size, height=n * size, bg="gray")
        self.score_board = Canvas(self, width=n * size, height=60, bg="gray", highlightthickness=0)
        self.black_score_widget = Label(self.score_board, compound=LEFT, image=self.black_img,
                                        text=self.game.black_score, bg="gray", padx=25,
                                        textvariable=self.black_score_var, font='System 30 bold')
        self.white_score_widget = Label(self.score_board, compound=RIGHT, image=self.white_img,
                                        text=self.game.white_score, bg="gray", padx=25,
                                        textvariable=self.white_score_var, font='System 30 bold')
        self.info_widget = Label(self.score_board, compound=RIGHT,
                                 text=BLACK_TURN_TEXT, bg="gray",
                                 textvariable=self.game_info_var, font='System 15')
        self.black_score_widget.image = self.black_img
        self.white_score_widget.image = self.white_img
        self.canvas.pack(side="top", fill="both", expand=True, padx=4, pady=4)
        self.score_board.pack(side="bottom", fill="both", expand=True, padx=4, pady=4)
        self.black_score_widget.pack(side="left")
        self.info_widget.pack(side="left", expand=True)
        self.white_score_widget.pack(side="right")

        self.canvas.bind("<Configure>", self.refresh)
        self.moves_btns = []
        self.run_player_move()

    def set_game_info_text(self):
        if self.current_player.identifier == WHITE and self.current_player.agent_type == "computer":
            self.game_info_var.set(WHITE_LOADING_TEXT)
        if self.current_player.identifier == BLACK and self.current_player.agent_type == "computer":
            self.game_info_var.set(BLACK_LOADING_TEXT)
        if self.current_player.identifier == WHITE and self.current_player.agent_type == "human":
            self.game_info_var.set(WHITE_TURN_TEXT)
        if self.current_player.identifier == BLACK and self.current_player.agent_type == "human":
            self.game_info_var.set(BLACK_TURN_TEXT)

    def run_player_move(self, move=None):
        if self.current_player.agent_type == "human" and move is not None:
            self.game.apply_move(self.current_player.identifier, move)
            self.black_score_var.set(self.game.black_score)
            self.white_score_var.set(self.game.white_score)
            self.current_player = self.black if self.current_player.identifier == WHITE else self.white
            self.set_game_info_text()
            self.canvas.delete("move")
            for btn in self.moves_btns:
                btn.destroy()
            self.moves_btns = []
            self.refresh()
        elif self.current_player.agent_type == "computer":
            possible_moves = self.game.move_generator(self.current_player.identifier)
            player_move = self.current_player.get_move(possible_moves)
            self.game.apply_move(self.current_player.identifier, player_move)
            self.black_score_var.set(self.game.black_score)
            self.white_score_var.set(self.game.white_score)
            self.current_player = self.black if self.current_player.identifier == WHITE else self.white
            self.set_game_info_text()
            self.refresh()

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
            self.canvas.create_window(x0, y0, anchor=CENTER, window=move_btn, height=self.size - 1, width=self.size - 1,
                                      tags="move")

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
        self.canvas.delete("move")
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
