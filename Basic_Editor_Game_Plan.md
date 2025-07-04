# Basic Editor & Game Framework Plan

## 1. Purpose
Provide a lightweight, extensible GUI for creating and experimenting with ARC-style grid puzzles/games.  The initial goal is an **8 × 8 editor** that can easily scale up to the full 30 × 30 grid used by official ARC tasks.  All geometry, colour handling, file I/O and fill-logic are implemented in reusable, UI-agnostic Python functions so future front-ends (Tkinter, PyGame, web) can share the same core.

## 2. Chosen Toolkit  ✅
* **Tkinter** – ships with Python, zero extra deps, Canvas API is perfect for painting cells.
* Rationale: fastest path to a working prototype; later we can embed into PyGame or export to the web without rewriting business-logic.

## 3. Grid & Data Model
* `Grid` class: list-of-lists of ints, size `H × W` (default 8×8, max 30×30).
* Colour codes 0-9 (visualised with the canonical ARC palette).
* Helper ops: `get(x,y)`, `set(x,y,val)`, `resize(h,w)`, `clone()`, `flood_fill(x,y,new_colour)`.
* JSON export/import obeys ARC task format:
  ```json
  {
    "train": [{"input": [[..]], "output": [[..]]}, ...],
    "test":  [{"input": [[..]]}]
  }
  ```

## 4. Folder Layout  📂
```
arc_agi_editor/
├─ editor/
│  ├─ __init__.py
│  ├─ app.py           # Tk root, menu bar
│  ├─ grid_canvas.py   # Canvas subclass – paint & drag
│  ├─ palette.py       # Colour selector widget
│  ├─ grid_model.py    # Pure-logic Grid + fill algorithm
│  └─ utils.py         # JSON helpers, colour constants
├─ examples/           # Sample tasks in JSON
├─ tests/              # pytest for grid logic
├─ requirements.txt    # only pytest for now
└─ README.md
```

## 5. MVP Feature Set  🎯
1. **Display grid** (zoomable squares, snap-to-pixel).
2. **Palette** with 8 colours (+ transparent for erase).
3. **Tools**
   * Paint (single-cell)
   * Flood-fill (contiguous area)
4. **Menu/File I/O**
   * New, Open, Save-As (ARC JSON)
5. **Status bar** – current tool, colour, cell coords.
6. **Keyboard shortcuts** – `1-9` colours, `P`aint, `F`ill, `Cmd+S` save.

## 6. Implementation Roadmap  🛠️
| Phase | Scope | Est. Time |
|-------|-------|-----------|
| 1 | Core logic (`grid_model.py`, flood-fill, unit tests) | ½ day |
| 2 | Basic GUI skeleton (`app.py`, `GridCanvas`) | 1 day |
| 3 | Fill tool + JSON load/save dialogs | ½ day |
| 4 | Polish: status bar, resize behaviour, shortcuts | ½ day |
| 5 | **Game stubs** – `Game` interface with `step(action)` + placeholder menu | ½ day |

## 7. Future Extensions  🔭
* **Board sizes up to 30×30** (already supported by `Grid.resize`).
* High-performance front-end (PyGame) for real-time games.
* Multi-frame timeline to record sequences (turn-based puzzles).
* AI solver playground that obeys Kaggle submission constraints (two outputs per test grid, JSON writer).

## 8. Promising Solution Shapes (ARC Tip #10)
> Hybrid **discrete program search** guided by a deep-learning intuition model is considered the leading research direction for solving ARC-style tasks.

We keep the codebase modular so search engines or neural models can plug into `Grid` and `Game` objects without UI dependencies.

---
_Last updated: {{DATE}}_ 