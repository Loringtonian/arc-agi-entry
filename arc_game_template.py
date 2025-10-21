#!/usr/bin/env python3
"""
ARC-AGI-3 Game Template v2.0

⚠️ DISCLAIMER: This template includes SPECULATION, not just official requirements

OFFICIAL REQUIREMENTS (from arcprize.org):
- ✅ No text during gameplay
- ✅ Core knowledge priors only (no language/culture/trivia)
- ✅ Human accessible (<1 min to learn, 5-10 min to play)
- ✅ Deterministic behavior

SPECULATION (from agent API, NOT official game requirements):
- 🟡 16-color palette (mentioned for agents, not explicitly required for games)
- 🟡 7-action framework (AGENT API, games can use whatever controls work)
- 🟡 Grid sizes (64×64 max from agent docs, not explicit game requirement)

This template is USEFUL for building agent-compatible games, but you can submit
games without following this exact structure. See OFFICIAL_REQUIREMENTS.md.
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

    venv_python = os.path.join(parent_dir, ".venv", "bin", "python")

    if os.path.exists(venv_python):
        os.execv(venv_python, [venv_python, __file__] + sys.argv[1:])
    else:
        print(f"Error: pygame not found and virtual environment not available at {venv_python}")
        sys.exit(1)

# ARC-AGI-3 OFFICIAL 16-COLOR PALETTE (indices 0-15)
# DO NOT MODIFY - This is the official ARC color specification
ARC_COLORS = {
    # Original 10 ARC colors (0-9)
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

    # Extended 6 colors for ARC-AGI-3 (10-15)
    10: (87, 117, 144),   # Slate Gray
    11: (255, 195, 160),  # Peach
    12: (180, 255, 180),  # Light Green
    13: (255, 255, 200),  # Cream
    14: (220, 160, 220),  # Lavender
    15: (160, 220, 255)   # Light Blue
}

class Direction(Enum):
    """4 directional movement (maps to ACTION1-4)."""
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Action(Enum):
    """
    ARC-AGI-3 Official Action Framework

    Your game should implement relevant subset of these:
    - RESET: Always required (restart level)
    - ACTION1-4: Typically movement (Up/Down/Left/Right)
    - ACTION5: General interaction (activate, select, rotate, etc.)
    - ACTION6: Click/target with X,Y coordinates (optional)
    - ACTION7: Undo previous action (optional)
    """
    RESET = "reset"
    ACTION1 = "up"      # Typically: Move Up
    ACTION2 = "down"    # Typically: Move Down
    ACTION3 = "left"    # Typically: Move Left
    ACTION4 = "right"   # Typically: Move Right
    ACTION5 = "interact"  # General interaction
    ACTION6 = "click"    # Click at position (requires x, y)
    ACTION7 = "undo"     # Undo (optional)

class GameTemplate:
    """
    ARC-AGI-3 Compliant Game Template

    DESIGN CONSTRAINTS (Official ARC-AGI-3):
    - Human learns in < 1 minute
    - Playable in 5-10 minutes
    - No text/instructions required
    - Uses only core knowledge priors (no language/trivia/culture)
    - Deterministic behavior
    - Square grid only (8×8 to 64×64)
    - Resists brute-force (requires reasoning)

    TODO CHECKLIST:
    1. Change self.grid_size to your desired size (8-64)
    2. Change pygame.display.set_caption("Your Game Name")
    3. Implement setup_level() with your level design
    4. Implement game-specific logic in move_player() or update()
    5. Implement check_game_state() with your win/loss conditions
    6. (Optional) Implement handle_interaction() if using ACTION5
    7. (Optional) Implement handle_click() if using ACTION6
    8. (Optional) Implement undo system if using ACTION7
    9. Test that game is learnable without instructions
    10. Document in GAME_SPEC.md
    """

    def __init__(self):
        pygame.init()

        # ===== GAME SETTINGS - CUSTOMIZE THESE =====

        # Grid size - MUST BE SQUARE (8×8 to 64×64)
        self.grid_size = 12  # Change this to your desired size
        self.cell_size = 40  # Adjust for visibility (smaller grid = larger cells)

        # Game caption - Change this to your game name
        pygame.display.set_caption("ARC Game")

        # FPS - Adjust based on your game mechanics
        self.fps = 10  # Slower for turn-based, faster for real-time

        # ===== END CUSTOMIZABLE SETTINGS =====

        # Screen setup
        self.screen_width = self.grid_size * self.cell_size
        self.screen_height = self.grid_size * self.cell_size
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))

        # Game state
        self.clock = pygame.time.Clock()
        self.running = True

        # Grid (initialize as empty - black background)
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        # Player position (if your game has an agent)
        self.player_x = 1
        self.player_y = 1

        # Win/Loss state - MANDATORY
        self.won = False
        self.lost = False
        self.flash_timer = 0
        self.flash_duration = 1000  # ms

        # NOTE: Official agent API uses these state names (from docs.arcprize.org/games):
        #   - "NOT_FINISHED" (game in progress)
        #   - "WIN" (player succeeded)
        #   - "GAME_OVER" (player failed or action limit reached)
        # This template uses simplified booleans (won/lost) which is fine for human play.
        # If targeting agent compatibility, map these to official states in your adapter.

        # Action history for undo (optional - only if implementing ACTION7)
        self.action_history: List[Dict] = []
        self.max_history = 50  # Limit undo depth

        # Setup level
        self.setup_level()

    def setup_level(self):
        """
        Setup the game level.

        TODO: Replace this with your game-specific level design.

        Examples:
        - Procedurally generate obstacles
        - Place goal markers
        - Initialize game-specific state
        - Ensure level is solvable
        """
        # Clear grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                self.grid[y][x] = 0

        # Example: Add borders
        for x in range(self.grid_size):
            self.grid[0][x] = 1  # Top wall (blue)
            self.grid[self.grid_size-1][x] = 1  # Bottom wall
        for y in range(self.grid_size):
            self.grid[y][0] = 1  # Left wall
            self.grid[y][self.grid_size-1] = 1  # Right wall

        # TODO: Add your game-specific setup here
        # Example: Place goal
        # self.grid[self.grid_size-2][self.grid_size-2] = 4  # Yellow goal

        # Reset player
        self.player_x = 1
        self.player_y = 1

        # Reset game state
        self.won = False
        self.lost = False
        self.flash_timer = 0

        # Clear action history
        self.action_history.clear()

    # ===== HELPER METHODS =====

    def is_valid_pos(self, x: int, y: int) -> bool:
        """Check if position is within grid bounds."""
        return 0 <= x < self.grid_size and 0 <= y < self.grid_size

    def can_move_to(self, x: int, y: int) -> bool:
        """
        Check if position is valid and not blocked.

        TODO: Customize this based on your game's movement rules.
        """
        if not self.is_valid_pos(x, y):
            return False
        # Example: Wall is color 1 (blue)
        return self.grid[y][x] != 1

    def save_state_for_undo(self):
        """
        Save current game state for undo functionality.
        Only needed if implementing ACTION7 (undo).
        """
        state = {
            'grid': [row[:] for row in self.grid],  # Deep copy
            'player_x': self.player_x,
            'player_y': self.player_y,
            # TODO: Add any other state variables your game needs to track
        }
        self.action_history.append(state)

        # Limit history size
        if len(self.action_history) > self.max_history:
            self.action_history.pop(0)

    def undo_last_action(self):
        """
        Undo the last action (ACTION7).
        Only implement if your game supports undo.
        """
        if not self.action_history or self.won or self.lost:
            return

        state = self.action_history.pop()
        self.grid = state['grid']
        self.player_x = state['player_x']
        self.player_y = state['player_y']
        # TODO: Restore any other state variables

    # ===== ACTION HANDLERS =====

    def move_player(self, direction: Direction):
        """
        ACTION1-4: Move player in given direction.

        TODO: Customize movement behavior for your game.

        Examples:
        - Simple movement (current implementation)
        - Push-block mechanics (Sokoban-style)
        - Momentum glide (continue until wall)
        - Wrap-around (toroidal grid)
        """
        if self.won or self.lost:
            return

        # Save state for undo (optional)
        # self.save_state_for_undo()

        dx, dy = direction.value
        new_x = self.player_x + dx
        new_y = self.player_y + dy

        if self.can_move_to(new_x, new_y):
            self.player_x = new_x
            self.player_y = new_y

            # TODO: Add your game logic here
            # Examples:
            # - Collect items
            # - Trigger switches
            # - Update game state
            # - Check for interactions with other objects

            self.check_game_state()

    def handle_interaction(self):
        """
        ACTION5: General interaction key.

        TODO: Implement if your game needs an action besides movement.

        Examples:
        - Activate switch at current position
        - Pick up/drop item
        - Rotate object
        - Fire projectile
        - Execute special ability
        """
        if self.won or self.lost:
            return

        # Save state for undo (optional)
        # self.save_state_for_undo()

        # TODO: Implement your interaction logic
        # Example: Toggle cell color at player position
        # current_color = self.grid[self.player_y][self.player_x]
        # self.grid[self.player_y][self.player_x] = (current_color + 1) % 10

        self.check_game_state()

    def handle_click(self, grid_x: int, grid_y: int):
        """
        ACTION6: Click at grid position (optional).

        TODO: Implement if your game uses position targeting.

        Examples:
        - Click to place object
        - Click to select target
        - Click to activate distant object

        Note: Mouse input maps to ACTION6 in ARC-AGI-3 spec.
        """
        if self.won or self.lost:
            return

        if not self.is_valid_pos(grid_x, grid_y):
            return

        # Save state for undo (optional)
        # self.save_state_for_undo()

        # TODO: Implement your click logic
        # Example: Change clicked cell color
        # self.grid[grid_y][grid_x] = 4  # Yellow

        self.check_game_state()

    def check_game_state(self):
        """
        Check for win/loss conditions.

        MANDATORY: Every game MUST have clear win and loss conditions.
        When win/loss occurs, set self.won = True or self.lost = True
        and set self.flash_timer = pygame.time.get_ticks()

        TODO: Replace these examples with your actual win/loss conditions.

        Examples:
        - Win: Reach goal position
        - Win: Collect all items
        - Win: Match target pattern
        - Win: Clear all enemies
        - Lose: Touch hazard
        - Lose: Run out of moves/energy
        - Lose: Exceed time limit
        """

        # Example win condition: Reach bottom-right corner
        if self.player_x == self.grid_size - 2 and self.player_y == self.grid_size - 2:
            self.won = True
            self.flash_timer = pygame.time.get_ticks()

        # Example loss condition: Touch red cell
        if self.grid[self.player_y][self.player_x] == 2:  # Red = hazard
            self.lost = True
            self.flash_timer = pygame.time.get_ticks()

    def reset_game(self):
        """RESET: Restart the game."""
        self.setup_level()

    def update(self, dt: float):
        """
        Update game state (called every frame).

        TODO: Add your update logic here if needed.

        Examples:
        - Move NPCs/enemies
        - Update animations
        - Progress timers
        - Apply physics
        - Check automatic state changes
        """
        current_time = pygame.time.get_ticks()

        # Handle win/loss timing - DO NOT MODIFY
        if (self.won or self.lost) and self.flash_timer > 0:
            if current_time - self.flash_timer > self.flash_duration:
                self.reset_game()

        # TODO: Add your update logic here

    def draw(self):
        """
        Draw the game.

        NO TEXT ALLOWED - Pure visual communication only.

        TODO: Customize rendering for your game.
        """
        self.screen.fill(ARC_COLORS[0])  # Black background

        # Draw grid cells
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                rect = pygame.Rect(x * self.cell_size, y * self.cell_size,
                                 self.cell_size, self.cell_size)

                cell_value = self.grid[y][x]
                if cell_value > 0:
                    pygame.draw.rect(self.screen, ARC_COLORS[cell_value], rect)

                # Grid lines (optional - remove if too cluttered)
                pygame.draw.rect(self.screen, ARC_COLORS[5], rect, 1)

        # Draw player (if your game has one)
        # TODO: Customize player appearance or remove if not needed
        player_rect = pygame.Rect(self.player_x * self.cell_size + 2,
                                self.player_y * self.cell_size + 2,
                                self.cell_size - 4, self.cell_size - 4)
        pygame.draw.rect(self.screen, ARC_COLORS[3], player_rect)  # Green player
        pygame.draw.rect(self.screen, (255, 255, 255), player_rect, 2)

        # NO TEXT - EVER - This is a mandatory ARC-AGI-3 constraint

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
        """
        Handle input events.

        ARC-AGI-3 Action Mapping:
        - ESC: Quit (development only)
        - R: RESET (restart level)
        - WASD/Arrows: ACTION1-4 (movement)
        - SPACE/E: ACTION5 (interaction) - optional
        - Mouse Click: ACTION6 (click position) - optional
        - U/Z: ACTION7 (undo) - optional
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                # ESC: Quit (development only - remove for submission)
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                # RESET: Restart level
                elif event.key == pygame.K_r:
                    self.reset_game()

                # ACTION1-4: Movement (WASD or arrows)
                elif event.key in [pygame.K_w, pygame.K_UP]:
                    self.move_player(Direction.UP)
                elif event.key in [pygame.K_s, pygame.K_DOWN]:
                    self.move_player(Direction.DOWN)
                elif event.key in [pygame.K_a, pygame.K_LEFT]:
                    self.move_player(Direction.LEFT)
                elif event.key in [pygame.K_d, pygame.K_RIGHT]:
                    self.move_player(Direction.RIGHT)

                # ACTION5: Interaction (SPACE or E) - optional
                elif event.key in [pygame.K_SPACE, pygame.K_e]:
                    self.handle_interaction()

                # ACTION7: Undo (U or Z) - optional
                elif event.key in [pygame.K_u, pygame.K_z]:
                    self.undo_last_action()

            # ACTION6: Click (mouse) - optional
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_x, mouse_y = event.pos
                    grid_x = mouse_x // self.cell_size
                    grid_y = mouse_y // self.cell_size
                    self.handle_click(grid_x, grid_y)

    def run(self):
        """Main game loop - DO NOT MODIFY."""
        while self.running:
            dt = self.clock.tick(self.fps)

            self.handle_events()
            self.update(dt)
            self.draw()

            pygame.display.flip()

        pygame.quit()

# ===== ENTRY POINT =====

if __name__ == "__main__":
    # TODO: Change GameTemplate to your game class name
    game = GameTemplate()
    game.run()

# ===== ARC-AGI-3 SUBMISSION CHECKLIST =====
"""
Before submitting your game, verify:

TECHNICAL REQUIREMENTS:
[ ] Grid is square (width = height)
[ ] Grid size is between 8×8 and 64×64
[ ] Uses only colors 0-15 from ARC_COLORS
[ ] All colors have semantic meaning (not decoration)
[ ] Game is deterministic (same input = same output)
[ ] No randomness during gameplay (procedural generation OK)

DESIGN CONSTRAINTS:
[ ] Human can learn in < 1 minute of play
[ ] Playable in 5-10 minutes by competent human
[ ] No text/instructions during gameplay
[ ] Rules discoverable through visual observation only
[ ] Uses only core knowledge priors (no language/culture/trivia)
[ ] Fun and engaging for humans

GAME MECHANICS:
[ ] Clear, visually obvious win condition
[ ] Clear, visually obvious loss condition (if applicable)
[ ] Win/loss triggers green/red flash
[ ] Behavior is consistent and predictable
[ ] Resists brute-force (requires reasoning, not random actions)

ACTION MAPPING:
[ ] Document which ACTION1-7 are used in your GAME_SPEC.md
[ ] RESET always restarts level
[ ] ACTION1-4 mapped (typically movement)
[ ] ACTION5 mapped if needed (interaction)
[ ] ACTION6 mapped if needed (click)
[ ] ACTION7 mapped if needed (undo)

SUBMISSION MATERIALS:
[ ] GAME_SPEC.md created from template
[ ] Demo video of human playthrough
[ ] Screenshots of key moments
[ ] Tested against all constraints above

SUBMIT VIA:
- Form: https://forms.gle/aVD4L4xRaJqJoZvE6
- Discord: https://discord.gg/9b77dPAmcA
- Email: team@arcprize.org
"""
