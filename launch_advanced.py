#!/Users/lts/Desktop/arc\ agi\ entry/game_engine_env/bin/python
"""
🎮 ARC Interactive Game Engine - Main Launcher
Launches the advanced Pygame-based game engine with full editor capabilities
"""

import subprocess
import sys
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    venv_python = os.path.join(script_dir, "game_engine_env", "bin", "python")
    engine_script = os.path.join(script_dir, "advanced_game_engine.py")
    
    print("🚀 Launching Advanced ARC Game Engine...")
    print("🎮 Features:")
    print("   - Professional UI layout")
    print("   - Grid size controls (text input + arrows)")
    print("   - Paint & Fill tools with drag support")
    print("   - Color palette (2×5 grid)")
    print("   - Adaptive screen sizing")
    print("   - Keyboard shortcuts (0-9, P, F, ESC)")
    print()
    
    try:
        subprocess.run([venv_python, engine_script], cwd=script_dir)
    except KeyboardInterrupt:
        print("\n👋 Engine closed")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()