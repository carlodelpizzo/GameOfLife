import pygame
from pygame.locals import *
import random


def game(screen_width, screen_height, rows, cols, ran):
    pygame.init()
    # Initialize screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    # Title
    pygame.display.set_caption("Life")
    # Screen colors
    bg_color = [0, 0, 0]
    fg_color = [50, 100, 200]
    divider_color = [50, 50, 50]
    divider_color_paused = [50, 25, 25]

    class Cell:
        def __init__(self, x, y, w, h, index, pos):
            self.alive = False
            self.x = x
            self.y = y
            self.width = w
            self.height = h
            self.color = bg_color
            self.index = index
            self.pos = pos
            self.neighbors = []

        def update_screen(self):
            if self.alive:
                pygame.draw.rect(screen, fg_color, (int(self.x), int(self.y), int(self.width), int(self.height)))
            elif not self.alive:
                pygame.draw.rect(screen, bg_color, (int(self.x), int(self.y), int(self.width), int(self.height)))

        def find_neighbors(self):
            self.neighbors = []

            # Neighbors on row above
            if 0 <= self.index - cols - 1 <= len(cells) - 1:
                if cells[self.index - cols - 1].pos[1] == self.pos[1] - 1:
                    if cells[self.index - cols - 1].alive:
                        self.neighbors.append(cells[self.index - cols - 1])
            if 0 <= self.index - cols <= len(cells) - 1:
                if cells[self.index - cols].pos[1] == self.pos[1]:
                    if cells[self.index - cols].alive:
                        self.neighbors.append(cells[self.index - cols])
            if 0 <= self.index - cols + 1 <= len(cells) - 1:
                if cells[self.index - cols + 1].pos[1] == self.pos[1] + 1:
                    if cells[self.index - cols + 1].alive:
                        self.neighbors.append(cells[self.index - cols + 1])

            # Neighbors on same row
            if 0 <= self.index - 1 <= len(cells) - 1:
                if cells[self.index - 1].pos[1] == self.pos[1] - 1:
                    if cells[self.index - 1].alive:
                        self.neighbors.append(cells[self.index - 1])
            if 0 <= self.index + 1 <= len(cells) - 1:
                if cells[self.index + 1].pos[1] == self.pos[1] + 1:
                    if cells[self.index + 1].alive:
                        self.neighbors.append(cells[self.index + 1])

            # Neighbors on row below
            if 0 <= self.index + cols - 1 <= len(cells) - 1:
                if cells[self.index + cols - 1].pos[1] == self.pos[1] - 1:
                    if cells[self.index + cols - 1].alive:
                        self.neighbors.append(cells[self.index + cols - 1])
            if 0 <= self.index + cols <= len(cells) - 1:
                if cells[self.index + cols].pos[1] == self.pos[1]:
                    if cells[self.index + cols].alive:
                        self.neighbors.append(cells[self.index + cols])
            if 0 <= self.index + cols + 1 <= len(cells) - 1:
                if cells[self.index + cols + 1].pos[1] == self.pos[1] + 1:
                    if cells[self.index + cols + 1].alive:
                        self.neighbors.append(cells[self.index + cols + 1])

        def advance(self):
            alive_neighbors = len(self.neighbors)
            if self.alive:
                if alive_neighbors == 3 or alive_neighbors == 2:
                    self.alive = True
                else:
                    self.alive = False
            else:
                if alive_neighbors == 3:
                    self.alive = True

    def init_cells(num_rows, num_cols):
        cell_array = []
        cell_w = (screen_width / num_cols) * 0.95
        cell_h = (screen_height / num_rows) * 0.95
        pad_x = (screen_width / num_cols - cell_w) * num_cols / (num_cols + 1)
        pad_y = (screen_height / num_rows - cell_h) * num_rows / (num_rows + 1)
        for row in range(num_rows):
            for col in range(num_cols):
                index = (row * num_cols) + col
                x_offset = pad_x + (cell_w + pad_x) * col
                y_offset = pad_y + (cell_h + pad_y) * row
                cell_array.append(Cell(x_offset, y_offset, cell_w, cell_h, index, (row, col)))
        return cell_array

    def mouse_draw():
        mouse_pos = pygame.mouse.get_pos()
        border_x = (screen_width / cols - cells[0].width) * cols / (cols + 1)
        border_y = (screen_height / rows - cells[0].height) * rows / (rows + 1)
        for c in range(len(cells)):
            if cells[c].x - border_x <= mouse_pos[0] <= cells[c].x + cells[c].width + border_x:
                if cells[c].y - border_y <= mouse_pos[1] <= cells[c].y + cells[c].height + border_y:
                    if not removing:
                        cells[c].alive = True
                    elif removing:
                        cells[c].alive = False
                    break

    cells = init_cells(rows, cols)
    # Randomize cells
    if ran:
        for i in range(len(cells)):
            a = random.randint(1, 2)
            if a % 2 == 0:
                cells[i].alive = True
            else:
                cells[i].alive = False

    clock = pygame.time.Clock()
    frame_rate = 240
    slowed_rate = 10
    pause = True
    turbo = False
    slow = False
    drag_mouse = False
    removing = False
    running = True
    while running:
        # Event Loop
        for event in pygame.event.get():
            # Close Window
            if event.type == pygame.QUIT:
                running = False
                break

            keys = pygame.key.get_pressed()
            # Key down events
            if event.type == pygame.KEYDOWN:
                # Pause/Unpause
                if keys[K_SPACE] and not pause:
                    pause = True
                elif keys[K_SPACE] and pause:
                    pause = False
                # Kill all cells
                if keys[K_k]:
                    for i in range(len(cells)):
                        cells[i].alive = False
                # Randomize cells
                if keys[K_r]:
                    for i in range(len(cells)):
                        a = random.randint(1, 2)
                        if a % 2 == 0:
                            cells[i].alive = True
                        else:
                            cells[i].alive = False
                # Turbo
                if keys[K_t] and not turbo:
                    turbo = True
                # Slow mode
                if keys[K_s] and not slow:
                    slow = True
                # Advance one stage
                if (keys[K_RIGHT] or keys[K_n]) and pause:
                    for i in range(len(cells)):
                        cells[i].find_neighbors()
                    for i in range(len(cells)):
                        cells[i].advance()

            # Key up events
            if event.type == pygame.KEYUP:
                if not keys[K_t] and turbo:
                    turbo = False
                if not keys[K_s] and slow:
                    slow = False

            # Drawing cells with mouse
            # Mouse button down
            if event.type == pygame.MOUSEBUTTONDOWN and not drag_mouse:
                drag_mouse = True
                if event.button == 3:
                    removing = True
                mouse_draw()
            # Mouse button up
            elif event.type == pygame.MOUSEBUTTONUP and drag_mouse:
                mouse_draw()
                drag_mouse = False
                removing = False

        # Cell stage advancement
        if not pause:
            screen.fill(divider_color)
            for i in range(len(cells)):
                cells[i].find_neighbors()
            for i in range(len(cells)):
                cells[i].advance()

            if not turbo and not slow:
                clock.tick(slowed_rate)
            elif not turbo and slow:
                clock.tick(int(slowed_rate/4))
            else:
                clock.tick(frame_rate)
        else:
            screen.fill(divider_color_paused)
            if drag_mouse:
                mouse_draw()
            clock.tick(frame_rate)

        for i in range(len(cells)):
            cells[i].update_screen()

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
