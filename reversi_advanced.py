import pygame
import sys
import random
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants from ReversiConstants.h (scaled for larger screen)
BOARD_START_POSITION_X = 50
BOARD_START_POSITION_Y = 50
BOARD_GRID_SIZE = 60
BOARD_GRID_NUMBER = 8
BOARD_GRID_LENGTH = BOARD_GRID_SIZE * BOARD_GRID_NUMBER
BOARD_GRID_LINE_WIDTH = 2

BOARD_COLOR = (0, 32, 0)  # Dark green
BOARD_GRID_LINE_COLOR = (0, 0, 0)  # Black

STONE_SIZE_XY = 50

SUB_TITLE_PANE_SIZE_X = 200
SUB_TITLE_PANE_SIZE_Y = 100

CURSOR_SIZE_XY = 50
CURSOR_FIXED_OFFSET = 5

STONE_BLACK = 1
STONE_WHITE = 0

BG_COLOR = (99, 24, 24)  # Brown background

# Game constants from ReversiEngine.h
ID_STONE_NONE = 0
ID_STONE_BLACK = 1
ID_STONE_WHITE = 2

GAME_STATUS_NORMAL = 0
GAME_STATUS_END = 1
GAME_STATUS_BLACK_PASS = 2
GAME_STATUS_WHITE_PASS = 3
GAME_STATUS_BLACK_PUT = 4
GAME_STATUS_WHITE_PUT = 5

GAME_TURN_WHITE = 1
GAME_TURN_BLACK = 0

# View states
class ViewStatus(Enum):
    KViewOpening = 0
    KViewColorSelect = 1
    KViewLevelSelect = 2
    KViewGame = 3
    KViewGameEnd = 4

# Screen setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Reversi")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
DARK_GREEN = (0, 64, 0)
BROWN = (139, 69, 19)
LIGHT_BROWN = (160, 82, 45)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)

class Evaluation:
    def __init__(self, x=0, y=0, score=0):
        self.x = x
        self.y = y
        self.score = score

class ReversiEngine:
    def __init__(self):
        self.board = [[ID_STONE_NONE for _ in range(BOARD_GRID_NUMBER)] for _ in range(BOARD_GRID_NUMBER)]
        self.game_status_changed = False
        
    def init_base_info(self):
        """Initialize the board with starting stones"""
        for j in range(BOARD_GRID_NUMBER):
            for i in range(BOARD_GRID_NUMBER):
                self.board[i][j] = ID_STONE_NONE
        
        # Set up initial stones
        self.board[3][3] = ID_STONE_WHITE
        self.board[3][4] = ID_STONE_BLACK
        self.board[4][3] = ID_STONE_BLACK
        self.board[4][4] = ID_STONE_WHITE
    
    def get_stone(self, x, y):
        """Get stone at position (x, y)"""
        if 0 <= x < BOARD_GRID_NUMBER and 0 <= y < BOARD_GRID_NUMBER:
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
                
                if (0 <= around_x < BOARD_GRID_NUMBER and 
                    0 <= around_y < BOARD_GRID_NUMBER and
                    self.get_stone(around_x, around_y) == target_color):
                    
                    # Follow the line
                    lined_x = around_x
                    lined_y = around_y
                    while (0 <= lined_x < BOARD_GRID_NUMBER and 
                           0 <= lined_y < BOARD_GRID_NUMBER and
                           self.get_stone(lined_x, lined_y) == target_color):
                        lined_x += dx
                        lined_y += dy
                    
                    # Check if we can close the line
                    if (0 <= lined_x < BOARD_GRID_NUMBER and 
                        0 <= lined_y < BOARD_GRID_NUMBER and
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
        for j in range(BOARD_GRID_NUMBER):
            for i in range(BOARD_GRID_NUMBER):
                black_status += self.check_position(i, j, ID_STONE_BLACK, False)
                white_status += self.check_position(i, j, ID_STONE_WHITE, False)
        
        if black_status + white_status == 0:
            return GAME_STATUS_END
        elif next_color == ID_STONE_BLACK and black_status == 0:
            return GAME_STATUS_BLACK_PASS
        elif next_color == ID_STONE_WHITE and white_status == 0:
            return GAME_STATUS_WHITE_PASS
        
        return GAME_STATUS_NORMAL
    
    def count_score(self):
        """Count the score for both players"""
        black_score = white_score = 0
        for j in range(BOARD_GRID_NUMBER):
            for i in range(BOARD_GRID_NUMBER):
                if self.board[i][j] == ID_STONE_BLACK:
                    black_score += 1
                elif self.board[i][j] == ID_STONE_WHITE:
                    white_score += 1
        return black_score, white_score
    
    def copy_board(self, new_board, org_board):
        """Copy board state"""
        for j in range(BOARD_GRID_NUMBER):
            for i in range(BOARD_GRID_NUMBER):
                new_board[i][j] = org_board[i][j]
    
    def piece_count(self, brd, com_color):
        """Count pieces for a specific color"""
        count = 0
        for j in range(BOARD_GRID_NUMBER):
            for i in range(BOARD_GRID_NUMBER):
                if brd[i][j] == com_color:
                    count += 1
        return count
    
    def corner_evaluate(self, board, put_color):
        """Evaluate corner positions"""
        corners = [(0, 0), (0, 7), (7, 0), (7, 7)]
        score = 0
        for x, y in corners:
            if board[x][y] == put_color:
                score += 25
        return score
    
    def get_evaluate(self, brd, com_color):
        """Get board evaluation"""
        eva = Evaluation()
        eva.score = self.piece_count(brd, com_color)
        eva.score += self.corner_evaluate(brd, com_color)
        return eva
    
    def read_next_move(self, brd, read_moves, com_color, put_color):
        """Read next move using minimax algorithm"""
        best = Evaluation(0, 0, -1000)
        worst = Evaluation(0, 0, 1000)
        
        if read_moves == 0:
            # Find first valid move
            for j in range(BOARD_GRID_NUMBER):
                for i in range(BOARD_GRID_NUMBER):
                    if self.check_position(i, j, put_color, False) > 0:
                        return Evaluation(i, j, 0)
            return Evaluation(0, 0, 0)
        
        # Minimax search
        for j in range(BOARD_GRID_NUMBER):
            for i in range(BOARD_GRID_NUMBER):
                if self.check_position(i, j, put_color, False) > 0:
                    # Make a copy of the board
                    temp_board = [[0 for _ in range(BOARD_GRID_NUMBER)] for _ in range(BOARD_GRID_NUMBER)]
                    self.copy_board(temp_board, brd)
                    
                    # Make the move
                    self.check_position(i, j, put_color, True)
                    
                    # Recursive evaluation
                    next_color = ID_STONE_WHITE if put_color == ID_STONE_BLACK else ID_STONE_BLACK
                    eva = self.read_next_move(brd, read_moves - 1, com_color, next_color)
                    
                    # Restore board
                    self.copy_board(brd, temp_board)
                    
                    # Update best/worst
                    if put_color == com_color:
                        if eva.score > best.score:
                            best = Evaluation(i, j, eva.score)
                    else:
                        if eva.score < worst.score:
                            worst = Evaluation(i, j, eva.score)
        
        if put_color == com_color:
            return best
        else:
            return worst
    
    def ai_move(self, com_color, com_level):
        """AI move with different difficulty levels"""
        if com_level == 0:  # Easy - random valid move
            valid_moves = []
            for j in range(BOARD_GRID_NUMBER):
                for i in range(BOARD_GRID_NUMBER):
                    if self.check_position(i, j, com_color, False) > 0:
                        valid_moves.append((i, j))
            
            if valid_moves:
                x, y = random.choice(valid_moves)
                self.check_position(x, y, com_color, True)
                return True
        else:
            # Use minimax for harder levels
            eva = self.read_next_move(self.board, com_level * 2, com_color, com_color)
            if eva.score > -1000:
                self.check_position(eva.x, eva.y, com_color, True)
                return True
        
        return False

class ReversiGame:
    def __init__(self):
        self.engine = ReversiEngine()
        self.view_number = ViewStatus.KViewOpening
        self.my_color = 0  # 0 = Black, 1 = White
        self.game_level = 1  # 0 = Hard, 1 = Medium, 2 = Easy
        self.cursor_x = BOARD_GRID_NUMBER // 2 + 1
        self.cursor_y = BOARD_GRID_NUMBER // 2 + 1
        self.game_turn = GAME_TURN_WHITE
        self.my_stone_color = ID_STONE_BLACK
        self.com_stone_color = ID_STONE_WHITE
        
    def draw_board(self):
        """Draw the game board"""
        # Draw background
        screen.fill(BG_COLOR)
        
        # Draw board background
        board_rect = pygame.Rect(BOARD_START_POSITION_X, BOARD_START_POSITION_Y, 
                               BOARD_GRID_LENGTH, BOARD_GRID_LENGTH)
        pygame.draw.rect(screen, BOARD_COLOR, board_rect)
        
        # Draw grid lines
        for i in range(BOARD_GRID_NUMBER + 1):
            x = BOARD_START_POSITION_X + i * BOARD_GRID_SIZE
            y = BOARD_START_POSITION_Y + i * BOARD_GRID_SIZE
            pygame.draw.line(screen, BOARD_GRID_LINE_COLOR, 
                           (x, BOARD_START_POSITION_Y), 
                           (x, BOARD_START_POSITION_Y + BOARD_GRID_LENGTH))
            pygame.draw.line(screen, BOARD_GRID_LINE_COLOR, 
                           (BOARD_START_POSITION_X, y), 
                           (BOARD_START_POSITION_X + BOARD_GRID_LENGTH, y))
    
    def draw_stones(self):
        """Draw all stones on the board"""
        for j in range(BOARD_GRID_NUMBER):
            for i in range(BOARD_GRID_NUMBER):
                self.draw_stone(i, j)
    
    def draw_stone(self, x, y):
        """Draw a single stone at position (x, y)"""
        if y >= BOARD_GRID_NUMBER:
            return
        
        pos_x = x * BOARD_GRID_SIZE + BOARD_START_POSITION_X
        pos_y = y * BOARD_GRID_SIZE + BOARD_START_POSITION_Y
        
        stone = self.engine.get_stone(x, y)
        if stone == ID_STONE_BLACK:
            pygame.draw.circle(screen, BLACK, 
                             (pos_x + BOARD_GRID_SIZE // 2, pos_y + BOARD_GRID_SIZE // 2), 
                             STONE_SIZE_XY // 2)
        elif stone == ID_STONE_WHITE:
            pygame.draw.circle(screen, WHITE, 
                             (pos_x + BOARD_GRID_SIZE // 2, pos_y + BOARD_GRID_SIZE // 2), 
                             STONE_SIZE_XY // 2)
    
    def draw_cursor(self, x, y, is_player_turn):
        """Draw the cursor at position (x, y)"""
        pos_x = x * BOARD_GRID_SIZE + BOARD_START_POSITION_X
        pos_y = y * BOARD_GRID_SIZE + BOARD_START_POSITION_Y + CURSOR_FIXED_OFFSET
        
        if is_player_turn:
            # Draw finger cursor (red rectangle)
            cursor_rect = pygame.Rect(pos_x, pos_y, CURSOR_SIZE_XY, CURSOR_SIZE_XY)
            pygame.draw.rect(screen, RED, cursor_rect, 2)
        else:
            # Draw hourglass cursor (blue rectangle)
            cursor_rect = pygame.Rect(pos_x, pos_y, CURSOR_SIZE_XY, CURSOR_SIZE_XY)
            pygame.draw.rect(screen, BLUE, cursor_rect, 2)
    
    def draw_info(self):
        """Draw game information (level, scores)"""
        black_score, white_score = self.engine.count_score()
        
        # Level info
        level_text = f"LEVEL: {self.game_level + 1}"
        level_surface = font.render(level_text, True, BLACK)
        screen.blit(level_surface, (BOARD_START_POSITION_X + BOARD_GRID_LENGTH + 30, 
                                   BOARD_START_POSITION_Y + 50))
        
        # Black score
        black_text = f"BLACK: {black_score}"
        black_surface = font.render(black_text, True, BLACK)
        screen.blit(black_surface, (BOARD_START_POSITION_X + BOARD_GRID_LENGTH + 30, 
                                   BOARD_START_POSITION_Y + 150))
        
        # White score
        white_text = f"WHITE: {white_score}"
        white_surface = font.render(white_text, True, BLACK)
        screen.blit(white_surface, (BOARD_START_POSITION_X + BOARD_GRID_LENGTH + 30, 
                                   BOARD_START_POSITION_Y + 200))
    
    def draw_message(self, message):
        """Draw a message box"""
        message_rect = pygame.Rect(BOARD_START_POSITION_X + BOARD_GRID_LENGTH + 30, 
                                 BOARD_START_POSITION_Y + 300, 
                                 300, 40)
        pygame.draw.rect(screen, (0, 31, 0), message_rect)
        
        message_surface = small_font.render(message, True, BLACK)
        screen.blit(message_surface, (BOARD_START_POSITION_X + BOARD_GRID_LENGTH + 40, 
                                     BOARD_START_POSITION_Y + 310))
    
    def view_opening(self):
        """Show opening screen"""
        screen.fill(BG_COLOR)
        title_text = "REVERSI"
        title_surface = font.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(title_surface, title_rect)
        
        subtitle_text = "Press SPACE to continue"
        subtitle_surface = small_font.render(subtitle_text, True, WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
        screen.blit(subtitle_surface, subtitle_rect)
        
        pygame.display.flip()
        
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                        self.view_number = ViewStatus.KViewColorSelect
        
        return True
    
    def view_color_select(self):
        """Show color selection screen"""
        waiting = True
        while waiting:
            # Draw the screen
            screen.fill(BG_COLOR)
            
            title_text = "Select Your Color"
            title_surface = font.render(title_text, True, WHITE)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 60))
            screen.blit(title_surface, title_rect)
            
            # Draw color options
            colors = ["BLACK", "WHITE"]
            for i, color in enumerate(colors):
                color_surface = font.render(color, True, WHITE)
                color_rect = color_surface.get_rect(center=(SCREEN_WIDTH // 2, 130 + i * 50))
                screen.blit(color_surface, color_rect)
                
                # Draw selection cursor
                if i == self.my_color:
                    cursor_width = 200
                    cursor_height = 40
                    cursor_x = SCREEN_WIDTH // 2 - cursor_width // 2
                    cursor_y = 110 + i * 50
                    cursor_rect = pygame.Rect(cursor_x, cursor_y, cursor_width, cursor_height)
                    pygame.draw.rect(screen, RED, cursor_rect, 3)
            
            pygame.display.flip()
            
            # Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.my_color > 0:
                        self.my_color -= 1
                    elif event.key == pygame.K_DOWN and self.my_color < 1:
                        self.my_color += 1
                    elif event.key == pygame.K_RETURN:
                        waiting = False
                        self.view_number = ViewStatus.KViewLevelSelect
            
            pygame.time.wait(100)  # Small delay to prevent excessive CPU usage
        
        return True
    
    def view_level_select(self):
        """Show level selection screen"""
        waiting = True
        while waiting:
            # Draw the screen
            screen.fill(BG_COLOR)
            
            title_text = "Select Difficulty"
            title_surface = font.render(title_text, True, WHITE)
            title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 60))
            screen.blit(title_surface, title_rect)
            
            # Draw level options
            levels = ["EASY", "MEDIUM", "HARD"]
            for i, level in enumerate(levels):
                level_surface = font.render(level, True, WHITE)
                level_rect = level_surface.get_rect(center=(SCREEN_WIDTH // 2, 130 + i * 50))
                screen.blit(level_surface, level_rect)
                
                # Draw selection cursor
                if i == self.game_level:
                    cursor_width = 200
                    cursor_height = 40
                    cursor_x = SCREEN_WIDTH // 2 - cursor_width // 2
                    cursor_y = 110 + i * 50
                    cursor_rect = pygame.Rect(cursor_x, cursor_y, cursor_width, cursor_height)
                    pygame.draw.rect(screen, RED, cursor_rect, 3)
            
            pygame.display.flip()
            
            # Handle input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and self.game_level > 0:
                        self.game_level -= 1
                    elif event.key == pygame.K_DOWN and self.game_level < 2:
                        self.game_level += 1
                    elif event.key == pygame.K_LEFT:
                        self.view_number = ViewStatus.KViewColorSelect
                        waiting = False
                    elif event.key == pygame.K_RETURN:
                        waiting = False
                        self.view_number = ViewStatus.KViewGame
            
            pygame.time.wait(100)  # Small delay to prevent excessive CPU usage
        
        return True
    
    def view_game(self):
        """Main game view"""
        # Set up game based on selections
        if self.my_color == 0:  # Black
            self.my_stone_color = ID_STONE_BLACK
            self.com_stone_color = ID_STONE_WHITE
            self.game_turn = GAME_TURN_WHITE
        else:  # White
            self.my_stone_color = ID_STONE_WHITE
            self.com_stone_color = ID_STONE_BLACK
            self.game_turn = GAME_TURN_BLACK
        
        # Initialize board
        self.engine.init_base_info()
        
        # Game loop
        running = True
        while running:
            # Check if it's player's turn
            is_player_turn = ((self.game_turn == GAME_TURN_BLACK and self.my_stone_color == ID_STONE_BLACK) or
                              (self.game_turn == GAME_TURN_WHITE and self.my_stone_color == ID_STONE_WHITE))
            
            if is_player_turn:
                # Check if player has any valid moves
                has_move = False
                for j in range(BOARD_GRID_NUMBER):
                    for i in range(BOARD_GRID_NUMBER):
                        if self.engine.check_position(i, j, self.my_stone_color, False):
                            has_move = True
                            break
                    if has_move:
                        break
                if not has_move:
                    # Show pass message and wait for Enter
                    self.draw_board()
                    self.draw_stones()
                    self.draw_info()
                    self.draw_message("No valid moves! Press Enter to pass.")
                    pygame.display.flip()
                    waiting_pass = True
                    while waiting_pass:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                return False
                            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                                waiting_pass = False
                        pygame.time.wait(100)
                    self.game_turn = not self.game_turn
                    self.check_game_status()
                    continue
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame.KEYDOWN:
                    # Check if it's player's turn
                    is_player_turn = ((self.game_turn == GAME_TURN_BLACK and self.my_stone_color == ID_STONE_BLACK) or
                                     (self.game_turn == GAME_TURN_WHITE and self.my_stone_color == ID_STONE_WHITE))
                    
                    if is_player_turn:  # Player's turn
                        if event.key == pygame.K_UP and self.cursor_y > 0:
                            self.cursor_y -= 1
                        elif event.key == pygame.K_DOWN and self.cursor_y < BOARD_GRID_NUMBER - 1:
                            self.cursor_y += 1
                        elif event.key == pygame.K_LEFT and self.cursor_x > 0:
                            self.cursor_x -= 1
                        elif event.key == pygame.K_RIGHT and self.cursor_x < BOARD_GRID_NUMBER - 1:
                            self.cursor_x += 1
                        elif event.key == pygame.K_RETURN:
                            # Try to place stone
                            if self.engine.check_position(self.cursor_x, self.cursor_y, 
                                                        self.my_stone_color, True):
                                self.game_turn = not self.game_turn
                                self.check_game_status()
            
            # AI turn
            is_ai_turn = ((self.game_turn == GAME_TURN_BLACK and self.com_stone_color == ID_STONE_BLACK) or
                         (self.game_turn == GAME_TURN_WHITE and self.com_stone_color == ID_STONE_WHITE))
            
            if is_ai_turn:
                self.draw_message("Thinking..")
                pygame.display.flip()
                pygame.time.wait(500)  # Small delay for AI thinking
                
                com_level = 2 - self.game_level  # Convert to AI difficulty
                if self.engine.ai_move(self.com_stone_color, com_level):
                    self.game_turn = not self.game_turn
                    self.check_game_status()
                else:
                    # No valid move for AI, check if player can move
                    player_status = self.engine.game_status_check(self.my_stone_color)
                    if player_status in [GAME_STATUS_BLACK_PASS, GAME_STATUS_WHITE_PASS, GAME_STATUS_END]:
                        # Both sides cannot move, end game and exit loop
                        self.check_game_status()
                        running = False
                        continue
                    else:
                        # Pass turn to player
                        self.game_turn = not self.game_turn
            
            # Draw everything
            self.draw_board()
            self.draw_stones()
            self.draw_info()
            # Check if it's player's turn for display
            is_player_turn_display = ((self.game_turn == GAME_TURN_BLACK and self.my_stone_color == ID_STONE_BLACK) or
                                     (self.game_turn == GAME_TURN_WHITE and self.my_stone_color == ID_STONE_WHITE))
            
            if is_player_turn_display:
                self.draw_message("Your Turn.")
                self.draw_cursor(self.cursor_x, self.cursor_y, True)
            else:
                self.draw_cursor(self.cursor_x, self.cursor_y, False)
            
            pygame.display.flip()
            pygame.time.wait(100)
        
        return True
    
    def check_game_status(self):
        """Check and handle game status changes"""
        game_status = self.engine.game_status_check(self.game_turn + 1)
        
        if game_status == GAME_STATUS_END:
            self.show_game_end()
        elif game_status == GAME_STATUS_BLACK_PASS:
            self.show_pass_message("Black Pass")
        elif game_status == GAME_STATUS_WHITE_PASS:
            self.show_pass_message("White Pass")
    
    def show_game_end(self):
        """Show game end screen"""
        black_score, white_score = self.engine.count_score()
        
        # Draw overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Show result
        if black_score > white_score:
            result_text = "Black Win!"
        elif white_score > black_score:
            result_text = "White Win!"
        else:
            result_text = "Draw!"
        
        result_surface = font.render(result_text, True, WHITE)
        result_rect = result_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(result_surface, result_rect)
        
        pygame.display.flip()
        pygame.time.wait(2000)
        
        self.view_number = ViewStatus.KViewOpening
    
    def show_pass_message(self, message):
        """Show pass message"""
        self.draw_message(message)
        pygame.display.flip()
        pygame.time.wait(1000)
    
    def run(self):
        """Main game loop"""
        running = True
        while running:
            if self.view_number == ViewStatus.KViewOpening:
                running = self.view_opening()
            elif self.view_number == ViewStatus.KViewColorSelect:
                running = self.view_color_select()
            elif self.view_number == ViewStatus.KViewLevelSelect:
                running = self.view_level_select()
            elif self.view_number == ViewStatus.KViewGame:
                running = self.view_game()
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = ReversiGame()
    game.run() 