from tkinter import *
import numpy as np
import PIL.Image
import PIL.ImageTk
import math
from othello import Othello
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
        # Initialize agents
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
        # Initialize game object
        self.game = Othello(n)
        # Pass turn to black as black always starts first
        self.current_player = self.black
        # Initialize board parameters
        n = 2 ** math.ceil(math.log2(n))
        self.n = n
        self.size = size
        self.color = color
        # Initialize images
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
        # Initialize widgets (board, scoreboard)
        Frame.__init__(self, parent, bg="gray")
        self.black_score_var = IntVar(value=self.game.black_score)
        self.white_score_var = IntVar(value=self.game.white_score)
        if self.current_player.agent_type == "computer":
            self.game_info_var = StringVar(value=BLACK_LOADING_TEXT)
        else:
            self.game_info_var = StringVar(value=BLACK_TURN_TEXT)
        self.canvas = Canvas(self, borderwidth=0, highlightthickness=0, width=n * size, height=n * size, bg="gray")
        self.score_board = Canvas(self, width=n * size, height=60, bg="gray", highlightthickness=0)
        self.black_score_widget = Label(self.score_board, compound=LEFT, image=self.black_img,
                                        text=self.game.black_score, bg="gray", padx=25,
                                        textvariable=self.black_score_var, font='System 30 bold')
        self.white_score_widget = Label(self.score_board, compound=RIGHT, image=self.white_img,
                                        text=self.game.white_score, bg="gray", padx=25,
                                        textvariable=self.white_score_var, font='System 30 bold')
        self.info_widget = Label(self.score_board, compound=RIGHT, text=BLACK_TURN_TEXT, bg="gray", font='System 15',
                                 textvariable=self.game_info_var)
        self.black_score_widget.image = self.black_img
        self.white_score_widget.image = self.white_img
        self.moves_btns = []
        # Render widgets
        self.canvas.pack(side="top", fill="both", expand=True, padx=4, pady=4)
        self.score_board.pack(side="bottom", fill="both", expand=True, padx=4, pady=4)
        self.black_score_widget.pack(side="left")
        self.info_widget.pack(side="left", expand=True)
        self.white_score_widget.pack(side="right")

        self.canvas.bind("<Destroy>", self.quit)
        self.window_destroyed = False
        self.initialize_board()
        if self.current_player.agent_type == "computer":
            self.canvas.after(1000, self.run_player_move)
        else:
            self.run_player_move()

    def set_game_info_text(self, event=GAME_IN_PROGRESS):
        if event == GAME_IN_PROGRESS:
            if self.current_player.identifier == WHITE and self.current_player.agent_type == "computer":
                self.game_info_var.set(WHITE_LOADING_TEXT)
            if self.current_player.identifier == BLACK and self.current_player.agent_type == "computer":
                self.game_info_var.set(BLACK_LOADING_TEXT)
            if self.current_player.identifier == WHITE and self.current_player.agent_type == "human":
                self.game_info_var.set(WHITE_TURN_TEXT)
            if self.current_player.identifier == BLACK and self.current_player.agent_type == "human":
                self.game_info_var.set(BLACK_TURN_TEXT)
        elif event == BLACK_WON:
            self.game_info_var.set(BLACK_WON_TEXT)
        elif event == WHITE_WON:
            self.game_info_var.set(WHITE_WON_TEXT)
        elif event == DRAW:
            self.game_info_var.set(DRAW_TEXT)

    def run_player_move(self, move=None):
        pass_turn_to_computer = False
        if self.current_player.agent_type == "human":
            if move is not None:
                self.game.apply_move(self.current_player.identifier, move)
                self.current_player = self.black if self.current_player.identifier == WHITE else self.white
            event = self.game.status()
            if event == GAME_IN_PROGRESS:
                if self.current_player.agent_type == "human":
                    moves = self.game.move_generator(self.current_player.identifier)
                    if len(moves) == 0:  # If a player doesn't have a move, pass the play to the other player
                        self.current_player = self.black if self.current_player.identifier == WHITE else self.white
                        moves = self.game.move_generator(self.current_player.identifier)
                        if len(moves) == 0:
                            self.current_player = self.black if self.current_player.identifier == WHITE else self.white
                            event = self.game.status()
                elif self.current_player.agent_type == "computer":
                    pass_turn_to_computer = True
            self.black_score_var.set(self.game.black_score)
            self.white_score_var.set(self.game.white_score)
            self.set_game_info_text(event)
            self.refresh()
            if pass_turn_to_computer:
                self.canvas.after(0, self.run_player_move)
        elif self.current_player.agent_type == "computer":
            player_move = self.current_player.get_move(self.game)
            if player_move is not None:
                self.game.apply_move(self.current_player.identifier, player_move)
            self.current_player = self.black if self.current_player.identifier == WHITE else self.white
            event = self.game.status()
            if event == GAME_IN_PROGRESS:
                if self.current_player.agent_type == "human":
                    moves = self.game.move_generator(self.current_player.identifier)
                    if len(moves) == 0:  # If a player doesn't have a move, pass the play to the other player
                        self.current_player = self.black if self.current_player.identifier == WHITE else self.white
                        pass_turn_to_computer = True
                elif self.current_player.agent_type == "computer":
                    pass_turn_to_computer = True
            self.black_score_var.set(self.game.black_score)
            self.white_score_var.set(self.game.white_score)
            self.set_game_info_text(event)
            self.refresh()
            if pass_turn_to_computer:
                self.canvas.after(0, self.run_player_move)

    def add_piece(self, kind, row, column, hints=False):
        x0 = (column * self.size) + int(self.size / 2)
        y0 = (row * self.size) + int(self.size / 2)
        if kind == WHITE:
            self.canvas.create_image(x0, y0, image=self.white_img, tags="piece", anchor=CENTER)
        elif kind == BLACK:
            self.canvas.create_image(x0, y0, image=self.black_img, tags="piece", anchor=CENTER)
        elif kind == VALID_MOVE:
            move_btn = Button(self, bg=self.color, activebackground=self.color, relief=FLAT, overrelief=FLAT,
                              command=lambda: self.run_player_move([row, column]), anchor=CENTER)
            if hints:
                move_btn.configure(image=self.next_move_img)
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

    def refresh(self):
        if self.window_destroyed:
            return
        self.canvas.delete("piece")
        self.canvas.delete("move")
        for btn in self.moves_btns:
            btn.destroy()
            del btn
        white_pieces_indices = np.argwhere(self.game.state == WHITE)
        black_pieces_indices = np.argwhere(self.game.state == BLACK)
        next_move_indices = np.argwhere(self.game.state == VALID_MOVE)
        for index in white_pieces_indices:
            self.add_piece(WHITE, index[0], index[1])
        for index in black_pieces_indices:
            self.add_piece(BLACK, index[0], index[1])
        if self.current_player.agent_type == "human":
            for index in next_move_indices:
                self.add_piece(VALID_MOVE, index[0], index[1], self.current_player.hints)
        self.canvas.tag_raise("move")
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")
        self.canvas.update()

    def initialize_board(self):
        for row in range(self.n):
            for col in range(self.n):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=self.color, tags="square")
        white_pieces_indices = np.argwhere(self.game.state == WHITE)
        black_pieces_indices = np.argwhere(self.game.state == BLACK)
        next_move_indices = np.argwhere(self.game.state == VALID_MOVE)
        for index in white_pieces_indices:
            self.add_piece(WHITE, index[0], index[1])
        for index in black_pieces_indices:
            self.add_piece(BLACK, index[0], index[1])
        if self.current_player.agent_type == "human":
            for index in next_move_indices:
                self.add_piece(VALID_MOVE, index[0], index[1], self.current_player.hints)
        self.canvas.tag_raise("move")
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")
        self.canvas.update()

    def quit(self, event=None):
        self.window_destroyed = True
        self.destroy()
