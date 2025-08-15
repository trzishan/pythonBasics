
import curses
import random
import time

# Define shapes
SHAPES = {
    'I': [[1, 1, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'Z': [[1, 1, 0],
          [0, 1, 1]]
}

COLS = 10
ROWS = 20

class Piece:
    def __init__(self, shape):
        self.shape = SHAPES[shape]
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

def create_grid():
    return [[0 for _ in range(COLS)] for _ in range(ROWS)]

def draw_grid(stdscr, grid, score):
    stdscr.clear()
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val:
                stdscr.addstr(y, x*2, "[]")
            else:
                stdscr.addstr(y, x*2, "  ")
    stdscr.addstr(0, COLS*2 + 2, f"Score: {score}")
    stdscr.refresh()

def piece_fits(piece, grid):
    for y, row in enumerate(piece.shape):
        for x, val in enumerate(row):
            if val:
                px = piece.x + x
                py = piece.y + y
                if px < 0 or px >= COLS or py >= ROWS:
                    return False
                if py >= 0 and grid[py][px]:
                    return False
    return True

def merge_piece(piece, grid):
    for y, row in enumerate(piece.shape):
        for x, val in enumerate(row):
            if val:
                grid[piece.y + y][piece.x + x] = 1

def clear_lines(grid):
    new_grid = [row for row in grid if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_grid)
    for _ in range(lines_cleared):
        new_grid.insert(0, [0 for _ in range(COLS)])
    return new_grid, lines_cleared

def tetris(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    grid = create_grid()
    current = Piece(random.choice(list(SHAPES)))
    next_drop = time.time() + 0.5
    score = 0

    while True:
        draw_grid(stdscr, grid, score)

        # User input
        try:
            key = stdscr.getkey()
        except:
            key = None

        moved = False

        if key in ['a', 'KEY_LEFT']:
            current.x -= 1
            if not piece_fits(current, grid):
                current.x += 1
        elif key in ['d', 'KEY_RIGHT']:
            current.x += 1
            if not piece_fits(current, grid):
                current.x -= 1
        elif key in ['s', 'KEY_DOWN']:
            current.y += 1
            if not piece_fits(current, grid):
                current.y -= 1
        elif key in ['w', 'KEY_UP', ' ']:
            old_shape = current.shape
            current.rotate()
            if not piece_fits(current, grid):
                current.shape = old_shape

        # Auto drop
        if time.time() > next_drop:
            current.y += 1
            if not piece_fits(current, grid):
                current.y -= 1
                merge_piece(current, grid)
                grid, cleared = clear_lines(grid)
                score += cleared * 100
                current = Piece(random.choice(list(SHAPES)))
                if not piece_fits(current, grid):
                    draw_grid(stdscr, grid, score)
                    stdscr.addstr(10, COLS * 2 + 2, "GAME OVER")
                    stdscr.refresh()
                    time.sleep(2)
                    break
            next_drop = time.time() + 0.5

curses.wrapper(tetris)
