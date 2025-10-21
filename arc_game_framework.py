#!/Users/lts/Desktop/arc\ agi\ entry/game_engine_env/bin/python
"""
ARC Game Framework - Strict Grid-Based Game Engine
Ensures all positioning respects grid boundaries and constraints
"""

import sys
import os
import pygame
import math
from typing import Dict, List, Tuple, Optional, Any
from enum import Enum

# Add our existing modules to path
sys.path.insert(0, 'arc_agi_editor')
from arc_agi_editor.editor.grid_model import Grid
from arc_agi_editor.editor.utils import get_color_hex, ARC_COLOR_CODES

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class GridPosition:
    """Strict grid position that enforces boundaries."""
    def __init__(self, x: int, y: int, grid_width: int, grid_height: int):
        self._grid_width = grid_width
        self._grid_height = grid_height
        self._x = max(0, min(grid_width - 1, x))
        self._y = max(0, min(grid_height - 1, y))
    
    @property
    def x(self) -> int:
        return self._x
    
    @property
    def y(self) -> int:
        return self._y
    
    def move(self, direction: Direction) -> 'GridPosition':
        """Create new position moved in direction, clamped to grid."""
        dx, dy = direction.value
        new_x = self._x + dx
        new_y = self._y + dy
        return GridPosition(new_x, new_y, self._grid_width, self._grid_height)
    
    def move_by(self, dx: int, dy: int) -> 'GridPosition':
        """Create new position moved by delta, clamped to grid."""
        new_x = self._x + dx
        new_y = self._y + dy
        return GridPosition(new_x, new_y, self._grid_width, self._grid_height)
    
    def is_valid(self) -> bool:
        """Check if position is within grid bounds."""
        return (0 <= self._x < self._grid_width and 
                0 <= self._y < self._grid_height)
    
    def distance_to(self, other: 'GridPosition') -> int:
        """Manhattan distance to another position."""
        return abs(self._x - other._x) + abs(self._y - other._y)
    
    def __eq__(self, other) -> bool:
        return self._x == other._x and self._y == other._y
    
    def __repr__(self) -> str:
        return f"GridPosition({self._x}, {self._y})"

class GameObject:
    """Base class for all grid-based game objects."""
    def __init__(self, position: GridPosition, color: int):
        self.position = position
        self.color = color
        self.active = True
    
    def move_to(self, new_position: GridPosition):
        """Move object to new position."""
        self.position = new_position
    
    def move_direction(self, direction: Direction):
        """Move object in a direction."""
        self.position = self.position.move(direction)
    
    def update(self, dt: float):
        """Update object state."""
        pass

class ARCGameFramework:
    """Base framework for ARC-compliant games."""
    def __init__(self, grid_width: int, grid_height: int, title: str = "ARC Game"):
        # Validate grid size
        if grid_width > 64 or grid_height > 64:
            raise ValueError(f"Grid size {grid_width}x{grid_height} exceeds 64x64 limit")
        
        pygame.init()
        
        # Grid settings
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = min(800 // max(grid_width, grid_height), 50)  # Auto-scale
        
        # Screen setup
        self.screen_width = self.grid_width * self.cell_size
        self.screen_height = self.grid_height * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(title)
        
        # ARC color palette
        self.arc_colors = {}
        for color_idx, hex_color in ARC_COLOR_CODES.items():
            hex_color = hex_color.lstrip('#')
            rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            self.arc_colors[color_idx] = rgb
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 10  # Slow for deliberate moves
        
        # Grid state - enforces only integer positions
        self.grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]
        self.game_objects: List[GameObject] = []
        
        # Input handling
        self.key_repeat_delay = 200  # ms before key repeat
        self.last_key_time = 0
    
    def create_position(self, x: int, y: int) -> GridPosition:
        """Create a valid grid position."""
        return GridPosition(x, y, self.grid_width, self.grid_height)
    
    def get_cell(self, position: GridPosition) -> int:
        """Get cell value at position."""
        if position.is_valid():
            return self.grid[position.y][position.x]
        return 0
    
    def set_cell(self, position: GridPosition, value: int):
        """Set cell value at position."""
        if position.is_valid():
            self.grid[position.y][position.x] = value
    
    def is_cell_empty(self, position: GridPosition) -> bool:
        """Check if cell is empty (value 0)."""
        return self.get_cell(position) == 0
    
    def clear_grid(self):
        """Clear all grid cells."""
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                self.grid[y][x] = 0
    
    def draw_grid(self):
        """Draw the grid with current state."""
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size, 
                                 self.cell_size, self.cell_size)
                
                cell_value = self.grid[y][x]
                color = self.arc_colors.get(cell_value, self.arc_colors[0])
                
                pygame.draw.rect(self.screen, color, rect)
                
                # Grid lines for clarity
                pygame.draw.rect(self.screen, self.arc_colors[8], rect, 1)
    
    def draw_objects(self):
        """Draw all game objects."""
        for obj in self.game_objects:
            if not obj.active:
                continue
            
            rect = pygame.Rect(obj.position.x * self.cell_size, 
                             obj.position.y * self.cell_size,
                             self.cell_size, self.cell_size)
            
            color = self.arc_colors.get(obj.color, self.arc_colors[0])
            pygame.draw.rect(self.screen, color, rect)
    
    def handle_direction_input(self, direction: Direction):
        """Override this to handle directional input."""
        pass
    
    def handle_action_input(self):
        """Override this to handle action input (space/enter)."""
        pass
    
    def update_game_logic(self, dt: float):
        """Override this to implement game-specific logic."""
        pass
    
    def handle_events(self):
        """Handle pygame events with key repeat prevention."""
        current_time = pygame.time.get_ticks()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # Prevent key repeat spam
                if current_time - self.last_key_time < self.key_repeat_delay:
                    continue
                
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # Directional movement
                elif event.key in [pygame.K_w, pygame.K_UP]:
                    self.handle_direction_input(Direction.UP)
                    self.last_key_time = current_time
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.handle_direction_input(Direction.DOWN)
                    self.last_key_time = current_time
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.handle_direction_input(Direction.LEFT)
                    self.last_key_time = current_time
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.handle_direction_input(Direction.RIGHT)
                    self.last_key_time = current_time
                
                # Action keys
                elif event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                    self.handle_action_input()
                    self.last_key_time = current_time
    
    def update(self, dt: float):
        """Update game state."""
        # Update all game objects
        for obj in self.game_objects:
            obj.update(dt)
        
        # Update game-specific logic
        self.update_game_logic(dt)
    
    def draw(self):
        """Draw the entire game."""
        self.screen.fill(self.arc_colors[0])  # Black background
        self.draw_grid()
        self.draw_objects()
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(self.fps)
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        pygame.quit()

# Example implementation: Simple sliding puzzle
class SlidingPuzzle(ARCGameFramework):
    """Example game using the framework."""
    def __init__(self):
        super().__init__(8, 8, "Sliding Puzzle")
        
        # Player object
        self.player_pos = self.create_position(1, 1)
        self.goal_pos = self.create_position(6, 6)
        
        # Setup level
        self.setup_level()
    
    def setup_level(self):
        """Setup a simple level."""
        self.clear_grid()
        
        # Add walls (color 1 = red)
        for x in range(self.grid_width):
            self.set_cell(self.create_position(x, 0), 1)
            self.set_cell(self.create_position(x, self.grid_height-1), 1)
        for y in range(self.grid_height):
            self.set_cell(self.create_position(0, y), 1)
            self.set_cell(self.create_position(self.grid_width-1, y), 1)
        
        # Add some obstacles
        self.set_cell(self.create_position(3, 3), 1)
        self.set_cell(self.create_position(4, 3), 1)
        self.set_cell(self.create_position(3, 4), 1)
        
        # Set goal
        self.set_cell(self.goal_pos, 2)  # Blue goal
        
        # Set player
        self.set_cell(self.player_pos, 3)  # Green player
    
    def handle_direction_input(self, direction: Direction):
        """Handle player movement with sliding."""
        # Clear current player position
        self.set_cell(self.player_pos, 0)
        
        # Slide until hitting wall
        current_pos = self.player_pos
        while True:
            next_pos = current_pos.move(direction)
            
            # Check if next position is blocked
            if not next_pos.is_valid() or self.get_cell(next_pos) == 1:
                break
            
            current_pos = next_pos
        
        # Update player position
        self.player_pos = current_pos
        
        # Check win condition
        if self.player_pos == self.goal_pos:
            # Reset level
            self.setup_level()
        else:
            # Place player
            self.set_cell(self.player_pos, 3)

if __name__ == "__main__":
    game = SlidingPuzzle()
    game.run()