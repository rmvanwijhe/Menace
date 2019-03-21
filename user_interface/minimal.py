import user_interface
import random
from collections import Counter


class Minimal(user_interface.UI):

    def __init__(self):
        self.score = []

    def render(self, board):
        pass

    def get_move(self, board):
        return random.sample(board.legal_moves(unique=False), 1)[0]

    def add_score(self, winner):
        self.score.append(winner)

        if len(self.score) % 100 == 0:
            print(Counter(self.score), Counter(self.score[-100:-1]))
