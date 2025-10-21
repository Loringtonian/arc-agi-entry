#!/usr/bin/env python3
"""
Shadow Walker - ARC-AGI-3 v2.0
Control a player while avoiding your shadow that follows your movement trail

ARC-AGI-3 Compliance:
- ✅ 16-color palette (colors 0-15)
- ✅ Square grid (12×12)
- ✅ No text during gameplay (pure visual)
- ✅ Deterministic behavior
- ✅ 7-action framework compatible
- ✅ Novel mechanic (shadow trail following)

Game Mechanics:
- Player (green) moves normally
- Shadow (maroon) follows player's movement trail with delay
- Both must reach goal zones (yellow)
- Avoid:
  - Hazards (red) kill both
  - Player and shadow cannot touch
- Portals (sky blue/magenta) teleport both characters

Controls:
- WASD/Arrows: Move player
- R: Reset level
- ESC: Quit
"""

import sys
import os
from typing import List, Tuple, Optional, Dict
from enum import Enum
import random
import pygame

# Add tools to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
from arc_agi_editor.editor.utils import ARC_COLORS

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class CellType(Enum):
    EMPTY = 0
    WALL = 1
    GOAL = 2
    PORTAL_BLUE = 3
    PORTAL_RED = 4
    HAZARD = 5

class Character:
    """A character that can move on the grid."""
    def __init__(self, x: int, y: int, color: int):
        self.x = x
        self.y = y
        self.color = color
        self.start_x = x
        self.start_y = y
        self.on_goal = False
    
    def move_to(self, x: int, y: int):
        """Move to new position."""
        self.x = x
        self.y = y
    
    def reset(self):
        """Reset to starting position."""
        self.x = self.start_x
        self.y = self.start_y
        self.on_goal = False

class ShadowWalker:
    """Shadow Walker puzzle game."""
    def __init__(self):
        pygame.init()
        
        # Game settings
        self.grid_size = 12
        self.cell_size = 45
        
        # Screen setup
        self.screen_width = self.grid_size * self.cell_size
        self.screen_height = self.grid_size * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Shadow Walker - ARC-AGI-3 v2.0")
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 8  # Slower for deliberate movement
        
        # Grid
        self.grid = [[CellType.EMPTY for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        # Characters
        self.player = Character(1, 1, 3)  # Green player
        self.shadow = Character(1, 1, 9)  # Dark red shadow
        
        # Move history for shadow (reverse movement)
        self.move_history: List[Tuple[int, int]] = []
        self.max_history = 20
        
        # Portal pairs
        self.portals: Dict[int, List[Tuple[int, int]]] = {}
        
        # Game state
        self.won = False
        self.lost = False
        self.flash_timer = 0
        self.flash_duration = 1000
        self.level = 1
        
        self.setup_level()
    
    def setup_level(self):
        """Setup the current level."""
        # Clear grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.grid[y][x] = CellType.EMPTY
        
        # Add walls around border
        for x in range(self.grid_size):
            self.grid[0][x] = CellType.WALL
            self.grid[self.grid_size-1][x] = CellType.WALL
        for y in range(self.grid_size):
            self.grid[y][0] = CellType.WALL
            self.grid[y][self.grid_size-1] = CellType.WALL
        
        # Add some internal walls
        obstacles = [
            (3, 3), (4, 3), (5, 3),
            (7, 5), (8, 5), (9, 5),
            (3, 8), (4, 8), (5, 8),
            (7, 7), (7, 8), (7, 9)
        ]
        for x, y in obstacles:
            if self.is_valid_pos(x, y):
                self.grid[y][x] = CellType.WALL
        
        # Add hazards (things that kill both characters)
        hazards = [(6, 4), (4, 6), (8, 8)]
        for x, y in hazards:
            if self.is_valid_pos(x, y):
                self.grid[y][x] = CellType.HAZARD
        
        # Add portal pairs
        self.portals = {
            3: [(2, 5), (9, 2)],  # Blue portals
            4: [(5, 9), (10, 6)]  # Red portals
        }
        
        for color, positions in self.portals.items():
            for x, y in positions:
                if self.is_valid_pos(x, y):
                    if color == 3:
                        self.grid[y][x] = CellType.PORTAL_BLUE
                    else:
                        self.grid[y][x] = CellType.PORTAL_RED
        
        # Add goals (both characters must reach goals)
        self.grid[10][10] = CellType.GOAL  # Player goal
        self.grid[1][10] = CellType.GOAL   # Shadow goal
        
        # Reset characters
        self.player.reset()
        self.shadow.reset()
        self.move_history.clear()
        self.move_history.append((self.player.x, self.player.y))
        
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
        return self.grid[y][x] != CellType.WALL
    
    def handle_portal(self, character: Character):
        """Handle portal teleportation."""
        cell_type = self.grid[character.y][character.x]
        
        if cell_type == CellType.PORTAL_BLUE:
            # Find the other blue portal
            other_portals = [pos for pos in self.portals[3] if pos != (character.x, character.y)]
            if other_portals:
                new_x, new_y = other_portals[0]
                character.move_to(new_x, new_y)
        
        elif cell_type == CellType.PORTAL_RED:
            # Find the other red portal
            other_portals = [pos for pos in self.portals[4] if pos != (character.x, character.y)]
            if other_portals:
                new_x, new_y = other_portals[0]
                character.move_to(new_x, new_y)
    
    def move_player(self, direction: Direction):
        """Move the player and update shadow."""
        if self.won or self.lost:
            return
        
        dx, dy = direction.value
        new_x = self.player.x + dx
        new_y = self.player.y + dy
        
        # Check if player can move
        if not self.can_move_to(new_x, new_y):
            return
        
        # Move player
        self.player.move_to(new_x, new_y)
        
        # Add to move history
        self.move_history.append((self.player.x, self.player.y))
        if len(self.move_history) > self.max_history:
            self.move_history.pop(0)
        
        # Handle player portal
        self.handle_portal(self.player)
        
        # Update shadow position (reverse of move history)
        if len(self.move_history) >= 2:
            # Shadow follows the reverse path
            shadow_index = len(self.move_history) - min(8, len(self.move_history))
            shadow_x, shadow_y = self.move_history[shadow_index]
            self.shadow.move_to(shadow_x, shadow_y)
            
            # Handle shadow portal
            self.handle_portal(self.shadow)
        
        # Check collisions and win conditions
        self.check_game_state()
    
    def check_game_state(self):
        """Check for win/loss conditions."""
        # Check if characters collide with hazards
        if (self.grid[self.player.y][self.player.x] == CellType.HAZARD or
            self.grid[self.shadow.y][self.shadow.x] == CellType.HAZARD):
            self.lost = True
            self.flash_timer = pygame.time.get_ticks()
            return
        
        # Check if characters collide with each other
        if self.player.x == self.shadow.x and self.player.y == self.shadow.y:
            self.lost = True
            self.flash_timer = pygame.time.get_ticks()
            return
        
        # Check win condition (both on goals)
        player_on_goal = self.grid[self.player.y][self.player.x] == CellType.GOAL
        shadow_on_goal = self.grid[self.shadow.y][self.shadow.x] == CellType.GOAL
        
        if player_on_goal and shadow_on_goal:
            self.won = True
            self.flash_timer = pygame.time.get_ticks()
    
    def reset_level(self):
        """Reset the current level."""
        self.setup_level()
    
    def next_level(self):
        """Go to next level."""
        self.level += 1
        self.setup_level()
    
    def update(self, dt: float):
        """Update game state."""
        current_time = pygame.time.get_ticks()
        
        # Handle win/loss timing
        if (self.won or self.lost) and self.flash_timer > 0:
            if current_time - self.flash_timer > self.flash_duration:
                if self.won:
                    self.next_level()
                else:
                    self.reset_level()
    
    def draw(self):
        """Draw the game."""
        self.screen.fill(ARC_COLORS[0])  # Black background
        
        # Draw grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                 self.cell_size, self.cell_size)
                
                cell_type = self.grid[y][x]
                
                if cell_type == CellType.WALL:
                    pygame.draw.rect(self.screen, ARC_COLORS[1], rect)  # Blue walls
                elif cell_type == CellType.GOAL:
                    pygame.draw.rect(self.screen, ARC_COLORS[4], rect)  # Yellow goals
                elif cell_type == CellType.PORTAL_BLUE:
                    pygame.draw.rect(self.screen, ARC_COLORS[8], rect)  # Sky blue portals
                elif cell_type == CellType.PORTAL_RED:
                    pygame.draw.rect(self.screen, ARC_COLORS[6], rect)  # Magenta portals
                elif cell_type == CellType.HAZARD:
                    pygame.draw.rect(self.screen, ARC_COLORS[2], rect)  # Red hazards
                
                # Grid lines
                pygame.draw.rect(self.screen, ARC_COLORS[5], rect, 1)
        
        # Draw movement trail (faded)
        for i, (x, y) in enumerate(self.move_history[:-1]):
            alpha = int(50 * (i / len(self.move_history)))
            trail_surface = pygame.Surface((self.cell_size, self.cell_size))
            trail_surface.set_alpha(alpha)
            trail_surface.fill(ARC_COLORS[7])  # Orange trail
            self.screen.blit(trail_surface, (x * self.cell_size, y * self.cell_size))
        
        # Draw shadow
        shadow_rect = pygame.Rect(self.shadow.x * self.cell_size + 2, 
                                self.shadow.y * self.cell_size + 2,
                                self.cell_size - 4, self.cell_size - 4)
        pygame.draw.rect(self.screen, ARC_COLORS[self.shadow.color], shadow_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), shadow_rect, 2)
        
        # Draw player
        player_rect = pygame.Rect(self.player.x * self.cell_size + 2, 
                                self.player.y * self.cell_size + 2,
                                self.cell_size - 4, self.cell_size - 4)
        pygame.draw.rect(self.screen, ARC_COLORS[self.player.color], player_rect)
        pygame.draw.rect(self.screen, (255, 255, 255), player_rect, 2)
        
        # No UI text - pure visual experience
        
        # Win/Loss effects
        current_time = pygame.time.get_ticks()
        if self.won and self.flash_timer > 0:
            elapsed = current_time - self.flash_timer
            if elapsed < self.flash_duration:
                alpha = int(80 * (1 - elapsed / self.flash_duration))
                overlay = pygame.Surface((self.screen_width, self.screen_height))
                overlay.set_alpha(alpha)
                overlay.fill(ARC_COLORS[3])  # Green flash
                self.screen.blit(overlay, (0, 0))
        
        elif self.lost and self.flash_timer > 0:
            elapsed = current_time - self.flash_timer
            if elapsed < self.flash_duration:
                alpha = int(80 * (1 - elapsed / self.flash_duration))
                overlay = pygame.Surface((self.screen_width, self.screen_height))
                overlay.set_alpha(alpha)
                overlay.fill(ARC_COLORS[2])  # Red flash
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
                    self.reset_level()
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
    game = ShadowWalker()
    game.run()