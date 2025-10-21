# ARC-AGI-3 Development Tools

**Updated**: October 2025
**Status**: ✅ 100% ARC-AGI-3 Compliant (16-color palette)

---

## 📁 Contents

This folder contains professional development utilities for creating ARC-AGI-3 games:

| Tool | Purpose | Status |
|------|---------|--------|
| **level_editor.py** | Interactive grid design tool | ✅ v2.0 - Production ready |
| **arc_agi_editor/** | Grid utilities and JSON I/O | ✅ Updated for 16 colors |

---

## 🎨 Level Editor v2.0

### Overview

Professional grid design tool for creating ARC-AGI-3 compatible game levels.

**Key Features**:
- ✅ **16-color ARC-AGI-3 palette** (colors 0-15)
- ✅ **Adaptive grid sizes** (8×8 to 64×64 square grids)
- ✅ **Paint & Fill tools** for efficient design
- ✅ **Save/Load** in ARC-compatible JSON format
- ✅ **High-performance rendering** using pygame surfarray
- ✅ **Adaptive resolution** support (laptop to 4K displays)
- ✅ **Real-time preview** with grid visualization

### Quick Start

```bash
# Activate virtual environment
source .venv/bin/activate

# Launch level editor
python tools/level_editor.py
```

### Controls

#### Mouse Controls
- **Left Click + Drag**: Paint with selected color
- **Click Color Palette**: Select color (0-15)
- **Click Buttons**: Activate UI controls

#### Keyboard Shortcuts
- **ESC**: Exit editor
- **Ctrl+S**: Quick save (if implemented)

#### UI Buttons
- **Paint Tool**: Switch to paint mode (click & drag to paint)
- **Fill Tool**: Switch to fill mode (click to flood fill)
- **Clear Grid**: Reset entire grid to black (color 0)
- **+ / -**: Increase/decrease grid size
- **Save**: Export grid to ARC-compatible JSON
- **Load**: Import grid from JSON file

### Color Palette

The editor displays all 16 ARC-AGI-3 official colors:

**Original 10 Colors (0-9)**:
- 0: Black (Background)
- 1: Blue
- 2: Red
- 3: Green
- 4: Yellow
- 5: Gray
- 6: Magenta
- 7: Orange
- 8: Sky Blue
- 9: Maroon

**Extended 6 Colors (10-15)**:
- 10: Slate Gray
- 11: Peach
- 12: Light Green
- 13: Cream
- 14: Lavender
- 15: Light Blue

### File Format

Grids are saved in standard ARC-AGI JSON format:

```json
{
  "train": [
    {
      "input": [[0, 1, 2], [3, 4, 5], [6, 7, 8]],
      "output": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    }
  ],
  "test": []
}
```

### Workflow

1. **Launch Editor**: `python tools/level_editor.py`
2. **Set Grid Size**: Use +/- buttons to adjust (8×8 to 64×64)
3. **Select Color**: Click color in palette (shows all 16 colors)
4. **Choose Tool**: Paint (brush) or Fill (bucket)
5. **Design Grid**: Click and drag to paint
6. **Save**: Export to JSON file
7. **Use in Game**: Load JSON in your game code

### Technical Details

**Requirements**:
- Python 3.10+
- pygame 2.6+
- numpy 2.2+

**Performance**:
- Uses `pygame.surfarray` for fast rendering
- Adaptive cell sizes for different grid dimensions
- 60 FPS smooth performance up to 64×64 grids

**Resolution Support**:
- Laptop (1366×768): Base cell size 20px
- 1080p (1920×1080): Base cell size 24px
- 4K+ (2560+): Base cell size 28px
- Automatic window sizing (85% of screen)

---

## 📦 arc_agi_editor/ - Grid Utilities

### Overview

Python module for programmatic grid manipulation and ARC format I/O.

**Structure**:
```
arc_agi_editor/
└── editor/
    ├── grid_model.py    # Grid data structure and operations
    └── utils.py         # ARC format utilities (16-color)
```

### Grid Model (grid_model.py)

**Features**:
- Create grids of any size
- Get/set cell values
- Flood fill algorithm
- Grid validation
- Export to ARC JSON format

**Example Usage**:

```python
from arc_agi_editor.editor.grid_model import Grid

# Create a 10×10 grid
grid = Grid(10, 10)

# Set individual cells
grid.set(5, 5, 3)  # Set cell at (5,5) to green (color 3)

# Flood fill from a position
grid.flood_fill(0, 0, 1)  # Fill connected region with blue

# Get cell value
color = grid.get(5, 5)  # Returns 3

# Get as 2D list
grid_data = grid.to_list()

# Get dimensions
width = grid.width
height = grid.height
```

### Utilities (utils.py)

**Features**:
- Load/save ARC tasks from/to JSON
- Validate ARC format compliance
- 16-color palette constants (RGB & hex)
- Helper functions for color conversion
- Grid data validation

**Example Usage**:

```python
from arc_agi_editor.editor.utils import (
    load_arc_task,
    save_arc_task,
    create_empty_task,
    add_train_example,
    get_color_rgb,
    get_color_hex,
    ARC_COLORS,
    ARC_COLOR_CODES
)

# Create a new task
task = create_empty_task()

# Add training example
input_grid = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
output_grid = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]
add_train_example(task, input_grid, output_grid)

# Save to file
save_arc_task(task, "my_puzzle.json")

# Load from file
loaded_task = load_arc_task("my_puzzle.json")

# Get color values
rgb = get_color_rgb(15)  # (160, 220, 255) - Light Blue
hex_code = get_color_hex(15)  # "#A0DCFF"

# Access palette
all_colors = ARC_COLORS  # Dict of color_index -> (r, g, b)
all_hex = ARC_COLOR_CODES  # Dict of color_index -> "#RRGGBB"
```

### Validation

The utilities automatically validate:
- Grid dimensions (must be ≤ 30×30 per ARC spec)
- Color values (must be 0-15)
- Rectangular grids (all rows same length)
- Non-empty grids
- Proper task structure (train/test format)

**Note**: ARC-AGI-3 games support up to 64×64, but the training data format uses 30×30 max. Your games can exceed this.

---

## 🔧 Integration with Games

### Using Level Editor Outputs in Games

1. **Design your level** in the level editor
2. **Save as JSON** (e.g., `level_001.json`)
3. **Load in your game**:

```python
from arc_agi_editor.editor.utils import load_arc_task

class MyGame:
    def __init__(self):
        # Load level
        task = load_arc_task("levels/level_001.json")

        # Get the first training example's input as starting grid
        self.grid = task['train'][0]['input']

        # Or get the expected solution
        self.solution = task['train'][0]['output']
```

### Creating Levels Programmatically

```python
from arc_agi_editor.editor.grid_model import Grid
from arc_agi_editor.editor.utils import create_empty_task, add_train_example, save_arc_task

# Create grid programmatically
grid = Grid(12, 12)

# Design pattern (e.g., checkerboard)
for y in range(12):
    for x in range(12):
        color = 1 if (x + y) % 2 == 0 else 2
        grid.set(x, y, color)

# Create task and save
task = create_empty_task()
add_train_example(task, grid.to_list(), [[0]*12 for _ in range(12)])
save_arc_task(task, "checkerboard_level.json")
```

---

## 📚 Best Practices

### Level Design

1. **Start Small**: Begin with 8×8 or 10×10 grids to test concepts
2. **Use Contrast**: Choose colors that are visually distinct
3. **Test Patterns**: Save multiple versions to compare
4. **Incremental Complexity**: Build levels progressively harder
5. **Validate**: Ensure saved JSON loads correctly in your game

### Color Usage

1. **Black (0)**: Use as background/empty space
2. **Primary Colors (1-4)**: Blue, Red, Green, Yellow - core gameplay elements
3. **Extended Colors (10-15)**: Use for variety and advanced mechanics
4. **Consistency**: Same color = same meaning across levels

### File Organization

```
your_game/
├── levels/
│   ├── level_001.json    # Beginner
│   ├── level_002.json    # Intermediate
│   └── level_003.json    # Advanced
├── my_game.py
└── README.md
```

---

## 🐛 Troubleshooting

### Editor won't start

**Error**: `ModuleNotFoundError: No module named 'pygame'`

**Solution**:
```bash
source .venv/bin/activate
pip install pygame numpy
python tools/level_editor.py
```

### Colors look wrong

**Issue**: Palette showing only 10 colors instead of 16

**Solution**: You're using an old version. The updated version shows all 16 colors in a 2×8 layout.

### Save/Load not working

**Check**:
1. File path is valid
2. Directory exists
3. JSON format is correct
4. Grid dimensions are valid (≤64×64 for games, ≤30×30 for training data)

### Performance issues with large grids

**Optimization**:
1. Grid sizes >48×48 may be slower
2. Use Fill tool instead of Paint for large areas
3. Consider designing smaller levels for better gameplay

---

## 🚀 Advanced Usage

### Custom Color Schemes

While you must use the official 16 ARC colors, you can create themed levels:

**Example - Nature Theme**:
- 3 (Green): Grass
- 1 (Blue): Water
- 4 (Yellow): Sand
- 2 (Red): Lava
- 12 (Light Green): Trees

### Multi-Level Design

Create level progressions:

```python
from arc_agi_editor.editor.utils import create_empty_task, add_train_example, save_arc_task

def create_level_pack(levels):
    """Create a multi-level game from list of (input, output) grids."""
    task = create_empty_task()

    for input_grid, output_grid in levels:
        add_train_example(task, input_grid, output_grid)

    save_arc_task(task, "level_pack.json")

# Use in game to load sequential levels
```

### Integration with Game Template

The `arc_game_template.py` already includes grid support. To use editor outputs:

```python
# In your game's __init__():
self.levels = []
for i in range(1, 11):  # Load 10 levels
    task = load_arc_task(f"levels/level_{i:03d}.json")
    self.levels.append(task['train'][0]['input'])

self.current_level = 0
self.grid_data = self.levels[self.current_level]
```

---

## 📝 Updates from v1.0 to v2.0

### What Changed

**v1.0** (Original):
- 10-color palette (colors 0-9)
- Basic editing features
- Manual color definitions

**v2.0** (Current):
- ✅ **16-color palette** (colors 0-15) - ARC-AGI-3 compliant
- ✅ **Updated utils.py** with new color constants
- ✅ **Updated validation** to accept colors 0-15
- ✅ **Display improvements** showing all 16 colors
- ✅ **Professional documentation**

### Migration

If you have old saved grids using colors 0-9, they will still work. The new colors (10-15) are additions, not replacements.

---

## 🎯 Quick Reference

### Common Tasks

| Task | Command/Action |
|------|----------------|
| **Launch editor** | `python tools/level_editor.py` |
| **Change grid size** | Click +/- buttons |
| **Select color** | Click color in palette (2×8 grid) |
| **Paint mode** | Click "Paint Tool" button |
| **Fill mode** | Click "Fill Tool" button |
| **Clear grid** | Click "Clear Grid" button |
| **Save grid** | Click "Save" button |
| **Load grid** | Click "Load" button |
| **Exit** | Press ESC or close window |

### Color Quick Reference

```python
# In your game code
from arc_agi_editor.editor.utils import ARC_COLORS

# Get RGB for color index
rgb = ARC_COLORS[15]  # (160, 220, 255) - Light Blue

# All 16 colors available:
# 0-9:  Original ARC colors
# 10-15: Extended ARC-AGI-3 colors
```

---

## 📧 Support

**Questions?**
- Check `documents/official/` for ARC-AGI-3 specifications
- Review `FILE_INDEX.md` for file locations
- See `arc_game_template.py` for integration examples

**Found a bug?**
- The tools are tested and working
- Ensure you're using Python 3.10+ and pygame 2.6+
- Check that virtual environment is activated

---

**Last Updated**: October 2025
**Version**: 2.0
**ARC-AGI-3 Compliance**: ✅ 100%
