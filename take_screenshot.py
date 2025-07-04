#!/usr/bin/env python3
"""
Screenshot script to capture GUI applications
"""

import subprocess
import time
import os
import sys

def take_screenshot_linux():
    """Take screenshot on Linux using various methods"""
    print("Taking screenshot...")
    
    # Try different screenshot methods
    methods = [
        # Method 1: Using import (ImageMagick)
        ["import", "-window", "root", "screenshot.png"],
        # Method 2: Using gnome-screenshot
        ["gnome-screenshot", "-f", "screenshot.png"],
        # Method 3: Using scrot
        ["scrot", "screenshot.png"],
        # Method 4: Using xwd and convert
        ["sh", "-c", "xwd -root | convert xwd:- screenshot.png"]
    ]
    
    for method in methods:
        try:
            print(f"Trying method: {' '.join(method)}")
            result = subprocess.run(method, capture_output=True, text=True, timeout=10)
            if result.returncode == 0 and os.path.exists("screenshot.png"):
                print("Screenshot saved as screenshot.png")
                return True
            else:
                print(f"Method failed: {result.stderr}")
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"Method failed: {e}")
            continue
    
    return False

def take_screenshot_macos():
    """Take screenshot on macOS"""
    try:
        subprocess.run(["screencapture", "-x", "screenshot.png"], check=True)
        print("Screenshot saved as screenshot.png")
        return True
    except subprocess.CalledProcessError as e:
        print(f"macOS screenshot failed: {e}")
        return False

def main():
    print("Waiting 3 seconds for GUI to stabilize...")
    time.sleep(3)
    
    # Detect platform and take screenshot
    if sys.platform.startswith('darwin'):
        success = take_screenshot_macos()
    elif sys.platform.startswith('linux'):
        success = take_screenshot_linux()
    else:
        print(f"Unsupported platform: {sys.platform}")
        return
    
    if success:
        print("Screenshot captured successfully!")
        if os.path.exists("screenshot.png"):
            size = os.path.getsize("screenshot.png")
            print(f"Screenshot file size: {size} bytes")
    else:
        print("Failed to capture screenshot")

if __name__ == "__main__":
    main()