import random


class TetrisGame(object):

    def __init__(self, rows, cols):
        self.grid = [[0] * cols for _ in range(rows)]
        self.rows = rows
        self.cols = cols
        self.active_shape = None
        self.score = 0

    def add_shape(self, tetris_shape):
        """Picks a random shape from dictionary of shapes below, ads the indexes, type of shape to this instance and
            draws the shape to the top center of grid"""
        self.active_shape = tetris_shape
        center = self.cols // 2 - 2  # find the position of leftmost brick so the whole shape is centered
        self.active_shape.coordinates = [(row, col + center) for (row, col) in self.active_shape.coordinates]
        self.draw_shape()

    def draw_shape(self):
        for row, col in self.active_shape.coordinates:
            self.grid[row][col] = self.active_shape.type

    def move_down(self):
        """ moves the current shape one row down"""
        self.delete_current_shape()  # delete the current shape position so it doesnt get in way of collision check
        if any(row + 1 >= self.rows or self.grid[row + 1][col] != 0 for row, col in self.active_shape.coordinates):
            self.draw_shape()  # if any brick collides redraw the original position of shape to the grid
            self.active_shape = None
        else:
            # if no collision, change the indexes by one row down
            self.active_shape.coordinates = [(row + 1, col) for (row, col) in self.active_shape.coordinates]
            self.draw_shape()

    def move_right(self):
        """ moves the current shape one col to the right"""
        self.delete_current_shape()  # delete the current shape position so it doesnt get in way of collision check
        if any(col + 1 >= self.cols or self.grid[row][col + 1] != 0 for row, col in self.active_shape.coordinates):
            self.draw_shape()  # if any brick collides redraw the original position of shape to the grid
        else:
            # if no collision - change the indexes by one col to the right and draw new position to the grid
            self.active_shape.coordinates = [(row, col + 1) for (row, col) in self.active_shape.coordinates]
            self.draw_shape()

    def move_left(self):
        """ moves the current shape one column to the left"""
        self.delete_current_shape()  # delete the current shape position so it doesnt get in way of collision check
        if any(col - 1 < 0 or self.grid[row][col - 1] != 0 for row, col in self.active_shape.coordinates):
            self.draw_shape()  # if any brick collides redraw the original position of shape to the grid
        else:
            # if no collision - change the indexes by one col to the right and draw new position to the grid
            self.active_shape.coordinates = [(row, col - 1) for (row, col) in self.active_shape.coordinates]
            self.draw_shape()

    def rotate(self):
        self.delete_current_shape()
        self.active_shape.coordinates = [(col, row) for (row, col) in self.active_shape.coordinates]
        self.draw_shape()

    def delete_current_shape(self):
        for row, col in self.active_shape.coordinates:
            self.grid[row][col] = 0

    def check_complete_rows(self):
        score_multiplier = [0, 40, 100, 300, 1200]
        number_of_rows = 0
        for row in self.grid:
            if 0 not in row:  # checks if row is filled completely
                number_of_rows += 1
                self.grid.remove(row)  # removes the filled row from grid
                self.grid.insert(0, [0] * self.cols)  # add a new empty row to the top of grid
        self.score += score_multiplier[number_of_rows]


class TetrisShape(object):

    shapes = {"I": [(1, 0), (1, 1), (1, 2), (1, 3)], "O": [(0, 1), (0, 2), (1, 1), (1, 2)],
              "S": [(0, 1), (0, 2), (1, 0), (1, 1)], "L": [(0, 2), (1, 0), (1, 1), (1, 2)],
              "J": [(0, 0), (1, 0), (1, 1), (1, 2)], "T": [(0, 1), (1, 0), (1, 1), (1, 2)],
              "Z": [(0, 0), (0, 1), (1, 1), (1, 2)]}

    def __init__(self, type):
        self.type = type
        self.coordinates = self.shapes[self.type]

    @property
    def representation(self):
        grid = [[0]*4 for _ in range(4)]
        for row, col in self.coordinates:
            grid[row][col] = self.type
        return grid

    @classmethod
    def random(cls):
        return TetrisShape(random.choice(list(cls.shapes)))

