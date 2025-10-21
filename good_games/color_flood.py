#!/usr/bin/env python3
"""
Color Flood - ARC AGI Style
Based on "Color Flood Fill" mechanic from game dump
Goal: Flood the entire grid with one color in limited moves
"""

import sys
import os
import pygame
from typing import Set, Tuple
from enum import Enum

# ARC color palette (hardcoded)
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

class ColorFlood:
    """Color flood fill puzzle game."""
    def __init__(self):
        pygame.init()
        
        # Game settings
        self.grid_size = 12
        self.cell_size = 40
        
        # Screen setup
        self.screen_width = self.grid_size * self.cell_size
        self.screen_height = self.grid_size * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Color Flood")
        
        # ARC color palette
        self.arc_colors = ARC_COLORS
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 10
        
        # Grid state
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.colors_available = [1, 2, 3, 4, 5]  # Red, Blue, Green, Yellow, Purple
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
        import random
        
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
    
    def draw_color_selector(self):
        """Draw color selector at bottom of screen."""
        selector_y = self.screen_height - 60
        selector_height = 50
        color_width = self.screen_width // len(self.colors_available)
        
        for i, color in enumerate(self.colors_available):
            x = i * color_width
            rect = pygame.Rect(x, selector_y, color_width, selector_height)
            
            # Draw color
            pygame.draw.rect(self.screen, self.arc_colors[color], rect)
            
            # Highlight current color
            if color == self.current_color:
                pygame.draw.rect(self.screen, (255, 255, 255), rect, 4)
            else:
                pygame.draw.rect(self.screen, (100, 100, 100), rect, 2)
    
    def draw_moves_indicator(self):
        """Draw moves indicator using colored cells."""
        indicator_y = self.screen_height - 120
        cell_size = 20
        
        for i in range(self.max_moves):
            x = i * (cell_size + 2)
            rect = pygame.Rect(x, indicator_y, cell_size, cell_size)
            
            if i < self.moves_used:
                # Used move - red
                pygame.draw.rect(self.screen, self.arc_colors[1], rect)
            else:
                # Available move - gray
                pygame.draw.rect(self.screen, self.arc_colors[8], rect)
            
            pygame.draw.rect(self.screen, (100, 100, 100), rect, 1)
    
    def draw(self):
        """Draw the game."""
        self.screen.fill(self.arc_colors[0])  # Black background
        
        # Draw main grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                 self.cell_size, self.cell_size)
                
                cell_color = self.grid[y][x]
                pygame.draw.rect(self.screen, self.arc_colors[cell_color], rect)
                pygame.draw.rect(self.screen, (50, 50, 50), rect, 1)
        
        # Draw UI elements
        self.draw_color_selector()
        self.draw_moves_indicator()
        
        # Win/Loss effects
        current_time = pygame.time.get_ticks()
        if self.won and self.flash_timer > 0:
            # Green flash for win
            elapsed = current_time - self.flash_timer
            if elapsed < self.flash_duration:
                alpha = int(100 * (1 - elapsed / self.flash_duration))
                overlay = pygame.Surface((self.screen_width, self.screen_height))
                overlay.set_alpha(alpha)
                overlay.fill(self.arc_colors[3])  # Green
                self.screen.blit(overlay, (0, 0))
        
        elif self.lost and self.flash_timer > 0:
            # Red flash for loss
            elapsed = current_time - self.flash_timer
            if elapsed < self.flash_duration:
                alpha = int(100 * (1 - elapsed / self.flash_duration))
                overlay = pygame.Surface((self.screen_width, self.screen_height))
                overlay.set_alpha(alpha)
                overlay.fill(self.arc_colors[1])  # Red
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
        while self.running:
            dt = self.clock.tick(self.fps)
            
            self.handle_events()
            self.update(dt)
            self.draw()
            
            pygame.display.flip()
        
        pygame.quit()

if __name__ == "__main__":
    game = ColorFlood()
    game.run()