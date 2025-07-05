#!/opt/homebrew/bin/python3.13
"""Working ARC AGI Editor with proper color support."""

import sys
import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'
sys.path.insert(0, 'arc_agi_editor')

import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import json
from arc_agi_editor.editor.grid_model import Grid
from arc_agi_editor.editor.utils import get_color_hex

class WorkingARCEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ARC AGI Editor")
        
        # Detect screen resolution and calculate adaptive sizes
        self._detect_screen_and_set_sizes()
        
        # Bring window to front and focus
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after_idle(lambda: self.root.attributes('-topmost', False))
        self.root.focus_force()
        
        # Application state
        self.current_color = 1  # Start with blue
        self.current_tool = "paint"
        self.grid = Grid(8, 8)
        self.current_file = None
        self.current_file_name = "Untitled"
        
        # Grid display settings (in pixels)
        self.cell_size = 20  # Square cells in pixels
        self.grid_canvas = None
        self.canvas_cells = {}
        
        # Mouse tracking for drag painting
        self.is_dragging = False
        self.last_painted_cell = None
        
        self._create_interface()
        self._setup_sample_grid()
        
        # Update grid size after window is fully created
        self.root.after(100, self._refresh_grid_size)
    
    def _detect_screen_and_set_sizes(self):
        """Detect screen resolution and set optimal cell size."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Calculate base cell size based on screen resolution
        if screen_width >= 2560:  # 4K or larger
            self.base_cell_size = 24
        elif screen_width >= 1920:  # 1080p
            self.base_cell_size = 20
        elif screen_width >= 1366:  # Standard laptop
            self.base_cell_size = 16
        else:  # Smaller screens
            self.base_cell_size = 12
        
        self.cell_size = self.base_cell_size
        
        # Set fixed window size that works well on this screen
        window_width = min(1200, int(screen_width * 0.8))
        window_height = min(900, int(screen_height * 0.8))
        self.root.geometry(f"{window_width}x{window_height}")
        
        print(f"Screen: {screen_width}x{screen_height}, Cell size: {self.cell_size}px")
        
    def _create_interface(self):
        """Create the main interface."""
        # Main container
        main_frame = tk.Frame(self.root, bg='lightgray')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # LEFT PANEL - Controls
        left_panel = tk.Frame(main_frame, width=250, bg='lightgray', relief=tk.RAISED, borderwidth=2)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Header
        header = tk.Label(left_panel, text="ARC AGI EDITOR", font=("Arial", 14, "bold"), 
                         bg='lightblue', fg='darkblue')
        header.pack(fill=tk.X, pady=10, padx=10)
        
        # Color Palette Section
        color_section = tk.Frame(left_panel, bg='lightgray')
        color_section.pack(fill=tk.X, padx=10, pady=(0,10))
        
        tk.Label(color_section, text="COLOR PALETTE", font=("Arial", 11, "bold"), 
                bg='lightgray').pack(pady=(0,5))
        
        # Color grid (2 columns of 5 rows)
        colors_frame = tk.Frame(color_section, bg='lightgray')
        colors_frame.pack()
        
        for i in range(10):
            color_hex = get_color_hex(i)
            row = i % 5  # 5 rows
            col = i // 5  # 2 columns
            
            # Create a frame container for each color
            color_frame = tk.Frame(colors_frame, bg=color_hex, 
                                 relief=tk.RAISED, borderwidth=2)
            color_frame.grid(row=row, column=col, padx=2, pady=2)
            
            # Create a label inside the frame to show the color
            color_label = tk.Label(color_frame, text="", 
                                 width=4, height=2,
                                 bg=color_hex,
                                 relief=tk.FLAT)
            color_label.pack()
            
            # Bind click events to both frame and label
            def make_click_handler(color_idx):
                return lambda event: self._select_color(color_idx)
            
            click_handler = make_click_handler(i)
            color_frame.bind("<Button-1>", click_handler)
            color_label.bind("<Button-1>", click_handler)
        
        # Current selection display
        self.color_display = tk.Label(left_panel, text=f"Selected Color: {self.current_color}", 
                                     bg='lightyellow', relief=tk.SUNKEN, font=("Arial", 10))
        self.color_display.pack(fill=tk.X, padx=10, pady=(0,10))
        
        # Tools Section
        tools_section = tk.Frame(left_panel, bg='lightgray')
        tools_section.pack(fill=tk.X, padx=10, pady=(0,10))
        
        tk.Label(tools_section, text="TOOLS", font=("Arial", 11, "bold"), 
                bg='lightgray').pack(pady=(0,5))
        
        self.paint_btn = tk.Button(tools_section, text="Paint Tool", bg='lightgreen', 
                                  width=20, height=2, font=("Arial", 10),
                                  command=lambda: self._select_tool("paint"))
        self.paint_btn.pack(pady=2)
        
        self.fill_btn = tk.Button(tools_section, text="Fill Tool", bg='lightcoral',
                                 width=20, height=2, font=("Arial", 10),
                                 command=lambda: self._select_tool("fill"))
        self.fill_btn.pack(pady=2)
        
        self.tool_display = tk.Label(left_panel, text=f"Selected Tool: {self.current_tool}", 
                                    bg='lightcyan', relief=tk.SUNKEN, font=("Arial", 10))
        self.tool_display.pack(fill=tk.X, padx=10, pady=(0,10))
        
        # Grid Controls
        controls_section = tk.Frame(left_panel, bg='lightgray')
        controls_section.pack(fill=tk.X, padx=10, pady=(0,10))
        
        tk.Label(controls_section, text="GRID CONTROLS", font=("Arial", 11, "bold"), 
                bg='lightgray').pack(pady=(0,5))
        
        # Grid size controls
        size_frame = tk.Frame(controls_section, bg='lightgray')
        size_frame.pack(pady=2)
        
        tk.Label(size_frame, text="Grid Size:", bg='lightgray', font=("Arial", 10)).pack()
        
        size_control_frame = tk.Frame(size_frame, bg='lightgray')
        size_control_frame.pack()
        
        # Down arrow button
        down_btn = tk.Button(size_control_frame, text="▼", width=3, height=1,
                            command=self._decrease_grid_size)
        down_btn.pack(side=tk.LEFT)
        
        # Size entry field
        self.size_var = tk.StringVar(value=str(self.grid.width))
        self.size_entry = tk.Entry(size_control_frame, textvariable=self.size_var, 
                                  width=4, justify=tk.CENTER, font=("Arial", 12))
        self.size_entry.pack(side=tk.LEFT, padx=2)
        self.size_entry.bind('<Return>', self._on_size_entry)
        
        # Up arrow button
        up_btn = tk.Button(size_control_frame, text="▲", width=3, height=1,
                          command=self._increase_grid_size)
        up_btn.pack(side=tk.LEFT)
        
        clear_btn = tk.Button(controls_section, text="Clear Grid", bg='lightpink',
                             width=20, height=1, command=self._clear_grid)
        clear_btn.pack(pady=2)
        
        # RIGHT PANEL - Grid
        right_panel = tk.Frame(main_frame, bg='white', relief=tk.SUNKEN, borderwidth=2)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        grid_header = tk.Label(right_panel, text="GRID EDITOR", font=("Arial", 16, "bold"), 
                              bg='white', fg='darkgreen')
        grid_header.pack(pady=10)
        
        # Top bar with file operations
        top_bar = tk.Frame(right_panel, bg='lightblue', relief=tk.RAISED, borderwidth=1)
        top_bar.pack(fill=tk.X, padx=10, pady=(0,10))
        
        # File operations buttons
        file_frame = tk.Frame(top_bar, bg='lightblue')
        file_frame.pack(side=tk.LEFT, padx=5, pady=5)
        
        new_btn = tk.Button(file_frame, text="New", width=8, height=1,
                           bg='lightgreen', command=self._new_file)
        new_btn.pack(side=tk.LEFT, padx=2)
        
        save_btn = tk.Button(file_frame, text="Save", width=8, height=1,
                            bg='lightcoral', command=self._save_file)
        save_btn.pack(side=tk.LEFT, padx=2)
        
        load_btn = tk.Button(file_frame, text="Load", width=8, height=1,
                            bg='lightyellow', command=self._load_file)
        load_btn.pack(side=tk.LEFT, padx=2)
        
        save_as_btn = tk.Button(file_frame, text="Save As", width=8, height=1,
                               bg='lightpink', command=self._save_as_file)
        save_as_btn.pack(side=tk.LEFT, padx=2)
        
        # Current file name display
        self.file_name_label = tk.Label(top_bar, text=f"File: {self.current_file_name}", 
                                       font=("Arial", 12, "bold"), bg='lightblue', fg='darkblue')
        self.file_name_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # Grid container frame
        grid_frame = tk.Frame(right_panel, bg='white')
        grid_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        
        # Create canvas for grid (initially small, will be resized)
        self.grid_canvas = tk.Canvas(grid_frame, bg='black', relief=tk.SUNKEN, borderwidth=2)
        self.grid_canvas.pack(anchor=tk.CENTER)
        
        # Bind canvas mouse events
        self.grid_canvas.bind("<Button-1>", self._canvas_click)
        self.grid_canvas.bind("<B1-Motion>", self._canvas_drag)
        self.grid_canvas.bind("<ButtonRelease-1>", self._canvas_release)
        
        # Create grid (this will size the canvas properly)
        self._create_canvas_grid()
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="Ready - Select color and tool, then click grid cells", 
                                 relief=tk.SUNKEN, anchor=tk.W, bg='lightgray', font=("Arial", 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _calculate_cell_size(self):
        """Calculate optimal cell size to maximize use of available space."""
        # Get available space for grid (right panel minus margins and other elements)
        self.root.update_idletasks()
        
        # Estimate available space (total window minus left panel and margins)
        window_width = self.root.winfo_width()
        window_height = self.root.winfo_height()
        
        # Available space calculation
        left_panel_width = 280  # approximate left panel width
        top_bottom_space = 150  # top bar + header + status bar + margins
        available_width = window_width - left_panel_width - 60  # extra margins
        available_height = window_height - top_bottom_space - 60  # extra margins
        
        # Calculate maximum cell size that fits in available space
        max_cell_width = available_width // self.grid.width
        max_cell_height = available_height // self.grid.height
        max_possible_cell_size = min(max_cell_width, max_cell_height)
        
        # Use the maximum possible size, but cap at a reasonable maximum
        max_reasonable_size = min(50, self.base_cell_size * 2)  # Don't go crazy large
        
        self.cell_size = max(4, min(max_possible_cell_size, max_reasonable_size))

    def _create_canvas_grid(self):
        """Create grid using canvas rectangles."""
        if not self.grid_canvas:
            return
            
        # Clear existing canvas
        self.grid_canvas.delete("all")
        self.canvas_cells.clear()
        
        # Calculate cell size
        self._calculate_cell_size()
        
        # Calculate grid dimensions in pixels
        grid_width = self.grid.width * self.cell_size
        grid_height = self.grid.height * self.cell_size
        
        # Configure canvas size to exactly fit the grid
        self.grid_canvas.configure(
            width=grid_width,
            height=grid_height,
            scrollregion=(0, 0, grid_width, grid_height)
        )
        
        # Create cells as canvas rectangles
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                
                cell_id = self.grid_canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill='black', outline='gray', width=1
                )
                self.canvas_cells[(x, y)] = cell_id
    
    def _get_grid_coordinates(self, event):
        """Convert canvas event coordinates to grid coordinates."""
        if not self.grid_canvas:
            return None, None
            
        canvas_x = self.grid_canvas.canvasx(event.x)
        canvas_y = self.grid_canvas.canvasy(event.y)
        
        grid_x = int(canvas_x // self.cell_size)
        grid_y = int(canvas_y // self.cell_size)
        
        # Check bounds
        if 0 <= grid_x < self.grid.width and 0 <= grid_y < self.grid.height:
            return grid_x, grid_y
        return None, None

    def _canvas_click(self, event):
        """Handle canvas click events."""
        grid_x, grid_y = self._get_grid_coordinates(event)
        if grid_x is not None and grid_y is not None:
            self.is_dragging = True
            self.last_painted_cell = (grid_x, grid_y)
            self._click_cell(grid_x, grid_y)
    
    def _canvas_drag(self, event):
        """Handle canvas drag events for paint tool."""
        if not self.is_dragging or self.current_tool != "paint":
            return
            
        grid_x, grid_y = self._get_grid_coordinates(event)
        if grid_x is not None and grid_y is not None:
            # Only paint if we've moved to a different cell
            current_cell = (grid_x, grid_y)
            if current_cell != self.last_painted_cell:
                self._paint_cell(grid_x, grid_y)
                self.last_painted_cell = current_cell
    
    def _canvas_release(self, event):
        """Handle canvas mouse release events."""
        self.is_dragging = False
        self.last_painted_cell = None

    def _select_color(self, color_index):
        """Select a color."""
        self.current_color = color_index
        self.color_display.config(text=f"Selected Color: {color_index}")
        self.status_bar.config(text=f"Selected color {color_index}")
    
    def _select_tool(self, tool):
        """Select a tool."""
        self.current_tool = tool
        self.tool_display.config(text=f"Selected Tool: {tool}")
        
        # Update button appearance
        if tool == "paint":
            self.paint_btn.config(relief=tk.SUNKEN, bg='darkgreen', fg='white')
            self.fill_btn.config(relief=tk.RAISED, bg='lightcoral', fg='black')
        else:
            self.fill_btn.config(relief=tk.SUNKEN, bg='darkred', fg='white')
            self.paint_btn.config(relief=tk.RAISED, bg='lightgreen', fg='black')
        
        self.status_bar.config(text=f"Selected {tool} tool")
    
    def _click_cell(self, x, y):
        """Handle cell click."""
        if self.current_tool == "paint":
            self._paint_cell(x, y)
        elif self.current_tool == "fill":
            self._fill_cell(x, y)
    
    def _paint_cell(self, x, y):
        """Paint a single cell."""
        self.grid.set(x, y, self.current_color)
        self._update_cell_display(x, y)
        self.status_bar.config(text=f"Painted cell ({x},{y}) with color {self.current_color}")
    
    def _fill_cell(self, x, y):
        """Fill connected cells."""
        self.grid.flood_fill(x, y, self.current_color)
        self._refresh_all_cells()
        self.status_bar.config(text=f"Filled from ({x},{y}) with color {self.current_color}")
    
    def _update_cell_display(self, x, y):
        """Update a single cell's appearance."""
        if (x, y) not in self.canvas_cells:
            return
            
        cell_value = self.grid.get(x, y)
        color_hex = get_color_hex(cell_value)
        cell_id = self.canvas_cells[(x, y)]
        self.grid_canvas.itemconfig(cell_id, fill=color_hex)
    
    def _refresh_all_cells(self):
        """Refresh all cell colors."""
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                self._update_cell_display(x, y)
    
    def _refresh_grid_size(self):
        """Refresh grid to use available space optimally."""
        self._create_canvas_grid()
        self._refresh_all_cells()
    
    def _setup_sample_grid(self):
        """Add sample colors to demonstrate functionality."""
        # Create a colorful sample pattern
        self.grid.set(1, 1, 1)  # Blue
        self.grid.set(2, 1, 2)  # Red
        self.grid.set(3, 1, 3)  # Green
        self.grid.set(1, 2, 4)  # Yellow
        self.grid.set(2, 2, 5)  # Gray
        self.grid.set(3, 2, 6)  # Magenta
        
        # Refresh display
        self._refresh_all_cells()
        
        # Select paint tool initially
        self._select_tool("paint")
    
    def _resize_grid_to(self, new_size):
        """Resize grid to specified size - fast canvas approach."""
        if new_size < 1 or new_size > 64:
            self.status_bar.config(text="Grid size must be between 1 and 64")
            return
            
        # Create new grid and copy data
        old_grid = self.grid
        self.grid = Grid(new_size, new_size)
        
        # Copy existing data where possible
        for y in range(min(new_size, old_grid.height)):
            for x in range(min(new_size, old_grid.width)):
                self.grid.set(x, y, old_grid.get(x, y))
        
        # Redraw canvas grid (much faster than recreating widgets)
        self._create_canvas_grid()
        self._refresh_all_cells()
        
        self.size_var.set(str(new_size))
        self.status_bar.config(text=f"Grid resized to {new_size}x{new_size} (cell size: {self.cell_size}px)")

    def _increase_grid_size(self):
        """Increase grid size by 1."""
        current_size = int(self.size_var.get())
        if current_size < 64:
            self._resize_grid_to(current_size + 1)
    
    def _decrease_grid_size(self):
        """Decrease grid size by 1."""
        current_size = int(self.size_var.get())
        if current_size > 1:
            self._resize_grid_to(current_size - 1)
    
    def _on_size_entry(self, event):
        """Handle manual size entry."""
        try:
            new_size = int(self.size_var.get())
            self._resize_grid_to(new_size)
        except ValueError:
            self.status_bar.config(text="Please enter a valid number")
            self.size_var.set(str(self.grid.width))
    
    def _clear_grid(self):
        """Clear all grid cells to black."""
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                self.grid.set(x, y, 0)
        self._refresh_all_cells()
        self.status_bar.config(text="Grid cleared")
    
    def _grid_to_list(self):
        """Convert current grid to 2D list for JSON export."""
        grid_data = []
        for y in range(self.grid.height):
            row = []
            for x in range(self.grid.width):
                row.append(self.grid.get(x, y))
            grid_data.append(row)
        return grid_data
    
    def _list_to_grid(self, grid_data):
        """Load 2D list data into current grid."""
        height = len(grid_data)
        width = len(grid_data[0]) if height > 0 else 0
        
        # Resize grid to match data
        if width != self.grid.width or height != self.grid.height:
            self._resize_grid_to(max(width, height))  # Use square grid
        
        # Load data
        for y in range(height):
            for x in range(width):
                if x < len(grid_data[y]):
                    self.grid.set(x, y, grid_data[y][x])
    
    def _new_file(self):
        """Create a new file."""
        result = messagebox.askyesnocancel("New File", "Save current work before creating new file?")
        if result is None:  # Cancel
            return
        elif result:  # Yes, save first
            if not self._save_file():
                return
        
        # Clear grid and reset
        self._clear_grid()
        self.current_file = None
        self.current_file_name = "Untitled"
        self.file_name_label.config(text=f"File: {self.current_file_name}")
        self.status_bar.config(text="New file created")
    
    def _save_file(self):
        """Save current file."""
        if self.current_file is None:
            return self._save_as_file()
        
        try:
            arc_data = {
                "train": [{
                    "input": self._grid_to_list(),
                    "output": self._grid_to_list()
                }],
                "test": [{
                    "input": self._grid_to_list()
                }]
            }
            
            with open(self.current_file, 'w') as f:
                json.dump(arc_data, f, indent=2)
            
            self.status_bar.config(text=f"Saved: {self.current_file_name}")
            return True
            
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save file: {str(e)}")
            return False
    
    def _save_as_file(self):
        """Save file with new name."""
        # Create default save directory if it doesn't exist
        default_dir = os.path.join(os.path.dirname(__file__), "saved grids")
        os.makedirs(default_dir, exist_ok=True)
        
        filename = filedialog.asksaveasfilename(
            initialdir=default_dir,
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save ARC Design As"
        )
        
        if filename:
            self.current_file = filename
            self.current_file_name = os.path.basename(filename)
            self.file_name_label.config(text=f"File: {self.current_file_name}")
            return self._save_file()
        return False
    
    def _load_file(self):
        """Load an ARC file."""
        result = messagebox.askyesnocancel("Load File", "Save current work before loading?")
        if result is None:  # Cancel
            return
        elif result:  # Yes, save first
            if not self._save_file():
                return
        
        # Use same default directory for loading
        default_dir = os.path.join(os.path.dirname(__file__), "saved grids")
        os.makedirs(default_dir, exist_ok=True)
        
        filename = filedialog.askopenfilename(
            initialdir=default_dir,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Load ARC Design"
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    arc_data = json.load(f)
                
                # Load the first training example input
                if 'train' in arc_data and len(arc_data['train']) > 0:
                    grid_data = arc_data['train'][0]['input']
                elif 'test' in arc_data and len(arc_data['test']) > 0:
                    grid_data = arc_data['test'][0]['input']
                else:
                    messagebox.showerror("Load Error", "No valid grid data found in file")
                    return
                
                self._list_to_grid(grid_data)
                self._refresh_all_cells()
                
                self.current_file = filename
                self.current_file_name = os.path.basename(filename)
                self.file_name_label.config(text=f"File: {self.current_file_name}")
                self.status_bar.config(text=f"Loaded: {self.current_file_name}")
                
            except Exception as e:
                messagebox.showerror("Load Error", f"Could not load file: {str(e)}")

    def run(self):
        """Run the application."""
        self.root.mainloop()

if __name__ == "__main__":
    print("Starting ARC AGI Editor with proper color support...")
    app = WorkingARCEditor()
    app.run()