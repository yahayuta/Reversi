import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
BOARD_SIZE = 8
CELL_SIZE = 40
BOARD_START_X = 50
BOARD_START_Y = 50
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 500

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
DARK_GREEN = (0, 64, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Game states
ID_STONE_NONE = 0
ID_STONE_BLACK = 1
ID_STONE_WHITE = 2

GAME_TURN_WHITE = 1
GAME_TURN_BLACK = 0

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Reversi")
font = pygame.font.Font(None, 24)

class ReversiEngine:
    def __init__(self):
        self.board = [[ID_STONE_NONE for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.init_board()
    
    def init_board(self):
        """Initialize the board with starting stones"""
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.board[i][j] = ID_STONE_NONE
        
        # Set up initial stones
        self.board[3][3] = ID_STONE_WHITE
        self.board[3][4] = ID_STONE_BLACK
        self.board[4][3] = ID_STONE_BLACK
        self.board[4][4] = ID_STONE_WHITE
    
    def get_stone(self, x, y):
        """Get stone at position (x, y)"""
        if 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE:
            return self.board[x][y]
        return ID_STONE_NONE
    
    def check_position(self, x, y, my_color, with_reverse=False):
        """Check if a position is valid for placing a stone"""
        if self.get_stone(x, y) != ID_STONE_NONE:
            return 0
        
        target_color = ID_STONE_WHITE if my_color == ID_STONE_BLACK else ID_STONE_BLACK
        around_number = 0
        
        # Check all 8 directions
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                
                around_x = x + dx
                around_y = y + dy
                
                if (0 <= around_x < BOARD_SIZE and 
                    0 <= around_y < BOARD_SIZE and
                    self.get_stone(around_x, around_y) == target_color):
                    
                    # Follow the line
                    lined_x = around_x
                    lined_y = around_y
                    while (0 <= lined_x < BOARD_SIZE and 
                           0 <= lined_y < BOARD_SIZE and
                           self.get_stone(lined_x, lined_y) == target_color):
                        lined_x += dx
                        lined_y += dy
                    
                    # Check if we can close the line
                    if (0 <= lined_x < BOARD_SIZE and 
                        0 <= lined_y < BOARD_SIZE and
                        self.get_stone(lined_x, lined_y) == my_color):
                        
                        if with_reverse:
                            # Reverse the stones
                            reverse_x = around_x
                            reverse_y = around_y
                            while self.get_stone(reverse_x, reverse_y) == target_color:
                                self.board[reverse_x][reverse_y] = my_color
                                reverse_x += dx
                                reverse_y += dy
                            self.board[x][y] = my_color
                        
                        around_number += 1
        
        return around_number
    
    def game_status_check(self, next_color):
        """Check the current game status"""
        black_status = white_status = 0
        
        # Count valid moves for both colors
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                black_status += self.check_position(i, j, ID_STONE_BLACK, False)
                white_status += self.check_position(i, j, ID_STONE_WHITE, False)
        
        if black_status + white_status == 0:
            return "END"
        elif next_color == ID_STONE_BLACK and black_status == 0:
            return "BLACK_PASS"
        elif next_color == ID_STONE_WHITE and white_status == 0:
            return "WHITE_PASS"
        
        return "NORMAL"
    
    def count_score(self):
        """Count the score for both players"""
        black_score = white_score = 0
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                if self.board[i][j] == ID_STONE_BLACK:
                    black_score += 1
                elif self.board[i][j] == ID_STONE_WHITE:
                    white_score += 1
        return black_score, white_score
    
    def ai_move(self, com_color):
        """Simple AI move - just find first valid position"""
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                if self.check_position(i, j, com_color, True):
                    return True
        return False

class ReversiGame:
    def __init__(self):
        self.engine = ReversiEngine()
        self.game_turn = GAME_TURN_WHITE
        self.cursor_x = BOARD_SIZE // 2
        self.cursor_y = BOARD_SIZE // 2
        self.message = "White's turn"
        
    def draw_board(self):
        """Draw the game board"""
        screen.fill(BROWN)
        
        # Draw board background
        board_rect = pygame.Rect(BOARD_START_X, BOARD_START_Y, 
                               BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE)
        pygame.draw.rect(screen, GREEN, board_rect)
        
        # Draw grid lines
        for i in range(BOARD_SIZE + 1):
            x = BOARD_START_X + i * CELL_SIZE
            y = BOARD_START_Y + i * CELL_SIZE
            pygame.draw.line(screen, BLACK, 
                           (x, BOARD_START_Y), 
                           (x, BOARD_START_Y + BOARD_SIZE * CELL_SIZE))
            pygame.draw.line(screen, BLACK, 
                           (BOARD_START_X, y), 
                           (BOARD_START_X + BOARD_SIZE * CELL_SIZE, y))
    
    def draw_stones(self):
        """Draw all stones on the board"""
        for j in range(BOARD_SIZE):
            for i in range(BOARD_SIZE):
                self.draw_stone(i, j)
    
    def draw_stone(self, x, y):
        """Draw a single stone at position (x, y)"""
        pos_x = BOARD_START_X + x * CELL_SIZE + CELL_SIZE // 2
        pos_y = BOARD_START_Y + y * CELL_SIZE + CELL_SIZE // 2
        
        stone = self.engine.get_stone(x, y)
        if stone == ID_STONE_BLACK:
            pygame.draw.circle(screen, BLACK, (pos_x, pos_y), CELL_SIZE // 2 - 2)
        elif stone == ID_STONE_WHITE:
            pygame.draw.circle(screen, WHITE, (pos_x, pos_y), CELL_SIZE // 2 - 2)
    
    def draw_cursor(self, x, y):
        """Draw the cursor at position (x, y)"""
        pos_x = BOARD_START_X + x * CELL_SIZE
        pos_y = BOARD_START_Y + y * CELL_SIZE
        
        cursor_rect = pygame.Rect(pos_x, pos_y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, cursor_rect, 3)
    
    def draw_info(self):
        """Draw game information"""
        black_score, white_score = self.engine.count_score()
        
        # Scores
        black_text = f"Black: {black_score}"
        white_text = f"White: {white_score}"
        
        black_surface = font.render(black_text, True, BLACK)
        white_surface = font.render(white_text, True, BLACK)
        
        screen.blit(black_surface, (20, 20))
        screen.blit(white_surface, (20, 50))
        
        # Message
        message_surface = font.render(self.message, True, BLACK)
        screen.blit(message_surface, (20, SCREEN_HEIGHT - 40))
    
    def run(self):
        """Main game loop"""
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.cursor_y > 0:
                        self.cursor_y -= 1
                    elif event.key == pygame.K_DOWN and self.cursor_y < BOARD_SIZE - 1:
                        self.cursor_y += 1
                    elif event.key == pygame.K_LEFT and self.cursor_x > 0:
                        self.cursor_x -= 1
                    elif event.key == pygame.K_RIGHT and self.cursor_x < BOARD_SIZE - 1:
                        self.cursor_x += 1
                    elif event.key == pygame.K_RETURN:
                        # Try to place stone
                        current_color = ID_STONE_BLACK if self.game_turn == GAME_TURN_BLACK else ID_STONE_WHITE
                        if self.engine.check_position(self.cursor_x, self.cursor_y, current_color, True):
                            self.game_turn = not self.game_turn
                            self.check_game_status()
            
            # AI turn
            if self.game_turn == GAME_TURN_BLACK:  # AI plays black
                self.message = "AI thinking..."
                pygame.display.flip()
                pygame.time.wait(500)
                
                if self.engine.ai_move(ID_STONE_BLACK):
                    self.game_turn = GAME_TURN_WHITE
                    self.check_game_status()
            
            # Draw everything
            self.draw_board()
            self.draw_stones()
            self.draw_cursor(self.cursor_x, self.cursor_y)
            self.draw_info()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()
        sys.exit()
    
    def check_game_status(self):
        """Check and handle game status changes"""
        current_color = ID_STONE_BLACK if self.game_turn == GAME_TURN_BLACK else ID_STONE_WHITE
        game_status = self.engine.game_status_check(current_color)
        
        if game_status == "END":
            self.show_game_end()
        elif game_status == "BLACK_PASS":
            self.message = "Black passes"
        elif game_status == "WHITE_PASS":
            self.message = "White passes"
        else:
            turn_name = "Black" if self.game_turn == GAME_TURN_BLACK else "White"
            self.message = f"{turn_name}'s turn"
    
    def show_game_end(self):
        """Show game end screen"""
        black_score, white_score = self.engine.count_score()
        
        if black_score > white_score:
            self.message = f"Black wins! ({black_score}-{white_score})"
        elif white_score > black_score:
            self.message = f"White wins! ({white_score}-{black_score})"
        else:
            self.message = f"Draw! ({black_score}-{white_score})"

if __name__ == "__main__":
    game = ReversiGame()
    game.run() 