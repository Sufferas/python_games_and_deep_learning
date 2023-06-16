import pygame
import random

# Größe des Spielfelds und Anzahl der Minen
ROWS, COLS = 10, 10
MINES = 10

# Größe der einzelnen Felder und der Fenstergröße
SIZE = 40
WIDTH, HEIGHT = COLS * SIZE, ROWS * SIZE

# Farben definieren
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BLACK = (0, 0, 0)

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.mine = False
        self.revealed = False
        self.flagged = False
        self.adjacent_mines = 0

    def draw(self, win):
        rect = pygame.Rect(self.col * SIZE, self.row * SIZE, SIZE, SIZE)
        border_rect = pygame.Rect(self.col * SIZE + 1, self.row * SIZE + 1, SIZE - 2, SIZE - 2)
        pygame.draw.rect(win, BLACK, rect)
        pygame.draw.rect(win, GRAY if self.revealed else WHITE, border_rect)
        if self.revealed and not self.mine and self.adjacent_mines > 0:
            font = pygame.font.Font(None, 24)
            text = font.render(str(self.adjacent_mines), True, BLACK)
            win.blit(text, border_rect.move(SIZE / 4, SIZE / 4))
        if self.mine and self.revealed:
            pygame.draw.circle(win, BLACK, rect.center, SIZE / 4)
        if self.flagged and not self.revealed:
            pygame.draw.circle(win, BLACK, rect.center, SIZE / 4)

    def reveal(self, grid):
        if self.revealed:
            return
        self.revealed = True
        if self.adjacent_mines == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= self.row + i < ROWS and 0 <= self.col + j < COLS:
                        grid[self.row + i][self.col + j].reveal(grid)

    def reveal_neighbors(self, grid):
        for i in range(-1, 2):
            for j in range(-1, 2):
                row, col = self.row + i, self.col + j
                if 0 <= row < ROWS and 0 <= col < COLS:
                    neighbor = grid[row][col]
                    if not neighbor.revealed and not neighbor.mine:
                        neighbor.reveal(grid)

    def count_mines(self, grid):
        if self.mine:
            return
        for i in range(-1, 2):
            for j in range(-1, 2):
                row, col = self.row + i, self.col + j
                if 0 <= row < ROWS and 0 <= col < COLS and grid[row][col].mine:
                    self.adjacent_mines += 1

    def toggle_flag(self):
        if not self.revealed:
            self.flagged = not self.flagged
            return self.flagged
        return False

    def set_adjacent_mines(self, grid):
        if not self.mine:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= self.row + i < ROWS and 0 <= self.col + j < COLS:
                        if grid[self.row + i][self.col + j].mine:
                            self.adjacent_mines += 1


def check_win(grid):
    return all(cell.mine == cell.flagged for row in grid for cell in row)


def reset(grid):
    mines = random.sample([cell for row in grid for cell in row], MINES)
    for row in grid:
        for cell in row:
            cell.mine = False
            cell.revealed = False
            cell.flagged = False
            cell.adjacent_mines = 0
    for cell in mines:
        cell.mine = True
    for row in grid:
        for cell in row:
            cell.count_mines(grid)


def reveal_mines(grid):
    for row in grid:
        for cell in row:
            if cell.mine:
                cell.revealed = True

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.Font(None, 24)
        text = font.render(self.text, True, BLACK)
        win.blit(text, (self.x + self.width / 2 - text.get_width() / 2, self.y + self.height / 2 - text.get_height() / 2))

    def is_over(self, pos):
        return self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT + 50))
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)

    grid = [[Cell(row, col) for col in range(COLS)] for row in range(ROWS)]
    reset(grid)

    restart_button = Button(WIDTH // 2 - 40, HEIGHT + 10, 80, 30, "Neustart", GRAY)

    start_time = None
    end_time = None
    game_over = False
    won = False

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if start_time is None:
                    start_time = pygame.time.get_ticks()
                x, y = pygame.mouse.get_pos()
                if restart_button.is_over((x, y)):
                    reset(grid)
                    start_time = None
                    end_time = None
                    game_over = False
                    won = False
                elif y < HEIGHT:
                    row, col = y // SIZE, x // SIZE
                    if event.button == 1:  # Linke Maustaste
                        if grid[row][col].mine:
                            reveal_mines(grid)
                            end_time = pygame.time.get_ticks()
                            game_over = True
                            won = False
                        else:
                            grid[row][col].reveal(grid)
                    elif event.button == 3:  # Rechte Maustaste
                        if grid[row][col].toggle_flag() and check_win(grid):
                            end_time = pygame.time.get_ticks()
                            game_over = True
                            won = True

        win.fill(WHITE)
        for row in grid:
            for cell in row:
                cell.draw(win)
        restart_button.draw(win)

        if game_over:
            text = font.render("Gewonnen!" if won else "Verloren!", True, BLACK)
            win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT + 20))

            if end_time and start_time:
                time_text = font.render(f"Zeit: {(end_time - start_time) / 1000:.2f} Sekunden", True, BLACK)
                win.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT + 35))
        elif start_time:
            time_text = font.render(f"Zeit: {(pygame.time.get_ticks() - start_time) / 1000:.2f} Sekunden", True, BLACK)
            win.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, HEIGHT + 35))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()



if __name__ == "__main__":
    main()


# TODO fix position win text and reset