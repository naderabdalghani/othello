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
        self.log_file = open("player_{}_moves.txt".format(self.identifier), "w")
        self.log_file.close()

    def get_move(self, game, player):
        opponent = WHITE if player == BLACK else BLACK
        move = self.alpha_beta_pruning(game, self.depth, player, opponent)
        if move.x != -1 and move.y != -1:
            return [move.x, move.y]
        return None

    def alpha_beta_pruning(self, game, depth, player, opponent, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or game.status() != GAME_IN_PROGRESS:
            if self.evaluation_fn == "simple":
                game.simple_evaluation_fn()
            else:
                game.advanced_evaluation_fn()
            return game.last_move
        if player == MAXIMIZING_PLAYER:
            max_evaluation = Move(value=float('-inf'))
            possible_moves = game.move_generator(player)
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
                possible_moves.sort(reverse=True)
            for move in possible_moves:
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
            possible_moves = game.move_generator(player)
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
                possible_moves.sort()
            for move in possible_moves:
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
