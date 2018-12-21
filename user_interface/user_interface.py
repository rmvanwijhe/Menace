class UI(object):

    def render(self, board):
        raise NotImplementedError

    def get_move(self, board):
        raise NotImplementedError

    def tick(self):
        pass

    def add_score(self, winner):
        pass
