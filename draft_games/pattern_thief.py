#!/usr/bin/env python3
"""
Pattern Thief - ARC-AGI-3 Game (Multi-Level)

Level 1: Basic Sokoban push - learn the mechanics
Level 2: Gravity puzzle - position blocks, trigger fall, open door

ARC-AGI-3 Compliance:
- ✅ 16-color palette (colors 0-15)
- ✅ Square grid (20×20)
- ✅ No text during gameplay (visual icons only)
- ✅ Deterministic behavior
- ✅ Core priors: spatial reasoning, pattern matching, planning, causal reasoning

Controls (shown visually):
- Arrow keys: Move player (push blocks when you walk into them)
- SPACE: Lift block (above=both up, beside=block up only)
- R: Reset level
- ESC: Quit
"""

import sys
import os
from typing import List, Tuple, Optional, Dict, Set
from enum import Enum
import copy

# Auto-detect and use virtual environment for pygame
try:
    import pygame
except ImportError:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    venv_python = os.path.join(parent_dir, ".venv", "bin", "python")

    if os.path.exists(venv_python):
        os.execv(venv_python, [venv_python, __file__] + sys.argv[1:])
    else:
        print(f"Error: pygame not found and virtual environment not available at {venv_python}")
        sys.exit(1)

# ARC-AGI-3 OFFICIAL 16-COLOR PALETTE
ARC_COLORS = {
    0: (0, 0, 0),        # Black - Background/Empty
    1: (0, 116, 217),    # Blue
    2: (255, 65, 54),    # Red
    3: (46, 204, 64),    # Green
    4: (255, 220, 0),    # Yellow
    5: (170, 170, 170),  # Gray
    6: (240, 18, 190),   # Magenta/Pink
    7: (255, 133, 27),   # Orange
    8: (127, 219, 255),  # Sky Blue
    9: (135, 12, 37),    # Maroon
    10: (87, 117, 144),   # Slate Gray
    11: (255, 195, 160),  # Peach
    12: (180, 255, 180),  # Light Green
    13: (255, 255, 200),  # Cream
    14: (220, 160, 220),  # Lavender
    15: (160, 220, 255)   # Light Blue
}

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class PatternThief:
    """Pattern matching puzzle with progressive mechanics."""

    def __init__(self):
        pygame.init()

        # Game settings
        self.grid_size = 20  # Larger for level 2
        self.cell_size = 32

        # Screen setup
        self.screen_width = self.grid_size * self.cell_size
        self.screen_height = self.grid_size * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pattern Thief - ARC-AGI-3")

        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 10

        # Level management
        self.current_level = 1
        self.max_levels = 5
        self.completed_levels = set()  # Track which levels are completed

        # Grid (0 = empty)
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Player position
        self.player_x = 0
        self.player_y = 0

        # Target pattern
        self.target_pattern = []

        # Level-specific state
        self.landing_zone_x = 0
        self.landing_zone_y = 0
        self.target_display_x = 0
        self.target_display_y = 0

        # Level 2 specific
        self.gravity_trigger_x = 0
        self.gravity_trigger_y = 0
        self.door_trigger_x = 0
        self.door_trigger_y = 0
        self.door_open = False
        self.door_cells = []  # List of (x, y) for door positions

        # Win/Loss state
        self.won = False
        self.lost = False
        self.flash_timer = 0
        self.flash_duration = 1000

        # Setup first level
        self.setup_level()

    def setup_level(self):
        """Setup the current level."""
        if self.current_level == 1:
            self.setup_level_1()
        elif self.current_level == 2:
            self.setup_level_2()
        # Add more levels here

    def setup_level_1(self):
        """Level 1: Basic Sokoban push."""
        # Clear grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.grid[y][x] = 0

        # Target pattern (2x2)
        self.target_pattern = [
            [2, 4],  # Red, Yellow
            [1, 3]   # Blue, Green
        ]

        # Display positions
        self.target_display_x = 2
        self.target_display_y = 2
        self.landing_zone_x = 16
        self.landing_zone_y = 16

        # Add border walls
        for x in range(self.grid_size):
            self.grid[0][x] = 5
            self.grid[self.grid_size-1][x] = 5
        for y in range(self.grid_size):
            self.grid[y][0] = 5
            self.grid[y][self.grid_size-1] = 5

        # Landing zone background
        for dy in range(2):
            for dx in range(2):
                x = self.landing_zone_x + dx
                y = self.landing_zone_y + dy
                if self.is_valid_pos(x, y):
                    self.grid[y][x] = 10

        # Target display
        for dy in range(4):
            for dx in range(4):
                x = self.target_display_x - 1 + dx
                y = self.target_display_y - 1 + dy
                if self.is_valid_pos(x, y):
                    self.grid[y][x] = 10

        # Place target pattern
        for dy in range(2):
            for dx in range(2):
                x = self.target_display_x + dx
                y = self.target_display_y + dy
                self.grid[y][x] = self.target_pattern[dy][dx]

        # Place blocks
        self.grid[10][6] = 2   # Red
        self.grid[12][14] = 4  # Yellow
        self.grid[7][12] = 1   # Blue
        self.grid[14][8] = 3   # Green

        # Player start
        self.player_x = 10
        self.player_y = 10

        # Reset state
        self.won = False
        self.lost = False
        self.flash_timer = 0

    def setup_level_2(self):
        """Level 2: Gravity puzzle with lift mechanics."""
        # Clear grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.grid[y][x] = 0

        # Target pattern (2x2 horizontal line)
        self.target_pattern = [
            [2, 4, 1, 3]  # Red, Yellow, Blue, Green in a row
        ]

        # Display positions
        self.target_display_x = 2
        self.target_display_y = 2
        self.landing_zone_x = 8
        self.landing_zone_y = 16  # Bottom area

        # Add border walls
        for x in range(self.grid_size):
            self.grid[0][x] = 5
            self.grid[self.grid_size-1][x] = 5
        for y in range(self.grid_size):
            self.grid[y][0] = 5
            self.grid[y][self.grid_size-1] = 5

        # Create landing zone enclosure (3 walls + door on top)
        # Bottom wall
        for dx in range(6):
            self.grid[self.landing_zone_y + 1][self.landing_zone_x + dx - 1] = 5
        # Left wall
        for dy in range(3):
            self.grid[self.landing_zone_y - dy][self.landing_zone_x - 1] = 5
        # Right wall
        for dy in range(3):
            self.grid[self.landing_zone_y - dy][self.landing_zone_x + 4] = 5

        # Door (top of enclosure) - color 2 (red) when closed
        self.door_cells = []
        for dx in range(4):
            x = self.landing_zone_x + dx
            y = self.landing_zone_y - 2
            self.door_cells.append((x, y))
            self.grid[y][x] = 2  # Red door (closed)

        # Landing zone floor
        self.grid[self.landing_zone_y][self.landing_zone_x] = 10
        self.grid[self.landing_zone_y][self.landing_zone_x + 1] = 10
        self.grid[self.landing_zone_y][self.landing_zone_x + 2] = 10
        self.grid[self.landing_zone_y][self.landing_zone_x + 3] = 10

        # Target display
        for dx in range(6):
            for dy in range(3):
                x = self.target_display_x - 1 + dx
                y = self.target_display_y - 1 + dy
                if self.is_valid_pos(x, y):
                    self.grid[y][x] = 10

        # Place target pattern
        for dx in range(4):
            x = self.target_display_x + dx
            y = self.target_display_y
            self.grid[y][x] = self.target_pattern[0][dx]

        # Gravity trigger (orange square)
        self.gravity_trigger_x = 15
        self.gravity_trigger_y = 8
        self.grid[self.gravity_trigger_y][self.gravity_trigger_x] = 7  # Orange

        # Door trigger (sky blue square)
        self.door_trigger_x = 15
        self.door_trigger_y = 11
        self.grid[self.door_trigger_y][self.door_trigger_x] = 8  # Sky blue

        # Place blocks at mid-height (they need to be aligned horizontally)
        self.grid[8][8] = 2   # Red
        self.grid[8][9] = 4   # Yellow
        self.grid[8][10] = 1  # Blue
        self.grid[8][11] = 3  # Green

        # Player start
        self.player_x = 5
        self.player_y = 10

        # Reset state
        self.won = False
        self.lost = False
        self.flash_timer = 0
        self.door_open = False

    def is_valid_pos(self, x: int, y: int) -> bool:
        """Check if position is within grid bounds."""
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size

    def is_wall(self, x: int, y: int) -> bool:
        """Check if position is a wall."""
        if not self.is_valid_pos(x, y):
            return True
        return self.grid[y][x] == 5

    def is_block(self, x: int, y: int) -> bool:
        """Check if position has a pushable block."""
        if not self.is_valid_pos(x, y):
            return False
        color = self.grid[y][x]
        return color in [1, 2, 3, 4]

    def is_door(self, x: int, y: int) -> bool:
        """Check if position is a door cell."""
        return (x, y) in self.door_cells

    def is_empty_or_floor(self, x: int, y: int) -> bool:
        """Check if position is empty or floor."""
        if not self.is_valid_pos(x, y):
            return False

        # In level 2, if door is open, door cells count as empty
        if self.current_level == 2 and self.door_open and self.is_door(x, y):
            return True

        color = self.grid[y][x]
        return color == 0 or color == 10 or color == 7 or color == 8  # Empty, floor, triggers

    def is_in_target_display(self, x: int, y: int) -> bool:
        """Check if position is in target display area."""
        if self.current_level == 1:
            return (self.target_display_x - 1 <= x <= self.target_display_x + 2 and
                    self.target_display_y - 1 <= y <= self.target_display_y + 2)
        elif self.current_level == 2:
            return (self.target_display_x - 1 <= x <= self.target_display_x + 4 and
                    self.target_display_y - 1 <= y <= self.target_display_y + 1)
        return False

    def can_push_block(self, block_x: int, block_y: int, dx: int, dy: int) -> bool:
        """Check if block can be pushed."""
        if self.is_in_target_display(block_x, block_y):
            return False

        behind_x = block_x + dx
        behind_y = block_y + dy

        if self.is_in_target_display(behind_x, behind_y):
            return False

        return self.is_empty_or_floor(behind_x, behind_y)

    def move_player(self, direction: Direction):
        """Move player with push mechanics."""
        if self.won or self.lost:
            return

        dx, dy = direction.value
        new_x = self.player_x + dx
        new_y = self.player_y + dy

        # Check wall
        if self.is_wall(new_x, new_y):
            return

        # Check target display
        if self.is_in_target_display(new_x, new_y):
            return

        # Check door (level 2)
        if self.current_level == 2 and self.is_door(new_x, new_y) and not self.door_open:
            return

        # Check block
        if self.is_block(new_x, new_y):
            if self.can_push_block(new_x, new_y, dx, dy):
                block_color = self.grid[new_y][new_x]
                behind_x = new_x + dx
                behind_y = new_y + dy

                # Move block
                self.grid[behind_y][behind_x] = block_color

                # Clear old position
                if self.is_landing_zone_pos(new_x, new_y):
                    self.grid[new_y][new_x] = 10
                elif (new_x, new_y) == (self.gravity_trigger_x, self.gravity_trigger_y):
                    self.grid[new_y][new_x] = 7  # Restore trigger
                elif (new_x, new_y) == (self.door_trigger_x, self.door_trigger_y):
                    self.grid[new_y][new_x] = 8  # Restore trigger
                else:
                    self.grid[new_y][new_x] = 0

                # Move player
                self.player_x = new_x
                self.player_y = new_y

                self.check_game_state()
            return

        # Normal movement
        if self.is_empty_or_floor(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y

            # Check triggers (level 2)
            if self.current_level == 2:
                if new_x == self.gravity_trigger_x and new_y == self.gravity_trigger_y:
                    self.trigger_gravity()
                elif new_x == self.door_trigger_x and new_y == self.door_trigger_y:
                    self.open_door()

            self.check_game_state()

    def is_landing_zone_pos(self, x: int, y: int) -> bool:
        """Check if position is in landing zone."""
        if self.current_level == 1:
            return (self.landing_zone_x <= x < self.landing_zone_x + 2 and
                    self.landing_zone_y <= y < self.landing_zone_y + 2)
        elif self.current_level == 2:
            return (self.landing_zone_x <= x < self.landing_zone_x + 4 and
                    y == self.landing_zone_y)
        return False

    def lift_block(self):
        """Lift block (SPACE key). Above=both up, beside=block only up."""
        if self.won or self.lost:
            return

        # Check above
        above_x = self.player_x
        above_y = self.player_y - 1
        if self.is_block(above_x, above_y):
            # Can we move both up?
            player_dest_y = self.player_y - 1
            block_dest_y = above_y - 1

            if (self.is_valid_pos(above_x, block_dest_y) and
                self.is_empty_or_floor(above_x, block_dest_y)):
                # Lift both
                block_color = self.grid[above_y][above_x]

                # Move block up
                self.grid[block_dest_y][above_x] = block_color

                # Clear old block position
                if self.is_landing_zone_pos(above_x, above_y):
                    self.grid[above_y][above_x] = 10
                else:
                    self.grid[above_y][above_x] = 0

                # Move player up
                self.player_y = player_dest_y
                return

        # Check left
        left_x = self.player_x - 1
        left_y = self.player_y
        if self.is_block(left_x, left_y):
            block_dest_y = left_y - 1
            if (self.is_valid_pos(left_x, block_dest_y) and
                self.is_empty_or_floor(left_x, block_dest_y)):
                # Lift block only
                block_color = self.grid[left_y][left_x]
                self.grid[block_dest_y][left_x] = block_color

                if self.is_landing_zone_pos(left_x, left_y):
                    self.grid[left_y][left_x] = 10
                else:
                    self.grid[left_y][left_x] = 0
                return

        # Check right
        right_x = self.player_x + 1
        right_y = self.player_y
        if self.is_block(right_x, right_y):
            block_dest_y = right_y - 1
            if (self.is_valid_pos(right_x, block_dest_y) and
                self.is_empty_or_floor(right_x, block_dest_y)):
                # Lift block only
                block_color = self.grid[right_y][right_x]
                self.grid[block_dest_y][right_x] = block_color

                if self.is_landing_zone_pos(right_x, right_y):
                    self.grid[right_y][right_x] = 10
                else:
                    self.grid[right_y][right_x] = 0
                return

    def trigger_gravity(self):
        """Make all blocks fall to bottom."""
        # Find all blocks
        blocks = []
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.is_block(x, y) and not self.is_in_target_display(x, y):
                    blocks.append((x, y, self.grid[y][x]))
                    # Clear old position
                    if self.is_landing_zone_pos(x, y):
                        self.grid[y][x] = 10
                    elif (x, y) == (self.gravity_trigger_x, self.gravity_trigger_y):
                        self.grid[y][x] = 7
                    elif (x, y) == (self.door_trigger_x, self.door_trigger_y):
                        self.grid[y][x] = 8
                    else:
                        self.grid[y][x] = 0

        # Drop each block to lowest point
        for x, y, color in blocks:
            # Find lowest empty position in this column
            fall_y = y
            for check_y in range(y + 1, self.grid_size):
                if self.is_empty_or_floor(x, check_y):
                    fall_y = check_y
                elif self.is_door(x, check_y) and self.door_open:
                    fall_y = check_y
                else:
                    break

            self.grid[fall_y][x] = color

    def open_door(self):
        """Open the door on top of landing zone."""
        if not self.door_open:
            self.door_open = True
            # Remove door cells
            for x, y in self.door_cells:
                self.grid[y][x] = 0

    def check_game_state(self):
        """Check win condition."""
        if self.current_level == 1:
            # Check 2x2 pattern
            match = True
            for dy in range(2):
                for dx in range(2):
                    x = self.landing_zone_x + dx
                    y = self.landing_zone_y + dy
                    expected = self.target_pattern[dy][dx]
                    actual = self.grid[y][x]
                    if actual != expected:
                        match = False
                        break
                if not match:
                    break

            if match:
                self.won = True
                self.flash_timer = pygame.time.get_ticks()
                self.completed_levels.add(1)

        elif self.current_level == 2:
            # Check 1x4 pattern
            match = True
            for dx in range(4):
                x = self.landing_zone_x + dx
                y = self.landing_zone_y
                expected = self.target_pattern[0][dx]
                actual = self.grid[y][x]
                if actual != expected:
                    match = False
                    break

            if match:
                self.won = True
                self.flash_timer = pygame.time.get_ticks()
                self.completed_levels.add(2)

    def reset_game(self):
        """Reset current level."""
        self.setup_level()

    def next_level(self):
        """Advance to next level."""
        if self.current_level < self.max_levels:
            self.current_level += 1
            self.setup_level()

    def update(self, dt: float):
        """Update game state."""
        current_time = pygame.time.get_ticks()

        if (self.won or self.lost) and self.flash_timer > 0:
            if current_time - self.flash_timer > self.flash_duration:
                # Advance to next level on win
                if self.won:
                    self.next_level()
                else:
                    self.reset_game()

    def draw_ui(self):
        """Draw UI elements (level counter + controls)."""
        # Level counter (top right)
        counter_start_x = self.grid_size - 7
        counter_y = 1

        for i in range(self.max_levels):
            level_num = i + 1
            x = counter_start_x + i
            rect = pygame.Rect(x * self.cell_size, counter_y * self.cell_size,
                             self.cell_size, self.cell_size)

            if level_num in self.completed_levels:
                # Completed: dark green fill
                pygame.draw.rect(self.screen, ARC_COLORS[3], rect)
            elif level_num == self.current_level:
                # Current: pink fill
                pygame.draw.rect(self.screen, ARC_COLORS[6], rect)
            else:
                # Future: hollow (just border)
                pygame.draw.rect(self.screen, ARC_COLORS[5], rect, 2)

        # Control hints (bottom left) - only show for level 2+
        if self.current_level >= 2:
            # Arrow keys icon (4 cells in cross pattern)
            hint_x = 1
            hint_y = self.grid_size - 4

            # Up arrow
            up_rect = pygame.Rect(hint_x * self.cell_size, hint_y * self.cell_size,
                                self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, ARC_COLORS[8], up_rect)

            # Down arrow
            down_rect = pygame.Rect(hint_x * self.cell_size, (hint_y + 2) * self.cell_size,
                                   self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, ARC_COLORS[8], down_rect)

            # Left arrow
            left_rect = pygame.Rect((hint_x - 1) * self.cell_size, (hint_y + 1) * self.cell_size,
                                   self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, ARC_COLORS[8], left_rect)

            # Right arrow
            right_rect = pygame.Rect((hint_x + 1) * self.cell_size, (hint_y + 1) * self.cell_size,
                                    self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, ARC_COLORS[8], right_rect)

            # Space bar (wide rectangle below arrows)
            space_rect = pygame.Rect((hint_x - 1) * self.cell_size, (hint_y + 3) * self.cell_size,
                                    3 * self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, ARC_COLORS[4], space_rect)

    def draw(self):
        """Draw the game."""
        self.screen.fill(ARC_COLORS[0])

        # Draw grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size,
                                 self.cell_size, self.cell_size)

                cell_value = self.grid[y][x]
                if cell_value > 0:
                    pygame.draw.rect(self.screen, ARC_COLORS[cell_value], rect)

                pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)

        # Highlight landing zone
        if self.current_level == 1:
            zone_rect = pygame.Rect(self.landing_zone_x * self.cell_size,
                                   self.landing_zone_y * self.cell_size,
                                   2 * self.cell_size, 2 * self.cell_size)
            pygame.draw.rect(self.screen, ARC_COLORS[8], zone_rect, 3)
        elif self.current_level == 2:
            zone_rect = pygame.Rect(self.landing_zone_x * self.cell_size,
                                   self.landing_zone_y * self.cell_size,
                                   4 * self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, ARC_COLORS[8], zone_rect, 3)

        # Highlight target display
        if self.current_level == 1:
            target_rect = pygame.Rect((self.target_display_x - 1) * self.cell_size,
                                     (self.target_display_y - 1) * self.cell_size,
                                     4 * self.cell_size, 4 * self.cell_size)
        elif self.current_level == 2:
            target_rect = pygame.Rect((self.target_display_x - 1) * self.cell_size,
                                     (self.target_display_y - 1) * self.cell_size,
                                     6 * self.cell_size, 3 * self.cell_size)
        pygame.draw.rect(self.screen, ARC_COLORS[8], target_rect, 3)

        # Draw player
        player_center_x = self.player_x * self.cell_size + self.cell_size // 2
        player_center_y = self.player_y * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, (255, 255, 255),
                         (player_center_x, player_center_y),
                         self.cell_size // 3)
        pygame.draw.circle(self.screen, ARC_COLORS[3],
                         (player_center_x, player_center_y),
                         self.cell_size // 3 - 2)

        # Draw UI
        self.draw_ui()

        # Win flash
        current_time = pygame.time.get_ticks()
        if self.won and self.flash_timer > 0:
            elapsed = current_time - self.flash_timer
            if elapsed < self.flash_duration:
                alpha = int(80 * (1 - elapsed / self.flash_duration))
                overlay = pygame.Surface((self.screen_width, self.screen_height))
                overlay.set_alpha(alpha)
                overlay.fill(ARC_COLORS[3])
                self.screen.blit(overlay, (0, 0))

    def handle_events(self):
        """Handle input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                elif event.key == pygame.K_r:
                    self.reset_game()

                # Movement
                elif event.key in [pygame.K_w, pygame.K_UP]:
                    self.move_player(Direction.UP)
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.move_player(Direction.DOWN)
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.move_player(Direction.LEFT)
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.move_player(Direction.RIGHT)

                # Lift (SPACE)
                elif event.key == pygame.K_SPACE:
                    self.lift_block()

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
    game = PatternThief()
    game.run()
