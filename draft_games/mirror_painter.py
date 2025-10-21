#!/usr/bin/env python3
"""
Mirror Painter - ARC-AGI-3 v2.0

Paint one side of a grid, see it mirror on the other side.
Goal: Match a target pattern shown at the top.

ARC-AGI-3 Compliance:
- ✅ 16-color palette (colors 0-15)
- ✅ Square grid (16×16)
- ✅ No text during gameplay (pure visual)
- ✅ Deterministic behavior
- ✅ 7-action framework compatible
- ✅ Core prior: Symmetry (fundamental cognitive concept)
- ✅ Instantly understandable (see mirror effect on first paint)

Game Mechanics:
- Paint cells on LEFT side of vertical mirror line
- Cells automatically appear MIRRORED on RIGHT side
- Match the target pattern shown at top
- Limited paint actions (move counter)

Controls:
- WASD/Arrows: Move cursor
- Q/E: Cycle through paint colors
- SPACE: Paint current cell with selected color
- U/Z: Undo last paint (optional)
- R: Reset level
- ESC: Quit
"""

import sys
import os
from typing import List, Tuple, Optional
from enum import Enum
import pygame

# Add tools to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'tools'))
from arc_agi_editor.editor.utils import ARC_COLORS

class Direction(Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class MirrorPainter:
    """Mirror Painter puzzle game."""

    def __init__(self):
        pygame.init()

        # Game settings
        self.grid_size = 16  # Square grid
        self.cell_size = 35  # Smaller cells for 16×16 grid

        # Mirror line (vertical center)
        self.mirror_line = self.grid_size // 2

        # Screen setup
        self.screen_width = self.grid_size * self.cell_size
        self.screen_height = self.grid_size * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Mirror Painter - ARC-AGI-3 v2.0")

        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 10

        # Grids
        self.target_grid = [[0]*self.grid_size for _ in range(self.grid_size)]
        self.player_grid = [[0]*self.grid_size for _ in range(self.grid_size)]

        # Target display area (top 3 rows reserved for showing target pattern)
        self.target_display_rows = 3
        self.playable_row_start = self.target_display_rows

        # Cursor position (starts in playable area)
        self.cursor_x = 2
        self.cursor_y = self.playable_row_start + 2

        # Color selection
        self.colors_available = [1, 2, 3, 4, 6, 7, 8]  # Blue, Red, Green, Yellow, Magenta, Orange, Sky Blue
        self.current_color_index = 0
        self.current_color = self.colors_available[self.current_color_index]

        # Game progress
        self.max_moves = 30
        self.moves_used = 0
        self.level = 0
        self.levels = []

        # Undo system
        self.paint_history: List[Tuple[int, int, int]] = []  # (x, y, old_color)

        # Win/loss state
        self.won = False
        self.lost = False
        self.flash_timer = 0
        self.flash_duration = 1000

        self.setup_levels()
        self.load_level(0)

    def setup_levels(self):
        """Create all target patterns."""

        # Level 1: Simple horizontal stripes
        level1 = [[0]*self.grid_size for _ in range(self.grid_size)]
        for y in range(self.playable_row_start, self.grid_size):
            if y % 3 == 0:
                for x in range(self.grid_size):
                    level1[y][x] = 1  # Blue stripe
            elif y % 3 == 1:
                for x in range(self.grid_size):
                    level1[y][x] = 2  # Red stripe

        # Level 2: Vertical stripes (symmetric)
        level2 = [[0]*self.grid_size for _ in range(self.grid_size)]
        for y in range(self.playable_row_start, self.grid_size):
            for x in range(self.grid_size):
                if x % 3 == 0:
                    level2[y][x] = 3  # Green
                elif x % 3 == 1:
                    level2[y][x] = 4  # Yellow

        # Level 3: Border frame
        level3 = [[0]*self.grid_size for _ in range(self.grid_size)]
        for y in range(self.playable_row_start, self.grid_size):
            for x in range(self.grid_size):
                if y == self.playable_row_start or y == self.grid_size - 1 or x == 0 or x == self.grid_size - 1:
                    level3[y][x] = 6  # Magenta frame

        # Level 4: Checkerboard pattern
        level4 = [[0]*self.grid_size for _ in range(self.grid_size)]
        for y in range(self.playable_row_start, self.grid_size):
            for x in range(self.grid_size):
                if (x + y) % 2 == 0:
                    level4[y][x] = 1  # Blue
                else:
                    level4[y][x] = 7  # Orange

        # Level 5: Cross pattern
        level5 = [[0]*self.grid_size for _ in range(self.grid_size)]
        mid = self.grid_size // 2
        for y in range(self.playable_row_start, self.grid_size):
            for x in range(self.grid_size):
                if x == mid or y == mid:
                    level5[y][x] = 2  # Red cross

        self.levels = [level1, level2, level3, level4, level5]

    def load_level(self, level_num: int):
        """Load a specific level's target pattern."""
        if level_num >= len(self.levels):
            level_num = 0  # Loop back to first level

        self.level = level_num
        self.target_grid = [row[:] for row in self.levels[level_num]]  # Deep copy

        # Clear player grid
        self.player_grid = [[0]*self.grid_size for _ in range(self.grid_size)]

        # Reset game state
        self.cursor_x = 2
        self.cursor_y = self.playable_row_start + 2
        self.moves_used = 0
        self.won = False
        self.lost = False
        self.flash_timer = 0
        self.paint_history.clear()
        self.current_color_index = 0
        self.current_color = self.colors_available[self.current_color_index]

    def move_cursor(self, direction: Direction):
        """Move cursor (restricted to playable area)."""
        if self.won or self.lost:
            return

        dx, dy = direction.value
        new_x = self.cursor_x + dx
        new_y = self.cursor_y + dy

        # Keep cursor in playable area
        if 0 <= new_x < self.grid_size and self.playable_row_start <= new_y < self.grid_size:
            self.cursor_x = new_x
            self.cursor_y = new_y

    def cycle_color(self, direction: int):
        """Select next/previous color."""
        if self.won or self.lost:
            return

        self.current_color_index = (self.current_color_index + direction) % len(self.colors_available)
        self.current_color = self.colors_available[self.current_color_index]

    def paint_cell(self):
        """Paint current cell and update mirror."""
        if self.won or self.lost:
            return

        # Only allow painting if cursor is in playable area
        if self.cursor_y < self.playable_row_start:
            return

        # Save for undo
        old_color = self.player_grid[self.cursor_y][self.cursor_x]

        # Don't count as move if painting same color
        if old_color == self.current_color:
            return

        self.paint_history.append((self.cursor_x, self.cursor_y, old_color))

        # Paint the cell
        self.player_grid[self.cursor_y][self.cursor_x] = self.current_color

        # Update mirror
        self.update_mirror()

        # Increment move counter
        self.moves_used += 1

        # Check win/loss
        self.check_game_state()

    def update_mirror(self):
        """Generate mirrored right side from left side."""
        mirror_x = self.grid_size - 1

        for y in range(self.grid_size):
            for x in range(self.grid_size // 2):
                # Mirror left to right
                mirrored_x = mirror_x - x
                self.player_grid[y][mirrored_x] = self.player_grid[y][x]

    def undo_last_paint(self):
        """Undo last paint action."""
        if not self.paint_history or self.won or self.lost:
            return

        x, y, old_color = self.paint_history.pop()
        self.player_grid[y][x] = old_color

        # Update mirror
        self.update_mirror()

        # Decrement move counter
        self.moves_used = max(0, self.moves_used - 1)

    def check_game_state(self):
        """Check for win/loss conditions."""
        # Check if player grid matches target grid (only in playable area)
        matches = True
        for y in range(self.playable_row_start, self.grid_size):
            for x in range(self.grid_size):
                if self.player_grid[y][x] != self.target_grid[y][x]:
                    matches = False
                    break
            if not matches:
                break

        if matches:
            self.won = True
            self.flash_timer = pygame.time.get_ticks()
            return

        # Check if out of moves
        if self.moves_used >= self.max_moves:
            self.lost = True
            self.flash_timer = pygame.time.get_ticks()

    def reset_level(self):
        """Reset current level."""
        self.load_level(self.level)

    def next_level(self):
        """Go to next level."""
        self.load_level(self.level + 1)

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

        # Draw target pattern in top 3 rows (scaled down)
        target_scale = 0.6
        target_cell_size = int(self.cell_size * target_scale)
        target_offset_x = (self.screen_width - self.grid_size * target_cell_size) // 2

        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if y < self.target_display_rows:
                    # Draw target pattern (scaled down)
                    rect = pygame.Rect(
                        target_offset_x + x * target_cell_size,
                        y * target_cell_size,
                        target_cell_size,
                        target_cell_size
                    )

                    # Map full grid to target display area
                    source_y = self.playable_row_start + int((y / self.target_display_rows) * (self.grid_size - self.playable_row_start))
                    if source_y < self.grid_size:
                        cell_color = self.target_grid[source_y][x]
                        if cell_color > 0:
                            pygame.draw.rect(self.screen, ARC_COLORS[cell_color], rect)
                        pygame.draw.rect(self.screen, ARC_COLORS[5], rect, 1)

        # Draw separator line between target and playable area
        separator_y = self.target_display_rows * self.cell_size
        pygame.draw.line(self.screen, ARC_COLORS[5],
                        (0, separator_y), (self.screen_width, separator_y), 3)

        # Draw playable grid
        for y in range(self.playable_row_start, self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size,
                                 self.cell_size, self.cell_size)

                cell_color = self.player_grid[y][x]
                if cell_color > 0:
                    pygame.draw.rect(self.screen, ARC_COLORS[cell_color], rect)

                # Grid lines
                pygame.draw.rect(self.screen, ARC_COLORS[5], rect, 1)

        # Draw vertical mirror line (bright white)
        mirror_x = self.mirror_line * self.cell_size
        pygame.draw.line(self.screen, (255, 255, 255),
                        (mirror_x, separator_y), (mirror_x, self.screen_height), 3)

        # Draw cursor (white border)
        if self.playable_row_start <= self.cursor_y < self.grid_size:
            cursor_rect = pygame.Rect(self.cursor_x * self.cell_size + 2,
                                     self.cursor_y * self.cell_size + 2,
                                     self.cell_size - 4, self.cell_size - 4)
            pygame.draw.rect(self.screen, (255, 255, 255), cursor_rect, 3)

            # Show current color in cursor
            inner_rect = pygame.Rect(self.cursor_x * self.cell_size + 6,
                                    self.cursor_y * self.cell_size + 6,
                                    self.cell_size - 12, self.cell_size - 12)
            pygame.draw.rect(self.screen, ARC_COLORS[self.current_color], inner_rect)

        # Draw move counter as colored bar
        moves_remaining = max(0, self.max_moves - self.moves_used)
        bar_width = 200
        bar_height = 10
        bar_x = (self.screen_width - bar_width) // 2
        bar_y = separator_y - bar_height - 5

        # Background bar
        pygame.draw.rect(self.screen, ARC_COLORS[5],
                        pygame.Rect(bar_x, bar_y, bar_width, bar_height))

        # Filled bar (green = remaining moves)
        filled_width = int(bar_width * (moves_remaining / self.max_moves))
        if filled_width > 0:
            color = ARC_COLORS[3] if moves_remaining > 10 else ARC_COLORS[2]  # Green or red
            pygame.draw.rect(self.screen, color,
                           pygame.Rect(bar_x, bar_y, filled_width, bar_height))

        # Win/Loss effects
        current_time = pygame.time.get_ticks()
        if self.won and self.flash_timer > 0:
            elapsed = current_time - self.flash_timer
            if elapsed < self.flash_duration:
                alpha = int(100 * (1 - elapsed / self.flash_duration))
                overlay = pygame.Surface((self.screen_width, self.screen_height))
                overlay.set_alpha(alpha)
                overlay.fill(ARC_COLORS[3])  # Green flash
                self.screen.blit(overlay, (0, 0))

        elif self.lost and self.flash_timer > 0:
            elapsed = current_time - self.flash_timer
            if elapsed < self.flash_duration:
                alpha = int(100 * (1 - elapsed / self.flash_duration))
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

                # Cursor movement
                elif event.key in [pygame.K_w, pygame.K_UP]:
                    self.move_cursor(Direction.UP)
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.move_cursor(Direction.DOWN)
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.move_cursor(Direction.LEFT)
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.move_cursor(Direction.RIGHT)

                # Paint action
                elif event.key == pygame.K_SPACE:
                    self.paint_cell()

                # Color selection
                elif event.key == pygame.K_q:
                    self.cycle_color(-1)
                elif event.key == pygame.K_e:
                    self.cycle_color(1)

                # Undo
                elif event.key in [pygame.K_u, pygame.K_z]:
                    self.undo_last_paint()

            # Click to paint
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    grid_x = mouse_x // self.cell_size
                    grid_y = mouse_y // self.cell_size

                    if (0 <= grid_x < self.grid_size and
                        self.playable_row_start <= grid_y < self.grid_size):
                        self.cursor_x = grid_x
                        self.cursor_y = grid_y
                        self.paint_cell()

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
    game = MirrorPainter()
    game.run()
