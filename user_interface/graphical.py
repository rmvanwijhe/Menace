import pygame, pygame.locals
import sys

import user_interface

red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)


class Graphical(user_interface.UI):

    def __init__(self, side=160, line=10):
        self.side_width = side
        self.line_width = line

        self.score = [0, 0, 0]
        self.score_100 = [0, 0, 0]

        screen_size = (3 * self.side_width + 2 * self.line_width, 4 * self.side_width + 2 * self.line_width)
        self.screen = pygame.display.set_mode(screen_size)
        self.clock = pygame.time.Clock()

        self.score = [0, 0, 0]
        pygame.font.init()
        # font = pygame.font.SysFont("freesansbold", 72)
        self.font = pygame.font.SysFont(None, 72)

    def index_to_coord(self, index):
        return index * (self.side_width + self.line_width)

    def index_to_rect(self, coordinate):
        return pygame.Rect(self.index_to_coord(coordinate[0]), self.index_to_coord(coordinate[1]), self.side_width, self.side_width)

    def draw_x(self, row, col):
        rect = self.index_to_rect((row, col))
        pygame.draw.line(self.screen, red, rect.topleft, rect.bottomright, self.line_width)
        pygame.draw.line(self.screen, red, rect.topright, rect.bottomleft, self.line_width)

    def draw_o(self, row, col):
        rect = self.index_to_rect((row, col))
        pygame.draw.ellipse(self.screen, green, rect, self.line_width)

    def draw_score(self, text, y_index):
        score_text = self.font.render(text, True, black)
        width, height = pygame.display.get_surface().get_size()
        text_rect = score_text.get_rect(center=(width / 2, height - y_index))
        self.screen.blit(score_text, text_rect)

    def draw_board(self):
        # Make the screen white.
        self.screen.fill(white)

        # Calculate where the lines should be
        width = self.screen.get_rect().width
        line1 = self.side_width + (self.line_width // 2)
        line2 = 2 * self.side_width + (3 * self.line_width // 2)

        # Draw lines in those locations
        pygame.draw.line(self.screen, black, (line1, 0), (line1, width), self.line_width)
        pygame.draw.line(self.screen, black, (line2, 0), (line2, width), self.line_width)
        pygame.draw.line(self.screen, black, (0, line1), (width, line1), self.line_width)
        pygame.draw.line(self.screen, black, (0, line2), (width, line2), self.line_width)

    def render(self, board):
        self.draw_board()

        # Go through the game board
        # TODO: since the board is stored in it's least str length state, the board might flip during play
        # That is annoying and making sure that doesn't happen can (should) be done (here?)
        if board is not None:
            for row in range(3):
                for col in range(3):
                    value = board.cell((col, row))
                    # Draw the appropriate figure
                    if value == 1:
                        self.draw_x(row, col)
                    if value == 2:
                        self.draw_o(row, col)

        self.draw_score("wins %d/%d" % (self.score[0], sum(self.score)), 110)
        self.draw_score("(draws %d, losses %d)" % (self.score[1], self.score[2]), 40)

        # Update the screen
        pygame.display.update()

    def tick(self, fps=60):
        self.clock.tick(fps)

        # If there are 'quit' events, end the game
        for _ in pygame.event.get(pygame.locals.QUIT):
            sys.exit(0)

    def get_move(self):
        for event in pygame.event.get():
            # print(event)
            if event.type == pygame.locals.QUIT:
                event.post(event)
            elif event.type == pygame.locals.KEYUP:
                return event.key
        return None

    def add_score(self, winner):
        self.score[winner - 1] += 1