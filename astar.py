import pygame
import math
from queue import PriorityQueue

import random
# ==== Window / UI sizes ====
WIDTH = 700            # grid is WIDTH x WIDTH
UI_H = 60              # height of bottom UI bar
WIN = pygame.display.set_mode((WIDTH, WIDTH + UI_H))
pygame.display.set_caption("A* Path Finding Algorithm")

# ==== Colors ====
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)   # note: this tuple is actually green; kept to match your original
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)
UI_BG = (245, 245, 245)
BTN_BG = (230, 230, 230)
BTN_BG_HOVER = (210, 210, 210)
BTN_BORDER = (160, 160, 160)
TEXT = (40, 40, 40)

# ==== UI: Reset button ====
pygame.font.init()
FONT = pygame.font.SysFont(None, 24)
RESET_BTN = pygame.Rect(12, WIDTH + 10, 120, 40)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        # Keeping your original x/y mapping
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self): return self.color == RED
    def is_open(self):   return self.color == GREEN
    def is_barrier(self):return self.color == BLACK
    def is_start(self):  return self.color == ORANGE
    def is_end(self):    return self.color == TURQUOISE

    def reset(self):       self.color = WHITE
    def make_start(self):  self.color = ORANGE
    def make_closed(self): self.color = RED
    def make_open(self):   self.color = GREEN
    def make_barrier(self):self.color = BLACK
    def make_end(self):    self.color = TURQUOISE
    def make_path(self):   self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # UP
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # RIGHT
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # LEFT
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    dx = abs(x1 - x2)
    dy = abs(y1 - y2)
    return (math.sqrt(2) - 1) * min(dx, dy) + max(dx, dy)



def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()

        draw()

        if current != start:
            current.make_closed()

    return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid


def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw_ui(win):
    # UI background bar
    pygame.draw.rect(win, UI_BG, (0, WIDTH, WIDTH, UI_H))
    # Reset button
    mx, my = pygame.mouse.get_pos()
    hovered = RESET_BTN.collidepoint(mx, my)
    pygame.draw.rect(win, BTN_BG_HOVER if hovered else BTN_BG, RESET_BTN, border_radius=8)
    pygame.draw.rect(win, BTN_BORDER, RESET_BTN, 1, border_radius=8)
    label = FONT.render("Reset (R)", True, TEXT)
    win.blit(label, (RESET_BTN.x + 20, RESET_BTN.y + 10))

    # Small hint text
    hint = FONT.render("Left: start/end then draw walls (drag) • Right: erase (drag) • Space: run A*", True, TEXT)
    win.blit(hint, (150, WIDTH + 18))


def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    draw_ui(win)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    # Only accept clicks inside the grid area (top WIDTH x WIDTH), ignore UI bar
    x, y = pos
    if y >= width or x < 0 or y < 0 or x >= width:
        return None  # clicked outside the grid (likely on UI)
    gap = width // rows
    # Keep your original mapping logic (swapped x/y)
    y_, x_ = pos
    row = y_ // gap
    col = x_ // gap
    return row, col


def hard_reset(rows, width):
    grid = make_grid(rows, width)
    start = None
    end = None
    return grid, start, end
def randomize_obstacles(grid, density=0.25, protect_start_end=True, seed=None):
    """
    Fill the grid with random barriers.
    - density: fraction of cells to turn into barriers (0.0–1.0)
    - protect_start_end: don't overwrite start/end cells if they exist
    - seed: optional seed for reproducible maps
    """
    if seed is not None:
        random.seed(seed)

    # First reset everything except start/end (if protected)
    # Then lay down barriers by probability.
    for row in grid:
        for spot in row:
            if protect_start_end and (spot.is_start() or spot.is_end()):
                continue
            spot.reset()

    for row in grid:
        for spot in row:
            if protect_start_end and (spot.is_start() or spot.is_end()):
                continue
            if random.random() < density:
                spot.make_barrier()



def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None

    # Drag state
    is_dragging = False
    drag_action = None   # 'barrier' or 'erase'
    last_cell = None     # avoid redundant writes while dragging

    run = True
    while run:
        draw(win, grid, ROWS, width)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # ===================== Mouse down =====================
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()

                # Reset button click
                if event.button == 1 and RESET_BTN.collidepoint(mx, my):
                    grid, start, end = hard_reset(ROWS, width)
                    is_dragging = False
                    drag_action = None
                    last_cell = None
                    continue

                rc = get_clicked_pos((mx, my), ROWS, width)
                if rc is None:
                    continue  # clicked UI, ignore
                row, col = rc
                spot = grid[row][col]

                if event.button == 1:
                    # Left click: first two clicks set start/end, then draw barriers
                    if not start and spot != end:
                        start = spot
                        start.make_start()
                        is_dragging = False
                        drag_action = None
                        last_cell = (row, col)
                    elif not end and spot != start:
                        end = spot
                        end.make_end()
                        is_dragging = False
                        drag_action = None
                        last_cell = (row, col)
                    else:
                        # start & end already chosen: begin barrier paint
                        if spot != start and spot != end and not spot.is_barrier():
                            spot.make_barrier()
                        is_dragging = True
                        drag_action = 'barrier'
                        last_cell = (row, col)

                elif event.button == 3:
                    # Right click: erase mode (also clears start/end if hit)
                    if spot == start:
                        start = None
                    if spot == end:
                        end = None
                    spot.reset()
                    is_dragging = True
                    drag_action = 'erase'
                    last_cell = (row, col)

            # ===================== Mouse motion (drag) =====================
            elif event.type == pygame.MOUSEMOTION and is_dragging:
                mx, my = pygame.mouse.get_pos()
                rc = get_clicked_pos((mx, my), ROWS, width)
                if rc is None:
                    continue
                row, col = rc
                if last_cell == (row, col):
                    continue  # avoid re-writing the same cell
                spot = grid[row][col]

                if drag_action == 'barrier':
                    if spot != start and spot != end and not spot.is_barrier():
                        spot.make_barrier()
                        last_cell = (row, col)
                elif drag_action == 'erase':
                    if spot == start:
                        start = None
                    if spot == end:
                        end = None
                    if not spot.is_barrier() and not spot.is_open() and not spot.is_closed() and not spot.is_start() and not spot.is_end():
                        # already white; still set for consistency
                        pass
                    spot.reset()
                    last_cell = (row, col)

            # ===================== Mouse up =====================
            elif event.type == pygame.MOUSEBUTTONUP:
                is_dragging = False
                drag_action = None
                last_cell = None

            # ===================== Keyboard =====================
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:  # original "clear colors" style
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

                if event.key == pygame.K_r:  # same as clicking Reset button
                    grid, start, end = hard_reset(ROWS, width)
                if event.key == pygame.K_q:
                    # Example: ~28% of the cells become obstacles; keep start/end if already placed
                    randomize_obstacles(grid, density=0.28, protect_start_end=True)


    pygame.quit()


if __name__ == "__main__":
    main(WIN, WIDTH)
