#!/usr/bin/env python3
"""
Demo of Standard ARC-AGI-3 UI Bar
Shows how the bottom control bar looks
"""

import sys
import os
import pygame

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'tools'))
from arc_agi_editor.editor.utils import ARC_COLORS
from arc_ui import StandardUI

def main():
    pygame.init()

    screen_width = 600
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Standard UI Demo")

    # Create standard UI
    ui = StandardUI(screen_width, screen_height, ARC_COLORS, ui_height=50)

    # Configure which actions are available
    ui.set_available_actions(
        arrows=True,
        space=True,
        click=True,
        undo=True,
        reset=True
    )

    # Set level info
    ui.set_level(current=3, total=5)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                # Demo: cycle through levels with number keys
                elif event.key == pygame.K_1:
                    ui.set_level(1, 5)
                elif event.key == pygame.K_2:
                    ui.set_level(2, 5)
                elif event.key == pygame.K_3:
                    ui.set_level(3, 5)
                elif event.key == pygame.K_4:
                    ui.set_level(4, 5)
                elif event.key == pygame.K_5:
                    ui.set_level(5, 5)

        # Draw
        screen.fill(ARC_COLORS[0])  # Black background

        # Draw some example game content
        for y in range(10):
            for x in range(10):
                rect = pygame.Rect(50 + x * 50, 50 + y * 50, 48, 48)
                color = ARC_COLORS[(x + y) % 10]
                pygame.draw.rect(screen, color, rect)

        # Draw standard UI bar
        ui.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
