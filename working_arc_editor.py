#!/usr/bin/env python3
"""
Working ARC AGI Editor - Fixed version with all features
Combined into a single file to avoid import issues
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Callable, Tuple, List
import os
import json


# ===== COLOR UTILITIES =====
ARC_COLORS = {
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

def get_color_hex(color_index: int) -> str:
    """Get hex color code for ARC color index."""
    return ARC_COLORS.get(color_index, "#000000")


# ===== GRID MODEL =====
class Grid:
    """Grid model for ARC tasks with all operations."""
    
    def __init__(self, width: int = 8, height: int = 8):
        self.width = width
        self.height = height
        self.data = [[0 for _ in range(width)] for _ in range(height)]
    
    def get(self, x: int, y: int) -> int:
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.data[y][x]
        return 0
    
    def set(self, x: int, y: int, value: int):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.data[y][x] = value
    
    def resize(self, width: int, height: int):
        """Resize the grid, preserving existing data where possible."""
        new_data = [[0 for _ in range(width)] for _ in range(height)]
        
        for y in range(min(height, self.height)):
            for x in range(min(width, self.width)):
                new_data[y][x] = self.data[y][x]
        
        self.width = width
        self.height = height
        self.data = new_data
    
    def clone(self):
        """Create a copy of this grid."""
        new_grid = Grid(self.width, self.height)
        new_grid.data = [row[:] for row in self.data]
        return new_grid
    
    def flood_fill(self, start_x: int, start_y: int, new_color: int):
        """Flood fill algorithm using iterative approach."""
        if not (0 <= start_x < self.width and 0 <= start_y < self.height):
            return
        
        original_color = self.get(start_x, start_y)
        if original_color == new_color:
            return
        
        stack = [(start_x, start_y)]
        
        while stack:
            x, y = stack.pop()
            
            if not (0 <= x < self.width and 0 <= y < self.height):
                continue
            if self.get(x, y) != original_color:
                continue
            
            self.set(x, y, new_color)
            
            # Add neighbors to stack
            stack.extend([(x+1, y), (x-1, y), (x, y+1), (x, y-1)])
    
    def to_list(self) -> List[List[int]]:
        """Convert to list format for JSON export."""
        return [row[:] for row in self.data]
    
    def from_list(self, data: List[List[int]]):
        """Load from list format."""
        if not data:
            return
        
        self.height = len(data)
        self.width = len(data[0]) if data else 0
        self.data = [row[:] for row in data]


# ===== GRID CANVAS =====
class GridCanvas(tk.Canvas):
    """Canvas widget for displaying and editing grids."""
    
    def __init__(self, parent, grid: Grid, cell_size: int = 30, 
                 on_cell_change: Optional[Callable[[int, int, str], None]] = None):
        self.grid = grid
        self.cell_size = cell_size
        self.on_cell_change = on_cell_change
        
        canvas_width = grid.width * cell_size
        canvas_height = grid.height * cell_size
        
        super().__init__(parent, width=canvas_width, height=canvas_height, 
                         bg="white", highlightthickness=2, highlightbackground="black")
        
        # Mouse tracking
        self._is_dragging = False
        self._last_cell = None
        self._hover_cell = None
        self._hover_rect = None
        
        # Bind events
        self.bind("<Button-1>", self._on_click)
        self.bind("<B1-Motion>", self._on_drag)
        self.bind("<Motion>", self._on_hover)
        
        self.refresh()
    
    def refresh(self):
        """Redraw the entire canvas."""
        self.delete("all")
        self._draw_grid()
        self._draw_cells()
    
    def _draw_grid(self):
        """Draw grid lines."""
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
        """Draw all cells."""
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                self._draw_cell(x, y)
    
    def _draw_cell(self, x: int, y: int):
        """Draw a single cell."""
        if not (0 <= x < self.grid.width and 0 <= y < self.grid.height):
            return
        
        cell_value = self.grid.get(x, y)
        color = get_color_hex(cell_value)
        
        x1 = x * self.cell_size + 1
        y1 = y * self.cell_size + 1
        x2 = (x + 1) * self.cell_size - 1
        y2 = (y + 1) * self.cell_size - 1
        
        self.create_rectangle(x1, y1, x2, y2, fill=color, outline="", 
                            tags=f"cell_{x}_{y}")
    
    def _pixel_to_cell(self, pixel_x: int, pixel_y: int) -> Optional[Tuple[int, int]]:
        """Convert pixel coordinates to cell coordinates."""
        cell_x = pixel_x // self.cell_size
        cell_y = pixel_y // self.cell_size
        
        if 0 <= cell_x < self.grid.width and 0 <= cell_y < self.grid.height:
            return (cell_x, cell_y)
        return None
    
    def _on_click(self, event):
        """Handle mouse clicks."""
        cell_coords = self._pixel_to_cell(event.x, event.y)
        if cell_coords:
            self._is_dragging = True
            self._last_cell = cell_coords
            self._handle_cell_interaction(cell_coords[0], cell_coords[1], "click")
    
    def _on_drag(self, event):
        """Handle mouse drags."""
        if not self._is_dragging:
            return
        
        cell_coords = self._pixel_to_cell(event.x, event.y)
        if cell_coords and cell_coords != self._last_cell:
            self._last_cell = cell_coords
            self._handle_cell_interaction(cell_coords[0], cell_coords[1], "drag")
    
    def _on_hover(self, event):
        """Handle mouse hover."""
        cell_coords = self._pixel_to_cell(event.x, event.y)
        
        if cell_coords != self._hover_cell:
            # Remove previous hover
            if self._hover_rect:
                self.delete(self._hover_rect)
                self._hover_rect = None
            
            # Add new hover
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
        """Handle cell interaction."""
        if self.on_cell_change:
            self.on_cell_change(x, y, interaction_type)
    
    def set_cell_value(self, x: int, y: int, value: int):
        """Set a cell value and redraw it."""
        if not (0 <= x < self.grid.width and 0 <= y < self.grid.height):
            return
        
        self.grid.set(x, y, value)
        self.delete(f"cell_{x}_{y}")
        self._draw_cell(x, y)
    
    def flood_fill(self, x: int, y: int, new_color: int):
        """Perform flood fill."""
        if not (0 <= x < self.grid.width and 0 <= y < self.grid.height):
            return
        
        old_grid = self.grid.clone()
        self.grid.flood_fill(x, y, new_color)
        
        # Redraw changed cells
        for grid_y in range(self.grid.height):
            for grid_x in range(self.grid.width):
                if old_grid.get(grid_x, grid_y) != self.grid.get(grid_x, grid_y):
                    self.delete(f"cell_{grid_x}_{grid_y}")
                    self._draw_cell(grid_x, grid_y)
    
    def set_grid(self, new_grid: Grid):
        """Set a new grid."""
        self.grid = new_grid
        canvas_width = new_grid.width * self.cell_size
        canvas_height = new_grid.height * self.cell_size
        self.config(width=canvas_width, height=canvas_height)
        self.refresh()
    
    def set_cell_size(self, cell_size: int):
        """Change cell size."""
        self.cell_size = cell_size
        canvas_width = self.grid.width * cell_size
        canvas_height = self.grid.height * cell_size
        self.config(width=canvas_width, height=canvas_height)
        self.refresh()
    
    def clear_hover(self):
        """Clear hover highlighting."""
        if self._hover_rect:
            self.delete(self._hover_rect)
            self._hover_rect = None
        self._hover_cell = None
    
    def finish_interaction(self):
        """Finish current interaction."""
        self._is_dragging = False
        self._last_cell = None
    
    def bind_mouse_release(self, handler):
        """Bind mouse release handler."""
        self.bind("<ButtonRelease-1>", handler)
    
    def bind_leave(self, handler):
        """Bind mouse leave handler."""
        self.bind("<Leave>", handler)


# ===== COLOR PALETTE =====
class ColorPalette(tk.Frame):
    """Color palette widget."""
    
    def __init__(self, parent, on_color_change: Optional[Callable[[int], None]] = None):
        super().__init__(parent)
        self.on_color_change = on_color_change
        self.current_color = 0
        self.color_buttons = {}
        
        self._create_widgets()
        self._update_selection()
    
    def _create_widgets(self):
        """Create the color palette widgets."""
        tk.Label(self, text="Colors", font=("Arial", 10, "bold")).pack()
        
        # Color grid
        color_frame = tk.Frame(self)
        color_frame.pack(pady=5)
        
        for i in range(10):
            row = i // 5
            col = i % 5
            
            color_hex = get_color_hex(i)
            btn = tk.Button(
                color_frame,
                bg=color_hex,
                width=3,
                height=1,
                command=lambda c=i: self._on_color_clicked(c),
                relief="raised",
                borderwidth=2
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
            self.color_buttons[i] = btn
        
        # Current color display
        self.current_color_display = tk.Frame(self, width=50, height=30, relief="sunken", bd=2)
        self.current_color_display.pack(pady=5)
        self.current_color_display.pack_propagate(False)
        
        self.current_color_label = tk.Label(self, text="(0)")
        self.current_color_label.pack()
    
    def _on_color_clicked(self, color_index: int):
        """Handle color button click."""
        self.set_current_color(color_index)
    
    def set_current_color(self, color_index: int):
        """Set the current selected color."""
        if not (0 <= color_index <= 9):
            return
        
        self.current_color = color_index
        self._update_selection()
        
        if self.on_color_change:
            self.on_color_change(color_index)
    
    def get_current_color(self) -> int:
        """Get the current selected color."""
        return self.current_color
    
    def _update_selection(self):
        """Update the visual selection."""
        # Reset all buttons
        for button in self.color_buttons.values():
            button.config(relief="raised", borderwidth=2)
        
        # Highlight current selection
        if self.current_color in self.color_buttons:
            self.color_buttons[self.current_color].config(relief="sunken", borderwidth=3)
        
        # Update current color display
        color_hex = get_color_hex(self.current_color)
        self.current_color_display.config(bg=color_hex)
        self.current_color_label.config(text=f"({self.current_color})")
    
    def handle_key_press(self, event):
        """Handle keyboard shortcuts."""
        if event.char.isdigit():
            color_index = int(event.char)
            if 0 <= color_index <= 9:
                self.set_current_color(color_index)
                return True
        return False


# ===== TOOL PALETTE =====
class ToolPalette(tk.Frame):
    """Tool palette widget."""
    
    def __init__(self, parent, on_tool_change: Optional[Callable[[str], None]] = None):
        super().__init__(parent)
        self.on_tool_change = on_tool_change
        self.current_tool = "paint"
        self.tool_buttons = {}
        
        self._create_widgets()
        self._update_selection()
    
    def _create_widgets(self):
        """Create the tool palette widgets."""
        tk.Label(self, text="Tools", font=("Arial", 10, "bold")).pack()
        
        tools = [
            ("paint", "Paint (P)"),
            ("fill", "Fill (F)")
        ]
        
        for tool_id, tool_name in tools:
            btn = tk.Button(
                self,
                text=tool_name,
                width=12,
                command=lambda t=tool_id: self._on_tool_clicked(t)
            )
            btn.pack(pady=2)
            self.tool_buttons[tool_id] = btn
        
        # Current tool display
        self.current_tool_label = tk.Label(self, text="Paint", font=("Arial", 9))
        self.current_tool_label.pack(pady=5)
    
    def _on_tool_clicked(self, tool_id: str):
        """Handle tool button click."""
        self.set_current_tool(tool_id)
    
    def set_current_tool(self, tool_id: str):
        """Set the current selected tool."""
        if tool_id not in self.tool_buttons:
            return
        
        self.current_tool = tool_id
        self._update_selection()
        
        if self.on_tool_change:
            self.on_tool_change(tool_id)
    
    def get_current_tool(self) -> str:
        """Get the current selected tool."""
        return self.current_tool
    
    def _update_selection(self):
        """Update the visual selection."""
        # Reset all buttons
        for button in self.tool_buttons.values():
            button.config(relief="raised", bg="lightgray")
        
        # Highlight current selection
        if self.current_tool in self.tool_buttons:
            self.tool_buttons[self.current_tool].config(relief="sunken", bg="lightblue")
        
        # Update current tool display
        self.current_tool_label.config(text=self.current_tool.title())
    
    def handle_key_press(self, event):
        """Handle keyboard shortcuts."""
        key = event.char.lower()
        
        if key == 'p':
            self.set_current_tool("paint")
            return True
        elif key == 'f':
            self.set_current_tool("fill")
            return True
        
        return False


# ===== UTILITIES =====
def create_empty_task():
    """Create an empty ARC task structure."""
    return {
        "train": [],
        "test": []
    }

def add_train_example(task_data, input_grid, output_grid):
    """Add a training example to task data."""
    if "train" not in task_data:
        task_data["train"] = []
    
    task_data["train"].append({
        "input": input_grid,
        "output": output_grid
    })

def save_arc_task(task_data, filename: str):
    """Save task data to JSON file."""
    with open(filename, 'w') as f:
        json.dump(task_data, f, indent=2)

def load_arc_task(filename: str):
    """Load task data from JSON file."""
    with open(filename, 'r') as f:
        return json.load(f)


# ===== MAIN APPLICATION =====
class ARCEditorApp:
    """Main application class."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ARC AGI Editor - Working Version")
        self.root.geometry("1000x700")
        
        # Application state
        self.current_file = None
        self.grid = Grid()
        self.current_color = 0
        self.current_tool = "paint"
        self.task_data = create_empty_task()
        
        # Create UI components
        self._create_menu()
        self._create_widgets()
        self._bind_events()
        self._update_status()
        
        print("ARC Editor initialized successfully!")
    
    def _create_menu(self):
        """Create the menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self._new_file, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Open...", command=self._open_file, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Save", command=self._save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self._save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Grid", command=self._clear_grid)
        edit_menu.add_command(label="Resize Grid...", command=self._resize_grid_dialog)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self._zoom_in)
        view_menu.add_command(label="Zoom Out", command=self._zoom_out)
        view_menu.add_command(label="Reset Zoom", command=self._reset_zoom)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_widgets(self):
        """Create the main widgets."""
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel
        left_panel = tk.Frame(main_frame, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Color palette
        self.color_palette = ColorPalette(left_panel, on_color_change=self._on_color_change)
        self.color_palette.pack(pady=(0, 10))
        
        # Tool palette
        self.tool_palette = ToolPalette(left_panel, on_tool_change=self._on_tool_change)
        self.tool_palette.pack(pady=(0, 10))
        
        # Grid info
        info_frame = tk.Frame(left_panel)
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(info_frame, text="Grid Info", font=("Arial", 10, "bold")).pack()
        self.grid_info_label = tk.Label(info_frame, text=f"{self.grid.width}×{self.grid.height}")
        self.grid_info_label.pack()
        
        # Right panel for canvas
        right_panel = tk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas frame with scrollbars
        canvas_frame = tk.Frame(right_panel)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable canvas container
        self.canvas_container = tk.Frame(canvas_frame)
        
        # Scrollbars
        v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        
        # Canvas for scrolling
        self.scroll_canvas = tk.Canvas(
            canvas_frame,
            yscrollcommand=v_scrollbar.set,
            xscrollcommand=h_scrollbar.set,
            bg="white"
        )
        
        v_scrollbar.config(command=self.scroll_canvas.yview)
        h_scrollbar.config(command=self.scroll_canvas.xview)
        
        # Pack scrollbars and canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.scroll_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Grid canvas
        self.grid_canvas = GridCanvas(
            self.canvas_container,
            self.grid,
            cell_size=30,
            on_cell_change=self._on_cell_change
        )
        self.grid_canvas.pack()
        
        # Add canvas container to scroll canvas
        self.scroll_canvas.create_window((0, 0), window=self.canvas_container, anchor="nw")
        self.canvas_container.update_idletasks()
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
        
        # Bind additional canvas events
        self.grid_canvas.bind_mouse_release(self._on_mouse_release)
        self.grid_canvas.bind_leave(self._on_mouse_leave)
        
        # Status bar
        self.status_bar = tk.Label(
            self.root,
            text="Ready",
            relief=tk.SUNKEN,
            anchor=tk.W,
            font=("Arial", 9)
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _bind_events(self):
        """Bind keyboard events."""
        self.root.bind("<Control-n>", lambda e: self._new_file())
        self.root.bind("<Control-o>", lambda e: self._open_file())
        self.root.bind("<Control-s>", lambda e: self._save_file())
        self.root.bind("<KeyPress>", self._on_key_press)
        self.root.focus_set()
    
    def _on_key_press(self, event):
        """Handle key press events."""
        if self.color_palette.handle_key_press(event):
            return
        if self.tool_palette.handle_key_press(event):
            return
    
    def _on_color_change(self, color_index: int):
        """Handle color change."""
        self.current_color = color_index
        self._update_status()
    
    def _on_tool_change(self, tool_id: str):
        """Handle tool change."""
        self.current_tool = tool_id
        self._update_status()
    
    def _on_cell_change(self, x: int, y: int, interaction_type: str):
        """Handle cell interaction."""
        if self.current_tool == "paint":
            self.grid_canvas.set_cell_value(x, y, self.current_color)
        elif self.current_tool == "fill":
            self.grid_canvas.flood_fill(x, y, self.current_color)
        
        self._update_status(f"Cell ({x}, {y}) changed")
    
    def _on_mouse_release(self, event):
        """Handle mouse release."""
        self.grid_canvas.finish_interaction()
    
    def _on_mouse_leave(self, event):
        """Handle mouse leave."""
        self.grid_canvas.clear_hover()
    
    def _update_status(self, message: Optional[str] = None):
        """Update the status bar."""
        if message:
            status_text = message
        else:
            tool_text = self.current_tool.title()
            color_text = f"Color {self.current_color}"
            grid_text = f"Grid {self.grid.width}×{self.grid.height}"
            status_text = f"{tool_text} | {color_text} | {grid_text}"
        
        self.status_bar.config(text=status_text)
        self.grid_info_label.config(text=f"{self.grid.width}×{self.grid.height}")
    
    def _new_file(self):
        """Create a new file."""
        self.current_file = None
        self.grid = Grid()
        self.task_data = create_empty_task()
        self.grid_canvas.set_grid(self.grid)
        self._update_canvas_scroll()
        self._update_status("New file created")
        self.root.title("ARC AGI Editor - Working Version - Untitled")
    
    def _open_file(self):
        """Open a file."""
        filename = filedialog.askopenfilename(
            title="Open ARC Task",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.task_data = load_arc_task(filename)
                
                if self.task_data.get("train"):
                    first_example = self.task_data["train"][0]
                    if "input" in first_example:
                        self.grid = Grid()
                        self.grid.from_list(first_example["input"])
                        self.grid_canvas.set_grid(self.grid)
                        self._update_canvas_scroll()
                
                self.current_file = filename
                self.root.title(f"ARC AGI Editor - {os.path.basename(filename)}")
                self._update_status(f"Loaded {os.path.basename(filename)}")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
    
    def _save_file(self):
        """Save file."""
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self._save_file_as()
    
    def _save_file_as(self):
        """Save file as."""
        filename = filedialog.asksaveasfilename(
            title="Save ARC Task",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            self._save_to_file(filename)
    
    def _save_to_file(self, filename: str):
        """Save to file."""
        try:
            current_grid_data = self.grid.to_list()
            
            if not self.task_data.get("train"):
                add_train_example(self.task_data, current_grid_data, current_grid_data)
            else:
                self.task_data["train"][0]["input"] = current_grid_data
            
            save_arc_task(self.task_data, filename)
            self.current_file = filename
            self.root.title(f"ARC AGI Editor - {os.path.basename(filename)}")
            self._update_status(f"Saved {os.path.basename(filename)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def _clear_grid(self):
        """Clear the grid."""
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                self.grid.set(x, y, 0)
        self.grid_canvas.refresh()
        self._update_status("Grid cleared")
    
    def _resize_grid_dialog(self):
        """Show resize dialog."""
        dialog = ResizeDialog(self.root, self.grid.width, self.grid.height)
        if dialog.result:
            width, height = dialog.result
            self.grid.resize(width, height)
            self.grid_canvas.set_grid(self.grid)
            self._update_canvas_scroll()
            self._update_status(f"Grid resized to {width}×{height}")
    
    def _zoom_in(self):
        """Zoom in."""
        current_size = self.grid_canvas.cell_size
        new_size = min(current_size + 5, 100)
        self.grid_canvas.set_cell_size(new_size)
        self._update_canvas_scroll()
        self._update_status(f"Zoom: {new_size}px")
    
    def _zoom_out(self):
        """Zoom out."""
        current_size = self.grid_canvas.cell_size
        new_size = max(current_size - 5, 10)
        self.grid_canvas.set_cell_size(new_size)
        self._update_canvas_scroll()
        self._update_status(f"Zoom: {new_size}px")
    
    def _reset_zoom(self):
        """Reset zoom."""
        self.grid_canvas.set_cell_size(30)
        self._update_canvas_scroll()
        self._update_status("Zoom reset")
    
    def _update_canvas_scroll(self):
        """Update scroll region."""
        self.canvas_container.update_idletasks()
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
    
    def _show_about(self):
        """Show about dialog."""
        about_text = """ARC AGI Editor - Working Version

A full-featured GUI for creating ARC-style grid puzzles.

Features:
• Paint and flood-fill tools
• Full ARC color palette  
• JSON import/export
• Keyboard shortcuts
• Zoom and resize

Shortcuts:
• 0-9: Select colors
• P: Paint tool
• F: Fill tool
• Ctrl+N/O/S: File operations"""
        
        messagebox.showinfo("About ARC AGI Editor", about_text)
    
    def run(self):
        """Run the application."""
        print("Starting ARC AGI Editor...")
        print("GUI should now be visible with full functionality!")
        self.root.mainloop()


# ===== RESIZE DIALOG =====
class ResizeDialog:
    """Dialog for resizing the grid."""
    
    def __init__(self, parent, current_width: int, current_height: int):
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Resize Grid")
        self.dialog.geometry("300x150")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        parent.update_idletasks()
        x = (parent.winfo_width() // 2) - (150) + parent.winfo_x()
        y = (parent.winfo_height() // 2) - (75) + parent.winfo_y()
        self.dialog.geometry(f"300x150+{x}+{y}")
        
        # Create widgets
        main_frame = tk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        tk.Label(main_frame, text="Width:").grid(row=0, column=0, sticky="w", pady=5)
        self.width_var = tk.StringVar(value=str(current_width))
        width_entry = tk.Entry(main_frame, textvariable=self.width_var, width=10)
        width_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        tk.Label(main_frame, text="Height:").grid(row=1, column=0, sticky="w", pady=5)
        self.height_var = tk.StringVar(value=str(current_height))
        height_entry = tk.Entry(main_frame, textvariable=self.height_var, width=10)
        height_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ok_button = tk.Button(button_frame, text="OK", command=self._ok_clicked)
        ok_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=self._cancel_clicked)
        cancel_button.pack(side=tk.LEFT)
        
        width_entry.focus_set()
        width_entry.select_range(0, tk.END)
        self.dialog.bind('<Return>', lambda e: self._ok_clicked())
        self.dialog.bind('<Escape>', lambda e: self._cancel_clicked())
        
        self.dialog.wait_window()
    
    def _ok_clicked(self):
        """Handle OK click."""
        try:
            width = int(self.width_var.get())
            height = int(self.height_var.get())
            
            if width <= 0 or height <= 0:
                raise ValueError("Dimensions must be positive")
            if width > 30 or height > 30:
                raise ValueError("Dimensions cannot exceed 30×30")
            
            self.result = (width, height)
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
    
    def _cancel_clicked(self):
        """Handle Cancel click."""
        self.dialog.destroy()


# ===== MAIN ENTRY POINT =====
def main():
    """Main entry point."""
    try:
        app = ARCEditorApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()