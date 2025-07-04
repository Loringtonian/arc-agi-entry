"""Utility functions for ARC AGI Editor.

Provides JSON load/save operations and color constants for ARC format compatibility.
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path

# ARC color palette - maps color indices to RGB values
ARC_COLORS = {
    0: (0, 0, 0),        # Black
    1: (0, 116, 217),    # Blue
    2: (255, 65, 54),    # Red
    3: (46, 204, 64),    # Green
    4: (255, 220, 0),    # Yellow
    5: (170, 170, 170),  # Gray
    6: (240, 18, 190),   # Magenta
    7: (255, 133, 27),   # Orange
    8: (127, 219, 255),  # Sky Blue
    9: (135, 12, 37),    # Maroon
}

# HTML color codes for web/GUI display
ARC_COLOR_CODES = {
    0: "#000000",  # Black
    1: "#0074D9",  # Blue
    2: "#FF4136",  # Red
    3: "#2ECC40",  # Green
    4: "#FFDC00",  # Yellow
    5: "#AAAAAA",  # Gray
    6: "#F012BE",  # Magenta
    7: "#FF851B",  # Orange
    8: "#7FDBFF",  # Sky Blue
    9: "#870C25",  # Maroon
}


def load_arc_task(file_path: str) -> Dict[str, Any]:
    """Load an ARC task from JSON file.
    
    Args:
        file_path: Path to the JSON file
        
    Returns:
        Dictionary containing the task data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
        ValueError: If the task format is invalid
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    with open(path, 'r') as f:
        data = json.load(f)
    
    # Validate basic structure
    if not isinstance(data, dict):
        raise ValueError("Task must be a dictionary")
    
    if 'train' not in data:
        raise ValueError("Task must contain 'train' key")
    
    if not isinstance(data['train'], list):
        raise ValueError("'train' must be a list")
    
    # Validate train examples
    for i, example in enumerate(data['train']):
        if not isinstance(example, dict):
            raise ValueError(f"Train example {i} must be a dictionary")
        if 'input' not in example or 'output' not in example:
            raise ValueError(f"Train example {i} must contain 'input' and 'output' keys")
        
        _validate_grid_data(example['input'], f"Train example {i} input")
        _validate_grid_data(example['output'], f"Train example {i} output")
    
    # Validate test examples if present
    if 'test' in data:
        if not isinstance(data['test'], list):
            raise ValueError("'test' must be a list")
        
        for i, example in enumerate(data['test']):
            if not isinstance(example, dict):
                raise ValueError(f"Test example {i} must be a dictionary")
            if 'input' not in example:
                raise ValueError(f"Test example {i} must contain 'input' key")
            
            _validate_grid_data(example['input'], f"Test example {i} input")
            
            # Output is optional for test cases
            if 'output' in example:
                _validate_grid_data(example['output'], f"Test example {i} output")
    
    return data


def save_arc_task(task_data: Dict[str, Any], file_path: str) -> None:
    """Save an ARC task to JSON file.
    
    Args:
        task_data: Dictionary containing the task data
        file_path: Path where to save the JSON file
        
    Raises:
        ValueError: If the task format is invalid
    """
    # Validate the task data before saving
    if not isinstance(task_data, dict):
        raise ValueError("Task data must be a dictionary")
    
    if 'train' not in task_data:
        raise ValueError("Task data must contain 'train' key")
    
    # Create directory if it doesn't exist
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    # Save with proper formatting
    with open(path, 'w') as f:
        json.dump(task_data, f, indent=2, separators=(',', ': '))


def _validate_grid_data(grid_data: List[List[int]], context: str) -> None:
    """Validate grid data format.
    
    Args:
        grid_data: List of lists representing the grid
        context: Context string for error messages
        
    Raises:
        ValueError: If the grid format is invalid
    """
    if not isinstance(grid_data, list):
        raise ValueError(f"{context} must be a list")
    
    if not grid_data:
        raise ValueError(f"{context} cannot be empty")
    
    if not all(isinstance(row, list) for row in grid_data):
        raise ValueError(f"{context} must be a list of lists")
    
    if not grid_data[0]:
        raise ValueError(f"{context} rows cannot be empty")
    
    # Check dimensions
    height = len(grid_data)
    width = len(grid_data[0])
    
    if height > 30 or width > 30:
        raise ValueError(f"{context} dimensions cannot exceed 30×30")
    
    # Check all rows have same length
    for i, row in enumerate(grid_data):
        if len(row) != width:
            raise ValueError(f"{context} row {i} has different length than first row")
    
    # Check all values are valid colors (0-9)
    for i, row in enumerate(grid_data):
        for j, value in enumerate(row):
            if not isinstance(value, int) or not (0 <= value <= 9):
                raise ValueError(f"{context} contains invalid value {value} at position ({j}, {i})")


def create_empty_task() -> Dict[str, Any]:
    """Create an empty ARC task structure.
    
    Returns:
        Dictionary with empty task structure
    """
    return {
        "train": [],
        "test": []
    }


def add_train_example(task_data: Dict[str, Any], input_grid: List[List[int]], output_grid: List[List[int]]) -> None:
    """Add a training example to a task.
    
    Args:
        task_data: Task dictionary to modify
        input_grid: Input grid as list of lists
        output_grid: Output grid as list of lists
    """
    if 'train' not in task_data:
        task_data['train'] = []
    
    _validate_grid_data(input_grid, "Input grid")
    _validate_grid_data(output_grid, "Output grid")
    
    task_data['train'].append({
        "input": input_grid,
        "output": output_grid
    })


def add_test_example(task_data: Dict[str, Any], input_grid: List[List[int]], output_grid: Optional[List[List[int]]] = None) -> None:
    """Add a test example to a task.
    
    Args:
        task_data: Task dictionary to modify
        input_grid: Input grid as list of lists
        output_grid: Optional output grid as list of lists
    """
    if 'test' not in task_data:
        task_data['test'] = []
    
    _validate_grid_data(input_grid, "Input grid")
    
    example = {"input": input_grid}
    if output_grid is not None:
        _validate_grid_data(output_grid, "Output grid")
        example["output"] = output_grid
    
    task_data['test'].append(example)


def get_color_rgb(color_index: int) -> tuple:
    """Get RGB values for a color index.
    
    Args:
        color_index: Color index (0-9)
        
    Returns:
        RGB tuple (r, g, b)
        
    Raises:
        ValueError: If color index is invalid
    """
    if not (0 <= color_index <= 9):
        raise ValueError(f"Color index {color_index} must be between 0-9")
    
    return ARC_COLORS[color_index]


def get_color_hex(color_index: int) -> str:
    """Get hex color code for a color index.
    
    Args:
        color_index: Color index (0-9)
        
    Returns:
        Hex color string (e.g., "#FF0000")
        
    Raises:
        ValueError: If color index is invalid
    """
    if not (0 <= color_index <= 9):
        raise ValueError(f"Color index {color_index} must be between 0-9")
    
    return ARC_COLOR_CODES[color_index]