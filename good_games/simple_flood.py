#!/usr/bin/env python3
"""
Simple Color Flood - ARC-AGI-3 v2.0
Simplified variant of Color Flood with minimal UI

ARC-AGI-3 Compliance:
- ✅ 16-color palette (colors 0-15)
- ✅ Square grid (12×12)
- ✅ No text during gameplay
- ✅ Deterministic behavior
- ✅ 7-action framework compatible

Controls:
- LEFT/RIGHT (A/D): Select color
- UP/DOWN/SPACE (W/S): Perform flood fill
- R: Reset/New level
- ESC: Quit
"""

import sys
import os
import pygame
import random
from typing import Set, Tuple
from enum import Enum

# Add tools to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
from arc_agi_editor.editor.utils import ARC_COLORS

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class SimpleFlood:
    """Simple flood fill game."""
    def __init__(self):
        pygame.init()
        
        # Game settings
        self.grid_size = 12
        self.cell_size = 40
        
        # Screen setup
        self.screen_width = self.grid_size * self.cell_size
        self.screen_height = self.grid_size * self.cell_size + 120  # Extra space for UI
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Simple Color Flood - ARC-AGI-3 v2.0")

        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 10

        # Grid state
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        # Using extended 16-color palette for variety
        self.colors_available = [1, 2, 3, 4, 6, 7, 8]  # Blue, Red, Green, Yellow, Magenta, Orange, Sky Blue
        self.current_color = 1
        self.max_moves = 15
        self.moves_used = 0
        
        # Game states
        self.won = False
        self.lost = False
        self.flash_timer = 0
        self.flash_duration = 1000  # ms
        
        self.setup_level()
    
    def setup_level(self):
        """Setup a random level."""
        # Fill grid with random colors
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.grid[y][x] = random.choice(self.colors_available)
        
        # Starting corner is always color 1
        self.grid[0][0] = 1
        self.current_color = 1
        
        # Reset game state
        self.moves_used = 0
        self.won = False
        self.lost = False
        self.flash_timer = 0
    
    def get_flood_fill_cells(self, start_x: int, start_y: int, target_color: int) -> Set[Tuple[int, int]]:
        """Get all cells that would be affected by flood fill."""
        if start_x < 0 or start_x >= self.grid_size or start_y < 0 or start_y >= self.grid_size:
            return set()
        
        original_color = self.grid[start_y][start_x]
        if original_color == target_color:
            return set()
        
        visited = set()
        to_visit = [(start_x, start_y)]
        
        while to_visit:
            x, y = to_visit.pop()
            
            if (x, y) in visited:
                continue
            
            if x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size:
                continue
            
            if self.grid[y][x] != original_color:
                continue
            
            visited.add((x, y))
            
            # Add neighbors
            to_visit.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
        
        return visited
    
    def flood_fill(self, start_x: int, start_y: int, new_color: int):
        """Perform flood fill from starting position."""
        cells_to_change = self.get_flood_fill_cells(start_x, start_y, new_color)
        
        for x, y in cells_to_change:
            self.grid[y][x] = new_color
        
        return len(cells_to_change) > 0
    
    def check_win_condition(self):
        """Check if all cells are the same color."""
        first_color = self.grid[0][0]
        
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x] != first_color:
                    return False
        
        return True
    
    def select_color(self, direction: Direction):
        """Select color based on direction."""
        current_index = self.colors_available.index(self.current_color)
        
        if direction == Direction.LEFT:
            new_index = (current_index - 1) % len(self.colors_available)
        elif direction == Direction.RIGHT:
            new_index = (current_index + 1) % len(self.colors_available)
        else:
            return  # Up/Down don't change color
        
        self.current_color = self.colors_available[new_index]
    
    def perform_flood(self):
        """Perform flood fill with current color."""
        if self.won or self.lost:
            return
        
        # Flood fill from top-left corner
        if self.flood_fill(0, 0, self.current_color):
            self.moves_used += 1
            
            # Check win condition
            if self.check_win_condition():
                self.won = True
                self.flash_timer = pygame.time.get_ticks()
            
            # Check loss condition
            elif self.moves_used >= self.max_moves:
                self.lost = True
                self.flash_timer = pygame.time.get_ticks()
    
    def reset_game(self):
        """Reset to new level."""
        self.setup_level()
    
    def update(self, dt: float):
        """Update game state."""
        current_time = pygame.time.get_ticks()
        
        # Handle win/loss flashing
        if (self.won or self.lost) and self.flash_timer > 0:
            if current_time - self.flash_timer > self.flash_duration:
                self.setup_level()
    
    def draw(self):
        """Draw the game."""
        self.screen.fill(ARC_COLORS[0])  # Black background
        
        # Draw main grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                 self.cell_size, self.cell_size)
                
                cell_color = self.grid[y][x]
                pygame.draw.rect(self.screen, ARC_COLORS[cell_color], rect)
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)
        
        # Draw UI at bottom
        ui_y = self.grid_size * self.cell_size + 10
        
        # Current color indicator
        color_rect = pygame.Rect(10, ui_y, 30, 30)
        pygame.draw.rect(self.screen, ARC_COLORS[self.current_color], color_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), color_rect, 2)
        
        # Moves indicator
        for i in range(self.max_moves):
            x = 50 + i * 25
            rect = pygame.Rect(x, ui_y, 20, 20)
            
            if i < self.moves_used:
                pygame.draw.rect(self.screen, ARC_COLORS[2], rect)  # Red for used
            else:
                pygame.draw.rect(self.screen, ARC_COLORS[5], rect)  # Gray for available
            
            pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
        
        # Win/Loss effects
        current_time = pygame.time.get_ticks()
        if self.won and self.flash_timer > 0:
            # Green flash for win
            elapsed = current_time - self.flash_timer
            if elapsed < self.flash_duration:
                alpha = int(100 * (1 - elapsed / self.flash_duration))
                overlay = pygame.Surface((self.screen_width, self.screen_height))
                overlay.set_alpha(alpha)
                overlay.fill(ARC_COLORS[3])  # Green
                self.screen.blit(overlay, (0, 0))
        
        elif self.lost and self.flash_timer > 0:
            # Red flash for loss
            elapsed = current_time - self.flash_timer
            if elapsed < self.flash_duration:
                alpha = int(100 * (1 - elapsed / self.flash_duration))
                overlay = pygame.Surface((self.screen_width, self.screen_height))
                overlay.set_alpha(alpha)
                overlay.fill(ARC_COLORS[2])  # Red
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
                
                # Color selection
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.select_color(Direction.LEFT)
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.select_color(Direction.RIGHT)
                
                # Perform flood fill
                elif event.key in [pygame.K_w, pygame.K_UP, pygame.K_s, pygame.K_DOWN, pygame.K_SPACE]:
                    self.perform_flood()
    
    def run(self):
        """Main game loop."""
        print("🌊 Simple Color Flood started!")
        print("Controls:")
        print("  A/D or ←/→ - Select color")
        print("  W/S/↑/↓/SPACE - Flood fill")
        print("  R - Restart")
        print("  ESC - Quit")
        
        while self.running:
            dt = self.clock.tick(self.fps)
            
            self.handle_events()
            self.update(dt)
            self.draw()
            
            pygame.display.flip()
        
        pygame.quit()
        print("👋 Simple Color Flood closed")

if __name__ == "__main__":
    game = SimpleFlood()
    game.run()