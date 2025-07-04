#!/usr/bin/env python3
"""
Simple ARC AGI Editor - A minimal working version
Run with: python3 simple_arc_editor.py
"""

import tkinter as tk
from tkinter import messagebox, filedialog
import json
from typing import List, Tuple

# ARC Color palette
ARC_COLORS = [
    "#000000",  # 0: Black
    "#0074D9",  # 1: Blue  
    "#FF4136",  # 2: Red
    "#2ECC40",  # 3: Green
    "#FFDC00",  # 4: Yellow
    "#AAAAAA",  # 5: Gray
    "#F012BE",  # 6: Magenta
    "#FF851B",  # 7: Orange
    "#7FDBFF",  # 8: Sky Blue
    "#870C25",  # 9: Maroon
]

class SimpleGrid:
    """Simple grid model for ARC tasks"""
    
    def __init__(self, width=8, height=8):
        self.width = width
        self.height = height
        self.data = [[0 for _ in range(width)] for _ in range(height)]
    
    def get(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.data[y][x]
        return 0
    
    def set(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.data[y][x] = value
    
    def clear(self):
        self.data = [[0 for _ in range(self.width)] for _ in range(self.height)]
    
    def to_list(self):
        return [row[:] for row in self.data]

class SimpleARCEditor:
    """Simple ARC Editor with basic functionality"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simple ARC Editor")
        self.root.geometry("900x700")
        
        # State
        self.grid = SimpleGrid()
        self.current_color = 1
        self.cell_size = 40
        
        self.setup_ui()
        self.draw_grid()
        
    def setup_ui(self):
        """Set up the user interface"""
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel for controls
        left_panel = tk.Frame(main_frame, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Color palette
        tk.Label(left_panel, text="Colors:", font=("Arial", 12, "bold")).pack(anchor="w")
        color_frame = tk.Frame(left_panel)
        color_frame.pack(fill=tk.X, pady=(5, 10))
        
        self.color_buttons = []
        for i in range(10):
            row = i // 5
            col = i % 5
            btn = tk.Button(
                color_frame,
                bg=ARC_COLORS[i],
                width=3,
                height=1,
                command=lambda c=i: self.select_color(c)
            )
            btn.grid(row=row, column=col, padx=1, pady=1)
            self.color_buttons.append(btn)
        
        # Current color display
        self.current_color_label = tk.Label(left_panel, text=f"Selected: Color {self.current_color}")
        self.current_color_label.pack(pady=5)
        
        # Buttons
        tk.Button(left_panel, text="Clear Grid", command=self.clear_grid, width=15).pack(pady=2)
        tk.Button(left_panel, text="Save JSON", command=self.save_file, width=15).pack(pady=2)
        tk.Button(left_panel, text="Load JSON", command=self.load_file, width=15).pack(pady=2)
        
        # Instructions
        instructions = tk.Text(left_panel, height=8, width=25, wrap=tk.WORD)
        instructions.pack(pady=(10, 0))
        instructions.insert("1.0", """Instructions:

1. Click colors to select
2. Click grid cells to paint
3. Use Clear Grid to reset
4. Save/Load JSON files

Keyboard shortcuts:
- 0-9: Select colors
- C: Clear grid""")
        instructions.config(state=tk.DISABLED)
        
        # Right panel for canvas
        right_panel = tk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas
        self.canvas = tk.Canvas(
            right_panel,
            width=self.grid.width * self.cell_size,
            height=self.grid.height * self.cell_size,
            bg="white",
            highlightthickness=2,
            highlightbackground="black"
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Bind events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.focus_set()
        
        # Update current color display
        self.update_color_display()
    
    def select_color(self, color_index):
        """Select a color from the palette"""
        self.current_color = color_index
        self.update_color_display()
    
    def update_color_display(self):
        """Update the color selection display"""
        # Reset all buttons
        for btn in self.color_buttons:
            btn.config(relief="raised", borderwidth=2)
        
        # Highlight selected color
        self.color_buttons[self.current_color].config(relief="sunken", borderwidth=3)
        self.current_color_label.config(text=f"Selected: Color {self.current_color}")
    
    def draw_grid(self):
        """Draw the entire grid"""
        self.canvas.delete("all")
        
        # Draw grid lines
        for i in range(self.grid.width + 1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, self.grid.height * self.cell_size, fill="gray")
        
        for i in range(self.grid.height + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, self.grid.width * self.cell_size, y, fill="gray")
        
        # Draw cells
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                self.draw_cell(x, y)
    
    def draw_cell(self, x, y):
        """Draw a single cell"""
        value = self.grid.get(x, y)
        color = ARC_COLORS[value]
        
        x1 = x * self.cell_size + 2
        y1 = y * self.cell_size + 2
        x2 = (x + 1) * self.cell_size - 2
        y2 = (y + 1) * self.cell_size - 2
        
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")
    
    def on_canvas_click(self, event):
        """Handle canvas clicks"""
        cell_x = event.x // self.cell_size
        cell_y = event.y // self.cell_size
        
        if 0 <= cell_x < self.grid.width and 0 <= cell_y < self.grid.height:
            self.grid.set(cell_x, cell_y, self.current_color)
            self.draw_cell(cell_x, cell_y)
    
    def on_key_press(self, event):
        """Handle keyboard shortcuts"""
        if event.char.isdigit():
            color = int(event.char)
            if 0 <= color <= 9:
                self.select_color(color)
        elif event.char.lower() == 'c':
            self.clear_grid()
    
    def clear_grid(self):
        """Clear the grid"""
        self.grid.clear()
        self.draw_grid()
        messagebox.showinfo("Cleared", "Grid cleared!")
    
    def save_file(self):
        """Save grid to JSON file"""
        filename = filedialog.asksaveasfilename(
            title="Save ARC Task",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                task_data = {
                    "train": [
                        {
                            "input": self.grid.to_list(),
                            "output": self.grid.to_list()
                        }
                    ],
                    "test": [
                        {
                            "input": self.grid.to_list()
                        }
                    ]
                }
                
                with open(filename, 'w') as f:
                    json.dump(task_data, f, indent=2)
                
                messagebox.showinfo("Saved", f"Grid saved to {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def load_file(self):
        """Load grid from JSON file"""
        filename = filedialog.askopenfilename(
            title="Open ARC Task",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    data = json.load(f)
                
                # Load first training input if available
                if "train" in data and len(data["train"]) > 0:
                    input_data = data["train"][0]["input"]
                    
                    # Update grid size and data
                    self.grid.height = len(input_data)
                    self.grid.width = len(input_data[0]) if input_data else 8
                    self.grid.data = [row[:] for row in input_data]
                    
                    # Update canvas size
                    self.canvas.config(
                        width=self.grid.width * self.cell_size,
                        height=self.grid.height * self.cell_size
                    )
                    
                    # Redraw
                    self.draw_grid()
                    
                    messagebox.showinfo("Loaded", f"Grid loaded from {filename}")
                else:
                    messagebox.showwarning("Warning", "No training data found in file")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
    
    def run(self):
        """Start the application"""
        print("Starting Simple ARC Editor...")
        print("Click on colors to select, then click on grid cells to paint")
        print("Use keyboard shortcuts: 0-9 for colors, C to clear")
        self.root.mainloop()

def main():
    """Main entry point"""
    app = SimpleARCEditor()
    app.run()

if __name__ == "__main__":
    main()