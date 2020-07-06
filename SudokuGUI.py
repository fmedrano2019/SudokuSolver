import pygame
import SudokuEngine
import time

# Size of the window
WINDOW_MULTIPLIER = 8  # this should be the only modification to affect the window size
WINDOW_SIZE = 90  # to ensure the window is always divisible by 9
WINDOW_WIDTH = WINDOW_SIZE * WINDOW_MULTIPLIER
WINDOW_HEIGHT = WINDOW_SIZE * WINDOW_MULTIPLIER
BOX_SIZE = int(WINDOW_WIDTH / 3)
CELL_SIZE = int(BOX_SIZE / 3)

# Grid parameters
rows = 9
cols = 9
cell_line_thickness = 1
box_line_thickness = 4

# Colors
WHITE = (255, 255, 255)
GREY = (125, 125, 125)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
ORANGE = (255, 125, 0)
GREEN = (0, 255, 0)

# Font
pygame.font.init()
FONT_SIZE = 55
FONT = pygame.font.Font('freesansbold.ttf', FONT_SIZE)

# Delay
STANDARD_DELAY = 10


class Grid:
    def __init__(self, window):
        self.board = [
            [0, 3, 0, 6, 0, 7, 0, 0, 4],
            [6, 7, 0, 5, 4, 0, 3, 8, 0],
            [8, 0, 5, 3, 0, 2, 6, 0, 0],
            [5, 0, 7, 4, 0, 3, 8, 0, 2],
            [3, 9, 0, 7, 2, 0, 0, 4, 0],
            [0, 8, 4, 0, 0, 1, 0, 6, 0],
            [7, 2, 0, 0, 3, 0, 9, 0, 0],
            [0, 5, 0, 8, 9, 6, 0, 1, 0],
            [9, 0, 1, 0, 0, 0, 4, 0, 8]
        ]
        self.cells = [[Cell(r, c, self.board[r][c]) for c in range(rows)] for r in range(cols)]
        self.window = window
        self.draw_grid()
        self.update_cells(True)

    def draw_grid(self):
        """
        Draws the grid lines on the board

        :return: None
        """

        # Cell lines
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):  # Vertical lines
            pygame.draw.line(self.window, GREY, (x, 0), (x, WINDOW_HEIGHT), cell_line_thickness)
        for y in range(0, WINDOW_HEIGHT, CELL_SIZE):  # Vertical lines
            pygame.draw.line(self.window, GREY, (0, y), (WINDOW_WIDTH, y), cell_line_thickness)

        # Box lines
        for x in range(0, WINDOW_WIDTH, BOX_SIZE):  # Vertical lines
            pygame.draw.line(self.window, BLACK, (x, 0), (x, WINDOW_HEIGHT), box_line_thickness)
        for y in range(0, WINDOW_HEIGHT, BOX_SIZE):  # Vertical lines
            pygame.draw.line(self.window, BLACK, (0, y), (WINDOW_WIDTH, y), box_line_thickness)

    def update_cells(self, first_ini=False):
        """
        Updates the cells on the board

        :return: None
        """

        if not first_ini:
            for r in range(rows):
                for c in range(cols):
                    self.cells[r][c].draw_value(BLACK, self.window)
        else:
            for r in range(rows):
                for c in range(cols):
                    self.cells[r][c].draw_value(GREY, self.window)

    def find_empty(self):
        """
        Finds an empty space on the board

        :return: the row and column of the empty space, None if there is no empty space
        """

        for r in range(rows):
            for c in range(cols):
                self.cells[r][c].draw_outline(ORANGE, self.window)
                if self.board[r][c] == 0:
                    return r, c
        return None

    def solve(self):
        """
        Solves the puzzle through recursive backtracking

        :return: True if the solution is valid, False if otherwise
        """

        space = self.find_empty()
        if space:
            row, col = space
        else:
            return True

        for i in range(1, 10):
            # Counting up effect
            self.cells[row][col].set_value(i)
            self.cells[row][col].draw_fill(self.window)
            self.cells[row][col].draw_value(GREY, self.window)
            pygame.display.update()
            pygame.time.delay(STANDARD_DELAY)
            if SudokuEngine.valid(row, col, i, self.board):
                self.board[row][col] = i
                self.cells[row][col].set_value(i)
                self.cells[row][col].draw_fill(self.window)
                self.cells[row][col].draw_value(GREY, self.window)
                self.cells[row][col].draw_outline(GREEN, self.window)
                pygame.display.update()
                pygame.time.delay(STANDARD_DELAY)

                if self.solve():
                    return True

                self.board[row][col] = 0
                self.cells[row][col].set_value(0)
                self.cells[row][col].draw_value(GREY, self.window)
                self.cells[row][col].draw_fill(self.window)
                self.cells[row][col].draw_outline(RED, self.window)
                pygame.display.update()
                pygame.time.delay(STANDARD_DELAY)
            else:
                self.cells[row][col].draw_fill(self.window)
                self.cells[row][col].draw_outline(RED, self.window)

        return False


class Cell:
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.value = val
        self.x = self.col * CELL_SIZE
        self.y = self.row * CELL_SIZE
        self.selected = False

    def draw_value(self, color, window):
        """
        Draws the cell on the board

        :param color: color of the text
        :param window: window to be drawn on
        :return: None
        """

        if self.value != 0:
            text = FONT.render(str(self.value), True, color)
            window.blit(text, (self.x + (CELL_SIZE / 2 - text.get_width() / 2),
                               self.y + (CELL_SIZE / 2 - text.get_height() / 2)))

    def draw_outline(self, color, window):
        """
        Draws an outline around the cell

        :param color: the color of the outline
        :param window: window to be drawn on
        :return: None
        """

        pygame.draw.rect(window, color, (self.x, self.y, CELL_SIZE, CELL_SIZE), box_line_thickness)

    def draw_fill(self, window):
        """
        Draws a filled rectangle to cover the previous Cell

        :param window: window to be drawn on
        :return: None
        """

        pygame.draw.rect(window, WHITE, (self.x,  self.y, CELL_SIZE, CELL_SIZE), 0)

    def set_value(self, value):
        """
        Sets the cell's value to the parameter value

        :param value: an integer; the new value
        :return: None
        """

        self.value = value


def main():
    pygame.init()

    # Formatting the window
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    window.fill(WHITE)
    pygame.display.set_caption("SudokuSolver")
    icon = pygame.image.load('icon.png')
    pygame.display.set_icon(icon)

    # Initializing the grid
    board = Grid(window)
    board.draw_grid()

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board.solve()

        # Reset the window
        window.fill(WHITE)
        board.draw_grid()
        board.update_cells()
        pygame.display.update()


if __name__ == '__main__':
    main()

pygame.quit()
