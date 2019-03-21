import random
import player


class RandomMove(player.Player):

    def move(self, board):
        return random.sample(board.legal_moves(unique=False), 1)[0]
