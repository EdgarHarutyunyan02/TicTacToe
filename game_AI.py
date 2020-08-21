import pygame
import math
from time import sleep, time
import random
import copy

pygame.init()


class TicTacToeAI():
    def __init__(self, competitor):
        self.competitor = competitor
        self.board = competitor.board

    def make_decision(self):
        original_board = self.competitor.board
        # print("ORIGINAL BOARD", original_board)
        board_copy = copy.deepcopy(original_board)
        # print("BOARD COPY", board_copy)

        # Make a winning move
        for i, row in enumerate(original_board):
            for j, item in enumerate(row):
                board_copy = copy.deepcopy(original_board)
                if item == '':
                    board_copy[i][j] = 'o'
                    logic = Logic(board_copy)
                    result = logic.check(draw=False)
                    if result:
                        if result['winner_name'] == 'o':
                            return i, j

        # If competitor wins, block him
        for i, row in enumerate(original_board):
            for j, item in enumerate(row):
                board_copy = copy.deepcopy(original_board)
                if item == '':
                    board_copy[i][j] = 'x'
                    logic = Logic(board_copy)
                    result = logic.check(draw=False)
                    if result:
                        if result['winner_name'] == 'x':
                            return i, j

        # move corners, choosing random corner
        corners = [(0, 0), (0, 2), (2, 2), (2, 0)]
        free_corners = list(
            filter(lambda item: original_board[item[0]][item[1]] == '', corners))
        if free_corners:
            return random.choice(free_corners)

        if board_copy[1][1] == '':
            return (1, 1)

        sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
        free_sides = list(
            filter(lambda item: original_board[item[0]][item[1]] == '', corners))
        if free_sides:
            return random.choice(free_sides)

    def move(self):

        index = self.make_decision()
        # print(index)
        if index:
            self.competitor.board[index[0]][index[1]] = 'o'


class Logic:
    def __init__(self, board):
        self.board = board

    def check(self, draw=True):
        # Checking rows
        for i, row in enumerate(self.board):
            item_for_check = row[0]
            row_is_correct = True
            for item in row:
                if item == '' or item != item_for_check:
                    row_is_correct = False
            if row_is_correct == True:
                if draw:
                    start_pos = (
                        self.position[0], self.position[1] + self.box_size*(i + 0.5))
                    end_pos = (
                        self.position[0] + self.size[0], self.position[1] + self.box_size*(i + 0.5))
                    line_color = self.x_color if item_for_check == 'x' else self.o_color
                    pygame.draw.line(self.surface, line_color,
                                     start_pos, end_pos, self.line_width)
                return {
                    "winner_name": item_for_check,
                    "draw": False
                }

        # Checking colunns
        for j in range(len(self.board[0])):
            item_for_check = self.board[0][j]
            column_is_correct = True
            for i in range(len(self.board)):
                if self.board[i][j] == '' or self.board[i][j] != item_for_check:
                    column_is_correct = False
            if column_is_correct:
                if draw:
                    start_pos = (
                        self.position[0]+self.box_size*(j + 0.5), self.position[1])
                    end_pos = (
                        self.position[0]+self.box_size*(j + 0.5), self.position[1]+self.size[1])
                    line_color = self.x_color if item_for_check == 'x' else self.o_color
                    pygame.draw.line(self.surface, line_color,
                                     start_pos, end_pos, self.line_width)
                return {
                    "winner_name": item_for_check,
                    "draw": False
                }

        diagonal_is_correct = True
        item_for_check = self.board[0][0]
        for i in range(len(self.board)):
            if self.board[i][i] == '' or item_for_check != self.board[i][i]:
                diagonal_is_correct = False
        if diagonal_is_correct:
            if draw:
                start_pos = (
                    self.position[0], self.position[1])
                end_pos = (
                    self.position[0]+self.size[0], self.position[1]+self.size[1])
                line_color = self.x_color if item_for_check == 'x' else self.o_color
                pygame.draw.line(self.surface, line_color,
                                 start_pos, end_pos, self.line_width)
            return {
                "winner_name": item_for_check,
                "draw": False
            }

        diagonal_is_correct = True
        item_for_check = self.board[0][len(self.board[0])-1]
        for i in range(len(self.board)):
            if self.board[i][len(self.board[0])-i-1] == '' or item_for_check != self.board[i][len(self.board[0])-i-1]:
                diagonal_is_correct = False
        if diagonal_is_correct:
            if draw:
                start_pos = (
                    self.position[0]+self.size[0], self.position[1])
                end_pos = (
                    self.position[0], self.position[1]+self.size[1])
                line_color = self.x_color if item_for_check == 'x' else self.o_color
                pygame.draw.line(self.surface, line_color,
                                 start_pos, end_pos, self.line_width)
            return {
                "winner_name": item_for_check,
                "draw": False
            }

        if self.is_full():
            return {
                "winner_name": None,
                "draw": True
            }

        return None

    def is_full(self):
        for row in self.board:
            for item in row:
                if item == '':
                    return False
        return True


class Board(Logic):
    def __init__(self, position, size, bg_color, window):
        self.board = [['' for j in range(3)] for i in range(3)]
        self.surface = window
        self.position = position
        self.size = size
        self.box_size = self.size[0] / 3
        self.bg_color = bg_color
        self.border_color = pygame.Color(13, 161, 146)
        self.x_color = (66, 66, 66)
        self.o_color = (224, 224, 224)
        self.border_width = 12
        self.line_width = 24
        self.turn = 'x'

    def get_winner(self):
        return self.check(draw=True)

    def get_index(self, mouse_position):
        position = (mouse_position[0]-self.position[0],
                    mouse_position[1]-self.position[1])
        for i in range(3):
            for j in range(3):
                if abs(self.box_size * (2 * j + 1) / 2-position[0]) <= (self.box_size - self.border_width) / 2 and abs(self.box_size * (2 * i + 1) / 2-position[1]) <= (self.box_size - self.border_width) / 2:
                    return i, j
        return None

    def insert(self, position):
        # print("Insert")
        indexes = self.get_index(position)
        if indexes:
            i, j = indexes
            if not self.board[i][j]:
                self.board[i][j] = self.turn
                if not self.get_winner():
                    computer.move()
                    self.get_winner()

    def draw_item(self, item, position):
        length = self.box_size*0.6
        if item == 'x':
            start_pos = (position[0]-length/2, position[1]-length/2)
            pygame.draw.line(self.surface, self.x_color, (start_pos[0], start_pos[1]), (
                start_pos[0] + length, start_pos[1] + length), self.line_width)
            pygame.draw.line(self.surface, self.x_color, (start_pos[0], start_pos[1]+length), (
                start_pos[0] + length, start_pos[1]), self.line_width)
        elif item == 'o':
            pygame.draw.circle(self.surface, self.o_color,
                               position, int(length/2), int(self.line_width*0.6))

    def draw_grid(self):
        # pygame.draw.rect(self.surface, (255, 255, 100), (
            # self.position[0], self.position[1], self.size[0], self.size[1]))

        # Drawing edges
        pygame.draw.line(self.surface, self.bg_color, (self.position[0], self.position[1]), (
            self.position[0]+self.size[0], self.position[1]), self.border_width)
        pygame.draw.line(self.surface, self.bg_color, (
            self.position[0]+self.size[0], self.position[1]), (
            self.position[0]+self.size[0], self.position[1]+self.size[1]), self.border_width)
        pygame.draw.line(self.surface, self.bg_color, (
            self.position[0]+self.size[0], self.position[1]+self.size[1]), (
            self.position[0], self.position[1]+self.size[1]), self.border_width)
        pygame.draw.line(self.surface, self.bg_color, (
            self.position[0], self.position[1]+self.size[1]), (
            self.position[0], self.position[1]), self.border_width)

        # Drawing colums
        pygame.draw.line(self.surface, self.border_color, (self.position[0]+self.size[0]/3, self.position[1]), (
            self.position[0]+self.size[0]/3, self.position[1]+self.size[1]), self.border_width)
        pygame.draw.line(self.surface, self.border_color, (self.position[0]+2*self.size[0]/3, self.position[1]), (
            self.position[0] + 2*self.size[0] / 3, self.position[1] + self.size[1]), self.border_width)

        # Drawing rows
        pygame.draw.line(self.surface, self.border_color, (self.position[0], self.position[1]+self.size[1]/3), (
            self.position[0] + self.size[0], self.position[1] + self.size[1] / 3), self.border_width)
        pygame.draw.line(self.surface, self.border_color, (self.position[0], self.position[1]+2*self.size[1]/3), (
            self.position[0]+self.size[0], self.position[1]+2*self.size[1]/3), self.border_width)

    def draw(self):
        self.draw_grid()
        for i, row in enumerate(self.board):
            for j, item in enumerate(row):
                if item:
                    self.draw_item(item, (int(
                        self.position[0] + self.box_size*(2*j + 1) / 2), int(self.position[1] + self.box_size*(2*i + 1) / 2)))


screen_size = width, height = 1024, 768
board_size = board_width, board_height = (600, 600)
bg_color = (20, 189, 172)
board_position = (width-board_width)//2, (height-board_height)//2

display_surface = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Tic Tac Toe')

board = Board(board_position, board_size, bg_color, display_surface)
computer = TicTacToeAI(board)
pygame.font.init()

winner_name_font = pygame.font.SysFont("Arial", int(screen_size[1]/3))
text_font = pygame.font.SysFont("Arial", 72)

start_time = None

while True:
    display_surface.fill(bg_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONUP:
            board.insert(event.pos)

    board.draw()
    winner = board.get_winner()

    if winner:
        if winner['winner_name']:
            winner_name = winner_name_font.render(
                winner['winner_name'].upper(), False, (66, 66, 66))
            text = text_font.render("WON", False, (66, 66, 66))
        elif winner['draw']:
            winner_name = winner_name_font.render('X O', False, (66, 66, 66))
            text = text_font.render("DRAW", False, (66, 66, 66))

        if not start_time:
            start_time = time()
        if time() - start_time > 1:
            display_surface.fill(bg_color)

            display_surface.blit(
                winner_name, ((screen_size[0]-winner_name.get_width())//2, (screen_size[1]-winner_name.get_height()-text.get_height())//2))
            display_surface.blit(
                text, ((screen_size[0] - text.get_width()) // 2, (screen_size[1] - winner_name.get_height() - text.get_height()) // 2 + winner_name.get_height()))
            sleep(1)
            winner = None

    pygame.display.update()
