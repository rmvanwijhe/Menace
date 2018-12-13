from board import Board
import player
import user_interface

# Choose the interface
ui = user_interface.Graphical()
# ui = user_interface.CommandLine()

# Choose the players for respectively the uneven and even moves
player1 = player.Menace("trained_menace.pickle", "trained_menace.pickle", True)
player2 = player1 # This does not call the constructor again! so same MENACE
# player2 = player.Human(ui) # The system needs know where the Human will be providing their input
# player2 = player.RandomMove() # Just make a random move


def play_game():
    # Initialize the gameloop variables
    board = Board()
    keep_going = True
    score = [0, 0, 0]

    # Game loop
    while keep_going:
        # Draw the board
        ui.tick()
        ui.render(board)

        if board.winner():
            # Previous game ended, reset board for new game
            # UI intervention could be build in here, i.e. keep_going?
            ui.add_score(board.winner())
            board = Board()

        if board.player() == 1:
            board = player1.move(board)
        else:
            board = player2.move(board)


play_game()
