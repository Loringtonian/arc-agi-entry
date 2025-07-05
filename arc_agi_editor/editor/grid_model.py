"""Grid data model for ARC AGI Editor.

Provides a Grid class for managing 2D grids with color values 0-9.
Includes operations for resizing, cloning, and flood filling.
"""

from typing import List, Optional, Tuple
import copy


class Grid:
    """A 2D grid of integers representing colors (0-9).
    
    Default size is 8×8, maximum size is 64×64 for extended editor use.
    """
    
    def __init__(self, width: int = 8, height: int = 8, default_value: int = 0):
        """Initialize a new grid.
        
        Args:
            width: Width of the grid (default 8)
            height: Height of the grid (default 8)
            default_value: Default value to fill cells with (default 0)
        """
        if width <= 0 or height <= 0:
            raise ValueError("Grid dimensions must be positive")
        if width > 64 or height > 64:
            raise ValueError("Grid dimensions cannot exceed 64×64")
        if not (0 <= default_value <= 9):
            raise ValueError("Grid values must be between 0-9")
            
        self.width = width
        self.height = height
        self.cells = [[default_value for _ in range(width)] for _ in range(height)]
    
    def get(self, x: int, y: int) -> int:
        """Get the value at position (x, y).
        
        Args:
            x: X coordinate (column)
            y: Y coordinate (row)
            
        Returns:
            The value at the specified position
            
        Raises:
            IndexError: If coordinates are out of bounds
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"Coordinates ({x}, {y}) out of bounds for {self.width}×{self.height} grid")
        return self.cells[y][x]
    
    def set(self, x: int, y: int, value: int) -> None:
        """Set the value at position (x, y).
        
        Args:
            x: X coordinate (column)
            y: Y coordinate (row)
            value: Value to set (0-9)
            
        Raises:
            IndexError: If coordinates are out of bounds
            ValueError: If value is not in range 0-9
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            raise IndexError(f"Coordinates ({x}, {y}) out of bounds for {self.width}×{self.height} grid")
        if not (0 <= value <= 9):
            raise ValueError(f"Value {value} must be between 0-9")
        self.cells[y][x] = value
    
    def resize(self, width: int, height: int, default_value: int = 0) -> None:
        """Resize the grid, preserving existing data where possible.
        
        Args:
            width: New width
            height: New height
            default_value: Value to use for new cells (default 0)
        """
        if width <= 0 or height <= 0:
            raise ValueError("Grid dimensions must be positive")
        if width > 64 or height > 64:
            raise ValueError("Grid dimensions cannot exceed 64×64")
        if not (0 <= default_value <= 9):
            raise ValueError("Default value must be between 0-9")
        
        # Create new grid with default values
        new_cells = [[default_value for _ in range(width)] for _ in range(height)]
        
        # Copy existing data
        for y in range(min(height, self.height)):
            for x in range(min(width, self.width)):
                new_cells[y][x] = self.cells[y][x]
        
        self.width = width
        self.height = height
        self.cells = new_cells
    
    def clone(self) -> 'Grid':
        """Create a deep copy of this grid.
        
        Returns:
            A new Grid instance with the same data
        """
        new_grid = Grid(self.width, self.height)
        new_grid.cells = copy.deepcopy(self.cells)
        return new_grid
    
    def flood_fill(self, x: int, y: int, new_color: int) -> None:
        """Fill a contiguous area of the same color with a new color.
        
        Args:
            x: X coordinate of the starting point
            y: Y coordinate of the starting point
            new_color: Color to fill with (0-9)
        """
        if not (0 <= x < self.width and 0 <= y < self.height):
            return  # Out of bounds, do nothing
        if not (0 <= new_color <= 9):
            raise ValueError(f"Color {new_color} must be between 0-9")
        
        original_color = self.get(x, y)
        if original_color == new_color:
            return  # No change needed
        
        # Use iterative flood fill to avoid recursion depth issues
        stack = [(x, y)]
        visited = set()
        
        while stack:
            cx, cy = stack.pop()
            
            if (cx, cy) in visited:
                continue
            if not (0 <= cx < self.width and 0 <= cy < self.height):
                continue
            if self.get(cx, cy) != original_color:
                continue
            
            visited.add((cx, cy))
            self.set(cx, cy, new_color)
            
            # Add neighbors to stack
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                stack.append((cx + dx, cy + dy))
    
    def to_list(self) -> List[List[int]]:
        """Convert grid to a list of lists format.
        
        Returns:
            Grid data as a list of lists
        """
        return copy.deepcopy(self.cells)
    
    def from_list(self, data: List[List[int]]) -> None:
        """Load grid data from a list of lists.
        
        Args:
            data: Grid data as a list of lists
        """
        if not data or not data[0]:
            raise ValueError("Grid data cannot be empty")
        
        height = len(data)
        width = len(data[0])
        
        # Validate dimensions
        if width > 64 or height > 64:
            raise ValueError("Grid dimensions cannot exceed 64×64")
        
        # Validate all rows have same length
        for row in data:
            if len(row) != width:
                raise ValueError("All rows must have the same length")
        
        # Validate all values are in range 0-9
        for row in data:
            for val in row:
                if not (0 <= val <= 9):
                    raise ValueError(f"All values must be between 0-9, got {val}")
        
        self.width = width
        self.height = height
        self.cells = copy.deepcopy(data)
    
    def __str__(self) -> str:
        """String representation of the grid."""
        return '\n'.join(' '.join(str(cell) for cell in row) for row in self.cells)
    
    def __repr__(self) -> str:
        """Detailed string representation of the grid."""
        return f"Grid({self.width}×{self.height})"