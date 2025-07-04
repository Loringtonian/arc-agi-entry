"""Main application for ARC AGI Editor.

Provides the main window with menu bar, grid canvas, and tool palettes.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional
import os
import json
import sys

from .grid_model import Grid
from .grid_canvas import GridCanvas
from .palette import ColorPalette, ToolPalette
from .utils import load_arc_task, save_arc_task, create_empty_task, add_train_example


class ARCEditorApp:
    """Main application class for the ARC AGI Editor."""
    
    def __init__(self):
        """Initialize the application."""
        self.root = tk.Tk()
        self.root.title("ARC AGI Editor")
        self.root.geometry("800x600")
        
        # Window management - bring to front and focus
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))
        self.root.focus_force()
        
        # Center the window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
        # Application state
        self.current_file = None
        self.grid = Grid()  # Default 8x8 grid
        self.current_color = 0
        self.current_tool = "paint"
        self.task_data = create_empty_task()
        
        # Create UI components
        self._create_menu()
        self._create_widgets()
        self._bind_events()
        
        # Update status and ensure everything is rendered
        self._update_status()
        self.root.update()
        
        # Debug output
        print("ARC AGI Editor initialized successfully")
        print(f"Window size: {self.root.winfo_width()}x{self.root.winfo_height()}")
        print(f"Grid size: {self.grid.width}x{self.grid.height}")
        
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
        file_menu.add_command(label="Save As...", command=self._save_file_as, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Clear Grid", command=self._clear_grid)
        edit_menu.add_separator()
        edit_menu.add_command(label="Resize Grid...", command=self._resize_grid_dialog)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self._zoom_in, accelerator="Ctrl+Plus")
        view_menu.add_command(label="Zoom Out", command=self._zoom_out, accelerator="Ctrl+Minus")
        view_menu.add_command(label="Reset Zoom", command=self._reset_zoom, accelerator="Ctrl+0")
        
        # Game menu (placeholder)
        game_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Game", menu=game_menu)
        game_menu.add_command(label="Play Mode (Coming Soon)", command=self._game_mode_placeholder)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about)
    
    def _create_widgets(self):
        """Create the main widgets."""
        print("Creating widgets...")
        
        # Main frame
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Left panel for tools and palette
        left_panel = tk.Frame(main_frame, width=200, bg="#f0f0f0")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Color palette
        print("Creating color palette...")
        self.color_palette = ColorPalette(left_panel, on_color_change=self._on_color_change)
        self.color_palette.pack(pady=(0, 10))
        
        # Tool palette
        print("Creating tool palette...")
        self.tool_palette = ToolPalette(left_panel, on_tool_change=self._on_tool_change)
        self.tool_palette.pack(pady=(0, 10))
        
        # Grid info
        info_frame = tk.Frame(left_panel, bg="#f0f0f0")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(info_frame, text="Grid Info", font=("Arial", 10, "bold"), bg="#f0f0f0").pack()
        self.grid_info_label = tk.Label(info_frame, text=f"{self.grid.width}×{self.grid.height}", bg="#f0f0f0")
        self.grid_info_label.pack()
        
        # Right panel for canvas
        right_panel = tk.Frame(main_frame, bg="#ffffff")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Canvas frame with scrollbars
        canvas_frame = tk.Frame(right_panel, bg="#ffffff")
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create scrollable canvas container
        self.canvas_container = tk.Frame(canvas_frame, bg="#ffffff")
        
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
        print("Creating grid canvas...")
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
        
        # Force update to ensure everything is rendered
        self.root.update_idletasks()
        self.root.update()
        
        print("Widgets created successfully")
    
    def _bind_events(self):
        """Bind keyboard events."""
        self.root.bind("<Control-n>", lambda e: self._new_file())
        self.root.bind("<Control-o>", lambda e: self._open_file())
        self.root.bind("<Control-s>", lambda e: self._save_file())
        self.root.bind("<Control-S>", lambda e: self._save_file_as())
        self.root.bind("<Control-plus>", lambda e: self._zoom_in())
        self.root.bind("<Control-minus>", lambda e: self._zoom_out())
        self.root.bind("<Control-0>", lambda e: self._reset_zoom())
        
        # Focus handling for key presses
        self.root.bind("<KeyPress>", self._on_key_press)
        self.root.focus_set()
    
    def _on_key_press(self, event):
        """Handle key press events."""
        # Let palettes handle their shortcuts first
        if self.color_palette.handle_key_press(event):
            return
        if self.tool_palette.handle_key_press(event):
            return
    
    def _on_color_change(self, color_index: int):
        """Handle color palette selection change."""
        self.current_color = color_index
        self._update_status()
    
    def _on_tool_change(self, tool_id: str):
        """Handle tool palette selection change."""
        self.current_tool = tool_id
        self._update_status()
    
    def _on_cell_change(self, x: int, y: int, interaction_type: str):
        """Handle cell interaction from grid canvas."""
        if self.current_tool == "paint":
            self.grid_canvas.set_cell_value(x, y, self.current_color)
        elif self.current_tool == "fill":
            self.grid_canvas.flood_fill(x, y, self.current_color)
        
        self._update_status(f"Cell ({x}, {y}) changed")
    
    def _on_mouse_release(self, event):
        """Handle mouse release events."""
        self.grid_canvas.finish_interaction()
    
    def _on_mouse_leave(self, event):
        """Handle mouse leave events."""
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
        if self._check_unsaved_changes():
            self.current_file = None
            self.grid = Grid()
            self.task_data = create_empty_task()
            self.grid_canvas.set_grid(self.grid)
            self._update_canvas_scroll()
            self._update_status("New file created")
            self.root.title("ARC AGI Editor - Untitled")
    
    def _open_file(self):
        """Open an existing file."""
        if not self._check_unsaved_changes():
            return
        
        filename = filedialog.askopenfilename(
            title="Open ARC Task",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                self.task_data = load_arc_task(filename)
                
                # Load the first training example if available
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
        """Save the current file."""
        if self.current_file:
            self._save_to_file(self.current_file)
        else:
            self._save_file_as()
    
    def _save_file_as(self):
        """Save the current file with a new name."""
        filename = filedialog.asksaveasfilename(
            title="Save ARC Task",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            self._save_to_file(filename)
    
    def _save_to_file(self, filename: str):
        """Save task data to a file."""
        try:
            # Update task data with current grid
            current_grid_data = self.grid.to_list()
            
            # If no training examples, add current grid as first example
            if not self.task_data.get("train"):
                add_train_example(self.task_data, current_grid_data, current_grid_data)
            else:
                # Update first training example input
                self.task_data["train"][0]["input"] = current_grid_data
            
            save_arc_task(self.task_data, filename)
            self.current_file = filename
            self.root.title(f"ARC AGI Editor - {os.path.basename(filename)}")
            self._update_status(f"Saved {os.path.basename(filename)}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save file:\n{str(e)}")
    
    def _check_unsaved_changes(self) -> bool:
        """Check if there are unsaved changes."""
        # For now, always return True (no unsaved changes tracking)
        # TODO: Implement proper unsaved changes tracking
        return True
    
    def _clear_grid(self):
        """Clear the grid."""
        for y in range(self.grid.height):
            for x in range(self.grid.width):
                self.grid.set(x, y, 0)
        self.grid_canvas.refresh()
        self._update_status("Grid cleared")
    
    def _resize_grid_dialog(self):
        """Show resize grid dialog."""
        dialog = ResizeDialog(self.root, self.grid.width, self.grid.height)
        if dialog.result:
            width, height = dialog.result
            self.grid.resize(width, height)
            self.grid_canvas.set_grid(self.grid)
            self._update_canvas_scroll()
            self._update_status(f"Grid resized to {width}×{height}")
    
    def _zoom_in(self):
        """Zoom in the grid."""
        current_size = self.grid_canvas.cell_size
        new_size = min(current_size + 5, 100)
        self.grid_canvas.set_cell_size(new_size)
        self._update_canvas_scroll()
        self._update_status(f"Zoom: {new_size}px")
    
    def _zoom_out(self):
        """Zoom out the grid."""
        current_size = self.grid_canvas.cell_size
        new_size = max(current_size - 5, 10)
        self.grid_canvas.set_cell_size(new_size)
        self._update_canvas_scroll()
        self._update_status(f"Zoom: {new_size}px")
    
    def _reset_zoom(self):
        """Reset zoom to default."""
        self.grid_canvas.set_cell_size(30)
        self._update_canvas_scroll()
        self._update_status("Zoom reset")
    
    def _update_canvas_scroll(self):
        """Update the scroll region for the canvas."""
        self.canvas_container.update_idletasks()
        self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all"))
    
    def _game_mode_placeholder(self):
        """Placeholder for game mode."""
        messagebox.showinfo("Game Mode", "Game mode coming soon!\n\nThis will allow you to play and test ARC-style puzzles.")
    
    def _show_about(self):
        """Show about dialog."""
        about_text = """ARC AGI Editor v0.1.0

A lightweight GUI for creating and experimenting with ARC-style grid puzzles.

Features:
• 8×8 to 30×30 grid support
• Paint and flood-fill tools
• ARC color palette
• JSON import/export
• Keyboard shortcuts

Shortcuts:
• 0-9: Select colors
• P: Paint tool
• F: Fill tool
• Ctrl+N: New file
• Ctrl+O: Open file
• Ctrl+S: Save file"""
        
        messagebox.showinfo("About ARC AGI Editor", about_text)
    
    def run(self):
        """Run the application."""
        print("Starting main loop...")
        self.root.mainloop()


class ResizeDialog:
    """Dialog for resizing the grid."""
    
    def __init__(self, parent, current_width: int, current_height: int):
        """Initialize the resize dialog."""
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Resize Grid")
        self.dialog.geometry("300x150")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.update_idletasks()
        parent.update_idletasks()
        x = (parent.winfo_width() // 2) - (300 // 2) + parent.winfo_x()
        y = (parent.winfo_height() // 2) - (150 // 2) + parent.winfo_y()
        self.dialog.geometry(f"300x150+{x}+{y}")
        
        # Create widgets
        main_frame = tk.Frame(self.dialog)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Width input
        tk.Label(main_frame, text="Width:").grid(row=0, column=0, sticky="w", pady=5)
        self.width_var = tk.StringVar(value=str(current_width))
        width_entry = tk.Entry(main_frame, textvariable=self.width_var, width=10)
        width_entry.grid(row=0, column=1, padx=(10, 0), pady=5)
        
        # Height input
        tk.Label(main_frame, text="Height:").grid(row=1, column=0, sticky="w", pady=5)
        self.height_var = tk.StringVar(value=str(current_height))
        height_entry = tk.Entry(main_frame, textvariable=self.height_var, width=10)
        height_entry.grid(row=1, column=1, padx=(10, 0), pady=5)
        
        # Buttons
        button_frame = tk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ok_button = tk.Button(button_frame, text="OK", command=self._ok_clicked)
        ok_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = tk.Button(button_frame, text="Cancel", command=self._cancel_clicked)
        cancel_button.pack(side=tk.LEFT)
        
        # Focus and bindings
        width_entry.focus_set()
        width_entry.select_range(0, tk.END)
        self.dialog.bind('<Return>', lambda e: self._ok_clicked())
        self.dialog.bind('<Escape>', lambda e: self._cancel_clicked())
        
        # Wait for dialog to complete
        self.dialog.wait_window()
    
    def _ok_clicked(self):
        """Handle OK button click."""
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
        """Handle Cancel button click."""
        self.dialog.destroy()


def main():
    """Main entry point."""
    try:
        print("Initializing ARC AGI Editor...")
        app = ARCEditorApp()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()