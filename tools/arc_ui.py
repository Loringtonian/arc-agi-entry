#!/usr/bin/env python3
"""
ARC-AGI-3 Standard UI Components
Provides consistent UI bar matching ARC-AGI website style with text labels
"""

import pygame
from typing import List, Tuple, Optional


class StandardUI:
    """Standard UI bar for ARC-AGI-3 games matching website style."""

    def __init__(self, screen_width: int, screen_height: int,
                 arc_colors: dict,
                 ui_height: int = 50):
        """
        Initialize standard UI.

        Args:
            screen_width: Width of game screen
            screen_height: Height of game screen
            arc_colors: ARC color palette dictionary
            ui_height: Height of UI bar in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.arc_colors = arc_colors
        self.ui_height = ui_height

        # Initialize fonts
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)

        # Which actions are available in this game
        self.has_arrows = True
        self.has_space = False
        self.has_click = False
        self.has_undo = False
        self.has_reset = True

        # Current level
        self.current_level = 1
        self.total_levels = 1

    def set_available_actions(self, arrows=True, space=False, click=False, undo=False, reset=True):
        """Configure which actions are available in this game."""
        self.has_arrows = arrows
        self.has_space = space
        self.has_click = click
        self.has_undo = undo
        self.has_reset = reset

    def set_level(self, current: int, total: Optional[int] = None):
        """Set current level and optionally total levels."""
        self.current_level = current
        if total is not None:
            self.total_levels = total

    def draw(self, surface: pygame.Surface):
        """Draw the standard UI bar at bottom of screen."""
        ui_y = self.screen_height - self.ui_height

        # Background bar
        pygame.draw.rect(surface, self.arc_colors[5],
                        pygame.Rect(0, ui_y, self.screen_width, self.ui_height))
        pygame.draw.line(surface, self.arc_colors[0],
                        (0, ui_y), (self.screen_width, ui_y), 2)

        x_offset = 15
        y_center = ui_y + self.ui_height // 2
        text_color = self.arc_colors[0]  # Black text on gray background

        # Draw available action labels
        if self.has_arrows:
            # Arrow symbols: ↑ ↓ ← →
            arrows_text = "↑ ↓ ← →"
            text_surface = self.font.render(arrows_text, True, text_color)
            text_rect = text_surface.get_rect(midleft=(x_offset, y_center))
            surface.blit(text_surface, text_rect)
            x_offset += text_surface.get_width() + 25

        if self.has_space:
            # "Space" text
            text_surface = self.font.render("Space", True, text_color)
            text_rect = text_surface.get_rect(midleft=(x_offset, y_center))
            surface.blit(text_surface, text_rect)
            x_offset += text_surface.get_width() + 25

        if self.has_click:
            # "Click" text
            text_surface = self.font.render("Click", True, text_color)
            text_rect = text_surface.get_rect(midleft=(x_offset, y_center))
            surface.blit(text_surface, text_rect)
            x_offset += text_surface.get_width() + 25

        if self.has_undo:
            # "Undo" text
            text_surface = self.font.render("Undo", True, text_color)
            text_rect = text_surface.get_rect(midleft=(x_offset, y_center))
            surface.blit(text_surface, text_rect)
            x_offset += text_surface.get_width() + 25

        if self.has_reset:
            # "Try Again" with reset arrow symbol
            text_surface = self.font.render("Try Again ↻", True, text_color)
            text_rect = text_surface.get_rect(midleft=(x_offset, y_center))
            surface.blit(text_surface, text_rect)
            x_offset += text_surface.get_width() + 25

        # Draw level indicator on the right side
        if self.total_levels > 1:
            # Show "Level X/Y" or visual dots
            level_text = f"Level {self.current_level}/{self.total_levels}"
            text_surface = self.small_font.render(level_text, True, text_color)
            text_rect = text_surface.get_rect(midright=(self.screen_width - 15, y_center))
            surface.blit(text_surface, text_rect)
        elif self.total_levels == 1:
            # Single level - show nothing or just current level
            pass

    def get_ui_rect(self) -> pygame.Rect:
        """Get the rectangle occupied by the UI bar."""
        return pygame.Rect(0, self.screen_height - self.ui_height,
                          self.screen_width, self.ui_height)

    def get_play_area_height(self) -> int:
        """Get the height available for game play (excluding UI bar)."""
        return self.screen_height - self.ui_height
