import pygame
from pygame.locals import *
import random
from datetime import datetime


def game(screen_width, screen_height, rows, cols, ran=False, alive_color=None):
    pygame.init()
    # Initialize screen
    screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)
    # Title
    pygame.display.set_caption("Life")
    # Screen colors
    black = [0, 0, 0]
    white = [255, 255, 255]
    fg_color = [50, 100, 200]
    divider_color = [25, 25, 25]
    divider_color_paused = [25, 50, 50]
    if alive_color is None:
        alive_color = fg_color
    # Font
    font_size = 25
    font_face = "Helvetica"
    font = pygame.font.SysFont(font_face, font_size)

    class Cell:
        def __init__(self, x: int, y: int, w: int, h: int, location, cell_color=None):
            if cell_color is None:
                cell_color = fg_color
            self.alive = False
            self.x = x
            self.y = y
            self.width = w
            self.height = h
            self.color = cell_color
            self.pos = location
            self.neighbors = [(location[0] - 1, location[1] + 1),
                              (location[0] - 0, location[1] + 1),
                              (location[0] + 1, location[1] + 1),
                              (location[0] - 1, location[1] - 0),
                              (location[0] + 1, location[1] - 0),
                              (location[0] - 1, location[1] - 1),
                              (location[0] - 0, location[1] - 1),
                              (location[0] + 1, location[1] - 1)]

        def update_screen(self):
            if self.alive:
                pygame.draw.rect(screen, black, (self.x, self.y, self.width, self.height))
                pygame.draw.rect(screen, self.color, (self.x + 1, self.y + 1, self.width - 2, self.height - 2))
            elif not self.alive:
                pygame.draw.rect(screen, divider_color, (self.x, self.y, self.width, self.height))
                pygame.draw.rect(screen, black, (self.x + 1, self.y + 1, self.width - 2, self.height - 2))

        def alive_next_stage(self):
            friends = 0
            for p in self.neighbors:
                if p in cell_dict:
                    if cell_dict[p].alive:
                        friends += 1
                if friends > 3:
                    break
            if self.alive and 2 <= friends <= 3:
                return True
            elif not self.alive and friends == 3:
                return True
            else:
                return False

        def give_life(self):
            if not self.alive:
                self.alive = True
                self.update_screen()
            alive_cells[self.pos] = self

        def give_death(self):
            if self.alive:
                self.alive = False
                self.update_screen()
            alive_cells.pop(self.pos, None)

        def draw(self):
            pygame.draw.rect(screen, divider_color_paused, (self.x, self.y, self.width, self.height))
            pygame.draw.rect(screen, black, (self.x + 1, self.y + 1, self.width - 2, self.height - 2))

    def mouse_draw():
        mouse_pos = pygame.mouse.get_pos()
        for p in cell_dict:
            if cell_dict[p].x <= mouse_pos[0] <= cell_dict[p].x + cell_dict[p].width:
                if cell_dict[p].y <= mouse_pos[1] <= cell_dict[p].y + cell_dict[p].height:
                    if not removing:
                        cell_dict[p].give_life()
                    elif removing:
                        cell_dict[p].give_death()
                    break

    def advance_stage():
        next_stage = {}
        for cell_grid_pos in alive_cells:
            if cell_grid_pos not in next_stage:
                next_stage[cell_grid_pos] = cell_dict[cell_grid_pos].alive_next_stage()
            for neighbor_pos in alive_cells[cell_grid_pos].neighbors:
                if neighbor_pos not in next_stage:
                    if neighbor_pos in alive_cells:
                        next_stage[neighbor_pos] = alive_cells[neighbor_pos].alive_next_stage()
                    elif neighbor_pos in cell_dict:
                        next_stage[neighbor_pos] = cell_dict[neighbor_pos].alive_next_stage()
        for cell_grid_pos in next_stage:
            if next_stage[cell_grid_pos]:
                cell_dict[cell_grid_pos].give_life()
            else:
                cell_dict[cell_grid_pos].give_death()

    def resize(new_width, new_height):
        if new_width == screen_width and new_height == screen_height:
            pass
        else:
            max_col = []
            max_row = []
            for p in cell_dict:
                max_col.append(p[1])
                max_row.append(p[0])
            max_col.sort(reverse=True)
            max_row.sort(reverse=True)
            max_col = int(max_col[0])
            max_row = int(max_row[0])
            max_x = cell_w * max_col
            max_y = cell_h * max_row
            add_cols = (new_width - max_x) / cell_w
            add_rows = (new_height - max_y) / cell_h
            if add_cols % 1 != 0:
                add_cols = int(add_cols) + 1
            else:
                add_cols = int(add_cols)
            if add_rows % 1 != 0:
                add_rows = int(add_rows) + 1
            else:
                add_rows = int(add_rows)
            for r in range(max_row + 1):
                for c in range(add_cols):
                    x_off = c * cell_w + max_x
                    y_off = r * cell_h
                    cell_p = (r, c + max_col)
                    if cell_p not in cell_dict:
                        cell_dict[cell_p] = Cell(x_off, y_off, cell_w, cell_h, cell_p, alive_color)
            for r in range(add_rows):
                for c in range(max_col + add_cols):
                    x_off = c * cell_w
                    y_off = r * cell_h + max_y
                    cell_p = (r + max_row, c)
                    if cell_p not in cell_dict:
                        cell_dict[cell_p] = Cell(x_off, y_off, cell_w, cell_h, cell_p, alive_color)

    cell_dict = {}
    alive_cells = {}
    cell_w = screen_width / cols
    cell_h = screen_height / rows
    for row in range(rows):
        for col in range(cols):
            x_offset = cell_w * col
            y_offset = cell_h * row
            cell_pos = (row, col)
            cell_dict[cell_pos] = Cell(x_offset, y_offset, cell_w, cell_h, cell_pos, alive_color)
    if ran:
        for pos in cell_dict:
            if random.randint(1, 2) % 2 == 0:
                cell_dict[pos].give_life()
            else:
                cell_dict[pos].give_death()

    clock = pygame.time.Clock()
    frame_rate = 60
    turbo_rate = 240
    slowed_rate = 10
    cell_stage = 0
    paused = True
    draw_once = True
    turbo = False
    slow = False
    drag_mouse = False
    removing = False
    running = True
    while running:
        time_start = datetime.utcnow()

        # Event Loop
        for event in pygame.event.get():
            # Close Window
            if event.type == pygame.QUIT:
                running = False
                break

            keys = pygame.key.get_pressed()
            # Key down events
            if event.type == pygame.KEYDOWN:
                # Close Window
                if (keys[K_LCTRL] or keys[K_RCTRL]) and keys[K_w]:
                    running = False
                    break
                # Pause/Unpause
                if keys[K_SPACE] and not paused:
                    paused = True
                    draw_once = True
                elif keys[K_SPACE] and paused:
                    screen.fill(black)
                    paused = False
                    draw_once = True
                # Kill all cells
                if keys[K_k] and paused:
                    for pos in cell_dict:
                        cell_dict[pos].give_death()
                    cell_stage = 0
                    draw_once = True
                # Randomize cells
                if keys[K_r] and paused:
                    for pos in cell_dict:
                        if random.randint(1, 2) % 2 == 0:
                            cell_dict[pos].give_life()
                        else:
                            cell_dict[pos].give_death()
                    cell_stage = 0
                    draw_once = True
                # Turbo mode
                if keys[K_t] and not turbo:
                    turbo = True
                # Slow mode
                if keys[K_s] and not slow:
                    slow = True
                # Advance one stage
                if (keys[K_RIGHT] or keys[K_n]) and paused:
                    advance_stage()
                    cell_stage += 1

            # Key up events
            if event.type == pygame.KEYUP:
                if not keys[K_t] and turbo:
                    turbo = False
                if not keys[K_s] and slow:
                    slow = False

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

            # Window resize event
            if event.type == pygame.VIDEORESIZE:
                draw_once = True
                resize(event.w, event.h)
                screen_width = event.w
                screen_height = event.h
                screen = pygame.display.set_mode((screen_width, screen_height), RESIZABLE)

        # Cell stage advancement
        if not paused:
            advance_stage()
            cell_stage += 1
        else:
            if drag_mouse:
                mouse_draw()

        # Draw cells
        if draw_once:
            for pos in cell_dict:
                cell_dict[pos].update_screen()
            draw_once = False

        # Draw cell stage counter
        display_stage = font.render(str(cell_stage), True, white)
        pygame.draw.rect(screen, black, (0, 0, display_stage.get_rect().width, display_stage.get_rect().height - 10))
        screen.blit(display_stage, (0, -5))

        # Draw pause indicator
        if paused:
            pygame.draw.rect(screen, white, (5, display_stage.get_rect().height, 4, 25))
            pygame.draw.rect(screen, white, (15, display_stage.get_rect().height, 4, 25))

        # Print loop delay timer
        loop_time_milliseconds = datetime.utcnow() - time_start
        loop_time_milliseconds = loop_time_milliseconds.microseconds / 1000
        if loop_time_milliseconds >= 1.5:
            if loop_time_milliseconds % 1 >= 0.5:
                loop_time_milliseconds = int(loop_time_milliseconds) + 1
                print('Loop time: ' + str(loop_time_milliseconds) + 'ms')
            else:
                loop_time_milliseconds = int(loop_time_milliseconds)
                print('Loop time: ' + str(loop_time_milliseconds) + 'ms')

        if slow:
            clock.tick(slowed_rate)
        elif turbo:
            clock.tick(turbo_rate)
        else:
            clock.tick(frame_rate)
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
