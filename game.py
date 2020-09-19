import pygame
from pygame.locals import *
import random


def game(screen_width, screen_height, ran=False):
    pygame.init()
    # Initialize screen
    screen = pygame.display.set_mode((screen_width, screen_height))
    # Title
    pygame.display.set_caption("Life")
    # Screen colors
    black = [0, 0, 0]
    fg_color = [50, 100, 200]
    divider_color = [50, 50, 50]
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
            self.width = int(w)
            self.height = int(h)
            self.color = black
            self.pos = location

        def update_screen(self):
            if self.alive and not paused:
                pygame.draw.rect(screen, divider_color, (self.x, self.y, self.width, self.height))
                pygame.draw.rect(screen, fg_color, (self.x + 1, self.y + 1, self.width - 1, self.height - 1))
            elif not self.alive and not paused:
                pygame.draw.rect(screen, divider_color, (self.x, self.y, self.width, self.height))
                pygame.draw.rect(screen, black, (self.x + 1, self.y + 1, self.width - 1, self.height - 1))
            elif self.alive and paused:
                pygame.draw.rect(screen, divider_color_paused, (self.x, self.y, self.width, self.height))
                pygame.draw.rect(screen, fg_color, (self.x + 1, self.y + 1, self.width - 1, self.height - 1))
            elif not self.alive and paused:
                pygame.draw.rect(screen, divider_color_paused, (self.x, self.y, self.width, self.height))
                pygame.draw.rect(screen, black, (self.x + 1, self.y + 1, self.width - 1, self.height - 1))

    def mouse_draw():
        mouse_pos = pygame.mouse.get_pos()
        for p in cells:
            if cells[p].x <= mouse_pos[0] <= cells[p].x + cells[p].width:
                if cells[p].y <= mouse_pos[1] <= cells[p].y + cells[p].height:
                    if not removing:
                        cells[p].alive = True
                    elif removing:
                        cells[p].alive = False
                    break

    cells = {}
    cell_w = 40
    cell_h = 40
    num_rows = int(screen_width / cell_w)
    num_cols = int(screen_height / cell_h)
    for row in range(num_rows):
        for col in range(num_cols):
            x_offset = cell_w * col
            y_offset = cell_h * row
            cell_pos = (row, col)
            cells[cell_pos] = Cell(x_offset, y_offset, cell_w, cell_h, (row, col))
    # Randomize cells
    if ran:
        for pos in cells:
            if random.randint(1, 2) % 2 == 0:
                cells[pos].alive = True
            else:
                cells[pos].alive = False

    clock = pygame.time.Clock()
    frame_rate = 240
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
                    cell_stage = 0
                # Randomize cells
                if keys[K_r] and paused:
                    cell_stage = 0
                # Turbo
                if keys[K_t] and not turbo:
                    turbo = True
                # Slow mode
                if keys[K_s] and not slow:
                    slow = True
                # Advance one stage
                if (keys[K_RIGHT] or keys[K_n]) and paused:
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

        # Cell stage advancement
        if not paused:
            cell_stage += 1

            if not turbo and not slow:
                clock.tick(slowed_rate)
            elif not turbo and slow:
                clock.tick(int(slowed_rate/4))
            else:
                clock.tick(frame_rate)
        else:
            if drag_mouse:
                mouse_draw()
            clock.tick(frame_rate)
            
        # Draw cells
        for pos in cells:
            cells[pos].update_screen()

        # Visually update cell stage counter
        display_stage = font.render(str(cell_stage), True, (255, 255, 255))
        screen.blit(display_stage, (0, 0))

        pygame.display.flip()

    pygame.display.quit()
    pygame.quit()


game(400, 400)
