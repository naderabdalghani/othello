import time
from copy import deepcopy
from move import Move
from constants import MAXIMIZING_PLAYER, GAME_IN_PROGRESS, WHITE, BLACK, LOG_FILE


class Agent:
    def __init__(self, identifier, agent_type, hints, depth, evaluation_fn, move_ordering):
        self.identifier = identifier
        self.agent_type = agent_type
        self.hints = hints
        self.depth = depth
        self.evaluation_fn = evaluation_fn
        self.move_ordering = move_ordering
        self.turns = 0
        self.branches_evaluated = 0
        self.nodes_per_level = [0]*(self.depth + 1)
        self.total_branching_factor = 0
        self.total_effective_branching_factor = 0
        self.total_execution_time = 0

    def calculate_effective_branching_factor(self):
        effective_branching_factors = []
        for i in range(len(self.nodes_per_level) - 1, 0, -1):
            if self.nodes_per_level[i - 1] == 0:
                return 0
            effective_branching_factors.append(self.nodes_per_level[i] / self.nodes_per_level[i - 1])
        return sum(effective_branching_factors) / len(effective_branching_factors)

    def log_data(self, player, move, time_consumed):
        player_name = "BLACK" if player == BLACK else "WHITE"
        self.turns += 1
        branching_factor = 0
        non_leaf_nodes = sum(self.nodes_per_level[:self.depth])
        if non_leaf_nodes != 0:
            branching_factor = self.branches_evaluated / non_leaf_nodes
        effective_branching_factor = self.calculate_effective_branching_factor()
        self.total_branching_factor += branching_factor
        self.total_effective_branching_factor += effective_branching_factor
        self.total_execution_time += time_consumed
        if move is not None:
            with open(LOG_FILE, "a") as f:
                f.write("{}: ({}, {}). Branching factor = {}. Effective Branching factor = {}, Execution time = {}\n"
                        .format(player_name, move.x, move.y, branching_factor, effective_branching_factor,
                                time_consumed))
        else:
            with open(LOG_FILE, "a") as f:
                f.write("{}: Turn skipped. Branching factor = {}. Effective Branching factor = {}, Execution time = {}"
                        "\n".format(player_name, branching_factor, effective_branching_factor, time_consumed))
        self.branches_evaluated = 0
        self.nodes_per_level = [0]*(self.depth + 1)

    def get_move(self, game, player):
        opponent = WHITE if player == BLACK else BLACK
        start_time = time.time()
        move = self.alpha_beta_pruning(game, self.depth, player, opponent)
        time_consumed = time.time() - start_time
        if move.x != -1 and move.y != -1:
            self.log_data(player, move, time_consumed)
            return [move.x, move.y]
        self.log_data(player, None, time_consumed)
        return None

    def alpha_beta_pruning(self, game, depth, player, opponent, alpha=float('-inf'), beta=float('inf')):
        self.nodes_per_level[-(depth + 1)] += 1
        possible_moves = game.move_generator(player)
        if len(possible_moves) == 0 and depth == self.depth:
            return Move()
        if depth == 0 or game.status() != GAME_IN_PROGRESS or len(possible_moves) == 0:
            if self.evaluation_fn == "simple":
                game.simple_evaluation_fn()
            else:
                game.advanced_evaluation_fn()
            return game.last_move
        if player == MAXIMIZING_PLAYER:
            max_evaluation = Move(value=float('-inf'))
            if self.move_ordering:
                for move in possible_moves:
                    temp_game = deepcopy(game)
                    temp_game.apply_move(player, [move.x, move.y])
                    if self.evaluation_fn == "simple":
                        temp_game.simple_evaluation_fn()
                    else:
                        temp_game.advanced_evaluation_fn()
                    move.value = temp_game.last_move.value
                    del temp_game
                possible_moves = sorted(possible_moves, key=lambda x: x.value, reverse=True)
            for move in possible_moves:
                self.branches_evaluated += 1
                new_game = deepcopy(game)
                new_game.apply_move(player, [move.x, move.y])
                move_evaluation = self.alpha_beta_pruning(new_game, depth - 1, opponent, player, alpha, beta)
                del new_game
                if max_evaluation.value < move_evaluation.value:
                    max_evaluation.value = move_evaluation.value
                    max_evaluation.x = move.x
                    max_evaluation.y = move.y
                alpha = max(alpha, move_evaluation.value)
                if beta <= alpha:
                    break
            return max_evaluation
        else:
            min_evaluation = Move(value=float('inf'))
            if self.move_ordering:
                for move in possible_moves:
                    temp_game = deepcopy(game)
                    temp_game.apply_move(player, [move.x, move.y])
                    if self.evaluation_fn == "simple":
                        temp_game.simple_evaluation_fn()
                    else:
                        temp_game.advanced_evaluation_fn()
                    move.value = temp_game.last_move.value
                    del temp_game
                possible_moves = sorted(possible_moves, key=lambda x: x.value)
            for move in possible_moves:
                self.branches_evaluated += 1
                new_game = deepcopy(game)
                new_game.apply_move(player, [move.x, move.y])
                move_evaluation = self.alpha_beta_pruning(new_game, depth - 1, opponent, player, alpha, beta)
                del new_game
                if min_evaluation.value > move_evaluation.value:
                    min_evaluation.value = move_evaluation.value
                    min_evaluation.x = move.x
                    min_evaluation.y = move.y
                beta = min(beta, move_evaluation.value)
                if beta <= alpha:
                    break
            return min_evaluation
