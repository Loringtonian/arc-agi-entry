#!/usr/bin/env python3
"""
Color Flood - ARC-AGI-3 v2.0
Based on "Color Flood Fill" mechanic from game dump
Goal: Flood the entire grid to match the bottom-right corner color in limited moves

ARC-AGI-3 Compliance:
- ✅ 16-color palette (colors 0-15)
- ✅ Square grid (12×12)
- ✅ No text during gameplay
- ✅ Deterministic behavior (fixed levels)
- ✅ 7-action framework compatible

Game Design:
- Fixed levels with exploitable patterns in apparent chaos
- Target color shown in bottom-right corner
- Must flood from top-left to convert entire grid to target color
- Patterns include: stripes, concentric rings, diagonal bands, clusters

Controls:
- LEFT/RIGHT (A/D): Select color
- UP/DOWN/SPACE (W/S): Perform flood fill
- R: Reset current level
- ESC: Quit
"""

import sys
import os
import pygame
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
        pygame.display.set_caption("Color Flood - ARC-AGI-3 v2.0")
        
        # ARC color palette
        self.arc_colors = ARC_COLORS
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 10
        
        # Grid state
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        # Using extended 16-color palette for variety
        self.colors_available = [1, 2, 3, 4, 6, 7, 8]  # Blue, Red, Green, Yellow, Magenta, Orange, Sky Blue
        self.current_color = 1
        self.moves_used = 0
        self.target_color = 1  # Color in bottom-right corner (goal)

        # Level management
        self.current_level = 0
        self.levels = self.create_levels()

        # Game states
        self.won = False
        self.lost = False
        self.flash_timer = 0
        self.flash_duration = 1000  # ms

        self.setup_level()

    def create_levels(self):
        """Create fixed level designs with exploitable patterns.

        Each level is a dict with:
        - 'grid': 12x12 list of lists with color values
        - 'max_moves': move limit for this level
        - 'name': internal name describing pattern
        """
        levels = []

        # Color shortcuts for readability
        B, R, G, Y, M, O, S = 1, 2, 3, 4, 6, 7, 8  # Blue, Red, Green, Yellow, Magenta, Orange, Sky

        # LEVEL 1: Vertical Stripes (Tutorial) - 8 moves
        # Simple left-to-right flooding, target color GREEN on right
        grid1 = [[B]*3 + [R]*3 + [Y]*3 + [G]*3 for _ in range(12)]
        levels.append({'grid': grid1, 'max_moves': 8, 'name': 'vertical_stripes'})

        # LEVEL 2: Concentric Squares - 12 moves
        # Must work from outside-in, target YELLOW in center
        grid2 = [[0]*12 for _ in range(12)]
        for y in range(12):
            for x in range(12):
                dist = min(x, y, 11-x, 11-y)  # Distance from edge
                if dist == 0:
                    grid2[y][x] = B  # Outer ring Blue
                elif dist == 1:
                    grid2[y][x] = R  # Next ring Red
                elif dist == 2:
                    grid2[y][x] = G  # Next ring Green
                else:
                    grid2[y][x] = Y  # Center Yellow
        levels.append({'grid': grid2, 'max_moves': 12, 'name': 'concentric_squares'})

        # LEVEL 3: Diagonal Bands - 15 moves
        # Diagonal pattern, target color ORANGE in bottom-right quadrant
        grid3 = [[0]*12 for _ in range(12)]
        for y in range(12):
            for x in range(12):
                diagonal_value = (x + y) % 4
                if diagonal_value == 0:
                    grid3[y][x] = B
                elif diagonal_value == 1:
                    grid3[y][x] = R
                elif diagonal_value == 2:
                    grid3[y][x] = Y
                else:
                    grid3[y][x] = O
        levels.append({'grid': grid3, 'max_moves': 15, 'name': 'diagonal_bands'})

        # LEVEL 4: Clustered Islands - 18 moves
        # Scattered color regions, target MAGENTA strategically placed
        grid4 = [[B]*12 for _ in range(12)]
        # Add color islands
        for y in range(0, 12, 3):
            for x in range(0, 12, 3):
                color = [R, Y, G, M][((y//3) + (x//3)) % 4]
                for dy in range(3):
                    for dx in range(3):
                        if y+dy < 12 and x+dx < 12:
                            grid4[y+dy][x+dx] = color
        levels.append({'grid': grid4, 'max_moves': 18, 'name': 'clustered_islands'})

        # LEVEL 5: False Abundance - 20 moves
        # Large regions of "wrong" color tempt wasted moves
        # Target is SKY BLUE in corners and edges
        grid5 = [[R]*12 for _ in range(12)]  # Fill with RED (false abundance)
        # Add strategic Sky Blue placement
        for y in range(12):
            for x in range(12):
                if y < 2 or y > 9 or x < 2 or x > 9:
                    grid5[y][x] = S  # Sky blue border
                elif (y + x) % 3 == 0:
                    grid5[y][x] = Y  # Yellow bridges
                elif (y * x) % 5 == 0:
                    grid5[y][x] = G  # Green stepping stones
        levels.append({'grid': grid5, 'max_moves': 20, 'name': 'false_abundance'})

        # LEVEL 6: Complex Maze - 25 moves (Master level)
        # Intricate pattern requiring careful planning
        grid6 = [[0]*12 for _ in range(12)]
        for y in range(12):
            for x in range(12):
                # Create complex pattern based on multiple factors
                val = (x * 3 + y * 2) % 7
                colors = [B, R, G, Y, M, O, S]
                grid6[y][x] = colors[val]
                # Add keystone regions
                if 4 <= x <= 7 and 4 <= y <= 7:
                    grid6[y][x] = G  # Green keystone in center
        levels.append({'grid': grid6, 'max_moves': 25, 'name': 'complex_maze'})

        return levels

    def setup_level(self):
        """Load the current fixed level."""
        # Get current level data
        level_data = self.levels[self.current_level % len(self.levels)]

        # Load grid from level
        self.grid = [row[:] for row in level_data['grid']]  # Deep copy
        self.max_moves = level_data['max_moves']

        # Set target color from bottom-right corner
        self.target_color = self.grid[self.grid_size - 1][self.grid_size - 1]

        # Starting color is top-left
        self.current_color = self.grid[0][0]

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
        """Check if all cells match the target color (bottom-right corner)."""
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.grid[y][x] != self.target_color:
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

        # Handle win/loss flashing and level progression
        if (self.won or self.lost) and self.flash_timer > 0:
            if current_time - self.flash_timer > self.flash_duration:
                if self.won:
                    # Advance to next level on win
                    self.current_level += 1
                # Reset level (either retry on loss, or load next on win)
                self.setup_level()
    
    def draw_target_indicator(self):
        """Draw target color indicator (shows goal from bottom-right corner)."""
        # Large target indicator in top-right corner of screen
        indicator_size = 60
        indicator_x = self.screen_width - indicator_size - 10
        indicator_y = 10

        # Draw target color box
        target_rect = pygame.Rect(indicator_x, indicator_y, indicator_size, indicator_size)
        pygame.draw.rect(self.screen, self.arc_colors[self.target_color], target_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), target_rect, 3)  # White border

        # Add pulsing effect to draw attention
        pulse = int(abs((pygame.time.get_ticks() % 2000) - 1000) / 1000 * 30)
        pulse_rect = target_rect.inflate(pulse, pulse)
        pygame.draw.rect(self.screen, (255, 255, 255), pulse_rect, 2)

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
        self.draw_target_indicator()  # Show goal color
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