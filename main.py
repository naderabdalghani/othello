from tkinter import *
from board import Board
from constants import RULES, CELL_SIZE, BOARD_SIZE_VALUES, EVALUATION_FNS

BOARD_SIZE = 8
BLACK_PLAYER_TYPE = "human"
WHITE_PLAYER_TYPE = "computer"
BLACK_HINTS = True
WHITE_HINTS = True
BLACK_MOVE_ORDERING = True
WHITE_MOVE_ORDERING = True
BLACK_EVALUATION_FN = "simple"
WHITE_EVALUATION_FN = "simple"
BLACK_DEPTH = 5
WHITE_DEPTH = 5


def get_cell_size(n):
    factor = n / 8
    return CELL_SIZE / factor


def display_about_window(root):
    new_window = Toplevel(root)
    new_window.grab_set()
    new_window.title("About")
    new_window.iconbitmap("./assets/icon.ico")
    new_window.resizable(False, False)
    new_window.transient(root)
    new_window.geometry("450x460")
    new_window.focus_force()
    title = Label(new_window, text="Othello v1.0", justify=LEFT, anchor=W)
    developer = Label(new_window, text="Nader AbdAlGhani — nader_abdelghani@hotmail.com",
                      justify=LEFT, anchor=W)
    rules_title = Label(new_window, text="RULES:", font='Helvetica 12 bold', justify=LEFT, anchor=W)
    rules = Label(new_window, text=RULES, wraplength=420, justify=CENTER, anchor=W)
    label_padding = 10
    title.pack(side="top", fill="both", padx=label_padding, pady=label_padding)
    developer.pack(side="top", fill="both", padx=label_padding, pady=label_padding)
    rules_title.pack(side="top", fill="both", padx=label_padding, pady=label_padding)
    rules.pack(side="top", fill="both", padx=label_padding, pady=label_padding / 2)


def toggle_widgets(widgets):
    for widget in widgets:
        if widget["state"] == NORMAL:
            widget["state"] = DISABLED
        else:
            widget["state"] = NORMAL


def save_game_data(root,
                   board_size,
                   black_type,
                   white_type,
                   black_hints,
                   white_hints,
                   black_depth,
                   white_depth,
                   black_eval_fn,
                   white_eval_fn,
                   black_move_ordering,
                   white_move_ordering):
    global BOARD_SIZE, \
        BLACK_PLAYER_TYPE, \
        WHITE_PLAYER_TYPE, \
        BLACK_HINTS, \
        WHITE_HINTS, \
        BLACK_DEPTH, \
        WHITE_DEPTH, \
        BLACK_EVALUATION_FN, \
        WHITE_EVALUATION_FN, \
        BLACK_MOVE_ORDERING, \
        WHITE_MOVE_ORDERING

    BOARD_SIZE = board_size.get()
    BLACK_PLAYER_TYPE = black_type.get()
    WHITE_PLAYER_TYPE = white_type.get()
    BLACK_HINTS = black_hints.get()
    WHITE_HINTS = white_hints.get()
    BLACK_DEPTH = black_depth.get()
    WHITE_DEPTH = white_depth.get()
    BLACK_EVALUATION_FN = black_eval_fn.get()
    WHITE_EVALUATION_FN = white_eval_fn.get()
    BLACK_MOVE_ORDERING = black_move_ordering.get()
    WHITE_MOVE_ORDERING = white_move_ordering.get()
    root.destroy()


def reset_game_data(root,
                    board_size,
                    black_type,
                    white_type,
                    black_hints,
                    white_hints,
                    black_depth,
                    white_depth,
                    black_eval_fn,
                    white_eval_fn,
                    black_move_ordering,
                    white_move_ordering):
    global BOARD_SIZE, \
        BLACK_PLAYER_TYPE, \
        WHITE_PLAYER_TYPE, \
        BLACK_HINTS, \
        WHITE_HINTS, \
        BLACK_DEPTH, \
        WHITE_DEPTH, \
        BLACK_EVALUATION_FN, \
        WHITE_EVALUATION_FN, \
        BLACK_MOVE_ORDERING, \
        WHITE_MOVE_ORDERING
    board_size.set(BOARD_SIZE)
    black_type.set(BLACK_PLAYER_TYPE)
    white_type.set(WHITE_PLAYER_TYPE)
    black_hints.set(BLACK_HINTS)
    white_hints.set(WHITE_HINTS)
    black_depth.set(BLACK_DEPTH)
    white_depth.set(WHITE_DEPTH)
    black_eval_fn.set(BLACK_EVALUATION_FN)
    white_eval_fn.set(WHITE_EVALUATION_FN)
    black_move_ordering.set(BLACK_MOVE_ORDERING)
    white_move_ordering.set(WHITE_MOVE_ORDERING)
    if root is not None:
        root.destroy()


def display_settings_window(root,
                            board_size,
                            black_type,
                            white_type,
                            black_hints,
                            white_hints,
                            black_depth,
                            white_depth,
                            black_eval_fn,
                            white_eval_fn,
                            black_move_ordering,
                            white_move_ordering):
    settings_window = Toplevel(root)
    settings_window.grab_set()
    settings_window.title("Settings")
    settings_window.iconbitmap("./assets/icon.ico")
    settings_window.resizable(False, False)
    settings_window.transient(root)
    settings_window.geometry("320x500")
    settings_window.focus_force()
    padding = 25

    # BOARD_SIZE values dropdown menu
    board_size_label = Label(settings_window, text="Board Size:", font='Helvetica 12 bold')
    board_size_dropdown = OptionMenu(settings_window, board_size, *BOARD_SIZE_VALUES)
    # Labels
    black_label = Label(settings_window, text="Black:", font='Helvetica 12 bold')
    white_label = Label(settings_window, text="White:", font='Helvetica 12 bold')
    # Player hints
    black_hints_checkbox = Checkbutton(settings_window, text="Hints", variable=black_hints,
                                       state=(NORMAL if black_type.get() == "human" else DISABLED))
    white_hints_checkbox = Checkbutton(settings_window, text="Hints", variable=white_hints,
                                       state=(NORMAL if white_type.get() == "human" else DISABLED))
    # Depth
    black_depth_label = Label(settings_window, text="Depth:",
                              state=(NORMAL if black_type.get() == "computer" else DISABLED))
    black_depth_spinbox = Spinbox(settings_window, from_=0, to=1000, textvariable=black_depth, width=5,
                                  state=(NORMAL if black_type.get() == "computer" else DISABLED))
    white_depth_label = Label(settings_window, text="Depth:",
                              state=(NORMAL if white_type.get() == "computer" else DISABLED))
    white_depth_spinbox = Spinbox(settings_window, from_=0, to=1000, textvariable=white_depth, width=5,
                                  state=(NORMAL if white_type.get() == "computer" else DISABLED))
    # Evaluation functions
    black_eval_label = Label(settings_window, text="Evaluation Fn:",
                             state=(NORMAL if black_type.get() == "computer" else DISABLED))
    black_eval_dropdown = OptionMenu(settings_window, black_eval_fn, *EVALUATION_FNS)
    black_eval_dropdown["state"] = NORMAL if black_type.get() == "computer" else DISABLED
    white_eval_label = Label(settings_window, text="Evaluation Fn:",
                             state=(NORMAL if white_type.get() == "computer" else DISABLED))
    white_eval_dropdown = OptionMenu(settings_window, white_eval_fn, *EVALUATION_FNS)
    white_eval_dropdown["state"] = NORMAL if white_type.get() == "computer" else DISABLED
    # Move ordering
    black_move_ord_checkbox = Checkbutton(settings_window, text="Move Ordering", variable=black_move_ordering,
                                          state=(NORMAL if black_type.get() == "computer" else DISABLED))
    white_move_ord_checkbox = Checkbutton(settings_window, text="Move Ordering", variable=white_move_ordering,
                                          state=(NORMAL if white_type.get() == "computer" else DISABLED))
    # Player type radio buttons
    black_human_radio_btn = Radiobutton(settings_window, text="Human", padx=20, variable=black_type, value="human",
                                        command=lambda: toggle_widgets([
                                                                            black_hints_checkbox,
                                                                            black_depth_label,
                                                                            black_depth_spinbox,
                                                                            black_eval_dropdown,
                                                                            black_eval_label,
                                                                            black_move_ord_checkbox
                                                                        ]))
    black_computer_radio_btn = Radiobutton(settings_window, text="Computer", padx=20, variable=black_type,
                                           value="computer", command=lambda: toggle_widgets([
                                                                                                black_hints_checkbox,
                                                                                                black_depth_label,
                                                                                                black_depth_spinbox,
                                                                                                black_eval_dropdown,
                                                                                                black_eval_label,
                                                                                                black_move_ord_checkbox
                                                                                            ]))
    white_human_radio_btn = Radiobutton(settings_window, text="Human", padx=20, variable=white_type, value="human",
                                        command=lambda: toggle_widgets([
                                                                            white_hints_checkbox,
                                                                            white_depth_label,
                                                                            white_depth_spinbox,
                                                                            white_eval_dropdown,
                                                                            white_eval_label,
                                                                            white_move_ord_checkbox
                                                                        ]))
    white_computer_radio_btn = Radiobutton(settings_window, text="Computer", padx=20, variable=white_type,
                                           value="computer", command=lambda: toggle_widgets([
                                                                                                white_hints_checkbox,
                                                                                                white_depth_label,
                                                                                                white_depth_spinbox,
                                                                                                white_eval_dropdown,
                                                                                                white_eval_label,
                                                                                                white_move_ord_checkbox
                                                                                            ]))

    board_size_label.grid(column=1, row=1, sticky=W, ipadx=padding, ipady=padding)
    board_size_dropdown.grid(column=2, row=1, sticky=W, ipadx=padding)

    black_label.grid(column=1, row=2, sticky=W, ipadx=padding)
    black_human_radio_btn.grid(column=1, row=3, sticky=W, ipadx=padding)
    black_computer_radio_btn.grid(column=2, row=3, sticky=W, ipadx=padding)
    black_hints_checkbox.grid(column=1, row=4, sticky=W, ipadx=padding)
    black_depth_label.grid(column=1, row=6, sticky=W, ipadx=padding)
    black_depth_spinbox.grid(column=2, row=6, sticky=W, ipadx=padding)
    black_eval_label.grid(column=1, row=7, sticky=W, ipadx=padding)
    black_eval_dropdown.grid(column=2, row=7, sticky=W, ipadx=padding)
    black_move_ord_checkbox.grid(column=1, row=8, sticky=W, ipadx=padding)

    white_label.grid(column=1, row=10, sticky=W, ipadx=padding, pady=(padding, 0))
    white_human_radio_btn.grid(column=1, row=11, sticky=W, ipadx=padding)
    white_computer_radio_btn.grid(column=2, row=11, sticky=W, ipadx=padding)
    white_hints_checkbox.grid(column=1, row=12, sticky=W, ipadx=padding)
    white_depth_label.grid(column=1, row=14, sticky=W, ipadx=padding)
    white_depth_spinbox.grid(column=2, row=14, sticky=W, ipadx=padding)
    white_eval_label.grid(column=1, row=15, sticky=W, ipadx=padding)
    white_eval_dropdown.grid(column=2, row=15, sticky=W, ipadx=padding)
    white_move_ord_checkbox.grid(column=1, row=16, sticky=W, ipadx=padding)

    save_btn = Button(settings_window, text="Save", font='Helvetica 12 italic',
                      command=lambda: save_game_data(settings_window,
                                                     board_size,
                                                     black_type,
                                                     white_type,
                                                     black_hints,
                                                     white_hints,
                                                     black_depth,
                                                     white_depth,
                                                     black_eval_fn,
                                                     white_eval_fn,
                                                     black_move_ordering,
                                                     white_move_ordering))
    cancel_btn = Button(settings_window, text="Cancel", font='Helvetica 12 italic',
                        command=lambda: reset_game_data(settings_window,
                                                        board_size,
                                                        black_type,
                                                        white_type,
                                                        black_hints,
                                                        white_hints,
                                                        black_depth,
                                                        white_depth,
                                                        black_eval_fn,
                                                        white_eval_fn,
                                                        black_move_ordering,
                                                        white_move_ordering))
    save_btn.grid(column=1, row=20, sticky=S, ipadx=padding, pady=padding)
    cancel_btn.grid(column=2, row=20, sticky=S, ipadx=padding, pady=padding)


def start_game(root,
               board_size,
               black_type,
               white_type,
               black_hints,
               white_hints,
               black_depth,
               white_depth,
               black_eval_fn,
               white_eval_fn,
               black_move_ordering,
               white_move_ordering):
    for widget in root.winfo_children():
        widget.destroy()
    root.geometry("")
    add_menu_widget(root,
                    board_size,
                    black_type,
                    white_type,
                    black_hints,
                    white_hints,
                    black_depth,
                    white_depth,
                    black_eval_fn,
                    white_eval_fn,
                    black_move_ordering,
                    white_move_ordering)
    board = Board(root,
                  BOARD_SIZE,
                  get_cell_size(BOARD_SIZE),
                  "green",
                  BLACK_PLAYER_TYPE,
                  WHITE_PLAYER_TYPE,
                  BLACK_HINTS,
                  WHITE_HINTS,
                  BLACK_DEPTH,
                  WHITE_DEPTH,
                  BLACK_EVALUATION_FN,
                  WHITE_EVALUATION_FN,
                  BLACK_MOVE_ORDERING,
                  WHITE_MOVE_ORDERING)
    board.pack(side="top", padx=4, pady=4)


def add_menu_widget(root,
                    board_size,
                    black_type,
                    white_type,
                    black_hints,
                    white_hints,
                    black_depth,
                    white_depth,
                    black_eval_fn,
                    white_eval_fn,
                    black_move_ordering,
                    white_move_ordering):
    menu_bar = Menu(root)
    game_menu = Menu(menu_bar, tearoff=0)
    game_menu.add_command(label="New Game", command=lambda: start_game(root,
                                                                       board_size,
                                                                       black_type,
                                                                       white_type,
                                                                       black_hints,
                                                                       white_hints,
                                                                       black_depth,
                                                                       white_depth,
                                                                       black_eval_fn,
                                                                       white_eval_fn,
                                                                       black_move_ordering,
                                                                       white_move_ordering))
    game_menu.add_command(label="Settings", command=lambda: display_settings_window(root,
                                                                                    board_size,
                                                                                    black_type,
                                                                                    white_type,
                                                                                    black_hints,
                                                                                    white_hints,
                                                                                    black_depth,
                                                                                    white_depth,
                                                                                    black_eval_fn,
                                                                                    white_eval_fn,
                                                                                    black_move_ordering,
                                                                                    white_move_ordering))
    game_menu.add_separator()
    game_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="Game", menu=game_menu)
    menu_bar.add_command(label="About", command=lambda: display_about_window(root))
    root.config(menu=menu_bar)


def main():
    root = Tk()
    root.title("Othello")
    root.iconbitmap("./assets/icon.ico")
    root.geometry("400x250")
    root.resizable(False, False)

    global BOARD_SIZE, \
        BLACK_PLAYER_TYPE, \
        WHITE_PLAYER_TYPE, \
        BLACK_HINTS, \
        WHITE_HINTS, \
        BLACK_DEPTH, \
        WHITE_DEPTH, \
        BLACK_EVALUATION_FN, \
        WHITE_EVALUATION_FN, \
        BLACK_MOVE_ORDERING, \
        WHITE_MOVE_ORDERING

    board_size = IntVar(value=BOARD_SIZE)
    black_type = StringVar(value=BLACK_PLAYER_TYPE)
    white_type = StringVar(value=WHITE_PLAYER_TYPE)
    black_hints = BooleanVar(value=BLACK_HINTS)
    white_hints = BooleanVar(value=WHITE_HINTS)
    black_depth = StringVar(value=BLACK_DEPTH)
    white_depth = StringVar(value=WHITE_DEPTH)
    black_eval_fn = StringVar(value=BLACK_EVALUATION_FN)
    white_eval_fn = StringVar(value=WHITE_EVALUATION_FN)
    black_move_ordering = BooleanVar(value=BLACK_MOVE_ORDERING)
    white_move_ordering = BooleanVar(value=WHITE_MOVE_ORDERING)

    add_menu_widget(root,
                    board_size,
                    black_type,
                    white_type,
                    black_hints,
                    white_hints,
                    black_depth,
                    white_depth,
                    black_eval_fn,
                    white_eval_fn,
                    black_move_ordering,
                    white_move_ordering)

    start_btn = Button(root, height=2, width=15, text="Start",
                       font='Helvetica 12 italic', command=lambda: start_game(root,
                                                                              board_size,
                                                                              black_type,
                                                                              white_type,
                                                                              black_hints,
                                                                              white_hints,
                                                                              black_depth,
                                                                              white_depth,
                                                                              black_eval_fn,
                                                                              white_eval_fn,
                                                                              black_move_ordering,
                                                                              white_move_ordering))
    settings_btn = Button(root, height=2, width=15, text="Settings",
                          font='Helvetica 12 italic',
                          command=lambda: display_settings_window(root,
                                                                  board_size,
                                                                  black_type,
                                                                  white_type,
                                                                  black_hints,
                                                                  white_hints,
                                                                  black_depth,
                                                                  white_depth,
                                                                  black_eval_fn,
                                                                  white_eval_fn,
                                                                  black_move_ordering,
                                                                  white_move_ordering))
    start_btn.place(relx=0.5, rely=0.3, anchor=CENTER)
    settings_btn.place(relx=0.5, rely=0.6, anchor=CENTER)
    root.mainloop()


if __name__ == "__main__":
    main()
