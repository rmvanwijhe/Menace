class Player(object):

    def move(self, board):
        raise NotImplementedError

    def game_finished(self, winning_board):
        pass