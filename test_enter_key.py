#!/usr/bin/env python3
"""
Test script to verify Enter key functionality in Reversi game
"""

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Enter Key Test")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Font
font = pygame.font.Font(None, 36)

def test_enter_key():
    """Test Enter key functionality"""
    print("Testing Enter key functionality...")
    print("Press Enter to continue, Escape to quit")
    
    current_screen = "menu"
    selection = 0
    options = ["Option 1", "Option 2", "Option 3"]
    
    running = True
    while running:
        screen.fill(BLACK)
        
        if current_screen == "menu":
            # Draw menu
            title = font.render("Enter Key Test", True, WHITE)
            screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))
            
            for i, option in enumerate(options):
                color = RED if i == selection else WHITE
                text = font.render(option, True, color)
                screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, 120 + i * 40))
            
            instruction = font.render("Use Arrow Keys + Enter", True, GREEN)
            screen.blit(instruction, (SCREEN_WIDTH//2 - instruction.get_width()//2, 250))
            
        elif current_screen == "result":
            result = font.render(f"Selected: {options[selection]}", True, WHITE)
            screen.blit(result, (SCREEN_WIDTH//2 - result.get_width()//2, 150))
            
            back = font.render("Press Enter to go back", True, GREEN)
            screen.blit(back, (SCREEN_WIDTH//2 - back.get_width()//2, 200))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                elif current_screen == "menu":
                    if event.key == pygame.K_UP and selection > 0:
                        selection -= 1
                        print(f"Selection: {selection}")
                    elif event.key == pygame.K_DOWN and selection < len(options) - 1:
                        selection += 1
                        print(f"Selection: {selection}")
                    elif event.key == pygame.K_RETURN:
                        print(f"Enter pressed! Selected: {options[selection]}")
                        current_screen = "result"
                
                elif current_screen == "result":
                    if event.key == pygame.K_RETURN:
                        print("Enter pressed! Going back to menu")
                        current_screen = "menu"
        
        pygame.time.wait(100)
    
    pygame.quit()
    print("Test completed!")

if __name__ == "__main__":
    test_enter_key() 