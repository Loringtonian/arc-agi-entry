#!/usr/bin/env python3
"""
Python-based screenshot tool using PIL
"""

import sys
import time
import os

try:
    from PIL import ImageGrab
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("PIL/Pillow not available")

try:
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

def take_screenshot_pil():
    """Take screenshot using PIL/Pillow"""
    if not PIL_AVAILABLE:
        return False
    
    try:
        print("Taking screenshot with PIL...")
        screenshot = ImageGrab.grab()
        screenshot.save("screenshot.png")
        print("Screenshot saved as screenshot.png")
        return True
    except Exception as e:
        print(f"PIL screenshot failed: {e}")
        return False

def check_gui_with_tkinter():
    """Check if we can create a basic tkinter window"""
    if not TKINTER_AVAILABLE:
        print("Tkinter not available")
        return False
    
    try:
        print("Testing basic Tkinter functionality...")
        root = tk.Tk()
        root.title("Test")
        root.geometry("200x100")
        
        # Just create the window, don't show it
        root.withdraw()  # Hide the window
        root.update()    # Process events
        
        print("Tkinter test successful - GUI system is working")
        root.destroy()
        return True
    except Exception as e:
        print(f"Tkinter test failed: {e}")
        return False

def main():
    print("Python Screenshot Tool")
    print("=" * 30)
    
    # First check if GUI system is working
    gui_working = check_gui_with_tkinter()
    
    if not gui_working:
        print("GUI system may not be available (no X11/display)")
        return
    
    # Try PIL screenshot
    if PIL_AVAILABLE:
        time.sleep(2)  # Wait a bit
        success = take_screenshot_pil()
        if success:
            if os.path.exists("screenshot.png"):
                size = os.path.getsize("screenshot.png")
                print(f"Screenshot size: {size} bytes")
        else:
            print("Failed to take PIL screenshot")
    else:
        print("No screenshot method available")
        print("Try installing: pip install pillow")

if __name__ == "__main__":
    main()