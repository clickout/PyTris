import pygame

from tetrisgrid import TetrisGame, TetrisShape

pygame.init()

font = pygame.font.SysFont("monospace", 20)

# window resolution
resolution = display_width, display_height = 800, 600
# colors
black = (0, 0, 0)
white = (255, 255, 255)
shapes_colors = {"I": (0, 255, 255), "J": (0, 0, 255), "L": (255, 140, 0),
                 "O": (255, 255, 0), "S": (0, 255, 0), "T": (128, 0, 128), "Z": (255, 0, 0)}
# brick size
brick_width = 5
brick_height = 5
brick_margin = 1
# grid size in bricks
grid_columns = 100
grid_rows = 100
grid_width = (brick_width + brick_margin) * grid_columns
grid_height = (brick_height + brick_margin) * grid_rows
# speed of brick falling (60 = 1 sec, 120 = 2 sec, 30 = 0.5 sec ...)
speed = 30

game_display = pygame.display.set_mode(resolution)
pygame.display.set_caption('PyTris')
clock = pygame.time.Clock()
full_to_top = False


def draw_grid():
    for row in range(grid_rows):
        for column in range(grid_columns):
            color = shapes_colors.get(tetris.grid[row][column], white)
            pygame.draw.rect(game_display, color, ((brick_width + brick_margin) * column + 10,
                                                   (brick_height + brick_margin) * row + display_height-grid_height-10,
                                                   brick_width,
                                                   brick_height))


def draw_next_shape():
    for row in range(4):
        for column in range(4):
            color = shapes_colors.get(shape.representation[row][column], white)
            pygame.draw.rect(game_display, color, ((brick_width + brick_margin) * (column + grid_columns) + 50,
                                                   (brick_height + brick_margin) * row + display_height - grid_height-10,
                                                   brick_width,
                                                   brick_height))


def draw_score():
    text = font.render("Score: {}".format(tetris.score), 1, white)
    game_display.blit(text, ((brick_width + brick_margin) * grid_columns + 50, display_height-grid_height+100))


if __name__ == "__main__":

    # Tetris game
    tetris = TetrisGame(grid_rows, grid_columns)
    # first shape
    shape = TetrisShape.random()
    tetris.add_shape(shape)  # create the first shape into game
    shape = TetrisShape.random()  # creates the next shape
    count = 0  # for the automatic falling, incremented for every frame
    while not full_to_top:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                full_to_top = True
            elif event.type == pygame.KEYDOWN:
                # events from key presses
                if event.key == pygame.K_RIGHT:
                    tetris.move_right()
                elif event.key == pygame.K_LEFT:
                    tetris.move_left()
                elif event.key == pygame.K_DOWN:
                    tetris.move_down()
                elif event.key == pygame.K_UP:
                    tetris.rotate()

        game_display.fill(black)  # cleans the windows
        # automatic falling
        if count == speed:
            tetris.move_down()
            count = 0
        count += 1

        draw_grid()
        if not tetris.active_shape:
            tetris.check_complete_rows()
            tetris.add_shape(shape)
            shape = TetrisShape.random()
        draw_next_shape()
        draw_score()

        pygame.display.update()

        clock.tick(60)


pygame.quit()
quit()
