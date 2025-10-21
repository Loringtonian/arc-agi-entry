#!/usr/bin/env python3
"""
ARC-AGI-3 Level Editor - Grid Design Tool
Updated October 2025 for full 16-color compliance

A professional level editor for designing ARC-AGI-3 game grids.
Features:
- 16-color palette (ARC-AGI-3 official spec)
- Grid editing up to 64×64
- Paint & Fill tools
- Save/Load in ARC-compatible JSON format
- Adaptive screen resolution support
- High-performance rendering with surfarray
"""

import sys
import os
import json
import pygame
import numpy as np
import math
from typing import Dict, List, Tuple, Optional, Any

# Add our existing modules to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
from arc_agi_editor.editor.grid_model import Grid
from arc_agi_editor.editor.utils import get_color_hex, ARC_COLOR_CODES, ARC_COLORS

class UIElement:
    """Base class for UI elements."""
    def __init__(self, x: int, y: int, width: int, height: int):
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = True
        self.enabled = True
    
    def contains_point(self, pos: Tuple[int, int]) -> bool:
        return self.rect.collidepoint(pos) if self.visible else False
    
    def draw(self, screen: pygame.Surface):
        pass
    
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        return False

class Button(UIElement):
    """Interactive button element."""
    def __init__(self, x: int, y: int, width: int, height: int, text: str, 
                 callback=None, color=(200, 200, 200), text_color=(0, 0, 0)):
        super().__init__(x, y, width, height)
        self.text = text
        self.callback = callback
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.Font(None, 24)
        self.pressed = False
    
    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        
        # Button color based on state
        current_color = self.color
        if self.pressed:
            current_color = tuple(max(0, c - 30) for c in self.color)
        elif not self.enabled:
            current_color = (150, 150, 150)
        
        # Draw button
        pygame.draw.rect(screen, current_color, self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)
        
        # Draw text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        if self.contains_point(pos) and self.enabled:
            self.pressed = True
            if self.callback:
                self.callback()
            return True
        return False
    
    def handle_release(self):
        self.pressed = False

class TextInput(UIElement):
    """Text input field."""
    def __init__(self, x: int, y: int, width: int, height: int, initial_value: str = ""):
        super().__init__(x, y, width, height)
        self.text = initial_value
        self.font = pygame.font.Font(None, 24)
        self.active = False
        self.cursor_pos = len(self.text)
        self.cursor_visible = True
        self.cursor_timer = 0
    
    def draw(self, screen: pygame.Surface):
        if not self.visible:
            return
        
        # Background
        bg_color = (255, 255, 255) if self.active else (240, 240, 240)
        pygame.draw.rect(screen, bg_color, self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)
        
        # Text
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_x = self.rect.x + 5
        text_y = self.rect.y + (self.rect.height - text_surface.get_height()) // 2
        screen.blit(text_surface, (text_x, text_y))
        
        # Cursor
        if self.active and self.cursor_visible:
            cursor_x = text_x + self.font.size(self.text[:self.cursor_pos])[0]
            cursor_y = text_y
            pygame.draw.line(screen, (0, 0, 0), 
                           (cursor_x, cursor_y), 
                           (cursor_x, cursor_y + text_surface.get_height()), 2)
    
    def handle_click(self, pos: Tuple[int, int]) -> bool:
        if self.contains_point(pos):
            self.active = True
            return True
        else:
            self.active = False
            return False
    
    def handle_keydown(self, event) -> bool:
        if not self.active:
            return False
        
        if event.key == pygame.K_BACKSPACE:
            if self.cursor_pos > 0:
                self.text = self.text[:self.cursor_pos-1] + self.text[self.cursor_pos:]
                self.cursor_pos -= 1
        elif event.key == pygame.K_DELETE:
            if self.cursor_pos < len(self.text):
                self.text = self.text[:self.cursor_pos] + self.text[self.cursor_pos+1:]
        elif event.key == pygame.K_LEFT:
            self.cursor_pos = max(0, self.cursor_pos - 1)
        elif event.key == pygame.K_RIGHT:
            self.cursor_pos = min(len(self.text), self.cursor_pos + 1)
        elif event.key == pygame.K_HOME:
            self.cursor_pos = 0
        elif event.key == pygame.K_END:
            self.cursor_pos = len(self.text)
        elif event.unicode.isprintable():
            self.text = self.text[:self.cursor_pos] + event.unicode + self.text[self.cursor_pos:]
            self.cursor_pos += 1
        
        return True
    
    def update(self, dt: float):
        if self.active:
            self.cursor_timer += dt
            if self.cursor_timer >= 500:  # Blink every 500ms
                self.cursor_visible = not self.cursor_visible
                self.cursor_timer = 0

class AdvancedGameEngine:
    """Advanced game engine with full Tkinter editor functionality in Pygame."""
    
    def __init__(self):
        pygame.init()
        
        # Detect screen resolution and set adaptive window size
        self._detect_screen_resolution()
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("ARC-AGI-3 Level Editor v2.0 (16-Color)")
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.LIGHT_GRAY = (200, 200, 200)
        self.DARK_GRAY = (64, 64, 64)
        self.BLUE = (100, 150, 255)
        self.GREEN = (100, 255, 100)
        self.RED = (255, 100, 100)
        self.YELLOW = (255, 255, 100)
        
        # Game state
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60
        
        # Grid and rendering
        self.grid = Grid(8, 8)
        self.calculate_grid_layout()
        
        # Editor state
        self.current_color = 1
        self.current_tool = "paint"
        self.is_dragging = False
        self.last_painted_cell = None
        
        # File management
        self.current_file = None
        self.current_file_name = "Untitled"
        
        # Fonts
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        # Use ARC-AGI-3 16-color palette
        self.arc_colors = ARC_COLORS  # Now includes colors 0-15
        
        # UI Elements
        self.ui_elements = []
        self.setup_ui()
        
        # Scroll offset for large grids
        self.scroll_x = 0
        self.scroll_y = 0
        
        print("🎨 ARC-AGI-3 Level Editor v2.0 initialized!")
        print(f"✅ 16-color palette loaded (ARC-AGI-3 compliant)")
        print(f"Screen: {self.window_width}x{self.window_height}")
        print(f"Grid: {self.grid.width}x{self.grid.height}, Cell size: {self.cell_size}px")
    
    def _detect_screen_resolution(self):
        """Detect screen resolution and set adaptive sizes."""
        # Get screen info
        pygame.init()
        display_info = pygame.display.Info()
        screen_width = display_info.current_w
        screen_height = display_info.current_h
        
        # Calculate adaptive sizes
        self.window_width = min(1400, int(screen_width * 0.85))
        self.window_height = min(1000, int(screen_height * 0.85))
        
        # Base cell size based on screen resolution
        if screen_width >= 2560:  # 4K+
            self.base_cell_size = 28
        elif screen_width >= 1920:  # 1080p
            self.base_cell_size = 24
        elif screen_width >= 1366:  # Standard laptop
            self.base_cell_size = 20
        else:  # Smaller screens
            self.base_cell_size = 16
        
        print(f"Detected screen: {screen_width}x{screen_height}")
        print(f"Window size: {self.window_width}x{self.window_height}")
        print(f"Base cell size: {self.base_cell_size}px")
    
    def calculate_grid_layout(self):
        """Calculate grid layout based on current grid size and available space."""
        # Available space for grid (minus UI panels)
        self.left_panel_width = 320  # Slightly wider to avoid cramping
        self.top_panel_height = 80
        self.status_bar_height = 30
        
        available_width = self.window_width - self.left_panel_width - 40
        available_height = self.window_height - self.top_panel_height - self.status_bar_height - 40
        
        # Calculate cell size to fit available space
        max_cell_width = available_width // self.grid.width
        max_cell_height = available_height // self.grid.height
        optimal_cell_size = min(max_cell_width, max_cell_height, self.base_cell_size)
        
        self.cell_size = max(4, optimal_cell_size)  # Minimum 4px cells
        
        # Grid position
        self.grid_start_x = self.left_panel_width + 20
        self.grid_start_y = self.top_panel_height + 20
        
        print(f"Grid layout: cell_size={self.cell_size}, pos=({self.grid_start_x}, {self.grid_start_y})")
    
    def setup_ui(self):
        """Setup all UI elements with proper spacing."""
        self.ui_elements.clear()
        
        # File operation buttons (top bar)
        button_y = 15
        button_width = 70
        button_height = 25
        button_spacing = 8
        
        x = self.left_panel_width + 20
        self.ui_elements.append(Button(x, button_y, button_width, button_height, "New", 
                                     self.new_file, self.GREEN))
        x += button_width + button_spacing
        self.ui_elements.append(Button(x, button_y, button_width, button_height, "Save", 
                                     self.save_file, self.BLUE))
        x += button_width + button_spacing
        self.ui_elements.append(Button(x, button_y, button_width, button_height, "Load", 
                                     self.load_file, self.YELLOW))
        x += button_width + button_spacing
        self.ui_elements.append(Button(x, button_y, button_width, button_height, "Save As", 
                                     self.save_as_file, self.RED))
        
        # Left panel content - calculate spacing more carefully
        panel_x = 20
        section_spacing = 50
        
        # Start after basic info
        current_y = 140
        
        # Grid size controls section
        self.size_label_y = current_y
        current_y += 25  # Space for title
        
        self.grid_size_input = TextInput(panel_x, current_y, 60, 30, str(self.grid.width))
        self.ui_elements.append(self.grid_size_input)
        
        self.ui_elements.append(Button(panel_x + 70, current_y, 30, 30, "+", 
                                     self.increase_grid_size, self.LIGHT_GRAY))
        self.ui_elements.append(Button(panel_x + 70, current_y + 35, 30, 30, "-", 
                                     self.decrease_grid_size, self.LIGHT_GRAY))
        
        current_y += 75  # Move down past the input controls
        current_y += section_spacing  # Add section spacing
        
        # Tool buttons section
        self.tools_label_y = current_y
        current_y += 25  # Space for title
        
        self.paint_button = Button(panel_x, current_y, 120, 35, "Paint Tool", 
                                  lambda: self.select_tool("paint"), self.GREEN)
        self.ui_elements.append(self.paint_button)
        
        current_y += 40  # Space between tool buttons
        self.fill_button = Button(panel_x, current_y, 120, 35, "Fill Tool", 
                                 lambda: self.select_tool("fill"), self.RED)
        self.ui_elements.append(self.fill_button)
        
        current_y += 40  # Space before clear button
        self.ui_elements.append(Button(panel_x, current_y, 120, 35, "Clear Grid", 
                                     self.clear_grid, self.YELLOW))
        
        current_y += 50  # Space before color palette
        current_y += section_spacing
        
        # Color palette position
        self.palette_label_y = current_y
    
    def get_grid_coordinates(self, mouse_pos: Tuple[int, int]) -> Tuple[Optional[int], Optional[int]]:
        """Convert mouse position to grid coordinates."""
        mouse_x, mouse_y = mouse_pos
        
        # Adjust for scroll offset
        mouse_x += self.scroll_x
        mouse_y += self.scroll_y
        
        # Check if mouse is within grid bounds
        grid_end_x = self.grid_start_x + (self.grid.width * self.cell_size)
        grid_end_y = self.grid_start_y + (self.grid.height * self.cell_size)
        
        if (self.grid_start_x <= mouse_x < grid_end_x and 
            self.grid_start_y <= mouse_y < grid_end_y):
            
            grid_x = (mouse_x - self.grid_start_x) // self.cell_size
            grid_y = (mouse_y - self.grid_start_y) // self.cell_size
            
            return grid_x, grid_y
        
        return None, None
    
    def draw_grid(self):
        """Render the grid using surfarray for performance."""
        grid_width = self.grid.width * self.cell_size
        grid_height = self.grid.height * self.cell_size
        
        # Create grid surface
        grid_surface = pygame.Surface((grid_width, grid_height))
        
        # Use surfarray for fast rendering
        try:
            pixel_array = pygame.surfarray.pixels3d(grid_surface)
            
            for y in range(self.grid.height):
                for x in range(self.grid.width):
                    color_idx = self.grid.get(x, y)
                    color_rgb = self.arc_colors.get(color_idx, self.BLACK)
                    
                    # Fill cell
                    start_x = x * self.cell_size
                    start_y = y * self.cell_size
                    end_x = start_x + self.cell_size
                    end_y = start_y + self.cell_size
                    
                    pixel_array[start_x:end_x, start_y:end_y] = color_rgb
                    
                    # Draw grid lines
                    if self.cell_size > 8:  # Only draw grid lines for larger cells
                        # Vertical lines
                        if x > 0:
                            pixel_array[start_x:start_x+1, start_y:end_y] = self.GRAY
                        # Horizontal lines
                        if y > 0:
                            pixel_array[start_x:end_x, start_y:start_y+1] = self.GRAY
            
            del pixel_array  # Release array
        except Exception as e:
            # Fallback to rect drawing if surfarray fails
            for y in range(self.grid.height):
                for x in range(self.grid.width):
                    color_idx = self.grid.get(x, y)
                    color_rgb = self.arc_colors.get(color_idx, self.BLACK)
                    
                    cell_rect = pygame.Rect(
                        x * self.cell_size, y * self.cell_size,
                        self.cell_size, self.cell_size
                    )
                    pygame.draw.rect(grid_surface, color_rgb, cell_rect)
                    
                    if self.cell_size > 8:
                        pygame.draw.rect(grid_surface, self.GRAY, cell_rect, 1)
        
        # Calculate visible area
        visible_x = max(0, self.scroll_x)
        visible_y = max(0, self.scroll_y)
        visible_width = min(grid_width - visible_x, self.window_width - self.grid_start_x)
        visible_height = min(grid_height - visible_y, self.window_height - self.grid_start_y - self.status_bar_height)
        
        # Blit visible portion to screen
        visible_rect = pygame.Rect(visible_x, visible_y, visible_width, visible_height)
        self.screen.blit(grid_surface, (self.grid_start_x - self.scroll_x, self.grid_start_y - self.scroll_y), visible_rect)
        
        # Draw border
        border_rect = pygame.Rect(
            self.grid_start_x - 2 - self.scroll_x,
            self.grid_start_y - 2 - self.scroll_y,
            min(grid_width + 4, visible_width + 4),
            min(grid_height + 4, visible_height + 4)
        )
        pygame.draw.rect(self.screen, self.DARK_GRAY, border_rect, 2)
    
    def draw_color_palette(self):
        """Draw the color selection palette."""
        palette_x = 20
        palette_y = self.palette_label_y + 30
        color_size = 30
        cols = 2
        
        # Title
        title_text = self.font_medium.render("COLOR PALETTE", True, self.BLACK)
        self.screen.blit(title_text, (palette_x, self.palette_label_y))

        for i in range(16):
            row = i % 8
            col = i // 8

            x = palette_x + col * (color_size + 3)
            y = palette_y + row * (color_size + 3)
            
            color_rgb = self.arc_colors.get(i, self.BLACK)
            
            # Draw color square
            color_rect = pygame.Rect(x, y, color_size, color_size)
            pygame.draw.rect(self.screen, color_rgb, color_rect)
            
            # Highlight selected color
            if i == self.current_color:
                pygame.draw.rect(self.screen, self.WHITE, color_rect, 3)
            else:
                pygame.draw.rect(self.screen, self.DARK_GRAY, color_rect, 1)
    
    def draw_ui(self):
        """Draw all UI elements."""
        # Draw background panels
        # Left panel
        left_panel = pygame.Rect(0, 0, self.left_panel_width, self.window_height)
        pygame.draw.rect(self.screen, self.LIGHT_GRAY, left_panel)
        pygame.draw.line(self.screen, self.DARK_GRAY, 
                        (self.left_panel_width, 0), (self.left_panel_width, self.window_height), 2)
        
        # Top panel
        top_panel = pygame.Rect(0, 0, self.window_width, self.top_panel_height)
        pygame.draw.rect(self.screen, (240, 240, 255), top_panel)
        pygame.draw.line(self.screen, self.DARK_GRAY, 
                        (0, self.top_panel_height), (self.window_width, self.top_panel_height), 2)
        
        # Status bar
        status_y = self.window_height - self.status_bar_height
        status_panel = pygame.Rect(0, status_y, self.window_width, self.status_bar_height)
        pygame.draw.rect(self.screen, (220, 220, 220), status_panel)
        pygame.draw.line(self.screen, self.DARK_GRAY, 
                        (0, status_y), (self.window_width, status_y), 1)
        
        # Draw all UI elements
        for element in self.ui_elements:
            element.draw(self.screen)
        
        # Draw color palette
        self.draw_color_palette()
        
        # Draw info text
        self.draw_info_text()
    
    def draw_info_text(self):
        """Draw informational text."""
        # Title in top panel
        title_text = self.font_large.render("ARC INTERACTIVE GAME ENGINE", True, self.BLACK)
        self.screen.blit(title_text, (self.left_panel_width + 20, 45))
        
        # Left panel info - positioned to not overlap with UI elements
        info_x = 20
        info_y = 100
        
        # Current file
        file_text = self.font_small.render(f"File: {self.current_file_name}", True, self.BLACK)
        self.screen.blit(file_text, (info_x, info_y))
        
        # Current status
        status_text = self.font_small.render(f"Tool: {self.current_tool.title()}", True, self.BLACK)
        self.screen.blit(status_text, (info_x, info_y + 18))
        
        # Grid size label
        size_text = self.font_medium.render("GRID SIZE", True, self.BLACK)
        self.screen.blit(size_text, (info_x, self.size_label_y))
        
        # Tools label
        tools_text = self.font_medium.render("TOOLS", True, self.BLACK)
        self.screen.blit(tools_text, (info_x, self.tools_label_y))
        
        # Status bar text
        status_y = self.window_height - self.status_bar_height + 5
        status_text = f"Ready - Grid: {self.grid.width}x{self.grid.height} | Cell size: {self.cell_size}px | Selected: Color {self.current_color}, {self.current_tool.title()} tool"
        status_surface = self.font_small.render(status_text, True, self.BLACK)
        self.screen.blit(status_surface, (10, status_y))
    
    # Tool selection methods
    def select_tool(self, tool: str):
        """Select a tool."""
        self.current_tool = tool
        
        # Update button appearance
        if tool == "paint":
            self.paint_button.color = (50, 150, 50)
            self.fill_button.color = self.RED
        else:
            self.fill_button.color = (150, 50, 50)
            self.paint_button.color = self.GREEN
        
        print(f"🛠️ Selected {tool} tool")
    
    # Grid modification methods
    def resize_grid(self, new_size: int):
        """Resize the grid to new dimensions."""
        if new_size < 1 or new_size > 64:
            print(f"❌ Grid size {new_size} out of range (1-64)")
            return
        
        old_grid = self.grid
        self.grid = Grid(new_size, new_size)
        
        # Copy existing data
        for y in range(min(new_size, old_grid.height)):
            for x in range(min(new_size, old_grid.width)):
                self.grid.set(x, y, old_grid.get(x, y))
        
        # Recalculate layout
        self.calculate_grid_layout()
        
        print(f"📏 Grid resized to {new_size}x{new_size}")
    
    def increase_grid_size(self):
        """Increase grid size by 1."""
        current_size = self.grid.width
        if current_size < 64:
            new_size = current_size + 1
            self.resize_grid(new_size)
            self.grid_size_input.text = str(new_size)
    
    def decrease_grid_size(self):
        """Decrease grid size by 1."""
        current_size = self.grid.width
        if current_size > 1:
            new_size = current_size - 1
            self.resize_grid(new_size)
            self.grid_size_input.text = str(new_size)
    
    def clear_grid(self):
        """Clear all grid cells."""
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                self.grid.set(x, y, 0)
        print("🧹 Grid cleared")
    
    # File operations (placeholder - will implement with proper dialogs)
    def new_file(self):
        """Create a new file."""
        self.current_file = None
        self.current_file_name = "Untitled"
        self.clear_grid()
        print("📄 New file created")
    
    def save_file(self):
        """Save current file."""
        print("💾 Save file (placeholder)")
    
    def load_file(self):
        """Load a file."""
        print("📂 Load file (placeholder)")
    
    def save_as_file(self):
        """Save file with new name."""
        print("💾 Save as file (placeholder)")
    
    # Event handling
    def handle_click(self, pos: Tuple[int, int]):
        """Handle mouse clicks."""
        # Check UI elements first
        for element in self.ui_elements:
            if element.handle_click(pos):
                return
        
        # Check color palette
        palette_x = 20
        palette_y = self.palette_label_y + 30
        color_size = 30

        for i in range(16):
            row = i % 8
            col = i // 8

            x = palette_x + col * (color_size + 3)
            y = palette_y + row * (color_size + 3)

            if x <= pos[0] <= x + color_size and y <= pos[1] <= y + color_size:
                self.current_color = i
                print(f"🎨 Selected color {i}")
                return
        
        # Check grid clicks
        grid_x, grid_y = self.get_grid_coordinates(pos)
        if grid_x is not None and grid_y is not None:
            self.handle_grid_click(grid_x, grid_y)
    
    def handle_grid_click(self, grid_x: int, grid_y: int):
        """Handle clicks on the grid."""
        if self.current_tool == "paint":
            self.grid.set(grid_x, grid_y, self.current_color)
        elif self.current_tool == "fill":
            self.grid.flood_fill(grid_x, grid_y, self.current_color)
    
    def handle_drag(self, pos: Tuple[int, int]):
        """Handle mouse drag for paint tool."""
        if not self.is_dragging or self.current_tool != "paint":
            return
        
        grid_x, grid_y = self.get_grid_coordinates(pos)
        if grid_x is not None and grid_y is not None:
            current_cell = (grid_x, grid_y)
            if current_cell != self.last_painted_cell:
                self.grid.set(grid_x, grid_y, self.current_color)
                self.last_painted_cell = current_cell
    
    def run(self):
        """Main game loop."""
        print("🚀 Starting advanced game engine...")
        
        while self.running:
            dt = self.clock.tick(self.fps)
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.is_dragging = True
                        self.handle_click(event.pos)
                        grid_x, grid_y = self.get_grid_coordinates(event.pos)
                        if grid_x is not None:
                            self.last_painted_cell = (grid_x, grid_y)
                
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:  # Left click release
                        self.is_dragging = False
                        self.last_painted_cell = None
                        # Handle button releases
                        for element in self.ui_elements:
                            if isinstance(element, Button):
                                element.handle_release()
                
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_drag(event.pos)
                
                elif event.type == pygame.KEYDOWN:
                    # Handle text input
                    handled = False
                    for element in self.ui_elements:
                        if isinstance(element, TextInput):
                            if element.handle_keydown(event):
                                handled = True
                                # Update grid size if it was the size input
                                if element == self.grid_size_input:
                                    try:
                                        new_size = int(element.text)
                                        if 1 <= new_size <= 64:
                                            self.resize_grid(new_size)
                                    except ValueError:
                                        pass
                                break
                    
                    if not handled:
                        # Global shortcuts
                        if pygame.K_0 <= event.key <= pygame.K_9:
                            color_num = event.key - pygame.K_0
                            self.current_color = color_num
                            print(f"🎨 Selected color {color_num}")
                        elif event.key == pygame.K_p:
                            self.select_tool("paint")
                        elif event.key == pygame.K_f:
                            self.select_tool("fill")
                        elif event.key == pygame.K_ESCAPE:
                            self.running = False
            
            # Update UI elements
            for element in self.ui_elements:
                if hasattr(element, 'update'):
                    element.update(dt)
            
            # Clear screen
            self.screen.fill(self.WHITE)
            
            # Draw everything
            self.draw_ui()
            self.draw_grid()
            
            # Update display
            pygame.display.flip()
        
        pygame.quit()
        print("👋 Advanced game engine closed")

if __name__ == "__main__":
    engine = AdvancedGameEngine()
    engine.run()