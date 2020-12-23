import numpy as np
from constants import EMPTY, WHITE, BLACK, VALID_MOVE, DIRECTIONS, BLACK_WON, WHITE_WON, DRAW, GAME_IN_PROGRESS


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
        self.no_moves_semaphore = 0

    def move_generator(self, player):
        moves = []
        self.state[self.state == VALID_MOVE] = EMPTY
        pieces_indices = np.argwhere(self.state == player)
        opponent = WHITE if player == BLACK else BLACK
        for index in pieces_indices:
            for direction in DIRECTIONS:
                self.single_piece_move_generator(player, opponent, index, direction, moves)
        if len(moves) == 0:
            self.no_moves_semaphore += 1
        else:
            self.no_moves_semaphore = 0
        return moves

    def single_piece_move_generator(self, player, opponent, start, direction, moves):
        delta_x = 0
        delta_y = 0
        if direction in ("north", "north_west", "north_east"):
            delta_x = -1
        elif direction in ("south", "south_west", "south_east"):
            delta_x = 1
        if direction in ("west", "north_west", "south_west"):
            delta_y = -1
        elif direction in ("east", "north_east", "south_east"):
            delta_y = 1
        x = start[0] + delta_x
        y = start[1] + delta_y
        last_seen_opponent_piece = None
        while not self.out_of_bounds(x, y):
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
            elif self.state[x, y] == VALID_MOVE:
                break
            x += delta_x
            y += delta_y

    def out_of_bounds(self, x, y):
        return x < 0 or y < 0 or x >= self.n or y >= self.n

    def apply_move(self, player, move):
        self.state[self.state == VALID_MOVE] = EMPTY
        self.state[move[0], move[1]] = player
        if player == BLACK:
            self.black_score += 1
        else:
            self.white_score += 1
        opponent = WHITE if player == BLACK else BLACK
        for direction in DIRECTIONS:
            self.apply_move_single_direction(player, opponent, move, direction)

    def apply_move_single_direction(self, player, opponent, move, direction):
        delta_x = 0
        delta_y = 0
        if direction in ("north", "north_west", "north_east"):
            delta_x = -1
        elif direction in ("south", "south_west", "south_east"):
            delta_x = 1
        if direction in ("west", "north_west", "south_west"):
            delta_y = -1
        elif direction in ("east", "north_east", "south_east"):
            delta_y = 1
        x = move[0] + delta_x
        y = move[1] + delta_y
        pieces_to_be_flipped = []
        while not self.out_of_bounds(x, y):
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
            x += delta_x
            y += delta_y

    def status(self):
        if self.black_score == 0:
            self.white_score = self.n * self.n
            return WHITE_WON
        elif self.white_score == 0:
            self.black_score = self.n * self.n
            return BLACK_WON
        if self.black_score + self.white_score == self.n * self.n or self.no_moves_semaphore >= 2:
            if self.black_score > self.white_score:
                self.black_score = self.n * self.n - self.white_score
                return BLACK_WON
            if self.white_score > self.black_score:
                self.white_score = self.n * self.n - self.black_score
                return WHITE_WON
            if self.black_score == self.white_score:
                return DRAW
        return GAME_IN_PROGRESS


def simple_evaluation_fn(player_type, moves):
    pass


def advanced_evaluation_fn(player_type, moves):
    pass
