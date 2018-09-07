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

    def move_shape(self, direction="down"):
        original = self.active_shape.coordinates[:]
        self.delete_current_shape()
        if direction == "down": self.active_shape.down()
        elif direction == "right": self.active_shape.right()
        elif direction == "left": self.active_shape.left()
        elif direction == "rotate": self.active_shape.rotate()
        else:
            print("Please choose direction from: 'down', 'right', 'left', 'rotate'")
            raise ValueError
        if any(row < 0 or row >= self.rows or col < 0 or col >= self.cols or self.grid[row][col] != 0
               for row, col in self.active_shape.coordinates):
            self.active_shape.coordinates = original
            self.draw_shape()
            if direction == "down":
                self.active_shape = None
        else:
            self.draw_shape()


class TetrisShape(object):

    shapes = {"I": [(1, 0), (1, 1), (1, 2), (1, 3)], "O": [(0, 1), (0, 2), (1, 1), (1, 2)],
              "S": [(0, 1), (0, 2), (1, 0), (1, 1)], "L": [(0, 2), (1, 0), (1, 1), (1, 2)],
              "J": [(0, 0), (1, 0), (1, 1), (1, 2)], "T": [(0, 1), (1, 0), (1, 1), (1, 2)],
              "Z": [(0, 0), (0, 1), (1, 1), (1, 2)]}

    def __init__(self, type):
        self.type = type
        self.coordinates = self.shapes[self.type]
        self.represent = self.shapes[self.type]

    @property
    def representation(self):
        grid = [[0]*4 for _ in range(4)]
        for row, col in self.represent:
            grid[row][col] = self.type
        return grid

    @classmethod
    def random(cls):
        return TetrisShape(random.choice(list(cls.shapes)))

    def down(self):
        """ moves the current shape one row down"""
        # change the indexes by one row down
        self.coordinates = [(row + 1, col) for (row, col) in self.coordinates]

    def right(self):
        """ moves the current shape one col to the right"""
        # change the indexes by one col to the right and draw new position to the grid
        self.coordinates = [(row, col + 1) for (row, col) in self.coordinates]

    def left(self):
        """ moves the current shape one column to the left"""
        # change the indexes by one col to the right and draw new position to the grid
        self.coordinates = [(row, col - 1) for (row, col) in self.coordinates]

    def rotate(self):
        if self.type != "O":
            shift = 3 if self.type == "I" else 2
            moves_till_now = [(brick1[0] - brick2[0], brick1[1] - brick2[1])
                              for brick1, brick2 in zip(self.coordinates, self.represent)]
            self.represent = [(col, shift - row) for row, col in self.represent]
            self.coordinates = [(row + row_moves, col + col_moves)
                                for (row, col), (row_moves, col_moves) in zip(self.represent, moves_till_now)]

