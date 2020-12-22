class Agent:
    def __init__(self, agent_type, hints, depth, evaluation_fn, move_ordering):
        self.agent_type = agent_type
        self.hints = hints
        self.depth = depth
        self.evaluation_fn = evaluation_fn
        self.move_ordering = move_ordering
        self.score = 2

    def get_move(self, possible_moves):
        pass
