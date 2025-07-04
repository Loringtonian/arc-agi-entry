"""Unit tests for Grid model."""

import pytest
import copy
from arc_agi_editor.editor.grid_model import Grid


class TestGridInitialization:
    """Test Grid initialization and basic properties."""
    
    def test_default_initialization(self):
        """Test default 8×8 grid with zeros."""
        grid = Grid()
        assert grid.width == 8
        assert grid.height == 8
        assert len(grid.cells) == 8
        assert len(grid.cells[0]) == 8
        assert all(cell == 0 for row in grid.cells for cell in row)
    
    def test_custom_size_initialization(self):
        """Test custom size initialization."""
        grid = Grid(width=5, height=3)
        assert grid.width == 5
        assert grid.height == 3
        assert len(grid.cells) == 3
        assert len(grid.cells[0]) == 5
    
    def test_custom_default_value(self):
        """Test initialization with custom default value."""
        grid = Grid(default_value=5)
        assert all(cell == 5 for row in grid.cells for cell in row)
    
    def test_invalid_dimensions(self):
        """Test initialization with invalid dimensions."""
        with pytest.raises(ValueError, match="Grid dimensions must be positive"):
            Grid(width=0, height=8)
        
        with pytest.raises(ValueError, match="Grid dimensions must be positive"):
            Grid(width=8, height=-1)
        
        with pytest.raises(ValueError, match="Grid dimensions cannot exceed 30×30"):
            Grid(width=31, height=8)
        
        with pytest.raises(ValueError, match="Grid dimensions cannot exceed 30×30"):
            Grid(width=8, height=31)
    
    def test_invalid_default_value(self):
        """Test initialization with invalid default value."""
        with pytest.raises(ValueError, match="Grid values must be between 0-9"):
            Grid(default_value=-1)
        
        with pytest.raises(ValueError, match="Grid values must be between 0-9"):
            Grid(default_value=10)


class TestGridAccessors:
    """Test Grid get/set operations."""
    
    def test_get_valid_coordinates(self):
        """Test getting values at valid coordinates."""
        grid = Grid()
        assert grid.get(0, 0) == 0
        assert grid.get(7, 7) == 0
    
    def test_get_invalid_coordinates(self):
        """Test getting values at invalid coordinates."""
        grid = Grid()
        
        with pytest.raises(IndexError, match="out of bounds"):
            grid.get(-1, 0)
        
        with pytest.raises(IndexError, match="out of bounds"):
            grid.get(0, -1)
        
        with pytest.raises(IndexError, match="out of bounds"):
            grid.get(8, 0)
        
        with pytest.raises(IndexError, match="out of bounds"):
            grid.get(0, 8)
    
    def test_set_valid_coordinates_and_values(self):
        """Test setting values at valid coordinates."""
        grid = Grid()
        grid.set(0, 0, 5)
        assert grid.get(0, 0) == 5
        
        grid.set(7, 7, 9)
        assert grid.get(7, 7) == 9
    
    def test_set_invalid_coordinates(self):
        """Test setting values at invalid coordinates."""
        grid = Grid()
        
        with pytest.raises(IndexError, match="out of bounds"):
            grid.set(-1, 0, 5)
        
        with pytest.raises(IndexError, match="out of bounds"):
            grid.set(8, 0, 5)
    
    def test_set_invalid_values(self):
        """Test setting invalid values."""
        grid = Grid()
        
        with pytest.raises(ValueError, match="Value .* must be between 0-9"):
            grid.set(0, 0, -1)
        
        with pytest.raises(ValueError, match="Value .* must be between 0-9"):
            grid.set(0, 0, 10)


class TestGridResize:
    """Test Grid resize functionality."""
    
    def test_resize_larger(self):
        """Test resizing to larger dimensions."""
        grid = Grid(width=3, height=3)
        grid.set(0, 0, 1)
        grid.set(2, 2, 2)
        
        grid.resize(5, 5)
        assert grid.width == 5
        assert grid.height == 5
        assert grid.get(0, 0) == 1
        assert grid.get(2, 2) == 2
        assert grid.get(4, 4) == 0  # New cells should be 0
    
    def test_resize_smaller(self):
        """Test resizing to smaller dimensions."""
        grid = Grid(width=5, height=5)
        grid.set(0, 0, 1)
        grid.set(4, 4, 2)
        
        grid.resize(3, 3)
        assert grid.width == 3
        assert grid.height == 3
        assert grid.get(0, 0) == 1
        # Cell at (4,4) should be lost
        with pytest.raises(IndexError):
            grid.get(4, 4)
    
    def test_resize_with_custom_default(self):
        """Test resizing with custom default value for new cells."""
        grid = Grid(width=2, height=2)
        grid.set(0, 0, 1)
        
        grid.resize(4, 4, default_value=7)
        assert grid.get(0, 0) == 1
        assert grid.get(3, 3) == 7
    
    def test_resize_invalid_dimensions(self):
        """Test resizing with invalid dimensions."""
        grid = Grid()
        
        with pytest.raises(ValueError, match="Grid dimensions must be positive"):
            grid.resize(0, 8)
        
        with pytest.raises(ValueError, match="Grid dimensions cannot exceed 30×30"):
            grid.resize(31, 8)
    
    def test_resize_invalid_default_value(self):
        """Test resizing with invalid default value."""
        grid = Grid()
        
        with pytest.raises(ValueError, match="Default value must be between 0-9"):
            grid.resize(10, 10, default_value=-1)


class TestGridClone:
    """Test Grid clone functionality."""
    
    def test_clone_basic(self):
        """Test basic cloning."""
        grid = Grid(width=3, height=3)
        grid.set(1, 1, 5)
        
        clone = grid.clone()
        assert clone.width == grid.width
        assert clone.height == grid.height
        assert clone.get(1, 1) == 5
    
    def test_clone_independence(self):
        """Test that cloned grids are independent."""
        grid = Grid(width=3, height=3)
        grid.set(1, 1, 5)
        
        clone = grid.clone()
        clone.set(1, 1, 7)
        
        assert grid.get(1, 1) == 5
        assert clone.get(1, 1) == 7
    
    def test_clone_deep_copy(self):
        """Test that clone creates a deep copy."""
        grid = Grid(width=3, height=3)
        grid.set(0, 0, 1)
        
        clone = grid.clone()
        assert clone.cells is not grid.cells
        assert clone.cells[0] is not grid.cells[0]


class TestGridFloodFill:
    """Test Grid flood fill functionality."""
    
    def test_flood_fill_basic(self):
        """Test basic flood fill."""
        grid = Grid(width=3, height=3)
        # Create a 2x2 square of 1s
        grid.set(0, 0, 1)
        grid.set(1, 0, 1)
        grid.set(0, 1, 1)
        grid.set(1, 1, 1)
        
        grid.flood_fill(0, 0, 5)
        
        assert grid.get(0, 0) == 5
        assert grid.get(1, 0) == 5
        assert grid.get(0, 1) == 5
        assert grid.get(1, 1) == 5
        assert grid.get(2, 2) == 0  # Unchanged
    
    def test_flood_fill_single_cell(self):
        """Test flood fill on single cell."""
        grid = Grid(width=3, height=3)
        grid.set(1, 1, 3)
        
        grid.flood_fill(1, 1, 7)
        
        assert grid.get(1, 1) == 7
        assert grid.get(0, 0) == 0  # Unchanged
    
    def test_flood_fill_no_change(self):
        """Test flood fill when new color is same as current."""
        grid = Grid(width=3, height=3)
        grid.set(1, 1, 3)
        
        grid.flood_fill(1, 1, 3)  # Same color
        
        assert grid.get(1, 1) == 3
    
    def test_flood_fill_out_of_bounds(self):
        """Test flood fill with out of bounds coordinates."""
        grid = Grid(width=3, height=3)
        
        # Should not raise an error, just do nothing
        grid.flood_fill(-1, 0, 5)
        grid.flood_fill(0, -1, 5)
        grid.flood_fill(3, 0, 5)
        grid.flood_fill(0, 3, 5)
    
    def test_flood_fill_invalid_color(self):
        """Test flood fill with invalid color."""
        grid = Grid(width=3, height=3)
        
        with pytest.raises(ValueError, match="Color .* must be between 0-9"):
            grid.flood_fill(0, 0, -1)
        
        with pytest.raises(ValueError, match="Color .* must be between 0-9"):
            grid.flood_fill(0, 0, 10)
    
    def test_flood_fill_complex_pattern(self):
        """Test flood fill with complex pattern."""
        grid = Grid(width=5, height=5)
        
        # Create a cross pattern of 1s
        grid.set(2, 0, 1)
        grid.set(2, 1, 1)
        grid.set(0, 2, 1)
        grid.set(1, 2, 1)
        grid.set(2, 2, 1)
        grid.set(3, 2, 1)
        grid.set(4, 2, 1)
        grid.set(2, 3, 1)
        grid.set(2, 4, 1)
        
        grid.flood_fill(2, 2, 8)
        
        # All connected 1s should be 8s now
        assert grid.get(2, 0) == 8
        assert grid.get(2, 1) == 8
        assert grid.get(0, 2) == 8
        assert grid.get(1, 2) == 8
        assert grid.get(2, 2) == 8
        assert grid.get(3, 2) == 8
        assert grid.get(4, 2) == 8
        assert grid.get(2, 3) == 8
        assert grid.get(2, 4) == 8
        
        # Corners should remain 0
        assert grid.get(0, 0) == 0
        assert grid.get(4, 4) == 0


class TestGridConversion:
    """Test Grid conversion methods."""
    
    def test_to_list(self):
        """Test converting grid to list format."""
        grid = Grid(width=3, height=2)
        grid.set(0, 0, 1)
        grid.set(2, 1, 2)
        
        result = grid.to_list()
        expected = [[1, 0, 0], [0, 0, 2]]
        assert result == expected
    
    def test_to_list_deep_copy(self):
        """Test that to_list returns a deep copy."""
        grid = Grid(width=2, height=2)
        result = grid.to_list()
        
        result[0][0] = 5
        assert grid.get(0, 0) == 0  # Original unchanged
    
    def test_from_list_basic(self):
        """Test loading grid from list format."""
        grid = Grid()
        data = [[1, 2, 3], [4, 5, 6]]
        
        grid.from_list(data)
        
        assert grid.width == 3
        assert grid.height == 2
        assert grid.get(0, 0) == 1
        assert grid.get(2, 1) == 6
    
    def test_from_list_invalid_data(self):
        """Test loading from invalid list data."""
        grid = Grid()
        
        with pytest.raises(ValueError, match="Grid data cannot be empty"):
            grid.from_list([])
        
        with pytest.raises(ValueError, match="Grid data cannot be empty"):
            grid.from_list([[]])
        
        with pytest.raises(ValueError, match="All rows must have the same length"):
            grid.from_list([[1, 2], [3, 4, 5]])
        
        with pytest.raises(ValueError, match="All values must be between 0-9"):
            grid.from_list([[1, 2], [3, 10]])
        
        with pytest.raises(ValueError, match="Grid dimensions cannot exceed 30×30"):
            grid.from_list([[0] * 31])


class TestGridStringRepresentation:
    """Test Grid string representation."""
    
    def test_str_representation(self):
        """Test string representation of grid."""
        grid = Grid(width=3, height=2)
        grid.set(0, 0, 1)
        grid.set(2, 1, 2)
        
        result = str(grid)
        expected = "1 0 0\n0 0 2"
        assert result == expected
    
    def test_repr_representation(self):
        """Test repr representation of grid."""
        grid = Grid(width=5, height=3)
        assert repr(grid) == "Grid(5×3)"