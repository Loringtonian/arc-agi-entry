# ARC-AGI-3 Game Development Rules

⚠️ **CRITICAL**: This document mixes OFFICIAL requirements with SPECULATION and BEST PRACTICES

**For official requirements ONLY**: See `OFFICIAL_REQUIREMENTS.md`

**Legend**:
- 🔵 **OFFICIAL** - Verified from arcprize.org sources
- 🟢 **BEST PRACTICE** - Industry-standard practices
- 🟡 **SPECULATION** - AI assumptions or agent API details (NOT game requirements)

**Based on**: Official ARC-AGI-3 specifications from [arcprize.org/arc-agi/3](https://arcprize.org/arc-agi/3/)
**Last Updated**: October 2025

See also: `documents/official/DESIGN_CONSTRAINTS.md` for official design constraints

---

## Core Constraints

### Input Controls
🟡 **SPECULATION** - These are suggested human play controls, NOT official requirements

- **RECOMMENDED** for human play: Directional movement (Up, Down, Left, Right)
- Use WASD or arrow keys for human players
- **NOTE**: ACTION6 (click with coordinates) exists in the official agent API
- Human play can be keyboard-only, but games MAY support click actions for agents
- Keep controls simple and discoverable

### Visual Display
🔵 **OFFICIAL** - From arcprize.org/arc-agi/3: "Should require no instructions to play"

- **NO** text on screen during gameplay
- **NO** scores, timers, or numerical displays
- **NO** UI elements with text labels
- **NO** instructions or hints displayed
- **NO** menus or dialogs with text
- **NO** rules or controls explained to player
- **NO** goal descriptions or objectives shown
- **ABSOLUTELY NO** tutorial text or help messages

### Color Palette
🟡 **FROM AGENT API** (not required for game submissions) - 16-color palette from docs.arcprize.org/games

- **Agent API docs mention**: 16 distinct colors (indices 0-15)
- **Our Current Implementation**: 10 ARC colors (indices 0-9)
  - This is a valid subset
  - Can be expanded to 16 colors for richer game design if needed
- **Semantic Meaning**: Each color should represent game state, not decoration
- **No Arbitrary Colors**: Every color used must have a purpose
- **Background**: Typically color 0 (black) for empty/passable space

### Grid System
🟡 **FROM AGENT API** (not required for game submissions) - 64×64 max from docs.arcprize.org/games, other details are inference

- **Agent API mentions**: 64×64 maximum grid (coordinates 0-63)
- **Square grids**: Implied but not explicitly stated as requirement
- **GRID SIZE RANGE**: 8×8 minimum is inference/recommendation (not official)
- **COORDINATE SYSTEM**: 0-63 inclusive for both X and Y axes (from agent API)
  - Origin at top-left: (0, 0)
- **EXAMPLES**: 8×8, 12×12, 16×16, 32×32, 64×64 are all valid
- Grid-based movement and positioning
- No sub-pixel or floating-point positions visible to player

### Game Mechanics
🔵 **OFFICIAL** - From arcprize.org/arc-agi/3: "Core Knowledge Priors (no language, trivia, cultural symbols)"

- Rules must be discoverable through play ONLY
- No cultural knowledge required
- No language or symbols needed
- Focus on basic math, geometry, and spatial reasoning
- Object-ness and agent-ness should be clear
- **NEVER EXPLAIN RULES TO PLAYER** - let them figure it out
- **PURE DISCOVERY** - no hints, no tutorials, no guidance

### Physics and Consistency
🔵 **OFFICIAL** - From arcprize.org blog: Games must be deterministic and resist brute-force

- **STRICT PHYSICS**: All movement and interactions must follow consistent rules
- **DETERMINISTIC BEHAVIOR**: Same input always produces same output (blog requirement)
- **PREDICTABLE INTERACTIONS**: Players must be able to predict outcomes
- **NO RANDOMNESS** during gameplay (random level generation is acceptable)
- **CONSISTENT TIMING**: All actions happen at predictable intervals
- **RELIABLE COLLISIONS**: Object interactions must be mathematically precise

### Sound and Effects
🟡 **SPECULATION** - Not mentioned in official docs, but aligns with "no text" philosophy

- **NO** sound effects or music
- **NO** audio cues or feedback
- Purely visual experience

### Action Space
🟡 **FROM AGENT API** (not required for game submissions) - This is the AGENT API framework from docs.arcprize.org

**Source**: docs.arcprize.org (agent documentation, NOT game submission requirements)

- **7 Core Actions for Agents**: RESET + ACTION1-7
  - **RESET**: Restart level/game
  - **ACTION1-5**: Single-parameter actions (typically movement/interaction)
  - **ACTION6**: Click with X,Y coordinates (0-63 range)
  - **ACTION7**: Undo (for supported games)
- **Games are NOT required to support all 7 actions**
- Games can use whatever controls make sense for human play
- If targeting agent compatibility, map game actions to this framework

## Official Design Principles (ARC-AGI-3)

### Human Accessibility
- **"Easy for humans (can pick it up in <1 min of game play)"** - Official requirement
- Rules must be discoverable through play alone
- No tutorial or instruction levels allowed
- First-time players should grasp mechanics within 60 seconds
- Playable duration: 5-10 minutes for competent humans

### Core Knowledge Priors Only
**Required (Official)**:
- Basic mathematics (counting, arithmetic, modular math)
- Basic geometry (shapes, symmetry, distance, area)
- Object-ness (recognizing distinct entities)
- Agent-ness (understanding purposeful actors)
- Spatial reasoning (positions, adjacency, containment)
- Temporal reasoning (sequences, cause-effect, prediction)

**Forbidden (Official)**:
- Language or linguistic knowledge
- Cultural knowledge or symbols
- Trivia or memorized facts
- Domain-specific expertise
- Reading or text interpretation

### Brute-Force Resistance (From Preview Competition)
**Key Learning**: Games must resist random search/exhaustive exploration

**Design for Reasoning**:
- Require pattern recognition to identify solutions
- Make action space large enough to prevent exhaustive search
- Introduce irreversible actions (mistakes have consequences)
- Reward insight over trial-and-error

**Avoid**:
- Goals achievable by clicking everywhere randomly
- Mechanics solvable through pure exhaustive exploration
- Ambiguous success conditions

## Implementation Guidelines

### Player Character
- Use a distinct color for the player (typically color 3 - green)
- Player should be easily identifiable on the grid
- Movement should be immediate and grid-based

### Game Objects
- Each object type should have a consistent color
- Objects should behave predictably
- Interactions should be visible through color changes

### Win/Lose Conditions
- **CLEAR WIN CONDITION**: Must be immediately obvious when achieved
- **CLEAR LOSS CONDITION**: Must be immediately obvious when triggered
- **MANDATORY WIN/LOSS FEEDBACK**: User MUST be informed when they win or lose
- Both conditions must be visually apparent without text
- Use color flashes, screen effects, or pattern changes
- **GREEN FLASH = WIN, RED FLASH = LOSE** (template provides this)
- Player should understand success/failure through visual feedback
- Win/loss should trigger immediate, unmistakable visual response

### Level Design
- Start with simple, clear examples
- Gradually introduce complexity
- Each level should teach one new concept
- No more than 3-4 mechanics per game

## Forbidden Elements

### Absolutely Not Allowed
- Mouse controls
- Text displays
- Scoring systems
- Timers
- Menus
- Dialog boxes
- Tooltips
- Help systems
- Complex key bindings
- Sound effects
- Cultural references
- Language elements
- Symbols or icons

### Development Philosophy

### Core Principles
- **Pure visual puzzle solving** - No text, ever
- **Emergent understanding** - Learning through experimentation
- **Minimal, elegant mechanics** - Simple rules, deep gameplay
- **Focus on reasoning** - Spatial, temporal, logical, mathematical
- **Every element serves the puzzle** - No decoration, only meaning

### ARC-AGI-3 Alignment
From official 30-Day Learnings post:
- **Resist brute-force**: Require reasoning, not random search
- **Clear affordances**: Make available actions visually obvious
- **Reward efficiency**: Optimal play requires insight
- **Test specific skills**: Each game probes particular cognitive capabilities

## Resources

### Official ARC-AGI-3 Documentation
- **Overview**: [arcprize.org/arc-agi/3](https://arcprize.org/arc-agi/3/)
- **30-Day Learnings**: [Blog post with design insights](https://arcprize.org/blog/arc-agi-3-preview-30-day-learnings)
- **Documentation**: [docs.arcprize.org](https://docs.arcprize.org)
- **Submit Games**: [Official form](https://forms.gle/aVD4L4xRaJqJoZvE6)
- **Discord**: [Community discussion](https://discord.gg/9b77dPAmcA)
- **Contact**: team@arcprize.org

### Our Documentation
- **Design Constraints**: `documents/official/DESIGN_CONSTRAINTS.md`
- **Agent API Reference**: `documents/official/AGENT_API_REFERENCE.md`
- **Submission Process**: `documents/specs/SUBMISSION_PROCESS.md`
- **Game Spec Template**: `documents/specs/GAME_SPEC_TEMPLATE.md`
- **Mechanics Library**: `GAME_MECHANICS_REFERENCE.md`
- **Implementation Notes**: `notes on ArcAGI games.txt`

## Evaluation Metrics (Official ARC-AGI-3)

### Action Efficiency
**Primary metric for AI evaluation**:
- How many actions does an agent require vs. human baseline?
- Calculation: Agent actions / Median human actions
  - < 1.0 = More efficient than humans
  - = 1.0 = Human-level efficiency
  - > 1.0 = Less efficient than humans

### Five Core Capabilities Tested
Official ARC-AGI-3 evaluates:
1. **Exploration** - Efficiently discover environmental rules
2. **Percept → Plan → Action** - Process observations and execute
3. **Memory** - Store and apply previous experience
4. **Goal Acquisition** - Identify objectives when unclear
5. **Alignment** - Understand and pursue intended goals

## Game Development Workflow
- **ALL NEW GAMES** go in `draft_games/` folder first
- **NEVER** put games directly in `good_games/` folder
- Only developer approval moves games from `draft_games/` to `good_games/`
- Game picker only shows games from `good_games/` folder
- Draft games must be tested and approved before promotion
- **For ARC-AGI-3 submission**: Create GAME_SPEC.md using template in `documents/specs/`

## Game File Requirements
- **MANDATORY TEMPLATE**: ALL games MUST be created from `arc_game_template.py`
- **DIRECT LAUNCHABLE**: Each game MUST be runnable by executing the Python script
- **CLICK AND RUN**: Must work by clicking the .py file and hitting "run"
- **SELF-CONTAINED**: Single .py file that runs independently
- **NO EXTERNAL DEPENDENCIES**: Beyond pygame (handled automatically by template)
- **NO MODIFICATIONS**: Never modify shebang, pygame import, or color palette sections
- **IMMEDIATE LAUNCH**: Game window opens directly when script is executed

## Using the Template
1. Copy `arc_game_template.py` to a new file in `draft_games/`
2. Rename the class and change the window caption
3. Implement your game logic in the TODO sections
4. Test by clicking the .py file and hitting "run"
5. Never modify the shebang, pygame import, or color palette sections

## Testing Criteria

Before releasing a game, verify:

### Technical Requirements ✅
1. **CREATED FROM TEMPLATE**: Game was built using `arc_game_template.py`
2. **DIRECTLY LAUNCHABLE**: Can execute the Python script to launch
3. **SQUARE GRID**: Uses square grid between 8×8 and 64×64 (no rectangles)
4. **COLOR PALETTE**: Uses only ARC colors (0-9 or expand to 0-15)
5. **GRID-BASED**: Grid-based movement and positioning only
6. **IMMEDIATE START**: Game window opens directly when run

### ARC-AGI-3 Design Constraints ✅
7. **HUMAN ACCESSIBILITY**: Can be learned in < 1 minute of play
8. **PLAYABILITY**: Completable in 5-10 minutes by competent human
9. **NO TEXT**: No text appears during gameplay
10. **NO INSTRUCTIONS**: Rules discoverable through play alone
11. **CORE PRIORS ONLY**: No language, trivia, or cultural knowledge required
12. **FUN FOR HUMANS**: Engaging and enjoyable, not tedious

### Game Mechanics ✅
13. **WIN/LOSS FEEDBACK**: User clearly informed when they win or lose
14. **CLEAR WIN CONDITION**: Visually obvious when achieved
15. **CLEAR LOSS CONDITION**: Visually obvious when triggered (if applicable)
16. **STRICT PHYSICS**: Consistent, predictable behavior
17. **DETERMINISTIC**: Same input = same output every time
18. **BRUTE-FORCE RESISTANT**: Requires reasoning, not random exploration

### Input/Output ✅
19. **SIMPLE CONTROLS**: Can be played with 4 directional keys (+ optional actions)
20. **NO SOUND**: No audio elements or sound effects
21. **NO MOUSE REQUIRED**: All control via keyboard (or maps to ACTION1-7)
22. **NO RANDOMNESS**: No random elements during gameplay (procedural generation OK)

### For ARC-AGI-3 Submission ✅
23. **GAME_SPEC.md**: Complete specification document created
24. **DEMO VIDEO**: Human playthrough recorded
25. **ACTION MAPPING**: Documented which ACTION1-7 does what
26. **PROCEDURAL LEVELS**: Level generation prevents memorization
27. **REASONING REQUIREMENT**: Clear what cognitive skill is being tested