#!/opt/homebrew/bin/python3.13
"""Launcher for ARC AGI Editor - ensures correct Python version is used."""

import subprocess
import sys
import os

# Change to the correct directory
os.chdir("/Users/lts/Desktop/arc agi entry")

# Launch the editor with the correct Python interpreter
subprocess.run(["/opt/homebrew/bin/python3.13", "working_arc_editor.py"])