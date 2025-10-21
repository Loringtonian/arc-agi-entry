#!/usr/bin/env python3
"""
ARC Game Template - Copy this for all new games
Self-contained, guaranteed to launch template
"""

import sys
import os
from typing import List, Tuple, Optional, Dict
from enum import Enum

# Auto-detect and use virtual environment for pygame
try:
    import pygame
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Check if we're in draft_games subfolder
    if os.path.basename(script_dir) == "draft_games":
        parent_dir = os.path.dirname(script_dir)
    else:
        parent_dir = script_dir
    
    venv_python = os.path.join(parent_dir, "game_engine_env", "bin", "python")
    
    if os.path.exists(venv_python):
        os.execv(venv_python, [venv_python, __file__] + sys.argv[1:])
    else:
        print(f"Error: pygame not found and virtual environment not available at {venv_python}")
        sys.exit(1)

# ARC color palette (hardcoded - NEVER CHANGE)
ARC_COLORS = {
    0: (0, 0, 0),        # Black
    1: (0, 116, 217),    # Blue  
    2: (255, 65, 54),    # Red
    3: (46, 204, 64),    # Green
    4: (255, 220, 0),    # Yellow
    5: (170, 170, 170),  # Gray
    6: (240, 18, 190),   # Magenta
    7: (255, 133, 27),   # Orange
    8: (127, 219, 255),  # Sky Blue
    9: (135, 12, 37)     # Maroon
}

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class GameTemplate:
    """Template for ARC-compliant games."""
    def __init__(self):
        pygame.init()
        
        # Standard game settings - MUST BE SQUARE GRID
        self.grid_size = 12  # MUST be square: 8×8 to 64×64 (change this value)
        self.cell_size = 40  # Adjust based on grid_size for good visibility
        
        # Screen setup
        self.screen_width = self.grid_size * self.cell_size
        self.screen_height = self.grid_size * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("ARC Game")  # Change this
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 10  # Slower for deliberate movement
        
        # Grid (change as needed)
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Player position
        self.player_x = 1
        self.player_y = 1
        
        # Game state
        self.won = False
        self.lost = False
        self.flash_timer = 0
        self.flash_duration = 1000  # ms
        
        self.setup_level()
    
    def setup_level(self):
        """Setup the game level."""
        # Clear grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.grid[y][x] = 0
        
        # Add borders
        for x in range(self.grid_size):
            self.grid[0][x] = 1  # Top wall
            self.grid[self.grid_size-1][x] = 1  # Bottom wall
        for y in range(self.grid_size):
            self.grid[y][0] = 1  # Left wall
            self.grid[y][self.grid_size-1] = 1  # Right wall
        
        # TODO: Add your game-specific setup here
        
        # Reset player
        self.player_x = 1
        self.player_y = 1
        
        # Reset game state
        self.won = False
        self.lost = False
        self.flash_timer = 0
    
    def is_valid_pos(self, x: int, y: int) -> bool:
        """Check if position is within grid bounds."""
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size
    
    def can_move_to(self, x: int, y: int) -> bool:
        """Check if position is valid and not blocked."""
        if not self.is_valid_pos(x, y):
            return False
        return self.grid[y][x] != 1  # Not a wall
    
    def move_player(self, direction: Direction):
        """Move player in given direction."""
        if self.won or self.lost:
            return
        
        dx, dy = direction.value
        new_x = self.player_x + dx
        new_y = self.player_y + dy
        
        if self.can_move_to(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y
            
            # TODO: Add your game logic here
            self.check_game_state()
    
    def check_game_state(self):
        """Check for win/loss conditions."""
        # MANDATORY: Every game MUST have clear win and loss conditions
        # When win/loss occurs, set self.won = True or self.lost = True
        # and set self.flash_timer = pygame.time.get_ticks()
        
        # TODO: Replace these examples with your actual win/loss conditions
        
        # Example win condition
        if self.player_x == self.grid_size - 2 and self.player_y == self.grid_size - 2:
            self.won = True
            self.flash_timer = pygame.time.get_ticks()
        
        # Example loss condition
        if self.grid[self.player_y][self.player_x] == 2:  # Red cell
            self.lost = True
            self.flash_timer = pygame.time.get_ticks()
    
    def reset_game(self):
        """Reset the game."""
        self.setup_level()
    
    def update(self, dt: float):
        """Update game state."""
        current_time = pygame.time.get_ticks()
        
        # Handle win/loss timing
        if (self.won or self.lost) and self.flash_timer > 0:
            if current_time - self.flash_timer > self.flash_duration:
                self.reset_game()
        
        # TODO: Add your update logic here
    
    def draw(self):
        """Draw the game."""
        self.screen.fill(ARC_COLORS[0])  # Black background
        
        # Draw grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                 self.cell_size, self.cell_size)
                
                cell_value = self.grid[y][x]
                if cell_value > 0:
                    pygame.draw.rect(self.screen, ARC_COLORS[cell_value], rect)
                
                # Grid lines
                pygame.draw.rect(self.screen, ARC_COLORS[5], rect, 1)
        
        # Draw player
        player_rect = pygame.Rect(self.player_x * self.cell_size + 2, 
                                self.player_y * self.cell_size + 2,
                                self.cell_size - 4, self.cell_size - 4)
        pygame.draw.rect(self.screen, ARC_COLORS[3], player_rect)  # Green player
        pygame.draw.rect(self.screen, (255, 255, 255), player_rect, 2)
        
        # NO TEXT - pure visual experience
        
        # Win/Loss effects - MANDATORY: User must be informed when they win or lose
        # GREEN FLASH = WIN, RED FLASH = LOSE (DO NOT CHANGE THESE COLORS)
        current_time = pygame.time.get_ticks()
        if self.won and self.flash_timer > 0:
            elapsed = current_time - self.flash_timer
            if elapsed < self.flash_duration:
                alpha = int(80 * (1 - elapsed / self.flash_duration))
                overlay = pygame.Surface((self.screen_width, self.screen_height))
                overlay.set_alpha(alpha)
                overlay.fill(ARC_COLORS[3])  # Green flash for WIN
                self.screen.blit(overlay, (0, 0))
        
        elif self.lost and self.flash_timer > 0:
            elapsed = current_time - self.flash_timer
            if elapsed < self.flash_duration:
                alpha = int(80 * (1 - elapsed / self.flash_duration))
                overlay = pygame.Surface((self.screen_width, self.screen_height))
                overlay.set_alpha(alpha)
                overlay.fill(ARC_COLORS[2])  # Red flash for LOSE
                self.screen.blit(overlay, (0, 0))
    
    def handle_events(self):
        """Handle input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.reset_game()
                
                # Movement - WASD or arrows only
                elif event.key in [pygame.K_w, pygame.K_UP]:
                    self.move_player(Direction.UP)
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.move_player(Direction.DOWN)
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.move_player(Direction.LEFT)
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.move_player(Direction.RIGHT)
    
    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(self.fps)
            
            self.handle_events()
            self.update(dt)
            self.draw()
            
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    game = GameTemplate()
    game.run()