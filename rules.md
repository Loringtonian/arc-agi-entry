# ARC AGI Game Development Rules

## Core Constraints

### Input Controls
- **ONLY** directional movement allowed: Up, Down, Left, Right
- Use WASD or arrow keys
- **NO** mouse clicking or pointing devices
- **NO** complex key combinations or shortcuts
- Games must be playable with 4 directional keys only

### Visual Display
- **NO** text on screen during gameplay
- **NO** scores, timers, or numerical displays
- **NO** UI elements with text labels
- **NO** instructions or hints displayed
- **NO** menus or dialogs with text
- **NO** rules or controls explained to player
- **NO** goal descriptions or objectives shown
- **ABSOLUTELY NO** tutorial text or help messages

### Color Palette
- Use only the 10 ARC colors (0-9 from ARC_COLOR_CODES)
- Each color should have semantic meaning within the game
- Colors represent game state, not decoration

### Grid System
- **MANDATORY SQUARE GRID**: All games must use a square grid ONLY
- **GRID SIZE RANGE**: Must be between 8×8 and 64×64 (inclusive)
- **EXAMPLES**: 8×8, 12×12, 16×16, 32×32, 64×64 are all valid
- **NO RECTANGULAR GRIDS**: Width must equal height always
- Grid-based movement and positioning
- No sub-pixel or floating-point positions visible to player

### Game Mechanics
- Rules must be discoverable through play ONLY
- No cultural knowledge required
- No language or symbols needed
- Focus on basic math, geometry, and spatial reasoning
- Object-ness and agent-ness should be clear
- **NEVER EXPLAIN RULES TO PLAYER** - let them figure it out
- **PURE DISCOVERY** - no hints, no tutorials, no guidance

### Physics and Consistency
- **STRICT PHYSICS**: All movement and interactions must follow consistent rules
- **DETERMINISTIC BEHAVIOR**: Same input always produces same output
- **PREDICTABLE INTERACTIONS**: Players must be able to predict outcomes
- **NO RANDOMNESS** during gameplay (random level generation is acceptable)
- **CONSISTENT TIMING**: All actions happen at predictable intervals
- **RELIABLE COLLISIONS**: Object interactions must be mathematically precise

### Sound and Effects
- **NO** sound effects or music
- **NO** audio cues or feedback
- Purely visual experience

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
- Pure visual puzzle solving
- Emergent understanding through experimentation
- Minimal, elegant mechanics
- Focus on spatial reasoning and pattern recognition
- Every element should serve the core puzzle

## Game Development Workflow
- **ALL NEW GAMES** go in `draft_games/` folder first
- **NEVER** put games directly in `good_games/` folder
- Only developer approval moves games from `draft_games/` to `good_games/`
- Game picker only shows games from `good_games/` folder
- Draft games must be tested and approved before promotion

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
1. **CREATED FROM TEMPLATE**: Game was built using `arc_game_template.py`
2. **DIRECTLY LAUNCHABLE**: Can execute the Python script to launch
3. **SQUARE GRID**: Uses square grid between 8×8 and 64×64 (no rectangles)
4. **WIN/LOSS FEEDBACK**: User is clearly informed when they win or lose
5. Can be played with only 4 directional keys
6. No text appears during gameplay
7. Rules are discoverable through play
8. Uses only ARC color palette
9. Grid-based movement and positioning
10. **CLEAR WIN CONDITION**: Obvious when achieved
11. **CLEAR LOSS CONDITION**: Obvious when triggered
12. **STRICT PHYSICS**: Consistent, predictable behavior
13. **DETERMINISTIC**: Same input = same output
14. No sound or audio elements
15. No mouse interaction required
16. No randomness during gameplay
17. **IMMEDIATE START**: Game window opens directly