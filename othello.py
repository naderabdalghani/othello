import numpy as np

EMPTY = 0
WHITE = 1
BLACK = 2
VALID_MOVE = 3
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


class Move:
    def __init__(self, x, y, value=None):
        self.x = x
        self.y = y
        self.value = value


class Othello:
    def __init__(self, n):
        self.n = n
        self.state = np.zeros((self.n, self.n))
        self.state[self.n // 2, self.n // 2] = WHITE
        self.state[self.n // 2 - 1, self.n // 2 - 1] = WHITE
        self.state[self.n // 2 - 1, self.n // 2] = BLACK
        self.state[self.n // 2, self.n // 2 - 1] = BLACK
        self.black_score = 2
        self.white_score = 2
        self.move_generator(BLACK)

    def move_generator(self, player):
        moves = []
        self.state[self.state == VALID_MOVE] = EMPTY
        pieces_indices = np.argwhere(self.state == player)
        opponent = WHITE if player == BLACK else BLACK
        for index in pieces_indices:
            for direction in DIRECTIONS:
                self.single_piece_move_generator(player, opponent, index, direction, moves)
        return moves

    def single_piece_move_generator(self, player, opponent, start, direction, moves):
        delta_x = None
        delta_y = None
        if direction == "north":
            delta_x = -1
            delta_y = 0
        elif direction == "south":
            delta_x = 1
            delta_y = 0
        elif direction == "west":
            delta_x = 0
            delta_y = -1
        elif direction == "east":
            delta_x = 0
            delta_y = 1
        elif direction == "north_west":
            delta_x = -1
            delta_y = -1
        elif direction == "north_east":
            delta_x = -1
            delta_y = 1
        elif direction == "south_west":
            delta_x = 1
            delta_y = -1
        elif direction == "south_east":
            delta_x = 1
            delta_y = 1
        x = start[0]
        y = start[1]
        last_seen_opponent_piece = None
        while not self.out_of_bounds(x, y):
            x += delta_x
            y += delta_y
            if self.state[x, y] == opponent:
                last_seen_opponent_piece = [x, y]
            elif self.state[x, y] == player:
                break
            elif self.state[x, y] == EMPTY:
                if last_seen_opponent_piece is not None:
                    if not self.out_of_bounds(x, y):
                        self.state[x, y] = VALID_MOVE
                        moves.append(Move(x, y))
                        break
                break

    def out_of_bounds(self, x, y):
        return x < 0 or y < 0 or x >= self.n or y >= self.n

    def apply_move(self, player, move):
        self.state[move[0], move[1]] = player
        if player == BLACK:
            self.black_score += 1
        else:
            self.white_score += 1
        opponent = WHITE if player == BLACK else BLACK
        for direction in DIRECTIONS:
            self.apply_move_single_direction(player, opponent, move, direction)
        self.state[self.state == VALID_MOVE] = EMPTY

    def apply_move_single_direction(self, player, opponent, move, direction):
        delta_x = None
        delta_y = None
        if direction == "north":
            delta_x = -1
            delta_y = 0
        elif direction == "south":
            delta_x = 1
            delta_y = 0
        elif direction == "west":
            delta_x = 0
            delta_y = -1
        elif direction == "east":
            delta_x = 0
            delta_y = 1
        elif direction == "north_west":
            delta_x = -1
            delta_y = -1
        elif direction == "north_east":
            delta_x = -1
            delta_y = 1
        elif direction == "south_west":
            delta_x = 1
            delta_y = -1
        elif direction == "south_east":
            delta_x = 1
            delta_y = 1
        x = move[0]
        y = move[1]
        pieces_to_be_flipped = []
        while not self.out_of_bounds(x, y):
            x += delta_x
            y += delta_y
            if self.state[x, y] == opponent:
                pieces_to_be_flipped.append([x, y])
            elif self.state[x, y] == player:
                if player == BLACK:
                    self.black_score += len(pieces_to_be_flipped)
                    self.white_score -= len(pieces_to_be_flipped)
                else:
                    self.white_score += len(pieces_to_be_flipped)
                    self.black_score -= len(pieces_to_be_flipped)
                for piece in pieces_to_be_flipped:
                    self.state[piece[0], piece[1]] = player
                break
            elif self.state[x, y] == EMPTY:
                break


def simple_evaluation_fn(player_type, moves):
    pass


def advanced_evaluation_fn(player_type, moves):
    pass
