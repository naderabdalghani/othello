class Agent:
    def __init__(self, identifier, agent_type, hints, depth, evaluation_fn, move_ordering):
        self.identifier = identifier
        self.agent_type = agent_type
        self.hints = hints
        self.depth = depth
        self.evaluation_fn = evaluation_fn
        self.move_ordering = move_ordering

    def get_move(self, possible_moves):
        pass
