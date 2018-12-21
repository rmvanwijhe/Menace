import random
import player
import pickle
from board import Board


class Menace(player.Player):

    # Build the pile of matchboxes
    @staticmethod
    def initialize_matchboxes(debug=False):
        # Round 0 is trivial, it is the starting (empty) board
        matchboxes = [[Matchbox(Board())]]
        # Subsequent rounds can be found by getting all possible states that could result from the previous round
        # Note that generating the 'even' boxes is necessary in this process
        # (though they could theoretically be discarded)
        for game_round in range(9):
            # Set ensures each board can appear at most once
            round_boards = set()
            for matchbox in matchboxes[game_round]:

                for move in matchbox.options.keys():
                    round_boards.add(matchbox.board.make_move(move))

            # Use list comprehension to generate a list of matchboxes for this game_round
            # and append this list to the pile of matchboxes
            matchboxes.append([Matchbox(board) for board in round_boards])
            if debug:
                print("Round %d has %d matchboxes" % (game_round + 1, len(matchboxes[game_round + 1])))
        return matchboxes

    def __init__(self, input_file=None, output_file=None, debug=False):
        self.debug = debug
        self.matchboxes = None
        if input_file:
            with open(input_file, "rb") as file:
                self.matchboxes = pickle.load(file)
        if self.matchboxes is None:
            self.matchboxes = self.initialize_matchboxes(debug=debug)
        self.game_history = []
        self.output_file = output_file
        if self.output_file:
            with open(self.output_file, "wb+") as file:
                pickle.dump(self.matchboxes, file)

    # Have the system learn from the current game_history
    def learn(self, winner, debug=False):
        debug = debug or self.debug

        # Learning means manipulating the beads in the matchboxes, so have each relevant matchbox do that to itself
        for matchbox, move_coordinate in self.game_history:
            matchbox.reinforce(play=move_coordinate, winner=winner, debug=debug)

        if self.output_file:
            with open(self.output_file, "wb+") as file:
                pickle.dump(self.matchboxes, file)

    # Return a new board representing the move we made
    def move(self, board):
        # Find the matchbox for the current state, have that matchbox decide on the next move (based on its beads)
        for matchbox in self.matchboxes[board.turn()]:
            if matchbox.board == board:
                move_coordinate = matchbox.move(debug=self.debug)
                self.game_history.append((matchbox, move_coordinate))
                return board.translate(matchbox.board, move_coordinate)
        else:
            print(board)
            # self.show_state(board.move())
            raise AssertionError("No matchbox matches this board")

    def game_finished(self, winning_board):
        self.learn(winning_board.winner())
        self.game_history = []

    # Have MENACE play a single game against itself, returns the winner
    def game(self, debug=False):
        board = Board()
        while not board.winner():
            board = self.move(board)
            if debug:
                print(board)
        return board.winner()

    # Have MENACE play multiple games against itself
    def train(self, iterations=100):
        outcomes = [0, 0, 0]
        for i in range(iterations):
            outcome = self.game()
            outcomes[outcome % 3] += 1
        print(outcomes)

    # Print the state of each matchbox in a certain round to get an idea of the state of the learning
    def show_state(self, round=0):
        for matchbox in self.matchboxes[round]:
            print(matchbox)

# Helper class for MENACE
class Matchbox(object):

    def __eq__(self, other):
        return self.board == other.board

    def __hash__(self):
        return hash(self.board)

    # TODO: Is this the most useful, maybe giving coords for the move to be made together with the weights?
    def __str__(self):
        weights = list(self.options.values())
        weights.sort()
        return str(self.board) + ' '.join([str(weight) for weight in weights])

    # When creating a new matchbox we create a dictionary of all possible moves (asking the board for that list)
    # For each move we add initial_value beads to the box (what that value should be can be experimented with)
    def __init__(self, board, initial_value=7):
        board.make_minimal()
        self.board = board
        self.options = {}
        for move in board.legal_moves(unique=True):
            self.options[move] = initial_value
        # TODO: check whether one of the options is a 'win', if so, all non winning options can be removed
        # This should reduce search space and increase training speed (i.e. in round 5 a winning option could exist,
        # but 4 non winning options need to be eliminated by trial and error now)

    # We select a number between zero and the total number of beads
    # We then look at the number of beads for each option and subtract that number from the random number
    # Once the random number is 'depleted' we found our option
    # So random number 0 gives us the first option, and random number = total beads gives us the last
    def move(self, debug=False):
        if debug:
            print(self.options)
            print(self.board)
        total_beads = sum(self.options.values())
        random_move = random.randint(0, total_beads)
        for move_candidate in self.options:
            random_move -= self.options[move_candidate]
            if random_move <= 0:
                return move_candidate
        else:
            print("No valid move found... %d / %d, %d" % (random_move, total_beads, len(self.options.keys())))

    # Add or subtract beads according to winning or losing
    def reinforce(self, play, winner, debug=False):
        if play not in self.options.keys():
            if debug:
                print("error, play not found")
            return
        if winner == 3:
            # Draw
            if debug:
                print("Not the worst option...")
            self.options[play] += 0
        elif (self.board.turn() % 2) + 1 == winner:
            # This move was part of a winning strategy
            if debug:
                print("Do this!")
            self.options[play] += 3
        else:
            # This move was part of a losing strategy
            if self.options[play] > 1:
                if debug:
                    print("Do this less")
                self.options[play] -= 1
            else:
                # This options would drop to zero, so remove it, but prevent the matchbox from "giving up"
                # TODO: maybe 'giving up' would be a nice feature, but it would probably require a flag in Board...
                if len(self.options.keys()) > 1:
                    self.options.pop(play)
                    if debug:
                        print("Don't do this")
                else:
                    # this option isn't a winner, but its the only option...
                    self.options[play] += 100
                    if debug:
                        print("Don't do this, but keep MENACE from dying...")
