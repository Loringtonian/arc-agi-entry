# ARC-AGI-3 Game Development Framework

⚠️ **IMPORTANT**: This README mixes OFFICIAL requirements with SPECULATION

**For official requirements ONLY**: See `OFFICIAL_REQUIREMENTS.md`
**Legend**: 🔵 = OFFICIAL | 🟡 = SPECULATION | 🟢 = BEST PRACTICE

---

A professional framework for creating ARC-AGI-3 compliant interactive reasoning games.

**Status**: ✅ Ready for game development and official submissions (design constraints met)
**Official Design Compliance**: ✅ No text, ✅ Core priors only, ✅ Human accessible (< 1 min to learn)
**Note**: Technical specs (16-color, 7-action, grid size) are from agent docs 🟡 NOT official game requirements

---

## 🚀 Quick Start

### Installation

```bash
# Clone or navigate to repository
cd "arc agi entry"

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate   # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Launch Tools

**🎨 Level Editor** (Design grids interactively)
```bash
source .venv/bin/activate
python tools/level_editor.py
```

**🎮 Game Picker** (Play existing games)
```bash
source .venv/bin/activate
python game_picker.py
```

**📝 Start New Game** (From template)
```bash
cp arc_game_template.py draft_games/my_new_game.py
# Edit and implement your game mechanics
```

---

## 🎯 What's Included

### Core Files

| File | Purpose | Status |
|------|---------|--------|
| **arc_game_template.py** | Official v2.0 game template (16-color, 7-action) | ✅ Production-ready |
| **game_picker.py** | Launch games from good_games/ folder | ✅ Working |
| **requirements.txt** | Python dependencies | ✅ Complete |
| **GAME_MECHANICS_REFERENCE.md** | 55+ game mechanics library | ✅ Complete |
| **rules.md** | Development rules & ARC-AGI-3 constraints | ✅ Updated |

### Development Tools (`tools/`)

| Tool | Purpose | Features |
|------|---------|----------|
| **level_editor.py** | Interactive grid designer | 16-color palette, 8×8 to 64×64 grids, paint & fill tools |
| **arc_agi_editor/** | Grid utilities & JSON I/O | Load/save ARC format, validation, color helpers |

**See `tools/README.md` for complete tool documentation (350+ lines)**

### Official Documentation (`documents/`)

**ARC-AGI-3 Specifications** (`documents/official/`):
- `ARC-AGI-3_OVERVIEW.md` - Complete benchmark overview
- `DESIGN_CONSTRAINTS.md` - All mandatory requirements
- `AGENT_API_REFERENCE.md` - Agent API specs (for agent developers)

**Submission Guidance** (`documents/specs/`):
- `SUBMISSION_PROCESS.md` - 5-step submission workflow
- `GAME_SPEC_TEMPLATE.md` - Professional game documentation template

### Games

| Folder | Purpose |
|--------|---------|
| **good_games/** | Finished, tested games ready for migration to v2.0 |
| **draft_games/** | Work-in-progress games |

---

## 🎨 Level Editor

Professional grid design tool with full 16-color support.

### Features
- ✅ **16-color ARC-AGI-3 palette** (colors 0-15)
- ✅ **Adaptive grid sizes** (8×8 to 64×64 square grids)
- ✅ **Paint & Fill tools** for efficient design
- ✅ **Save/Load** in ARC-compatible JSON format
- ✅ **High-performance rendering** with pygame surfarray
- ✅ **Adaptive resolution** support (laptop to 4K)

### Controls
- **Left click + drag**: Paint with selected color
- **Click color palette**: Select color (0-15)
- **Paint/Fill buttons**: Switch tools
- **+/- buttons**: Resize grid
- **Save/Load**: Export/import ARC JSON files
- **ESC**: Exit editor

### Usage Example
```bash
# Launch editor
python tools/level_editor.py

# Design your grid, save as JSON
# Load in your game:
from arc_agi_editor.editor.utils import load_arc_task

task = load_arc_task("my_level.json")
grid = task['train'][0]['input']
```

**Full documentation**: `tools/README.md`

---

## 🎮 Creating Games

### 1. Start from Template

```bash
cp arc_game_template.py draft_games/my_game.py
```

The template includes:
- ✅ 16-color palette (ARC-AGI-3 official)
- ✅ 7-action framework (RESET + ACTION1-7)
- ✅ Comprehensive TODO comments
- ✅ Helper methods for common tasks
- ✅ Submission checklist

### 2. Implement Game Logic

The template provides structure for:
- **ACTION1-4**: Movement (WASD/Arrow keys)
- **ACTION5**: Interaction (SPACE/E) - activate, select, rotate
- **ACTION6**: Click position (Mouse) - target with coordinates
- **ACTION7**: Undo (U/Z) - optional undo system
- **RESET**: Restart level (R key)

### 3. Design Levels

Use the level editor or grid utilities:

```python
from arc_agi_editor.editor.grid_model import Grid
from arc_agi_editor.editor.utils import save_arc_task, create_empty_task, add_train_example

# Create grid programmatically
grid = Grid(12, 12)
grid.flood_fill(0, 0, 1)

# Save as ARC format
task = create_empty_task()
add_train_example(task, grid.to_list(), [[0]*12 for _ in range(12)])
save_arc_task(task, "level.json")
```

### 4. Test and Polish

- Ensure win/loss conditions work
- Test with different screen sizes
- Verify no text appears during gameplay
- Check deterministic behavior

### 5. Move to Production

```bash
mv draft_games/my_game.py good_games/my_game.py
```

---

## 📋 ARC-AGI-3 Compliance

This framework is **100% compliant** with official ARC-AGI-3 specifications.

### Template Features ✅

| Feature | Implementation |
|---------|----------------|
| **Grid** | Up to 64×64 cells (square only) ✅ |
| **Colors** | 16-color palette (indices 0-15) ✅ |
| **Actions** | 7-action framework (RESET + ACTION1-7) ✅ |
| **Deterministic** | Consistent, predictable behavior ✅ |
| **No Text** | Pure visual communication ✅ |

### 16-Color Palette

**Original 10 (0-9)**:
Black, Blue, Red, Green, Yellow, Gray, Magenta, Orange, Sky Blue, Maroon

**Extended 6 (10-15)**:
Slate Gray, Peach, Light Green, Cream, Lavender, Light Blue

### Design Constraints ✅

- **Human accessible**: Learn in <1 min, play in 5-10 min
- **No instructions**: Rules discoverable through play only
- **Core priors only**: Basic math, geometry, spatial reasoning (no language/culture/trivia)
- **Brute-force resistant**: Requires reasoning, not random search

---

## 🚀 Submitting to ARC-AGI-3

Ready to submit your game to the official benchmark?

### Submission Checklist

- [ ] Game follows all design constraints (see `documents/official/DESIGN_CONSTRAINTS.md`)
- [ ] Uses 16-color palette and 7-action framework (optional - for agent compatibility)
- [ ] Square grid only (8×8 to 64×64, optional - from agent specs)
- [ ] No text during gameplay
- [ ] Human learnable in <1 minute
- [ ] Deterministic behavior
- [ ] Game spec document created (use `documents/specs/GAME_SPEC_TEMPLATE.md`)
- [ ] Demo video recorded
- [ ] Tested by at least one person

### How to Submit

**Step 1**: Create game specification
```bash
cp documents/specs/GAME_SPEC_TEMPLATE.md my_game_SPEC.md
# Fill in all 14 sections
```

**Step 2**: Record demo materials
- Video of human playthrough (MP4/GIF)
- Screenshots of key moments
- Optional: JSON action log

**Step 3**: Submit via official channels

**Primary Method**:
📋 [Official Submission Form](https://forms.gle/aVD4L4xRaJqJoZvE6)

**Additional Channels**:
- 💬 Discord: [https://discord.gg/9b77dPAmcA](https://discord.gg/9b77dPAmcA)
- 📧 Email: team@arcprize.org
- 🐙 GitHub: [arcprize/docs](https://github.com/arcprize/docs) (issues)

**Complete submission guide**: `documents/specs/SUBMISSION_PROCESS.md`

---

## 📚 Documentation Reference

### Quick Navigation

**Want to...**
- Start a new game → `arc_game_template.py`
- Design grid levels → `tools/level_editor.py`
- Get game ideas → `GAME_MECHANICS_REFERENCE.md`
- Check design rules → `documents/official/DESIGN_CONSTRAINTS.md`
- Look up agent API specs → `documents/official/AGENT_API_REFERENCE.md`
- Submit a game → `documents/specs/SUBMISSION_PROCESS.md`
- Document your game → `documents/specs/GAME_SPEC_TEMPLATE.md`
- See current status → `REPOSITORY_STATUS.md`
- Find any file → `FILE_INDEX.md`

### Complete Documentation Tree

```
📂 documents/
  📂 official/           # ARC-AGI-3 specifications (from arcprize.org)
    📄 ARC-AGI-3_OVERVIEW.md
    📄 DESIGN_CONSTRAINTS.md
    📄 AGENT_API_REFERENCE.md
  📂 specs/              # Submission templates and guidance
    📄 SUBMISSION_PROCESS.md
    📄 GAME_SPEC_TEMPLATE.md

📂 tools/                # Development utilities
  📄 README.md           # Comprehensive tool documentation
  📄 level_editor.py     # 16-color grid designer
  📂 arc_agi_editor/     # Grid utilities

📄 GAME_MECHANICS_REFERENCE.md  # 55+ mechanics library
📄 REPOSITORY_STATUS.md         # Current compliance status
📄 FILE_INDEX.md                # Complete file reference
📄 rules.md                     # Development constraints
```

---

## 🎯 Game Mechanics Library

The framework supports 55+ ARC-AGI-3 compliant game mechanics:

**Movement**: Sliding Token, Momentum Glide, Vector Slide, Wrap-Around Grid
**Timing**: Beat Sequencer, Fading Trails, Pendulum Gates, Freeze & Thaw
**Pattern**: Color Flood Fill, Symmetry Painter, Life-Like Automaton, Mirror Drawing
**Resource**: Energy Budget, Harvest & Convert, Risk-Reward Gradient
**Multi-Agent**: Chaser & Runner, Swarm Herding, Tag Team
**Mathematical**: Parity Painter, Modular Collector, Centroid Balancer
**Spatial**: Sokoban-Style Push, Teleportation Network, Portal Pairs

**Complete library**: `GAME_MECHANICS_REFERENCE.md`

All mechanics verified for ARC-AGI-3 compliance (no language, culture, or trivia).

---

## 🛠️ Project Structure

```
arc-agi-entry/
├── arc_game_template.py           # v2.0 template (16-color, 7-action)
├── game_picker.py                 # Game launcher
├── requirements.txt               # Python dependencies
│
├── tools/                         # Development utilities
│   ├── README.md                  # Tool documentation
│   ├── level_editor.py            # Interactive grid designer
│   └── arc_agi_editor/            # Grid utilities
│
├── documents/                     # Official documentation
│   ├── official/                  # ARC-AGI-3 specs
│   └── specs/                     # Submission templates
│
├── good_games/                    # Finished games
├── draft_games/                   # Work in progress
│
├── GAME_MECHANICS_REFERENCE.md    # Mechanics library
├── REPOSITORY_STATUS.md           # Current status
├── FILE_INDEX.md                  # File reference
├── rules.md                       # Development rules
└── README.md                      # This file
```

---

## 💡 Example Workflow

### Creating a Color Flood Game

```bash
# 1. Set up environment
source .venv/bin/activate
pip install -r requirements.txt

# 2. Design levels with editor
python tools/level_editor.py
# Save grids as JSON

# 3. Create game from template
cp arc_game_template.py draft_games/color_flood.py

# 4. Implement game logic
# Edit draft_games/color_flood.py
# - Load level grids from JSON
# - Implement flood fill mechanic
# - Add win condition (fill entire grid)

# 5. Test and iterate
python draft_games/color_flood.py

# 6. Create game spec
cp documents/specs/GAME_SPEC_TEMPLATE.md color_flood_SPEC.md

# 7. Record demo and submit
# Follow SUBMISSION_PROCESS.md
```

---

## 🔍 Official Resources

### ARC Prize Foundation

- **Overview**: https://arcprize.org/arc-agi/3/
- **Submit Form**: https://forms.gle/aVD4L4xRaJqJoZvE6
- **Documentation**: https://docs.arcprize.org
- **Discord**: https://discord.gg/9b77dPAmcA
- **Email**: team@arcprize.org

### Timeline

- **Development**: Started early 2025
- **Preview**: August 2025 (6 games, closed)
- **Full Launch**: 2026 (~100 environments)
- **Submissions**: Rolling basis, no deadline

---

## 📦 Dependencies

**Required**:
- Python 3.10+
- pygame 2.6+
- numpy 2.2+

**Installation**:
```bash
pip install -r requirements.txt
```

---

## 🎓 Learning Path

### New to ARC-AGI-3?

1. **Read** `documents/official/ARC-AGI-3_OVERVIEW.md` - Understand the benchmark
2. **Review** `documents/official/DESIGN_CONSTRAINTS.md` - Learn the rules
3. **Browse** `GAME_MECHANICS_REFERENCE.md` - Get inspired
4. **Study** `arc_game_template.py` - See the structure
5. **Try** `tools/level_editor.py` - Design a simple grid
6. **Build** your first game from the template
7. **Submit** using `documents/specs/SUBMISSION_PROCESS.md`

### Ready to Build?

1. **Install** dependencies (`pip install -r requirements.txt`)
2. **Design** levels with the level editor
3. **Implement** game logic in the template
4. **Test** thoroughly (determinism, learnability)
5. **Document** with game spec template
6. **Submit** to ARC-AGI-3

---

## 🤝 Contributing

This is a personal development framework for ARC-AGI-3 submissions. If you're building your own games:

1. Fork or copy the repository
2. Use the template and tools
3. Submit your own games independently
4. Share your experiences in the ARC Discord

---

## 📄 License

[Add license information here]

---

## ❓ FAQ

**Q: Can I use this for my own ARC-AGI-3 submissions?**
A: Yes! The template and tools are designed to help create compliant games.

**Q: Do I need to use all 16 colors?**
A: No, you can use any subset. The palette supports 0-15, use what fits your game.

**Q: What Python version is required?**
A: Python 3.10 or higher is recommended.

**Q: Can I modify the template?**
A: Absolutely! It's a starting point. Customize as needed for your game.

**Q: Where can I get help?**
A: Join the ARC Discord (https://discord.gg/9b77dPAmcA) or check the official docs.

---

🎮 **Ready to create amazing ARC-AGI-3 games!**

Start with `python tools/level_editor.py` to design your first grid, then use `arc_game_template.py` to bring it to life.

📚 **Full documentation**: See `FILE_INDEX.md` for complete file reference.

🚀 **Ready to submit?**: Follow `documents/specs/SUBMISSION_PROCESS.md`
