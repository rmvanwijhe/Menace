from board import Board
import player
import user_interface

# Choose the interface
ui = user_interface.Graphical()
# ui = user_interface.CommandLine()
# ui = user_interface.Minimal()

# Choose the players for respectively the uneven and even moves
# player1 = player.Menace("trained_menace.pickle", "trained_menace.pickle")
player1 = player.Menace()
# player2 = player1 # This does not call the constructor again! so same MENACE
# player2 = player.Human(ui) # The system needs know where the Human will be providing their input
player2 = player.RandomMove() # Just make a random move


def play_game():
    # Initialize the gameloop variables
    board = Board()
    keep_going = True

    # Game loop
    while keep_going:
        # Draw the board
        ui.tick()
        ui.render(board)

        if board.winner():
            # Previous game ended, reset board for new game

            # Update ui
            ui.add_score(board.winner())

            # Notify the players and show the final (winning) board
            player1.game_finished(board)
            player2.game_finished(board)

            # Reset board
            board = Board()

        if board.player() == 1:
            move = player1.move(board)
        else:
            move = player2.move(board)

        board = board.make_move(move)

play_game()
