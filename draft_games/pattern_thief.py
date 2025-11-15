#!/usr/bin/env python3
"""
Pattern Thief - ARC-AGI-3 Game (Multi-Level)

Level 1: Basic Sokoban push - learn the mechanics
Level 2: Gravity puzzle - position blocks, trigger fall, open door
Level 3: Teleportation puzzle - use teleporter to launch blocks through walls into enclosed zone

ARC-AGI-3 Compliance:
- ✅ 16-color palette (colors 0-15) + special block patterns (rim/center)
- ✅ Square grid (20×20)
- ✅ No text during gameplay (visual icons only)
- ✅ Deterministic behavior
- ✅ Core priors: spatial reasoning, pattern matching, planning, causal reasoning, tool use

Controls (shown visually):
- Arrow keys: Move player (push blocks when you walk into them)
- SPACE: Lift block (above=both up, beside=block up only) [Level 2]
- R: Reset level
- ESC: Quit

Special Blocks (Level 3):
- Yellow rim/red center: Teleporter - launches entities 4 spaces forward
- Red rim/yellow center: Teleporter Mover - push into teleporter to unlock it
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
        self.grid_height = self.grid_size * self.cell_size
        self.control_panel_height = 120  # Black area at bottom for controls (increased to fit spacebar)
        self.screen_width = self.grid_size * self.cell_size
        self.screen_height = self.grid_height + self.control_panel_height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Pattern Thief - ARC-AGI-3")

        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 10

        # Level management
        self.current_level = 3  # Start at level 3
        self.max_levels = 5
        self.completed_levels = {1, 2}  # Mark levels 1-2 as completed

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

        # Gravity animation
        self.gravity_active = False
        self.falling_blocks = []  # List of (x, current_y, target_y, color)
        self.last_fall_time = 0
        self.fall_interval = 200  # ms per cell

        # Level 3 specific - special blocks
        self.special_blocks = {}  # (x, y) -> {'type': 'teleporter'/'teleporter_mover', etc.}
        self.teleporter_pos = None  # (x, y) of teleporter
        self.teleporter_unlocked = False  # Can teleporter be moved?
        self.last_move_from = None  # Track direction for teleportation

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
        elif self.current_level == 3:
            self.setup_level_3()
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

        # Sliding door (top of enclosure) - 6 brown tiles
        # Covers x=7-12 (6 tiles wide) at y=14
        self.door_cells = []
        self.door_closed_positions = []  # Where door tiles are when closed
        self.door_open_positions = []    # Where door tiles are when open (slid to right)
        door_y = self.landing_zone_y - 2
        for dx in range(6):
            x_closed = self.landing_zone_x - 1 + dx  # x=7-12
            x_open = self.landing_zone_x + 5 + dx    # x=13-18 (slid to right)
            self.door_closed_positions.append((x_closed, door_y))
            self.door_open_positions.append((x_open, door_y))
            self.door_cells.append((x_closed, door_y))  # Start closed
            self.grid[door_y][x_closed] = 9  # Brown (maroon)

        # Landing zone floor
        self.grid[self.landing_zone_y][self.landing_zone_x] = 10
        self.grid[self.landing_zone_y][self.landing_zone_x + 1] = 10
        self.grid[self.landing_zone_y][self.landing_zone_x + 2] = 10
        self.grid[self.landing_zone_y][self.landing_zone_x + 3] = 10

        # Target display - match landing zone exactly (4x1 with slate gray floor)
        for dx in range(4):
            x = self.target_display_x + dx
            y = self.target_display_y
            self.grid[y][x] = 10  # Slate gray floor, just like landing zone

        # Place target pattern on top of floor
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

        # Place blocks SCATTERED (not pre-aligned)
        self.grid[6][5] = 2   # Red - top left area
        self.grid[10][13] = 4  # Yellow - right side
        self.grid[4][10] = 1  # Blue - top middle
        self.grid[12][7] = 3  # Green - bottom left

        # Player start
        self.player_x = 5
        self.player_y = 10

        # Reset state
        self.won = False
        self.lost = False
        self.flash_timer = 0
        self.door_open = False
        self.gravity_active = False
        self.falling_blocks = []
        self.last_fall_time = 0

    def setup_level_3(self):
        """Level 3: Teleportation puzzle with fully enclosed target zone."""
        # Clear grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.grid[y][x] = 0

        # Clear special blocks
        self.special_blocks = {}
        self.teleporter_pos = None
        self.teleporter_unlocked = False

        # Border walls
        for x in range(self.grid_size):
            self.grid[0][x] = 5
            self.grid[self.grid_size-1][x] = 5
        for y in range(self.grid_size):
            self.grid[y][0] = 5
            self.grid[y][self.grid_size-1] = 5

        # Fully enclosed target zone (4x4 gray enclosure)
        zone_x, zone_y = 12, 12
        zone_size = 4

        # Gray walls (all sides - fully enclosed)
        for dx in range(zone_size + 2):
            self.grid[zone_y - 1][zone_x - 1 + dx] = 5  # Top wall
            self.grid[zone_y + zone_size][zone_x - 1 + dx] = 5  # Bottom wall
        for dy in range(zone_size + 2):
            self.grid[zone_y - 1 + dy][zone_x - 1] = 5  # Left wall
            self.grid[zone_y - 1 + dy][zone_x + zone_size] = 5  # Right wall

        # Gray floor inside
        for dy in range(zone_size):
            for dx in range(zone_size):
                self.grid[zone_y + dy][zone_x + dx] = 10  # Slate gray

        # Target pattern (non-contiguous, 4 blocks in 4x4 zone)
        # Stored as list of (x, y, color)
        self.target_pattern_3 = [
            (zone_x, zone_y + 1, 2),        # Red - left side
            (zone_x + 3, zone_y, 1),        # Blue - top right
            (zone_x + 1, zone_y + 3, 4),    # Yellow - bottom
            (zone_x + 3, zone_y + 2, 3)     # Green - right side
        ]

        # Display target pattern (top-left corner)
        self.target_display_x = 2
        self.target_display_y = 2

        # Frame around target display (4x4 to match enclosure)
        for dy in range(6):
            for dx in range(6):
                x = self.target_display_x - 1 + dx
                y = self.target_display_y - 1 + dy
                if self.is_valid_pos(x, y):
                    if dx == 0 or dx == 5 or dy == 0 or dy == 5:
                        self.grid[y][x] = 5  # Gray frame
                    else:
                        self.grid[y][x] = 10  # Floor inside

        # Show target pattern in display
        for (target_x, target_y, color) in self.target_pattern_3:
            # Translate to display coords
            offset_x = target_x - zone_x
            offset_y = target_y - zone_y
            display_x = self.target_display_x + offset_x
            display_y = self.target_display_y + offset_y
            self.grid[display_y][display_x] = color

        # Landing zone position (for checking)
        self.landing_zone_x = zone_x
        self.landing_zone_y = zone_y

        # Place solution blocks (scattered OUTSIDE enclosure - zone walls are at 11-16)
        self.grid[5][5] = 2    # Red - top left, far from zone
        self.grid[6][17] = 1   # Blue - right side, outside zone
        self.grid[17][6] = 4   # Yellow - bottom left, outside zone
        self.grid[17][17] = 3  # Green - bottom right, outside zone

        # Place teleporter (yellow rim/red center) - Use grid value 20
        teleporter_x, teleporter_y = 10, 5
        self.grid[teleporter_y][teleporter_x] = 20  # Special value for teleporter
        self.special_blocks[(teleporter_x, teleporter_y)] = {'type': 'teleporter'}
        self.teleporter_pos = (teleporter_x, teleporter_y)

        # Place teleporter mover (red rim/yellow center) - Use grid value 21
        mover_x, mover_y = 12, 7
        self.grid[mover_y][mover_x] = 21  # Special value for teleporter mover
        self.special_blocks[(mover_x, mover_y)] = {'type': 'teleporter_mover'}

        # Player start
        self.player_x = 8
        self.player_y = 5

        # Reset state
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
        return self.grid[y][x] == 5

    def is_block(self, x: int, y: int) -> bool:
        """Check if position has a pushable block."""
        if not self.is_valid_pos(x, y):
            return False
        color = self.grid[y][x]
        # Normal blocks (1-4) + special blocks (20-21)
        if color in [1, 2, 3, 4]:
            return True
        # Special blocks: teleporter (20), teleporter_mover (21)
        if color in [20, 21]:
            # Teleporter only pushable if unlocked
            if color == 20:
                return self.teleporter_unlocked if self.current_level == 3 else False
            # Teleporter mover always pushable
            return True
        return False

    def is_door(self, x: int, y: int) -> bool:
        """Check if position is a door cell."""
        return (x, y) in self.door_cells

    def is_empty_or_floor(self, x: int, y: int) -> bool:
        """Check if position is empty or floor."""
        if not self.is_valid_pos(x, y):
            return False

        # Special case for level 2: if door is open, the closed positions are empty
        if self.current_level == 2 and self.door_open:
            if (x, y) in self.door_closed_positions:
                return True

        color = self.grid[y][x]
        # Empty, floor (10), triggers (7=gravity, 8=door)
        return color == 0 or color == 10 or color == 7 or color == 8

    def is_in_target_display(self, x: int, y: int) -> bool:
        """Check if position is in target display area."""
        if self.current_level == 1:
            return (self.target_display_x - 1 <= x <= self.target_display_x + 2 and
                    self.target_display_y - 1 <= y <= self.target_display_y + 2)
        elif self.current_level == 2:
            # 4x1 target display
            return (self.target_display_x <= x < self.target_display_x + 4 and
                    y == self.target_display_y)
        elif self.current_level == 3:
            # 6x6 target display (4x4 interior + 1 cell frame on each side)
            return (self.target_display_x - 1 <= x < self.target_display_x + 5 and
                    self.target_display_y - 1 <= y < self.target_display_y + 5)
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

    def try_teleport(self, x: int, y: int, dx: int, dy: int, is_player: bool = False) -> Optional[Tuple[int, int]]:
        """Try to teleport entity 4 spaces in direction (dx, dy). Returns target position or None."""
        if self.current_level != 3:
            return None

        # Only teleport if on teleporter
        if self.grid[y][x] != 20:  # Not on teleporter
            return None

        # Calculate target position (4 spaces away, ignoring walls)
        target_x = x + (dx * 4)
        target_y = y + (dy * 4)

        # Check if target is valid and empty (or landing zone)
        if not self.is_valid_pos(target_x, target_y):
            return None

        # Can land on empty space, floor, or landing zone
        target_cell = self.grid[target_y][target_x]
        if target_cell in [0, 10] or self.is_landing_zone_pos(target_x, target_y):
            return (target_x, target_y)

        return None

    def check_teleporter_mover_collision(self, x: int, y: int):
        """Check if teleporter mover pushed into teleporter - unlocks teleporter."""
        if self.current_level != 3:
            return

        # Check if this position is the teleporter and something pushed onto it
        if (x, y) == self.teleporter_pos:
            # If mover was pushed onto teleporter, unlock it
            if self.grid[y][x] == 21:  # Teleporter mover
                self.teleporter_unlocked = True
                # Remove mover (consumed by interaction)
                self.grid[y][x] = 20  # Just teleporter remains
                if (x, y) in self.special_blocks and self.special_blocks[(x, y)]['type'] == 'teleporter_mover':
                    del self.special_blocks[(x, y)]

    def move_player(self, direction: Direction):
        """Move player with push mechanics."""
        if self.won or self.lost:
            return  # Can't move during win/loss

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

                # Update special blocks dict if moving special block
                if (new_x, new_y) in self.special_blocks:
                    block_data = self.special_blocks[(new_x, new_y)]
                    del self.special_blocks[(new_x, new_y)]
                    self.special_blocks[(behind_x, behind_y)] = block_data
                    # Update teleporter position if moving teleporter
                    if block_data['type'] == 'teleporter':
                        self.teleporter_pos = (behind_x, behind_y)

                # Clear old position
                if self.is_landing_zone_pos(new_x, new_y):
                    self.grid[new_y][new_x] = 10
                elif (new_x, new_y) == (self.gravity_trigger_x, self.gravity_trigger_y):
                    self.grid[new_y][new_x] = 7  # Restore trigger
                elif (new_x, new_y) == (self.door_trigger_x, self.door_trigger_y):
                    self.grid[new_y][new_x] = 8  # Restore trigger
                elif (new_x, new_y) == self.teleporter_pos and self.current_level == 3:
                    self.grid[new_y][new_x] = 20  # Restore teleporter if block pushed off it
                else:
                    self.grid[new_y][new_x] = 0

                # Move player
                self.player_x = new_x
                self.player_y = new_y

                # Level 3: Check teleporter mover collision (unlocks teleporter)
                if self.current_level == 3:
                    self.check_teleporter_mover_collision(behind_x, behind_y)

                    # Check if block landed on teleporter - try to teleport it
                    teleport_result = self.try_teleport(behind_x, behind_y, dx, dy, is_player=False)
                    if teleport_result:
                        teleport_x, teleport_y = teleport_result
                        # Move block to teleport destination
                        self.grid[teleport_y][teleport_x] = block_color
                        # Clear block from behind position
                        if self.is_landing_zone_pos(behind_x, behind_y):
                            self.grid[behind_y][behind_x] = 10
                        elif (behind_x, behind_y) == self.teleporter_pos:
                            self.grid[behind_y][behind_x] = 20  # Restore teleporter
                        else:
                            self.grid[behind_y][behind_x] = 0

                self.check_game_state()
            return

        # Normal movement
        if self.is_empty_or_floor(new_x, new_y) or (self.current_level == 3 and self.grid[new_y][new_x] == 20):
            self.player_x = new_x
            self.player_y = new_y

            # Check triggers (level 2)
            if self.current_level == 2:
                if new_x == self.gravity_trigger_x and new_y == self.gravity_trigger_y:
                    self.trigger_gravity()
                # Door state is now updated in update() every frame

            # Level 3: Check if player landed on teleporter
            if self.current_level == 3 and self.grid[new_y][new_x] == 20:
                teleport_result = self.try_teleport(new_x, new_y, dx, dy, is_player=True)
                if teleport_result:
                    self.player_x, self.player_y = teleport_result

            self.check_game_state()

    def is_landing_zone_pos(self, x: int, y: int) -> bool:
        """Check if position is in landing zone."""
        if self.current_level == 1:
            return (self.landing_zone_x <= x < self.landing_zone_x + 2 and
                    self.landing_zone_y <= y < self.landing_zone_y + 2)
        elif self.current_level == 2:
            return (self.landing_zone_x <= x < self.landing_zone_x + 4 and
                    y == self.landing_zone_y)
        elif self.current_level == 3:
            # 4x4 zone
            return (self.landing_zone_x <= x < self.landing_zone_x + 4 and
                    self.landing_zone_y <= y < self.landing_zone_y + 4)
        return False

    def lift_block(self):
        """Lift block (SPACE key). Above=both up, beside=block only up."""
        if self.won or self.lost:
            return  # Can't lift during win/loss

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
        """Start animated gravity fall."""
        if self.gravity_active:
            return  # Already falling

        # Find all blocks and their target positions
        self.falling_blocks = []
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if self.is_block(x, y) and not self.is_in_target_display(x, y):
                    color = self.grid[y][x]

                    # Find lowest empty position in this column
                    fall_y = y
                    for check_y in range(y + 1, self.grid_size):
                        if self.is_empty_or_floor(x, check_y):
                            fall_y = check_y
                        elif self.is_door(x, check_y) and self.door_open:
                            fall_y = check_y
                        else:
                            break

                    # Only add if it will actually fall
                    if fall_y > y:
                        self.falling_blocks.append({
                            'x': x,
                            'current_y': y,
                            'target_y': fall_y,
                            'color': color
                        })

                        # Clear old position
                        if self.is_landing_zone_pos(x, y):
                            self.grid[y][x] = 10
                        elif (x, y) == (self.gravity_trigger_x, self.gravity_trigger_y):
                            self.grid[y][x] = 7
                        elif (x, y) == (self.door_trigger_x, self.door_trigger_y):
                            self.grid[y][x] = 8
                        else:
                            self.grid[y][x] = 0

        if self.falling_blocks:
            self.gravity_active = True
            self.last_fall_time = pygame.time.get_ticks()

    def update_door_state(self):
        """Update door based on player position (only open when standing on trigger)."""
        # Check if door should be open
        should_be_open = (self.player_x == self.door_trigger_x and
                         self.player_y == self.door_trigger_y)

        # Only update if state changed
        if should_be_open != self.door_open:
            self.door_open = should_be_open

            if self.door_open:
                # Slide door to the right
                for i in range(6):
                    x_old, y_old = self.door_closed_positions[i]
                    x_new, y_new = self.door_open_positions[i]

                    # Clear old position (only if no block there)
                    if not self.is_block(x_old, y_old):
                        self.grid[y_old][x_old] = 0

                    # Place at new position
                    if self.is_valid_pos(x_new, y_new):
                        self.grid[y_new][x_new] = 9  # Brown

                # Update door_cells to new positions
                self.door_cells = list(self.door_open_positions)
            else:
                # Slide door back to closed position
                for i in range(6):
                    x_old, y_old = self.door_open_positions[i]
                    x_new, y_new = self.door_closed_positions[i]

                    # Clear old position
                    if self.is_valid_pos(x_old, y_old):
                        self.grid[y_old][x_old] = 0

                    # Place at new position (only if no block there)
                    if not self.is_block(x_new, y_new):
                        self.grid[y_new][x_new] = 9  # Brown

                # Update door_cells to closed positions
                self.door_cells = list(self.door_closed_positions)

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

        elif self.current_level == 3:
            # Check non-contiguous 4-block pattern
            match = True
            for (target_x, target_y, expected_color) in self.target_pattern_3:
                actual = self.grid[target_y][target_x]
                if actual != expected_color:
                    match = False
                    break

            if match:
                self.won = True
                self.flash_timer = pygame.time.get_ticks()
                self.completed_levels.add(3)

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

        # Update door state (level 2)
        if self.current_level == 2:
            self.update_door_state()

        # Animate gravity fall
        if self.gravity_active and self.falling_blocks:
            if current_time - self.last_fall_time >= self.fall_interval:
                # Move each block down one cell (check dynamically if can continue)
                all_finished = True
                for block in self.falling_blocks:
                    x = block['x']
                    y = block['current_y']

                    # Check if can fall further (check cell below)
                    next_y = y + 1
                    can_fall = False

                    if self.is_valid_pos(x, next_y):
                        # Can fall if next position is empty/floor OR in landing zone
                        if self.is_empty_or_floor(x, next_y) or self.is_landing_zone_pos(x, next_y):
                            can_fall = True

                    if can_fall:
                        # Clear current position
                        if self.is_landing_zone_pos(x, y):
                            self.grid[y][x] = 10
                        elif (x, y) == (self.gravity_trigger_x, self.gravity_trigger_y):
                            self.grid[y][x] = 7
                        elif (x, y) == (self.door_trigger_x, self.door_trigger_y):
                            self.grid[y][x] = 8
                        else:
                            self.grid[y][x] = 0

                        # Move down one cell
                        block['current_y'] = next_y

                        # Place at new position
                        self.grid[next_y][x] = block['color']
                        all_finished = False

                if all_finished:
                    self.gravity_active = False
                    self.falling_blocks = []
                    self.check_game_state()
                else:
                    self.last_fall_time = current_time

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

    def draw_control_panel(self):
        """Draw control panel at bottom with keyboard layout."""
        # Black background for control panel
        panel_rect = pygame.Rect(0, self.grid_height, self.screen_width, self.control_panel_height)
        pygame.draw.rect(self.screen, (0, 0, 0), panel_rect)

        # Only show for level 2+
        if self.current_level >= 2:
            # Key dimensions
            key_size = 40
            key_spacing = 5

            # Center the keyboard horizontally
            keyboard_width = key_size * 3 + key_spacing * 2
            start_x = (self.screen_width - keyboard_width) // 2
            start_y = self.grid_height + 10

            # Keyboard layout: [SPACE]    [↑]
            #                          [←] [↓] [→]

            # Space bar on LEFT side
            space_width = 120
            space_height = 50
            space_x = start_x - space_width - 20  # To the left of arrows
            space_y = start_y + 20
            space_rect = pygame.Rect(space_x, space_y, space_width, space_height)
            pygame.draw.rect(self.screen, (60, 60, 60), space_rect)
            pygame.draw.rect(self.screen, (200, 200, 200), space_rect, 2)

            # Up arrow (middle, top row)
            up_x = start_x + key_size + key_spacing
            up_y = start_y
            up_rect = pygame.Rect(up_x, up_y, key_size, key_size)
            pygame.draw.rect(self.screen, (60, 60, 60), up_rect)
            pygame.draw.rect(self.screen, (200, 200, 200), up_rect, 2)
            self.draw_arrow_up(up_x, up_y, key_size)

            # Left arrow (left, bottom row)
            left_x = start_x
            left_y = start_y + key_size + key_spacing
            left_rect = pygame.Rect(left_x, left_y, key_size, key_size)
            pygame.draw.rect(self.screen, (60, 60, 60), left_rect)
            pygame.draw.rect(self.screen, (200, 200, 200), left_rect, 2)
            self.draw_arrow_left(left_x, left_y, key_size)

            # Down arrow (middle, bottom row)
            down_x = start_x + key_size + key_spacing
            down_y = start_y + key_size + key_spacing
            down_rect = pygame.Rect(down_x, down_y, key_size, key_size)
            pygame.draw.rect(self.screen, (60, 60, 60), down_rect)
            pygame.draw.rect(self.screen, (200, 200, 200), down_rect, 2)
            self.draw_arrow_down(down_x, down_y, key_size)

            # Right arrow (right, bottom row)
            right_x = start_x + (key_size + key_spacing) * 2
            right_y = start_y + key_size + key_spacing
            right_rect = pygame.Rect(right_x, right_y, key_size, key_size)
            pygame.draw.rect(self.screen, (60, 60, 60), right_rect)
            pygame.draw.rect(self.screen, (200, 200, 200), right_rect, 2)
            self.draw_arrow_right(right_x, right_y, key_size)

    def draw_arrow_up(self, x, y, size):
        """Draw up arrow symbol."""
        cx = x + size // 2
        cy = y + size // 2
        # Triangle pointing up
        points = [(cx, cy - 10), (cx - 8, cy + 5), (cx + 8, cy + 5)]
        pygame.draw.polygon(self.screen, (200, 200, 200), points)

    def draw_arrow_down(self, x, y, size):
        """Draw down arrow symbol."""
        cx = x + size // 2
        cy = y + size // 2
        # Triangle pointing down
        points = [(cx, cy + 10), (cx - 8, cy - 5), (cx + 8, cy - 5)]
        pygame.draw.polygon(self.screen, (200, 200, 200), points)

    def draw_arrow_left(self, x, y, size):
        """Draw left arrow symbol."""
        cx = x + size // 2
        cy = y + size // 2
        # Triangle pointing left
        points = [(cx - 10, cy), (cx + 5, cy - 8), (cx + 5, cy + 8)]
        pygame.draw.polygon(self.screen, (200, 200, 200), points)

    def draw_arrow_right(self, x, y, size):
        """Draw right arrow symbol."""
        cx = x + size // 2
        cy = y + size // 2
        # Triangle pointing right
        points = [(cx + 10, cy), (cx - 5, cy - 8), (cx - 5, cy + 8)]
        pygame.draw.polygon(self.screen, (200, 200, 200), points)

    def draw(self):
        """Draw the game."""
        self.screen.fill(ARC_COLORS[0])

        # Draw grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size,
                                 self.cell_size, self.cell_size)

                cell_value = self.grid[y][x]

                # Handle special blocks (Level 3)
                if cell_value == 20:  # Teleporter (yellow rim, red center)
                    pygame.draw.rect(self.screen, ARC_COLORS[4], rect)  # Yellow background
                    inner_rect = rect.inflate(-10, -10)  # Smaller rect for center
                    pygame.draw.rect(self.screen, ARC_COLORS[2], inner_rect)  # Red center
                elif cell_value == 21:  # Teleporter Mover (red rim, yellow center)
                    pygame.draw.rect(self.screen, ARC_COLORS[2], rect)  # Red background
                    inner_rect = rect.inflate(-10, -10)  # Smaller rect for center
                    pygame.draw.rect(self.screen, ARC_COLORS[4], inner_rect)  # Yellow center
                elif cell_value > 0 and cell_value <= 15:
                    pygame.draw.rect(self.screen, ARC_COLORS[cell_value], rect)

                pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)

        # Draw special trigger visuals (level 2)
        if self.current_level == 2:
            # Gravity trigger - checkerboard orange/yellow
            grav_rect = pygame.Rect(self.gravity_trigger_x * self.cell_size,
                                   self.gravity_trigger_y * self.cell_size,
                                   self.cell_size, self.cell_size)
            half_cell = self.cell_size // 2
            # Top-left: orange
            pygame.draw.rect(self.screen, ARC_COLORS[7],
                           (grav_rect.x, grav_rect.y, half_cell, half_cell))
            # Top-right: yellow
            pygame.draw.rect(self.screen, ARC_COLORS[4],
                           (grav_rect.x + half_cell, grav_rect.y, half_cell, half_cell))
            # Bottom-left: yellow
            pygame.draw.rect(self.screen, ARC_COLORS[4],
                           (grav_rect.x, grav_rect.y + half_cell, half_cell, half_cell))
            # Bottom-right: orange
            pygame.draw.rect(self.screen, ARC_COLORS[7],
                           (grav_rect.x + half_cell, grav_rect.y + half_cell, half_cell, half_cell))

            # Door trigger - checkerboard sky blue/light blue
            door_rect = pygame.Rect(self.door_trigger_x * self.cell_size,
                                   self.door_trigger_y * self.cell_size,
                                   self.cell_size, self.cell_size)
            # Top-left: sky blue
            pygame.draw.rect(self.screen, ARC_COLORS[8],
                           (door_rect.x, door_rect.y, half_cell, half_cell))
            # Top-right: light blue
            pygame.draw.rect(self.screen, ARC_COLORS[15],
                           (door_rect.x + half_cell, door_rect.y, half_cell, half_cell))
            # Bottom-left: light blue
            pygame.draw.rect(self.screen, ARC_COLORS[15],
                           (door_rect.x, door_rect.y + half_cell, half_cell, half_cell))
            # Bottom-right: sky blue
            pygame.draw.rect(self.screen, ARC_COLORS[8],
                           (door_rect.x + half_cell, door_rect.y + half_cell, half_cell, half_cell))

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
        elif self.current_level == 3:
            # 4x4 zone + walls (6x6 total)
            zone_rect = pygame.Rect((self.landing_zone_x - 1) * self.cell_size,
                                   (self.landing_zone_y - 1) * self.cell_size,
                                   6 * self.cell_size, 6 * self.cell_size)
            pygame.draw.rect(self.screen, ARC_COLORS[8], zone_rect, 3)

        # Highlight target display (matches landing zone)
        if self.current_level == 1:
            target_rect = pygame.Rect((self.target_display_x - 1) * self.cell_size,
                                     (self.target_display_y - 1) * self.cell_size,
                                     4 * self.cell_size, 4 * self.cell_size)
            pygame.draw.rect(self.screen, ARC_COLORS[8], target_rect, 3)
        elif self.current_level == 2:
            # Match landing zone exactly: 4x1 with sky blue border
            target_rect = pygame.Rect(self.target_display_x * self.cell_size,
                                     self.target_display_y * self.cell_size,
                                     4 * self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, ARC_COLORS[8], target_rect, 3)
        elif self.current_level == 3:
            # 4x4 target display with frame (6x6 total)
            target_rect = pygame.Rect((self.target_display_x - 1) * self.cell_size,
                                     (self.target_display_y - 1) * self.cell_size,
                                     6 * self.cell_size, 6 * self.cell_size)
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

        # Draw UI (level counter)
        self.draw_ui()

        # Draw control panel at bottom
        self.draw_control_panel()

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
