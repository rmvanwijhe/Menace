import user_interface


class CommandLine(user_interface.UI):

    symbol = [" ", "X", "O"]

    def render(self, board=None):
        row_strings = []
        for row in range(3):
            values = [self.symbol[board.cell((row, col))] for col in range(3)]
            row_strings.append(" " + " | ".join(values) + " ")

        print("\n---|---|---\n".join(row_strings))
        print("")

    def get_move(self, board):
        not_valid = True
        while not_valid:
            try:
                move = input("where would you like to move?")
                if len(move) != 1:
                    raise ValueError
                return ord(move)
            except ValueError:
                print("please provide a single character")

    def add_score(self, winner):
        if winner in [1,2]:
            player = self.symbol[winner]
        else:
            player = "Nobody"

        print("%s has won the game!" % player)
