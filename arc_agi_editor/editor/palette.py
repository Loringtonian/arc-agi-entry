"""Color palette widget for ARC AGI Editor.

Provides a graphical color selector with the ARC color palette.
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
from .utils import get_color_hex, ARC_COLORS


class ColorPalette(tk.Frame):
    """A color palette widget for selecting ARC colors."""
    
    def __init__(self, parent, on_color_change: Optional[Callable[[int], None]] = None):
        """Initialize the color palette.
        
        Args:
            parent: Parent widget
            on_color_change: Callback function called when color changes
        """
        super().__init__(parent)
        self.on_color_change = on_color_change
        self.current_color = 0
        self.color_buttons = {}
        
        self._create_widgets()
        self._update_selection()
    
    def _create_widgets(self):
        """Create the color palette widgets."""
        # Title
        title_label = tk.Label(self, text="Color Palette", font=("Arial", 10, "bold"))
        title_label.pack(pady=(0, 5))
        
        # Color grid (2 rows of 5 colors each)
        colors_frame = tk.Frame(self)
        colors_frame.pack()
        
        for i, (color_index, rgb_color) in enumerate(ARC_COLORS.items()):
            row = i // 5
            col = i % 5
            
            # Create color button
            color_hex = get_color_hex(color_index)
            button = tk.Button(
                colors_frame,
                width=3,
                height=2,
                bg=color_hex,
                relief="raised",
                border=2,
                command=lambda c=color_index: self._on_color_clicked(c)
            )
            button.grid(row=row, column=col, padx=1, pady=1)
            
            # Store button reference
            self.color_buttons[color_index] = button
            
            # Add tooltips showing color index
            self._create_tooltip(button, f"Color {color_index}")
        
        # Current color display
        info_frame = tk.Frame(self)
        info_frame.pack(pady=(10, 0))
        
        tk.Label(info_frame, text="Current Color:").pack(side=tk.LEFT)
        
        self.current_color_display = tk.Label(
            info_frame,
            width=4,
            height=2,
            bg=get_color_hex(self.current_color),
            relief="sunken",
            border=2
        )
        self.current_color_display.pack(side=tk.LEFT, padx=(5, 0))
        
        self.current_color_label = tk.Label(info_frame, text=f"({self.current_color})")
        self.current_color_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Keyboard shortcuts info
        shortcuts_frame = tk.Frame(self)
        shortcuts_frame.pack(pady=(10, 0))
        
        tk.Label(shortcuts_frame, text="Shortcuts: 0-9 keys", font=("Arial", 8)).pack()
    
    def _create_tooltip(self, widget, text):
        """Create a tooltip for a widget."""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            label = tk.Label(tooltip, text=text, background="yellow", relief="solid", borderwidth=1)
            label.pack()
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def _on_color_clicked(self, color_index: int):
        """Handle color button click."""
        self.set_current_color(color_index)
    
    def set_current_color(self, color_index: int):
        """Set the current selected color.
        
        Args:
            color_index: Color index (0-9)
        """
        if not (0 <= color_index <= 9):
            return
        
        self.current_color = color_index
        self._update_selection()
        
        if self.on_color_change:
            self.on_color_change(color_index)
    
    def get_current_color(self) -> int:
        """Get the current selected color.
        
        Returns:
            Current color index (0-9)
        """
        return self.current_color
    
    def _update_selection(self):
        """Update the visual selection of the current color."""
        # Reset all buttons
        for button in self.color_buttons.values():
            button.config(relief="raised", border=2)
        
        # Highlight current selection
        if self.current_color in self.color_buttons:
            self.color_buttons[self.current_color].config(relief="sunken", border=3)
        
        # Update current color display
        color_hex = get_color_hex(self.current_color)
        self.current_color_display.config(bg=color_hex)
        self.current_color_label.config(text=f"({self.current_color})")
    
    def handle_key_press(self, event):
        """Handle keyboard shortcuts for color selection.
        
        Args:
            event: Key press event
        
        Returns:
            True if handled, False otherwise
        """
        if event.char.isdigit():
            color_index = int(event.char)
            self.set_current_color(color_index)
            return True
        return False


class ToolPalette(tk.Frame):
    """A tool palette widget for selecting drawing tools."""
    
    def __init__(self, parent, on_tool_change: Optional[Callable[[str], None]] = None):
        """Initialize the tool palette.
        
        Args:
            parent: Parent widget
            on_tool_change: Callback function called when tool changes
        """
        super().__init__(parent)
        self.on_tool_change = on_tool_change
        self.current_tool = "paint"
        self.tool_buttons = {}
        
        self._create_widgets()
        self._update_selection()
    
    def _create_widgets(self):
        """Create the tool palette widgets."""
        # Title
        title_label = tk.Label(self, text="Tools", font=("Arial", 10, "bold"))
        title_label.pack(pady=(0, 5))
        
        # Tool buttons
        tools_frame = tk.Frame(self)
        tools_frame.pack()
        
        tools = [
            ("paint", "Paint (P)", "Paint individual cells"),
            ("fill", "Fill (F)", "Flood fill connected areas"),
        ]
        
        for tool_id, tool_name, tooltip in tools:
            button = tk.Button(
                tools_frame,
                text=tool_name,
                width=12,
                command=lambda t=tool_id: self._on_tool_clicked(t)
            )
            button.pack(pady=2)
            
            self.tool_buttons[tool_id] = button
            self._create_tooltip(button, tooltip)
        
        # Current tool display
        info_frame = tk.Frame(self)
        info_frame.pack(pady=(10, 0))
        
        tk.Label(info_frame, text="Current Tool:").pack()
        self.current_tool_label = tk.Label(info_frame, text=self.current_tool.title(), font=("Arial", 9, "bold"))
        self.current_tool_label.pack()
    
    def _create_tooltip(self, widget, text):
        """Create a tooltip for a widget."""
        def on_enter(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 10}+{event.y_root + 10}")
            label = tk.Label(tooltip, text=text, background="yellow", relief="solid", borderwidth=1)
            label.pack()
            widget.tooltip = tooltip
        
        def on_leave(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                delattr(widget, 'tooltip')
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def _on_tool_clicked(self, tool_id: str):
        """Handle tool button click."""
        self.set_current_tool(tool_id)
    
    def set_current_tool(self, tool_id: str):
        """Set the current selected tool.
        
        Args:
            tool_id: Tool identifier
        """
        if tool_id not in self.tool_buttons:
            return
        
        self.current_tool = tool_id
        self._update_selection()
        
        if self.on_tool_change:
            self.on_tool_change(tool_id)
    
    def get_current_tool(self) -> str:
        """Get the current selected tool.
        
        Returns:
            Current tool identifier
        """
        return self.current_tool
    
    def _update_selection(self):
        """Update the visual selection of the current tool."""
        # Reset all buttons
        for button in self.tool_buttons.values():
            button.config(relief="raised", bg="lightgray")
        
        # Highlight current selection
        if self.current_tool in self.tool_buttons:
            self.tool_buttons[self.current_tool].config(relief="sunken", bg="lightblue")
        
        # Update current tool display
        self.current_tool_label.config(text=self.current_tool.title())
    
    def handle_key_press(self, event):
        """Handle keyboard shortcuts for tool selection.
        
        Args:
            event: Key press event
        
        Returns:
            True if handled, False otherwise
        """
        key = event.char.lower()
        if key == 'p':
            self.set_current_tool("paint")
            return True
        elif key == 'f':
            self.set_current_tool("fill")
            return True
        return False