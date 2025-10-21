# ARC Interactive Game Engine

An advanced game engine for creating and playing ARC (Abstract Reasoning Challenge) style puzzle games, built with Pygame + surfarray for high performance.

## 🚀 Quick Start

### Main Applications:

**🎮 Advanced Game Engine** (Recommended)
```bash
./launch_advanced.py
```
- Complete Pygame implementation with game mechanics support
- Professional UI with proper spacing
- High-performance rendering with surfarray
- All original editor features preserved

**📝 Original Tkinter Editor** (Legacy)
```bash
./working_arc_editor.py
```
- Your original sophisticated editor
- Full-featured but limited to editing only

## 🎯 Features

### Editor Capabilities
- ✅ Grid editing up to 64×64
- ✅ 10-color ARC palette
- ✅ Paint & Fill tools with drag support
- ✅ Dynamic grid scaling based on screen resolution
- ✅ Save/Load in ARC-compatible JSON format
- ✅ Keyboard shortcuts (0-9 for colors, P/F for tools)

### Game Engine Ready
- ✅ Pygame + surfarray for fast rendering
- ✅ Event system for game mechanics
- ✅ Modular architecture for rule implementation
- 🔄 40+ game mechanics from mechanics dump (coming soon)

## 🎮 Controls

- **0-9**: Select colors
- **P**: Paint tool
- **F**: Fill tool
- **ESC**: Quit
- **Mouse**: Click and drag to paint
- **Text input**: Direct grid size entry
- **▲▼ buttons**: Increment/decrement grid size

## 📁 Project Structure

```
arc agi entry/
├── advanced_game_engine.py    # Main game engine
├── launch_advanced.py         # Primary launcher
├── working_arc_editor.py      # Original Tkinter editor
├── interactive_roadmap.md     # Development roadmap
├── game mechanics dump.txt    # 40+ game mechanics reference
├── saved grids/               # Your saved designs
├── arc_agi_editor/           # Core grid and color utilities
└── game_engine_env/          # Python virtual environment
```

## 🔮 Roadmap

**✅ Phase 1**: Pygame Foundation (Complete)
- Advanced UI with proper layout
- Screen resolution detection
- Performance optimization with surfarray

**🔄 Phase 2**: Game Engine Architecture (Next)
- Rule engine for game mechanics
- Entity system for interactive objects
- Animation framework

**📋 Phase 3**: Core Game Mechanics
- Movement mechanics (Sliding Token, Wrap-Around, etc.)
- Pattern mechanics (Flood Fill, Symmetry Painter)
- Resource mechanics (Energy Budget, Collection)

See `interactive_roadmap.md` for complete development plan.

## 🛠️ Development

The engine uses a virtual environment with Pygame and NumPy:

```bash
# Activate environment
source game_engine_env/bin/activate

# Run directly
python advanced_game_engine.py
```

## 🎯 Game Mechanics

The engine is designed to implement 40+ game mechanics including:

- **Movement**: Sliding Token, Momentum Glide, Vector Slide
- **Timing**: Beat Sequencer, Fading Trails, Pendulum Gates  
- **Pattern**: Color Flood Fill, Symmetry Painter, Life-Like Automaton
- **Resource**: Energy Budget, Harvest & Convert, Risk-Reward Gradient
- **Multi-Agent**: Chaser & Runner, Swarm Herding
- **And many more...** (see `game mechanics dump.txt`)

---

🎮 **Start creating ARC puzzles and games with `./launch_advanced.py`**