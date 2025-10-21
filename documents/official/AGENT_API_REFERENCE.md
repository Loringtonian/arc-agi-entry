# ARC-AGI-3 Agent API Reference

⚠️ **CRITICAL**: This document is for AGENT DEVELOPERS, NOT game submission requirements

**Purpose**: Reference for the official ARC-AGI-3 Agents SDK (for building AI agents that PLAY games)

**NOT FOR**: Game authors submitting game concepts (see `OFFICIAL_REQUIREMENTS.md` for actual submission requirements)

**Source**: [docs.arcprize.org](https://docs.arcprize.org) & [ARC-AGI-3-Agents GitHub](https://github.com/arcprize/ARC-AGI-3-Agents)
**Last Updated**: October 2025
**Version**: v0.9.2 (as of Aug 19, 2025)
**Audience**: Developers building AI agents to play ARC-AGI-3 games

---

## Why This File Exists

This file documents the **agent API** - the interface that AI agents use to interact with games. It describes:
- How agents call `reset()` and `step()` methods
- The action framework (ACTION1-7)
- Observation formats (FrameData objects)
- Session management

**Games are NOT required to implement this API for submission.** This is useful if you want your game to be agent-compatible, but it's not an official submission requirement.

## Environment Specification

### Grid System

- **Maximum Dimensions**: 64×64 cells
- **Coordinate System**: 0-63 inclusive (both X and Y axes)
- **Grid Representation**: 2D array where each cell contains a color index
- **Coordinate Origin**: Top-left corner is (0, 0)

### Color System

- **Total Colors**: 16 distinct colors available
- **Color Encoding**: Integer indices 0-15
- **Visual Representation**: Each index maps to a specific RGB color

**Note**: The exact RGB values for the 16-color palette are implementation-defined. Games should refer to colors by index (0-15) rather than assuming specific RGB values.

**Historical Context**: Original ARC-AGI-1/2 used 10 colors (0-9). ARC-AGI-3 expanded to 16 colors for richer game design.

### Action Space

ARC-AGI-3 defines **seven core action types**:

#### Simple Actions (Single-Parameter)

**ACTION1** - Typically: Move Up / Rotate / Primary Direction
- Single command, no additional parameters
- Game-specific interpretation

**ACTION2** - Typically: Move Down / Secondary Action
- Single command, no additional parameters
- Game-specific interpretation

**ACTION3** - Typically: Move Left / Tertiary Action
- Single command, no additional parameters
- Game-specific interpretation

**ACTION4** - Typically: Move Right / Quaternary Action
- Single command, no additional parameters
- Game-specific interpretation

**ACTION5** - General Interaction
- Select, activate, attach/detach, execute, etc.
- Most flexible action for game-specific mechanics
- Single command, no additional parameters

**ACTION7** - Undo (Optional)
- Reverses previous action
- Support is game-specific
- May be unavailable in some games

#### Complex Action (Two-Parameter)

**ACTION6** - Click/Target Action
- Requires explicit X,Y coordinates
- Both X and Y must be in range 0-63 inclusive
- Used for direct position targeting
- Format: `{"x": int, "y": int}`

#### RESET Command

**RESET** - Restart Level/Game
- Initiates new session or resets existing one
- Behavior depends on current game state:
  - If no actions taken: Starts fresh session
  - If actions executed: Resets to level start
- Returns initial game state, score, and win conditions

## API Structure

### Environment Methods

#### `reset(game_id: str, guid: str = None) -> Observation`

Initializes or resets a game session.

**Parameters**:
- `game_id`: Unique identifier for the game
- `guid`: Session identifier (optional; generated if omitted)

**Returns**:
- Initial visual frame
- Starting score (typically 0)
- Win condition data
- Session GUID

**Behavior**:
- Providing `guid` resets that specific session
- Omitting `guid` creates new session

#### `step(game_id: str, guid: str, action: Action, reasoning: dict = None) -> Observation`

Executes an action and advances the game state.

**Parameters**:
- `game_id`: Game identifier
- `guid`: Session identifier
- `action`: Action object (type + optional data)
- `reasoning`: Optional JSON blob (≤16 KB) for audit/explainability

**Returns**:
- Updated visual frame
- New score
- Game state (playing/won/lost)
- Additional metadata

### Observation Format

Each observation includes:

**Visual Frame**:
- Image representation of current game state
- Typically 64×64 grid rendered as image
- Format: PNG or similar image format

**Score**:
- Integer representing current performance
- Game-specific interpretation
- Often represents action count or efficiency metric

**Game State**:
- `PLAYING`: Game in progress
- `WIN`: Player achieved goal
- `LOSE`: Player failed (if applicable)

**Metadata**:
- Level information (if multi-level game)
- Additional game-specific data

### Action Object Structure

```python
# Simple action example
action = Action(type=ActionType.ACTION1)

# Complex action example (click)
action = Action(
    type=ActionType.ACTION6,
    data={"x": 32, "y": 45}
)

# Action with reasoning
action = Action(
    type=ActionType.ACTION5,
    reasoning={"strategy": "exploring", "hypothesis": "button activates"}
)
```

## Agent Interface

### Required Agent Methods

Agents must implement two core methods:

#### `is_done(frames: List[Frame], latest_frame: Frame) -> bool`

Determines if gameplay should end.

**Parameters**:
- `frames`: List of all previous frames
- `latest_frame`: Current frame with state information

**Returns**:
- `True` if game is complete (win or loss)
- `False` if game should continue

**Typical Implementation**:
```python
def is_done(self, frames, latest_frame):
    return latest_frame.state in [GameState.WIN, GameState.LOSE]
```

#### `choose_action(frames: List[Frame], latest_frame: Frame) -> Action`

Selects the next action to take.

**Parameters**:
- `frames`: Complete game history
- `latest_frame`: Current game state

**Returns**:
- Action object to execute

**Example**:
```python
def choose_action(self, frames, latest_frame):
    # Agent logic here
    return Action(type=ActionType.ACTION1)
```

## Scoring System

### Action Efficiency Metric

**Primary Evaluation**: How many actions does an agent require compared to human baseline?

**Calculation**:
- Record human playthroughs (multiple players)
- Determine median human action count per level
- Agent score = Agent actions / Median human actions

**Interpretation**:
- Score < 1.0: More efficient than average human
- Score = 1.0: Human-level efficiency
- Score > 1.0: Less efficient than average human

### Scorecards

**Scorecard**: Aggregate statistics across multiple game plays

**Tracked Metrics**:
- Games won
- Total games played
- Win rate
- Average action efficiency
- Per-game performance data

**Metadata Support**:
- URL (for replay/visualization)
- Tags (for categorization)
- Opaque JSON (custom data)

## Session Management

### Game Instance Lifecycle

1. **Session Creation**: `reset()` with no GUID generates new session
2. **Action Execution**: `step()` calls advance state
3. **Session Reset**: `reset()` with existing GUID restarts
4. **Per-Level State**: Multi-level games maintain state within session

### GUID Management

- **Format**: Unique identifier (typically UUID)
- **Persistence**: Same GUID maintains session continuity
- **Isolation**: Different GUIDs are independent sessions

## Game Discovery

### List Games Endpoint

**Functionality**: Retrieve available games

**Returns**:
- List of game metadata
- Ordered alphabetically by title
- Includes game IDs for `reset()`/`step()` calls

**Game Metadata**:
- Game ID
- Title
- Description (if available)
- Difficulty (if available)

## Implementation Notes

### For Game Authors

When designing games for ARC-AGI-3:

1. **Action Mapping**: Define what each ACTION1-7 does in your game
   - ACTION1-4 typically map to directional movement
   - ACTION5 is general interaction
   - ACTION6 is position targeting
   - ACTION7 is undo (optional)

2. **Visual Feedback**: All game state must be visible in frames
   - No hidden state that's impossible to discover
   - Visual changes should communicate action effects

3. **Deterministic Behavior**: Same action sequence must produce same result
   - No random elements during play
   - Procedural generation allowed for level creation

4. **Coordinate System**: If using ACTION6 (click):
   - Validate X,Y are in range 0-63
   - Handle out-of-bounds gracefully

5. **Win Conditions**: Make success visually obvious
   - Don't rely on score alone
   - Visual state should clearly indicate win

### For Agent Developers

Key integration points:

1. **API Key**: Required for all API calls
   - Obtain from [three.arcprize.org](https://three.arcprize.org)
   - Set as environment variable `ARC_API_KEY`

2. **Frame History**: Agents receive full game history
   - Can implement memory/learning across frames
   - Useful for pattern recognition

3. **Reasoning Field**: Optional but encouraged
   - Helps with debugging and analysis
   - Limited to 16 KB per action
   - Can be structured JSON

4. **Error Handling**: Handle invalid actions gracefully
   - Out-of-bounds coordinates
   - Invalid action types
   - Connection/API errors

## Repository Structure

Official agent framework: [github.com/arcprize/ARC-AGI-3-Agents](https://github.com/arcprize/ARC-AGI-3-Agents)

```
ARC-AGI-3-Agents/
├── agents/           # Agent implementations
│   ├── __init__.py
│   ├── random.py     # Random baseline
│   └── [your_agent].py
├── tests/            # Test suite
├── main.py           # Entry point
├── .env-example      # API key template
└── pyproject.toml    # Dependencies
```

### Running Agents

```bash
# Clone repository
git clone https://github.com/arcprize/ARC-AGI-3-Agents.git
cd ARC-AGI-3-Agents

# Configure API key
cp .env-example .env
# Edit .env and add your ARC_API_KEY

# Run specific agent on specific game
uv run main.py --agent=random --game=ls20

# Run agent on all games
uv run main.py --agent=myagent
```

### Creating Custom Agents

1. Create agent file in `agents/` directory
2. Import class in `agents/__init__.py`
3. Add to `AVAILABLE_AGENTS` dictionary
4. Run using lowercase class name

**Example**:
```python
# agents/myagent.py
class MyAgent:
    def is_done(self, frames, latest_frame):
        return latest_frame.state == GameState.WIN

    def choose_action(self, frames, latest_frame):
        # Your logic here
        return Action(type=ActionType.ACTION1)

# agents/__init__.py
from .myagent import MyAgent

AVAILABLE_AGENTS = {
    "myagent": MyAgent,
    # ...
}
```

## Technical Stack

### Required Dependencies

- **Python**: 3.10+ recommended
- **Package Manager**: `uv` (recommended) or `pip`
- **Testing**: `pytest`
- **Linting**: `ruff`

### API Communication

- **Protocol**: HTTPS REST API
- **Authentication**: API key in headers
- **Rate Limits**: TBD (check docs.arcprize.org for current limits)

## Resources

- **Documentation**: [docs.arcprize.org](https://docs.arcprize.org)
- **Agent Quickstart**: [docs.arcprize.org/agents-quickstart](https://docs.arcprize.org/agents-quickstart)
- **GitHub Repository**: [github.com/arcprize/ARC-AGI-3-Agents](https://github.com/arcprize/ARC-AGI-3-Agents)
- **API Portal**: [three.arcprize.org](https://three.arcprize.org)
- **Contact**: team@arcprize.org
