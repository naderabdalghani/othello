import numpy as np

WHITE = 1
BLACK = 2
NEXT_MOVE = 3


class Othello:
    def __init__(self, n=8):
        self.n = n
        self.state = self.init_state()

    def init_state(self):
        state = np.zeros((self.n, self.n))
        state[self.n//2, self.n//2] = WHITE
        state[self.n//2-1, self.n//2-1] = WHITE
        state[self.n // 2 - 1, self.n // 2] = BLACK
        state[self.n // 2, self.n // 2 - 1] = BLACK
        return state
