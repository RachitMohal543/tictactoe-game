import sys
import pygame

# Initialize Pygame
pygame.init()
pygame.font.init()

# Constants
WIDTH, HEIGHT = 600, 700
BOARD_SIZE = 600
GRID_SIZE = 3
CELL_SIZE = BOARD_SIZE // GRID_SIZE
LINE_WIDTH = 8
MARK_WIDTH = 14
RADIUS = CELL_SIZE // 4
SPACE = CELL_SIZE // 4

# Colors
BG_COLOR = (24, 26, 32)
GRID_COLOR = (55, 62, 78)
LINE_COLOR = (74, 85, 104)
COLOR_X = (239, 68, 68)     # Coral / Red
COLOR_O = (59, 130, 246)    # Sky / Blue
WIN_COLOR = (34, 197, 94)   # Emerald Green
TEXT_COLOR = (241, 245, 249)
HINT_COLOR = (148, 163, 184)
PANEL_COLOR = (18, 20, 25)

# Setup Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()

font_title = pygame.font.SysFont("segoeui", 32, bold=True)
font_sub = pygame.font.SysFont("segoeui", 20)

class TicTacToe:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.player = 'X'
        self.game_over = False
        self.winner = None
        self.winning_line = None  # ((x1, y1), (x2, y2))

    def make_move(self, row, col):
        if self.board[row][col] is None and not self.game_over:
            self.board[row][col] = self.player
            if self.check_win(self.player):
                self.game_over = True
                self.winner = self.player
            elif self.is_board_full():
                self.game_over = True
                self.winner = "Draw"
            else:
                self.player = 'O' if self.player == 'X' else 'X'
            return True
        return False

    def is_board_full(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if self.board[row][col] is None:
                    return False
        return True

    def check_win(self, p):
        # Rows
        for r in range(GRID_SIZE):
            if self.board[r][0] == self.board[r][1] == self.board[r][2] == p:
                y = r * CELL_SIZE + CELL_SIZE // 2
                self.winning_line = ((20, y), (BOARD_SIZE - 20, y))
                return True

        # Columns
        for c in range(GRID_SIZE):
            if self.board[0][c] == self.board[1][c] == self.board[2][c] == p:
                x = c * CELL_SIZE + CELL_SIZE // 2
                self.winning_line = ((x, 20), (x, BOARD_SIZE - 20))
                return True

        # Diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == p:
            self.winning_line = ((25, 25), (BOARD_SIZE - 25, BOARD_SIZE - 25))
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] == p:
            self.winning_line = ((BOARD_SIZE - 25, 25), (25, BOARD_SIZE - 25))
            return True

        return False

    def draw_grid(self):
        # Horizontal lines
        for i in range(1, GRID_SIZE):
            pygame.draw.line(
                screen, GRID_COLOR,
                (0, i * CELL_SIZE),
                (BOARD_SIZE, i * CELL_SIZE),
                LINE_WIDTH
            )
        # Vertical lines
        for i in range(1, GRID_SIZE):
            pygame.draw.line(
                screen, GRID_COLOR,
                (i * CELL_SIZE, 0),
                (i * CELL_SIZE, BOARD_SIZE),
                LINE_WIDTH
            )

    def draw_marks(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                mark = self.board[r][c]
                center_x = c * CELL_SIZE + CELL_SIZE // 2
                center_y = r * CELL_SIZE + CELL_SIZE // 2

                if mark == 'O':
                    pygame.draw.circle(
                        screen, COLOR_O,
                        (center_x, center_y),
                        RADIUS, MARK_WIDTH
                    )
                elif mark == 'X':
                    # Draw 'X' lines
                    start_asc = (c * CELL_SIZE + SPACE, r * CELL_SIZE + CELL_SIZE - SPACE)
                    end_asc = (c * CELL_SIZE + CELL_SIZE - SPACE, r * CELL_SIZE + SPACE)
                    pygame.draw.line(screen, COLOR_X, start_asc, end_asc, MARK_WIDTH)

                    start_desc = (c * CELL_SIZE + SPACE, r * CELL_SIZE + SPACE)
                    end_desc = (c * CELL_SIZE + CELL_SIZE - SPACE, r * CELL_SIZE + CELL_SIZE - SPACE)
                    pygame.draw.line(screen, COLOR_X, start_desc, end_desc, MARK_WIDTH)

    def draw_winning_line(self):
        if self.winning_line:
            start_pos, end_pos = self.winning_line
            pygame.draw.line(screen, WIN_COLOR, start_pos, end_pos, LINE_WIDTH + 4)

    def draw_bottom_panel(self):
        panel_rect = pygame.Rect(0, BOARD_SIZE, WIDTH, HEIGHT - BOARD_SIZE)
        pygame.draw.rect(screen, PANEL_COLOR, panel_rect)
        pygame.draw.line(screen, GRID_COLOR, (0, BOARD_SIZE), (WIDTH, BOARD_SIZE), 3)

        if not self.game_over:
            turn_color = COLOR_X if self.player == 'X' else COLOR_O
            status_text = f"Player {self.player}'s Turn"
            text_surface = font_title.render(status_text, True, turn_color)
            sub_surface = font_sub.render("Click any empty cell to place your move", True, HINT_COLOR)
        else:
            if self.winner == "Draw":
                text_surface = font_title.render("Game Over: It's a Draw!", True, HINT_COLOR)
            else:
                win_color = COLOR_X if self.winner == 'X' else COLOR_O
                text_surface = font_title.render(f"Player {self.winner} Wins!", True, win_color)
            sub_surface = font_sub.render("Press 'R' to Restart or 'ESC' to Quit", True, WIN_COLOR)

        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, BOARD_SIZE + 18))
        screen.blit(sub_surface, (WIDTH // 2 - sub_surface.get_width() // 2, BOARD_SIZE + 58))

    def render(self):
        screen.fill(BG_COLOR)
        self.draw_grid()
        self.draw_marks()
        self.draw_winning_line()
        self.draw_bottom_panel()
        pygame.display.flip()

def main():
    game = TicTacToe()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                if mouse_y < BOARD_SIZE and not game.game_over:
                    clicked_row = mouse_y // CELL_SIZE
                    clicked_col = mouse_x // CELL_SIZE
                    game.make_move(clicked_row, clicked_col)

        game.render()
        clock.tick(60)

if __name__ == "__main__":
    main()
