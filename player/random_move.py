import random
import player


class RandomMove(player.Player):

    def move(self, board):
        return random.sample(board.unique_legal_moves(), 1)[0]
