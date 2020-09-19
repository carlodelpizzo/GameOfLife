import pygame
from pygame.locals import *
import random


def game(screen_width, screen_height, rows, cols, ran=False):
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
    divider_color_paused = [50, 25, 25]
    # Font
    font_size = 25
    font_face = "Helvetica"
    font = pygame.font.SysFont(font_face, font_size)

    class Cell:
        def __init__(self, x, y, w, h, location):
            self.alive = False
            self.x = int(x)
            self.y = int(y)
            self.width = w
            self.height = h
            self.color = fg_color
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
            if self.alive and not paused:
                pygame.draw.rect(screen, black, (self.x, self.y, self.width, self.height))
                pygame.draw.rect(screen, self.color, (self.x + 1, self.y + 1, self.width - 2, self.height - 2))
            elif not self.alive and not paused:
                pygame.draw.rect(screen, divider_color, (self.x, self.y, self.width, self.height))
                pygame.draw.rect(screen, black, (self.x + 1, self.y + 1, self.width - 2, self.height - 2))
            elif self.alive and paused:
                pygame.draw.rect(screen, divider_color_paused, (self.x, self.y, self.width, self.height))
                pygame.draw.rect(screen, self.color, (self.x + 1, self.y + 1, self.width - 2, self.height - 2))
            elif not self.alive and paused:
                pygame.draw.rect(screen, divider_color_paused, (self.x, self.y, self.width, self.height))
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

    def mouse_draw():
        mouse_pos = pygame.mouse.get_pos()
        for p in cell_dict:
            if cell_dict[p].x <= mouse_pos[0] <= cell_dict[p].x + cell_dict[p].width:
                if cell_dict[p].y <= mouse_pos[1] <= cell_dict[p].y + cell_dict[p].height:
                    if not removing:
                        cell_dict[p].alive = True
                    elif removing:
                        cell_dict[p].alive = False
                    break

    def advance_stage():
        next_stage = {}
        for p in cell_dict:
            if not cell_dict[p].alive:
                continue
            for np in cell_dict[p].neighbors:
                if np in cell_dict and np not in next_stage:
                    next_stage[np] = cell_dict[np].alive_next_stage()
        for p in next_stage:
            cell_dict[p].alive = next_stage[p]

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
                        cell_dict[cell_p] = Cell(x_off, y_off, cell_w, cell_h, cell_p)
            for r in range(add_rows):
                for c in range(max_col + add_cols):
                    x_off = c * cell_w
                    y_off = r * cell_h + max_y
                    cell_p = (r + max_row, c)
                    if cell_p not in cell_dict:
                        cell_dict[cell_p] = Cell(x_off, y_off, cell_w, cell_h, cell_p)

    cell_dict = {}
    cell_w = screen_width / cols
    cell_h = screen_height / rows
    for row in range(rows):
        for col in range(cols):
            x_offset = cell_w * col
            y_offset = cell_h * row
            cell_pos = (row, col)
            cell_dict[cell_pos] = Cell(x_offset, y_offset, cell_w, cell_h, cell_pos)
    if ran:
        for pos in cell_dict:
            if random.randint(1, 2) % 2 == 0:
                cell_dict[pos].alive = True
            else:
                cell_dict[pos].alive = False

    clock = pygame.time.Clock()
    frame_rate = 60
    turbo_rate = 240
    slowed_rate = 10
    cell_stage = 0
    paused = True
    turbo = False
    slow = False
    drag_mouse = False
    removing = False
    running = True
    while running:
        screen.fill(black)
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
                elif keys[K_SPACE] and paused:
                    paused = False
                # Kill all cells
                if keys[K_k] and paused:
                    for pos in cell_dict:
                        cell_dict[pos].alive = False
                    cell_stage = 0
                # Randomize cells
                if keys[K_r] and paused:
                    for pos in cell_dict:
                        if random.randint(1, 2) % 2 == 0:
                            cell_dict[pos].alive = True
                        else:
                            cell_dict[pos].alive = False
                    cell_stage = 0
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
        for pos in cell_dict:
            cell_dict[pos].update_screen()

        # Draw cell stage counter
        display_stage = font.render(str(cell_stage), True, white)
        screen.blit(display_stage, (0, 0))

        if slow:
            clock.tick(slowed_rate)
        elif turbo:
            clock.tick(turbo_rate)
        else:
            clock.tick(frame_rate)
        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()
