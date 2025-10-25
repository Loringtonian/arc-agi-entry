#!/usr/bin/env python3
"""
Pattern Thief - ARC-AGI-3 Game

Combine pattern recognition with Sokoban-style push mechanics.
See a target pattern, find the colored blocks, push them to the landing zone,
and recreate the pattern.

Level 1 (Training): Push 4 colored blocks into a 2x2 landing zone to match target pattern.

ARC-AGI-3 Compliance:
- ✅ 16-color palette (colors 0-15)
- ✅ Square grid (16×16)
- ✅ No text during gameplay
- ✅ Deterministic behavior
- ✅ Core priors: spatial reasoning, pattern matching, planning

Controls:
- WASD/Arrows: Move player (push blocks when you walk into them)
- R: Reset level
- ESC: Quit
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
    6: (240, 18, 190),   # Magenta
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
    """Pattern matching puzzle with Sokoban push mechanics."""

    def __init__(self):
        pygame.init()

        # Game settings
        self.grid_size = 16
        self.cell_size = 40

        # Screen setup
        self.screen_width = self.grid_size * self.cell_size
        self.screen_height = self.grid_size * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pattern Thief - ARC-AGI-3")

        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 10

        # Grid (0 = empty)
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Player position
        self.player_x = 0
        self.player_y = 0

        # Target pattern (2x2 grid of colors for level 1)
        # This is what the player needs to recreate
        self.target_pattern = [
            [2, 4],  # Red, Yellow
            [1, 3]   # Blue, Green
        ]

        # Landing zone position (where pattern needs to be recreated)
        self.landing_zone_x = 13
        self.landing_zone_y = 13

        # Target pattern display position (top-left corner)
        self.target_display_x = 1
        self.target_display_y = 1

        # Win/Loss state
        self.won = False
        self.lost = False
        self.flash_timer = 0
        self.flash_duration = 1000

        # Setup level
        self.setup_level()

    def setup_level(self):
        """Setup Level 1: 4 colored blocks scattered, need to push to landing zone."""
        # Clear grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.grid[y][x] = 0

        # Add border walls (color 5 = gray)
        for x in range(self.grid_size):
            self.grid[0][x] = 5
            self.grid[self.grid_size-1][x] = 5
        for y in range(self.grid_size):
            self.grid[y][0] = 5
            self.grid[y][self.grid_size-1] = 5

        # Mark landing zone with subtle background (color 10 = slate gray)
        for dy in range(2):
            for dx in range(2):
                x = self.landing_zone_x + dx
                y = self.landing_zone_y + dy
                if self.is_valid_pos(x, y):
                    self.grid[y][x] = 10

        # Display target pattern in top-left (inside border)
        # Add a frame around it
        for dy in range(4):
            for dx in range(4):
                x = self.target_display_x - 1 + dx
                y = self.target_display_y - 1 + dy
                if self.is_valid_pos(x, y):
                    self.grid[y][x] = 10  # Frame background

        # Place target pattern
        for dy in range(2):
            for dx in range(2):
                x = self.target_display_x + dx
                y = self.target_display_y + dy
                self.grid[y][x] = self.target_pattern[dy][dx]

        # Place moveable blocks scattered around the grid
        # Red block
        self.grid[8][4] = 2
        # Yellow block
        self.grid[10][11] = 4
        # Blue block
        self.grid[5][9] = 1
        # Green block
        self.grid[12][6] = 3

        # Place player (use position that's not blocked)
        self.player_x = 7
        self.player_y = 7

        # Reset game state
        self.won = False
        self.lost = False
        self.flash_timer = 0

    def is_valid_pos(self, x: int, y: int) -> bool:
        """Check if position is within grid bounds."""
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size

    def is_wall(self, x: int, y: int) -> bool:
        """Check if position is a wall."""
        if not self.is_valid_pos(x, y):
            return True
        return self.grid[y][x] == 5  # Gray = wall

    def is_block(self, x: int, y: int) -> bool:
        """Check if position has a pushable block."""
        if not self.is_valid_pos(x, y):
            return False
        color = self.grid[y][x]
        # Blocks are colors 1, 2, 3, 4 (blue, red, green, yellow)
        return color in [1, 2, 3, 4]

    def is_empty_or_floor(self, x: int, y: int) -> bool:
        """Check if position is empty or just floor (landing zone background)."""
        if not self.is_valid_pos(x, y):
            return False
        color = self.grid[y][x]
        return color == 0 or color == 10  # Black or slate gray (landing zone)

    def is_in_target_display(self, x: int, y: int) -> bool:
        """Check if position is in the target pattern display area."""
        return (self.target_display_x - 1 <= x <= self.target_display_x + 2 and
                self.target_display_y - 1 <= y <= self.target_display_y + 2)

    def can_push_block(self, block_x: int, block_y: int, dx: int, dy: int) -> bool:
        """Check if block can be pushed in direction (dx, dy)."""
        # Don't push blocks in target display area
        if self.is_in_target_display(block_x, block_y):
            return False

        # Check space behind the block
        behind_x = block_x + dx
        behind_y = block_y + dy

        # Can push if space behind is empty/floor and not in target display
        if self.is_in_target_display(behind_x, behind_y):
            return False

        return self.is_empty_or_floor(behind_x, behind_y)

    def move_player(self, direction: Direction):
        """Move player with Sokoban-style push mechanics."""
        if self.won or self.lost:
            return

        dx, dy = direction.value
        new_x = self.player_x + dx
        new_y = self.player_y + dy

        # Check if moving into a wall
        if self.is_wall(new_x, new_y):
            return

        # Check if moving into target display area (can't walk on it)
        if self.is_in_target_display(new_x, new_y):
            return

        # Check if moving into a block
        if self.is_block(new_x, new_y):
            # Try to push the block
            if self.can_push_block(new_x, new_y, dx, dy):
                # Push the block
                block_color = self.grid[new_y][new_x]
                behind_x = new_x + dx
                behind_y = new_y + dy

                # Remember what was at the behind position
                behind_color = self.grid[behind_y][behind_x]

                # Move block to behind position
                self.grid[behind_y][behind_x] = block_color

                # Clear block's old position (restore background if it was landing zone)
                if (self.landing_zone_x <= new_x < self.landing_zone_x + 2 and
                    self.landing_zone_y <= new_y < self.landing_zone_y + 2):
                    self.grid[new_y][new_x] = 10  # Restore landing zone floor
                else:
                    self.grid[new_y][new_x] = 0  # Empty

                # Move player to where block was
                self.player_x = new_x
                self.player_y = new_y

                # Check win condition after push
                self.check_game_state()
            # If can't push, don't move
            return

        # Normal movement (empty space or landing zone floor)
        if self.is_empty_or_floor(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y

    def check_game_state(self):
        """Check if pattern in landing zone matches target pattern."""
        # Check if all positions in landing zone match target pattern
        match = True
        for dy in range(2):
            for dx in range(2):
                x = self.landing_zone_x + dx
                y = self.landing_zone_y + dy
                expected_color = self.target_pattern[dy][dx]
                actual_color = self.grid[y][x]

                if actual_color != expected_color:
                    match = False
                    break
            if not match:
                break

        if match:
            self.won = True
            self.flash_timer = pygame.time.get_ticks()

    def reset_game(self):
        """Reset the level."""
        self.setup_level()

    def update(self, dt: float):
        """Update game state."""
        current_time = pygame.time.get_ticks()

        # Handle win/loss timing
        if (self.won or self.lost) and self.flash_timer > 0:
            if current_time - self.flash_timer > self.flash_duration:
                self.reset_game()

    def draw(self):
        """Draw the game (no text allowed)."""
        self.screen.fill(ARC_COLORS[0])  # Black background

        # Draw grid cells
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size,
                                 self.cell_size, self.cell_size)

                cell_value = self.grid[y][x]
                if cell_value > 0:
                    pygame.draw.rect(self.screen, ARC_COLORS[cell_value], rect)

                # Subtle grid lines
                pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)

        # Highlight landing zone with a border
        landing_rect = pygame.Rect(
            self.landing_zone_x * self.cell_size,
            self.landing_zone_y * self.cell_size,
            2 * self.cell_size,
            2 * self.cell_size
        )
        pygame.draw.rect(self.screen, ARC_COLORS[8], landing_rect, 3)  # Sky blue border

        # Highlight target display with a border
        target_rect = pygame.Rect(
            (self.target_display_x - 1) * self.cell_size,
            (self.target_display_y - 1) * self.cell_size,
            4 * self.cell_size,
            4 * self.cell_size
        )
        pygame.draw.rect(self.screen, ARC_COLORS[8], target_rect, 3)  # Sky blue border

        # Draw player (white circle)
        player_center_x = self.player_x * self.cell_size + self.cell_size // 2
        player_center_y = self.player_y * self.cell_size + self.cell_size // 2
        pygame.draw.circle(self.screen, (255, 255, 255),
                         (player_center_x, player_center_y),
                         self.cell_size // 3)
        pygame.draw.circle(self.screen, ARC_COLORS[3],
                         (player_center_x, player_center_y),
                         self.cell_size // 3 - 2)  # Green center

        # Win flash (green)
        current_time = pygame.time.get_ticks()
        if self.won and self.flash_timer > 0:
            elapsed = current_time - self.flash_timer
            if elapsed < self.flash_duration:
                alpha = int(80 * (1 - elapsed / self.flash_duration))
                overlay = pygame.Surface((self.screen_width, self.screen_height))
                overlay.set_alpha(alpha)
                overlay.fill(ARC_COLORS[3])  # Green flash
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

                # Movement
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
    game = PatternThief()
    game.run()
