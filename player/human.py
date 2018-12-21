import player
from board import Board, _state_set_cell


class Human(player.Player):
    keys = {113: (0, 0), 119: (0, 1), 101: (0, 2),
            97: (1, 0), 115: (1, 1), 100: (1, 2),
            122: (2, 0), 120: (2, 1), 99: (2, 2)}

    # The human player object needs to be able to talk to the computer user through a UI
    def __init__(self, ui):
        self.ui = ui

    # Asking the human player for input means waiting until the user (finally) gives 'valid' feedback
    def move(self, board):
        while True:
            self.ui.tick()
            move = self.ui.get_move(board)
            if move in self.keys:
                coordinate = self.keys[move]
                return coordinate
