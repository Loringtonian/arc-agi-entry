#!/Users/lts/Desktop/arc\ agi\ entry/game_engine_env/bin/python
"""
Simple Game Picker - The One and Only
Click a game, click Launch. That's it.
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import glob

class GamePicker:
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("ARC Game Picker")
        self.root.geometry("300x400")
        
        # Find games
        self.games = self.find_games()
        
        # Create UI
        self.create_ui()
    
    def find_games(self):
        """Find all Python games in good_games folder."""
        games = []
        if os.path.exists("good_games"):
            for file_path in glob.glob("good_games/*.py"):
                name = os.path.basename(file_path).replace('.py', '').replace('_', ' ').title()
                games.append({'name': name, 'file': file_path})
        return games
    
    def create_ui(self):
        """Create the user interface."""
        # Title
        tk.Label(self.root, text="🎮 ARC GAMES", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Game list
        self.listbox = tk.Listbox(self.root, font=("Arial", 12), height=10)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Populate games
        for game in self.games:
            self.listbox.insert(tk.END, game['name'])
        
        # Select first game
        if self.games:
            self.listbox.selection_set(0)
        
        # Launch button
        launch_btn = tk.Button(
            self.root, 
            text="🚀 LAUNCH GAME", 
            font=("Arial", 14, "bold"),
            bg="green", 
            fg="white",
            command=self.launch_game
        )
        launch_btn.pack(pady=10)
        
        # Quit button
        tk.Button(self.root, text="Quit", command=self.root.quit).pack(pady=5)
        
        # Double-click to launch
        self.listbox.bind('<Double-1>', lambda e: self.launch_game())
    
    def launch_game(self):
        """Launch the selected game."""
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a game!")
            return
        
        game = self.games[selection[0]]
        
        try:
            # Use the virtual environment Python
            venv_python = os.path.join("game_engine_env", "bin", "python")
            subprocess.run([venv_python, game['file']])
        except Exception as e:
            messagebox.showerror("Error", f"Failed to launch {game['name']}: {e}")
    
    def run(self):
        """Start the game picker."""
        self.root.mainloop()

if __name__ == "__main__":
    picker = GamePicker()
    picker.run()