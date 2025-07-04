# ARC AGI Editor

A lightweight, extensible GUI for creating and experimenting with ARC-style grid puzzles. Built with Python and Tkinter for maximum compatibility and ease of use.

## Features

- **Grid Editor**: Create and edit grids from 8×8 up to 30×30 cells
- **ARC Color Palette**: Full 10-color palette matching ARC specifications
- **Drawing Tools**: 
  - Paint tool for individual cell editing
  - Flood fill tool for area filling
- **File Management**: JSON import/export compatible with ARC task format
- **Keyboard Shortcuts**: Efficient workflow with key bindings
- **Zoom Support**: Adjustable cell sizes for better visibility
- **Responsive UI**: Scrollable canvas with hover effects

## Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd arc_agi_editor
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the application:**
```bash
python -m arc_agi_editor.editor.app
```

## Usage

### Basic Operations

#### Creating a New Grid
- Use `File → New` or `Ctrl+N` to create a new 8×8 grid
- Use `Edit → Resize Grid` to change dimensions

#### Drawing
1. **Select a color**: Click on the color palette or use number keys (0-9)
2. **Choose a tool**: 
   - Paint tool (P): Click and drag to paint individual cells
   - Fill tool (F): Click to flood fill connected areas
3. **Edit the grid**: Click or drag on the grid to apply changes

#### File Operations
- **Open**: `File → Open` or `Ctrl+O` to load ARC JSON files
- **Save**: `File → Save` or `Ctrl+S` to save current grid
- **Save As**: `File → Save As` or `Ctrl+Shift+S` to save with new name

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `0-9` | Select color |
| `P` | Paint tool |
| `F` | Fill tool |
| `Ctrl+N` | New file |
| `Ctrl+O` | Open file |
| `Ctrl+S` | Save file |
| `Ctrl+Shift+S` | Save as |
| `Ctrl+Plus` | Zoom in |
| `Ctrl+Minus` | Zoom out |
| `Ctrl+0` | Reset zoom |

### File Format

The editor uses the standard ARC JSON format:

```json
{
  "train": [
    {
      "input": [[0, 1, 0], [1, 1, 1], [0, 1, 0]],
      "output": [[0, 2, 0], [2, 2, 2], [0, 2, 0]]
    }
  ],
  "test": [
    {
      "input": [[0, 3, 0], [3, 3, 3], [0, 3, 0]]
    }
  ]
}
```

### Color Palette

The editor uses the standard ARC color palette:

| Index | Color | Hex Code |
|-------|-------|----------|
| 0 | Black | #000000 |
| 1 | Blue | #0074D9 |
| 2 | Red | #FF4136 |
| 3 | Green | #2ECC40 |
| 4 | Yellow | #FFDC00 |
| 5 | Gray | #AAAAAA |
| 6 | Magenta | #F012BE |
| 7 | Orange | #FF851B |
| 8 | Sky Blue | #7FDBFF |
| 9 | Maroon | #870C25 |

## Examples

The `examples/` directory contains sample ARC tasks:

- `simple_pattern.json`: Basic pattern recognition
- `color_fill.json`: Color filling demonstration

Load these files using `File → Open` to see example tasks.

## Development

### Project Structure

```
arc_agi_editor/
├── editor/
│   ├── __init__.py
│   ├── app.py           # Main application
│   ├── grid_model.py    # Grid data model
│   ├── grid_canvas.py   # Canvas widget
│   ├── palette.py       # Color/tool palettes
│   └── utils.py         # Utilities and JSON handling
├── examples/            # Sample ARC tasks
├── tests/               # Unit tests
└── requirements.txt
```

### Running Tests

```bash
python -m pytest tests/
```

### Architecture

The editor is built with a clean separation of concerns:

- **Model**: `Grid` class handles all grid operations
- **View**: `GridCanvas` provides visual representation
- **Controller**: `ARCEditorApp` coordinates user interactions
- **Utilities**: JSON handling and color management

## Future Enhancements

- **Game Mode**: Play and test ARC puzzles interactively
- **Multi-frame Support**: Handle sequences and animations
- **AI Integration**: Plugin system for solver algorithms
- **Export Options**: PNG/SVG export for visualization
- **Undo/Redo**: Action history management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is open source. See LICENSE file for details.

## Acknowledgments

- Inspired by the ARC (Abstraction and Reasoning Corpus) dataset
- Built for the ARC AGI Prize competition
- Designed to support AI research in abstract reasoning