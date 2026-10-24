import sys
import math
import datetime
import pygame

# Initialize Pygame
pygame.init()
pygame.font.init()

# Window & Board Constants
WIDTH = 600
TOP_BAR_HEIGHT = 60
BOARD_SIZE = 600
BOTTOM_PANEL_HEIGHT = 90
HEIGHT = TOP_BAR_HEIGHT + BOARD_SIZE + BOTTOM_PANEL_HEIGHT  # 750px
OFFSET_Y = TOP_BAR_HEIGHT

GRID_SIZE = 3
CELL_SIZE = BOARD_SIZE // GRID_SIZE
LINE_WIDTH = 8
MARK_WIDTH = 14
RADIUS = CELL_SIZE // 4
SPACE = CELL_SIZE // 4

# Color Palettes for Themes
THEMES = {
    'dark': {
        'name': 'Dark',
        'bg': (24, 26, 32),
        'panel': (18, 20, 25),
        'grid': (52, 58, 72),
        'x': (239, 68, 68),        # Vibrant Red
        'o': (59, 130, 246),       # Vibrant Blue
        'win': (34, 197, 94),      # Emerald Green
        'text': (241, 245, 249),
        'hint': (148, 163, 184),
        'btn_bg': (33, 38, 50),
        'btn_border': (74, 85, 104),
        'btn_text': (226, 232, 240),
        'btn_label': "Light Mode",
        'clock_accent': (59, 130, 246),
    },
    'light': {
        'name': 'Light',
        'bg': (248, 250, 252),     # Clean Soft White
        'panel': (238, 242, 246),  # Soft Slate Panel
        'grid': (203, 213, 225),   # Slate Grid Lines
        'x': (220, 38, 38),        # Deep Crimson Red
        'o': (37, 99, 235),        # Deep Royal Blue
        'win': (22, 163, 74),      # Green
        'text': (15, 23, 42),      # Dark Slate Text
        'hint': (100, 116, 139),   # Muted Hint Text
        'btn_bg': (255, 255, 255),
        'btn_border': (203, 213, 225),
        'btn_text': (30, 41, 59),
        'btn_label': "Dark Mode",
        'clock_accent': (37, 99, 235),
    }
}

# Setup Display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()

# Fonts
font_title = pygame.font.SysFont("segoeui", 28, bold=True)
font_sub = pygame.font.SysFont("segoeui", 16)
font_btn = pygame.font.SysFont("segoeui", 15, bold=True)
font_clock_val = pygame.font.SysFont("consolas", 20, bold=True)
font_clock_lbl = pygame.font.SysFont("segoeui", 13, bold=True)

# Theme Toggle Button Bounds in Bottom Panel
theme_btn_rect = pygame.Rect(WIDTH - 135, OFFSET_Y + BOARD_SIZE + 24, 120, 42)


class TicTacToe:
    def __init__(self):
        self.theme_mode = 'dark'
        self.reset()

    @property
    def colors(self):
        return THEMES[self.theme_mode]

    def toggle_theme(self):
        self.theme_mode = 'light' if self.theme_mode == 'dark' else 'dark'

    def reset(self):
        self.board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.player = 'X'
        self.game_over = False
        self.winner = None
        self.winning_line = None  # ((x1, y1), (x2, y2))
        
        # Clock & Timer State
        self.timer_started = False
        self.start_ticks = 0
        self.elapsed_ms = 0

    def make_move(self, row, col):
        if self.board[row][col] is None and not self.game_over:
            # Start match clock on first move
            if not self.timer_started:
                self.timer_started = True
                self.start_ticks = pygame.time.get_ticks()

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

    def update_timer(self):
        if self.timer_started and not self.game_over:
            self.elapsed_ms = pygame.time.get_ticks() - self.start_ticks

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
                y = OFFSET_Y + r * CELL_SIZE + CELL_SIZE // 2
                self.winning_line = ((20, y), (BOARD_SIZE - 20, y))
                return True

        # Columns
        for c in range(GRID_SIZE):
            if self.board[0][c] == self.board[1][c] == self.board[2][c] == p:
                x = c * CELL_SIZE + CELL_SIZE // 2
                self.winning_line = ((x, OFFSET_Y + 20), (x, OFFSET_Y + BOARD_SIZE - 20))
                return True

        # Diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == p:
            self.winning_line = (
                (25, OFFSET_Y + 25),
                (BOARD_SIZE - 25, OFFSET_Y + BOARD_SIZE - 25)
            )
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] == p:
            self.winning_line = (
                (BOARD_SIZE - 25, OFFSET_Y + 25),
                (25, OFFSET_Y + BOARD_SIZE - 25)
            )
            return True

        return False

    def draw_top_bar(self):
        colors = self.colors
        # Background & divider
        pygame.draw.rect(screen, colors['panel'], (0, 0, WIDTH, TOP_BAR_HEIGHT))
        pygame.draw.line(screen, colors['grid'], (0, TOP_BAR_HEIGHT), (WIDTH, TOP_BAR_HEIGHT), 2)

        # 1. Match Timer (Left)
        total_seconds = int(self.elapsed_ms // 1000)
        mins = total_seconds // 60
        secs = total_seconds % 60
        timer_text = f"{mins:02d}:{secs:02d}"

        # Animated stopwatch icon
        cx, cy, r = 26, TOP_BAR_HEIGHT // 2, 11
        pygame.draw.circle(screen, colors['clock_accent'], (cx, cy), r, 2)
        pygame.draw.circle(screen, colors['clock_accent'], (cx, cy), 2)
        pygame.draw.line(screen, colors['clock_accent'], (cx - 3, cy - r - 2), (cx + 3, cy - r - 2), 2)
        pygame.draw.line(screen, colors['clock_accent'], (cx, cy - r), (cx, cy - r - 2), 2)

        # Rotating second hand based on elapsed time
        hand_angle = math.radians(-90 + (secs * 6))
        hx = cx + int((r - 3) * math.cos(hand_angle))
        hy = cy + int((r - 3) * math.sin(hand_angle))
        pygame.draw.line(screen, colors['clock_accent'], (cx, cy), (hx, hy), 2)

        lbl_timer = font_clock_lbl.render("MATCH", True, colors['hint'])
        val_timer = font_clock_val.render(timer_text, True, colors['text'])
        screen.blit(lbl_timer, (45, 12))
        screen.blit(val_timer, (45, 28))

        # 2. Header Title (Center)
        title_surf = font_title.render("TIC TAC TOE", True, colors['text'])
        screen.blit(title_surf, (WIDTH // 2 - title_surf.get_width() // 2, 13))

        # 3. Live System Clock (Right)
        now_str = datetime.datetime.now().strftime("%I:%M:%S %p")
        lbl_clock = font_clock_lbl.render("SYSTEM CLOCK", True, colors['hint'])
        val_clock = font_clock_val.render(now_str, True, colors['text'])
        screen.blit(lbl_clock, (WIDTH - val_clock.get_width() - 20, 12))
        screen.blit(val_clock, (WIDTH - val_clock.get_width() - 20, 28))

    def draw_grid(self):
        colors = self.colors
        # Horizontal lines
        for i in range(1, GRID_SIZE):
            y = OFFSET_Y + i * CELL_SIZE
            pygame.draw.line(screen, colors['grid'], (0, y), (BOARD_SIZE, y), LINE_WIDTH)

        # Vertical lines
        for i in range(1, GRID_SIZE):
            x = i * CELL_SIZE
            pygame.draw.line(screen, colors['grid'], (x, OFFSET_Y), (x, OFFSET_Y + BOARD_SIZE), LINE_WIDTH)

    def draw_marks(self):
        colors = self.colors
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                mark = self.board[row][col]
                center_x = col * CELL_SIZE + CELL_SIZE // 2
                center_y = OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2

                if mark == 'O':
                    pygame.draw.circle(
                        screen, colors['o'],
                        (center_x, center_y),
                        RADIUS, MARK_WIDTH
                    )
                elif mark == 'X':
                    start_asc = (col * CELL_SIZE + SPACE, OFFSET_Y + row * CELL_SIZE + CELL_SIZE - SPACE)
                    end_asc = (col * CELL_SIZE + CELL_SIZE - SPACE, OFFSET_Y + row * CELL_SIZE + SPACE)
                    pygame.draw.line(screen, colors['x'], start_asc, end_asc, MARK_WIDTH)

                    start_desc = (col * CELL_SIZE + SPACE, OFFSET_Y + row * CELL_SIZE + SPACE)
                    end_desc = (col * CELL_SIZE + CELL_SIZE - SPACE, OFFSET_Y + row * CELL_SIZE + CELL_SIZE - SPACE)
                    pygame.draw.line(screen, colors['x'], start_desc, end_desc, MARK_WIDTH)

    def draw_winning_line(self):
        if self.winning_line:
            start_pos, end_pos = self.winning_line
            pygame.draw.line(screen, self.colors['win'], start_pos, end_pos, LINE_WIDTH + 4)

    def draw_theme_button(self):
        colors = self.colors
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = theme_btn_rect.collidepoint(mouse_pos)

        border_color = colors['text'] if is_hovered else colors['btn_border']
        border_thickness = 3 if is_hovered else 2

        pygame.draw.rect(screen, colors['btn_bg'], theme_btn_rect, border_radius=8)
        pygame.draw.rect(screen, border_color, theme_btn_rect, width=border_thickness, border_radius=8)

        btn_text = font_btn.render(colors['btn_label'], True, colors['btn_text'])
        screen.blit(
            btn_text,
            (theme_btn_rect.centerx - btn_text.get_width() // 2,
             theme_btn_rect.centery - btn_text.get_height() // 2)
        )

    def draw_bottom_panel(self):
        colors = self.colors
        panel_y = OFFSET_Y + BOARD_SIZE
        panel_rect = pygame.Rect(0, panel_y, WIDTH, BOTTOM_PANEL_HEIGHT)
        pygame.draw.rect(screen, colors['panel'], panel_rect)
        pygame.draw.line(screen, colors['grid'], (0, panel_y), (WIDTH, panel_y), 2)

        # Center info area to the left of the button
        content_center_x = (WIDTH - 145) // 2

        if not self.game_over:
            turn_color = colors['x'] if self.player == 'X' else colors['o']
            status_text = f"Player {self.player}'s Turn"
            text_surface = font_title.render(status_text, True, turn_color)
            sub_surface = font_sub.render("Click cell to play  •  [T] Theme  •  [R] Reset", True, colors['hint'])
        else:
            if self.winner == "Draw":
                text_surface = font_title.render("Game Over: Draw!", True, colors['hint'])
            else:
                win_color = colors['x'] if self.winner == 'X' else colors['o']
                text_surface = font_title.render(f"Player {self.winner} Wins!", True, win_color)
            sub_surface = font_sub.render("Press 'R' to Play Again  •  'ESC' to Quit", True, colors['win'])

        screen.blit(text_surface, (content_center_x - text_surface.get_width() // 2, panel_y + 14))
        screen.blit(sub_surface, (content_center_x - sub_surface.get_width() // 2, panel_y + 54))

        self.draw_theme_button()

    def render(self):
        self.update_timer()
        screen.fill(self.colors['bg'])
        self.draw_top_bar()
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
                elif event.key == pygame.K_t:
                    game.toggle_theme()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                if theme_btn_rect.collidepoint(mouse_x, mouse_y):
                    game.toggle_theme()
                elif OFFSET_Y <= mouse_y < OFFSET_Y + BOARD_SIZE and not game.game_over:
                    clicked_row = (mouse_y - OFFSET_Y) // CELL_SIZE
                    clicked_col = mouse_x // CELL_SIZE
                    game.make_move(clicked_row, clicked_col)

        game.render()
        clock.tick(60)


if __name__ == "__main__":
    main()
