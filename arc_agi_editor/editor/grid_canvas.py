"""Grid canvas widget for ARC AGI Editor.

Provides a visual grid interface for drawing and editing ARC grids.
"""

import tkinter as tk
from tkinter import Canvas
from typing import Callable, Optional, Tuple
from .grid_model import Grid
from .utils import get_color_hex


class GridCanvas(Canvas):
    """A canvas widget for displaying and editing ARC grids."""
    
    def __init__(self, parent, grid: Grid, cell_size: int = 30, 
                 on_cell_change: Optional[Callable[[int, int, str], None]] = None):
        """Initialize the grid canvas.
        
        Args:
            parent: Parent widget
            grid: Grid model to display
            cell_size: Size of each cell in pixels
            on_cell_change: Callback when a cell is changed (x, y, interaction_type)
        """
        self.grid = grid
        self.cell_size = cell_size
        self.on_cell_change = on_cell_change
        
        # Calculate canvas size
        canvas_width = grid.width * cell_size
        canvas_height = grid.height * cell_size
        
        super().__init__(parent, width=canvas_width, height=canvas_height, 
                         bg="white", highlightthickness=2, highlightbackground="black")
        
        # Bind mouse events
        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<Motion>", self._on_hover)
        
        # Track mouse state
        self._is_dragging = False
        self._last_cell = None
        self._hover_cell = None
        self._hover_rect = None
        
        # Draw initial grid
        self.refresh()
    
    def refresh(self):
        """Refresh the entire canvas display."""
        self.delete("all")
        self._draw_grid()
        self._draw_cells()
    
    def _draw_grid(self):
        """Draw the grid lines."""
        # Vertical lines
        for x in range(self.grid.width + 1):
            x_pos = x * self.cell_size
            self.create_line(x_pos, 0, x_pos, self.grid.height * self.cell_size, 
                           fill="gray", width=1, tags="gridline")
        
        # Horizontal lines
        for y in range(self.grid.height + 1):
            y_pos = y * self.cell_size
            self.create_line(0, y_pos, self.grid.width * self.cell_size, y_pos, 
                           fill="gray", width=1, tags="gridline")
    
    def _draw_cells(self):
        """Draw all cells with their current colors."""
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                self._draw_cell(x, y)
    
    def _draw_cell(self, x: int, y: int):
        """Draw a single cell.
        
        Args:
            x: Cell x coordinate
            y: Cell y coordinate
        """
        if not (0 <= x < self.grid.width and 0 <= y < self.grid.height):
            return
        
        cell_value = self.grid.get(x, y)
        color = get_color_hex(cell_value)
        
        # Calculate pixel coordinates
        x1 = x * self.cell_size + 1
        y1 = y * self.cell_size + 1
        x2 = (x + 1) * self.cell_size - 1
        y2 = (y + 1) * self.cell_size - 1
        
        # Draw cell rectangle
        self.create_rectangle(x1, y1, x2, y2, fill=color, outline="", 
                            tags=f"cell_{x}_{y}")
    
    def _pixel_to_cell(self, pixel_x: int, pixel_y: int) -> Optional[Tuple[int, int]]:
        """Convert pixel coordinates to cell coordinates.
        
        Args:
            pixel_x: Pixel x coordinate
            pixel_y: Pixel y coordinate
            
        Returns:
            Cell coordinates (x, y) or None if out of bounds
        """
        cell_x = pixel_x // self.cell_size
        cell_y = pixel_y // self.cell_size
        
        if 0 <= cell_x < self.grid.width and 0 <= cell_y < self.grid.height:
            return (cell_x, cell_y)
        return None
    
    def _on_click(self, event):
        """Handle mouse click events."""
        cell_coords = self._pixel_to_cell(event.x, event.y)
        if cell_coords:
            self._is_dragging = True
            self._last_cell = cell_coords
            self._handle_cell_interaction(cell_coords[0], cell_coords[1], "click")
    
    def _on_drag(self, event):
        """Handle mouse drag events."""
        if not self._is_dragging:
            return
        
        cell_coords = self._pixel_to_cell(event.x, event.y)
        if cell_coords and cell_coords != self._last_cell:
            self._last_cell = cell_coords
            self._handle_cell_interaction(cell_coords[0], cell_coords[1], "drag")
    
    def _on_hover(self, event):
        """Handle mouse hover events."""
        cell_coords = self._pixel_to_cell(event.x, event.y)
        
        if cell_coords != self._hover_cell:
            # Remove previous hover highlight
            if self._hover_rect:
                self.delete(self._hover_rect)
                self._hover_rect = None
            
            # Add new hover highlight
            if cell_coords:
                x, y = cell_coords
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = (x + 1) * self.cell_size
                y2 = (y + 1) * self.cell_size
                
                self._hover_rect = self.create_rectangle(
                    x1, y1, x2, y2, outline="red", width=2, fill="", tags="hover"
                )
            
            self._hover_cell = cell_coords
    
    def _handle_cell_interaction(self, x: int, y: int, interaction_type: str):
        """Handle cell interaction (click or drag).
        
        Args:
            x: Cell x coordinate
            y: Cell y coordinate
            interaction_type: Type of interaction ("click" or "drag")
        """
        if self.on_cell_change:
            self.on_cell_change(x, y, interaction_type)
    
    def set_cell_value(self, x: int, y: int, value: int):
        """Set a cell value and update the display.
        
        Args:
            x: Cell x coordinate
            y: Cell y coordinate
            value: New cell value
        """
        if not (0 <= x < self.grid.width and 0 <= y < self.grid.height):
            return
        
        self.grid.set(x, y, value)
        
        # Remove old cell display
        self.delete(f"cell_{x}_{y}")
        
        # Draw new cell
        self._draw_cell(x, y)
    
    def flood_fill(self, x: int, y: int, new_color: int):
        """Perform flood fill starting from a cell.
        
        Args:
            x: Starting x coordinate
            y: Starting y coordinate
            new_color: Color to fill with
        """
        if not (0 <= x < self.grid.width and 0 <= y < self.grid.height):
            return
        
        # Store cells that will change for efficient redraw
        old_grid = self.grid.clone()
        
        # Perform flood fill on model
        self.grid.flood_fill(x, y, new_color)
        
        # Redraw only changed cells
        for grid_y in range(self.grid.height):
            for grid_x in range(self.grid.width):
                if old_grid.get(grid_x, grid_y) != self.grid.get(grid_x, grid_y):
                    self.delete(f"cell_{grid_x}_{grid_y}")
                    self._draw_cell(grid_x, grid_y)
    
    def set_grid(self, new_grid: Grid):
        """Set a new grid and refresh the display.
        
        Args:
            new_grid: New grid to display
        """
        self.grid = new_grid
        
        # Update canvas size
        canvas_width = new_grid.width * self.cell_size
        canvas_height = new_grid.height * self.cell_size
        self.config(width=canvas_width, height=canvas_height)
        
        # Refresh display
        self.refresh()
    
    def resize_grid(self, width: int, height: int):
        """Resize the grid and update the display.
        
        Args:
            width: New width
            height: New height
        """
        self.grid.resize(width, height)
        
        # Update canvas size
        canvas_width = width * self.cell_size
        canvas_height = height * self.cell_size
        self.config(width=canvas_width, height=canvas_height)
        
        # Refresh display
        self.refresh()
    
    def get_cell_at_pixel(self, pixel_x: int, pixel_y: int) -> Optional[Tuple[int, int, int]]:
        """Get cell coordinates and value at pixel position.
        
        Args:
            pixel_x: Pixel x coordinate
            pixel_y: Pixel y coordinate
            
        Returns:
            Tuple of (x, y, value) or None if out of bounds
        """
        cell_coords = self._pixel_to_cell(pixel_x, pixel_y)
        if cell_coords:
            x, y = cell_coords
            value = self.grid.get(x, y)
            return (x, y, value)
        return None
    
    def set_cell_size(self, cell_size: int):
        """Set the cell size and refresh the display.
        
        Args:
            cell_size: New cell size in pixels
        """
        self.cell_size = cell_size
        
        # Update canvas size
        canvas_width = self.grid.width * cell_size
        canvas_height = self.grid.height * cell_size
        self.config(width=canvas_width, height=canvas_height)
        
        # Refresh display
        self.refresh()
    
    def clear_hover(self):
        """Clear any hover highlighting."""
        if self._hover_rect:
            self.delete(self._hover_rect)
            self._hover_rect = None
        self._hover_cell = None
    
    def finish_interaction(self):
        """Finish current interaction (e.g., on mouse release)."""
        self._is_dragging = False
        self._last_cell = None
    
    def bind_mouse_release(self, handler):
        """Bind mouse release event handler.
        
        Args:
            handler: Function to call on mouse release
        """
        self.bind("<ButtonRelease-1>", handler)
    
    def bind_leave(self, handler):
        """Bind mouse leave event handler.
        
        Args:
            handler: Function to call when mouse leaves canvas
        """
        self.bind("<Leave>", handler)