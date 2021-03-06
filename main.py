import pygame

from time import sleep

from tetrisgrid import TetrisGame, TetrisShape

pygame.init()

"""Settings"""
# window resolution
resolution = display_width, display_height = 800, 600
# colors
black = (0, 0, 0)
white = (255, 255, 255)
shapes_colors = {"I": (0, 255, 255), "J": (0, 0, 255), "L": (255, 140, 0),
                 "O": (255, 255, 0), "S": (0, 255, 0), "T": (128, 0, 128), "Z": (255, 0, 0)}
# brick size
brick_width = 20
brick_height = 20
brick_margin = 1
# grid size in bricks
grid_columns = 10
grid_rows = 22
grid_width = (brick_width + brick_margin) * grid_columns
grid_height = (brick_height + brick_margin) * grid_rows
# speed of brick falling (60 = 1 sec, 120 = 2 sec, 30 = 0.5 sec ...)
speed = 48

"""Game features to display"""


def draw_grid():
    for row in range(grid_rows):
        for column in range(grid_columns):
            color = shapes_colors.get(tetris.grid[row][column], white)
            pygame.draw.rect(game_display, color, ((brick_width + brick_margin) * column + display_width/2 - 250,
                                                   (brick_height + brick_margin) * row + display_height-grid_height-10,
                                                   brick_width,
                                                   brick_height))


def draw_next_shape():
    for row in range(4):
        for column in range(4):
            color = shapes_colors.get(shape.representation[row][column], white)
            pygame.draw.rect(game_display, color, ((brick_width + brick_margin) * (column + grid_columns) + display_width/2 - 200,
                                                   (brick_height + brick_margin) * row + display_height - grid_height-10,
                                                   brick_width,
                                                   brick_height))


def draw_score():
    font = pygame.font.SysFont("monospace", 20)
    text = font.render("Score: {}".format(tetris.score), 1, white)
    game_display.blit(text, ((brick_width + brick_margin) * grid_columns + display_width/2 - 200, display_height-grid_height+100))


def draw_level():
    font = pygame.font.SysFont("monospace", 20)
    text = font.render("Level: {}".format(tetris.level), 1, white)
    game_display.blit(text, ((brick_width + brick_margin) * grid_columns + display_width/2 - 200, display_height-grid_height+130))


def draw_over():
    font = pygame.font.SysFont("monospace", 100)
    text = font.render("GAME OVER", 1, white)
    game_display.blit(text, (display_width/2 - 275, display_height/2 - 50))


def draw_title():
    title = [["I", "I", 'I', 0, "S", 0, 0, 0, 'S', 0, 'J', 'J', 'J', 'J', 'J', 0, 'L', 'L', 'L', 0, 'Z', 0, 'O', 'O', 'O'],
             ["I", 0,   "I", 0, 0, 'S', 0, 'S', 0, 0, 0, 0,     'J', 0, 0,     0, 'L',   0, 'L', 0, 'Z', 0, 'O',   0,   0],
             ["I", "I", 'I', 0, 0, 0, 'S', 0, 0,   0, 0, 0,     'J', 0, 0,     0, 'L', 'L', 'L', 0, 'Z', 0, 'O', 'O', 'O'],
             ["I", 0,   0, 0, 0, 0,   'S', 0, 0,   0, 0, 0,     'J', 0, 0,     0, 'L', 'L',   0, 0, 'Z', 0,   0,   0, 'O'],
             ["I", 0,   0, 0, 0, 0,   'S', 0, 0,   0, 0, 0,     'J', 0, 0,     0, 'L',   0, 'L', 0, 'Z', 0, 'O', 'O', 'O']]
    for x, row in enumerate(title):
        for y, brick in enumerate(row):
            color = shapes_colors.get(brick, black)
            pygame.draw.rect(game_display, color, ((brick_width + brick_margin) * y + display_width/2 - 275,
                                                   (brick_height + brick_margin) * x + 10,
                                                   brick_width,
                                                   brick_height))


if __name__ == "__main__":

    game_display = pygame.display.set_mode(resolution)
    pygame.display.set_caption('PyTris')
    clock = pygame.time.Clock()
    game_loop = True
    # Tetris game
    tetris = TetrisGame(grid_rows, grid_columns)
    # first shape
    shape = TetrisShape.random()
    tetris.add_shape(shape)  # create the first shape into game
    shape = TetrisShape.random()  # creates the next shape
    count = 0  # for the automatic falling, incremented for every frame
    speed = speed - tetris.level*5
    while game_loop:
        if tetris.active_shape:
            # event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_loop = False
                elif event.type == pygame.KEYDOWN:
                    # events from key presses
                    if event.key == pygame.K_RIGHT:
                        tetris.move_shape("right")
                    elif event.key == pygame.K_LEFT:
                        tetris.move_shape("left")
                    elif event.key == pygame.K_UP:
                        tetris.move_shape("rotate")
            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN]:
                tetris.move_shape("down")

        if not tetris.active_shape:
            if any(brick != 0 for brick in tetris.grid[2]):
                game_display.fill(black)
                draw_over()
                pygame.display.update()
                game_loop = False
            else:
                tetris.check_complete_rows()
                # speed -= 5
                tetris.add_shape(shape)
                shape = TetrisShape.random()
        # automatic falling
        if count == speed:
            tetris.move_shape("down")
            count = 0
        count += 1

        game_display.fill(black)  # cleans the windows
        draw_grid()
        draw_next_shape()
        draw_score()
        draw_level()
        draw_title()

        pygame.display.update()

        clock.tick(60)


pygame.quit()
quit()
