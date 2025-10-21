# Game Specification Template

**Use this template when proposing a new game for ARC-AGI-3**

---

# [GAME NAME]

**Author**: [Your Name/Organization]
**Date**: [Submission Date]
**Version**: 1.0

## 1. Game Overview

### Name
[Full game name]

### One-Sentence Description
[Concise description of the core mechanic/challenge]

### Skills Under Test
[Check all that apply and explain how your game tests each]

- [ ] **Exploration** - How players discover rules and mechanics
- [ ] **Memory** - What information must be retained
- [ ] **Planning** - What multi-step strategies are required
- [ ] **Abstraction** - What patterns must be recognized
- [ ] **Goal Acquisition** - How players identify objectives
- [ ] **Spatial Reasoning** - What geometric/positional understanding is needed
- [ ] **Theory of Mind** - Reasoning about other agents (if multi-agent)
- [ ] **Object-ness** - Understanding distinct entities
- [ ] **Agent-ness** - Understanding purposeful actors

**Primary Skill**: [The main cognitive capability this game probes]

**Why This Matters**: [1-2 sentences on why testing this skill is important for AGI evaluation]

---

## 2. Human Intuitiveness

### First 60 Seconds
**Question**: What does a human intuit when they first start playing?

[Describe the player's likely initial experience]

**Example**:
- "Player sees a green square (agent) and various colored obstacles"
- "First action (arrow key) moves the agent"
- "Within 30 seconds, player realizes they can push blue blocks but not red ones"
- "By 60 seconds, player understands goal is to reach the yellow target"

### Rule Discovery Path
**Question**: How do players discover the rules without instructions?

[Outline the intended discovery sequence]

**Example**:
1. Movement discovered through directional keys
2. Push mechanics discovered by attempting to move into blocks
3. Goal discovered by reaching it accidentally or through exploration
4. Optimal strategy emerges from understanding push constraints

### Visual Goal Communication
**Question**: How is the goal obvious without text?

[Explain what visual cues communicate the objective]

**Example**:
- "Yellow target square visually distinct"
- "Agent and target use contrasting colors"
- "Reaching target triggers clear visual feedback (flash/color change)"

---

## 3. Visual Design

### Grid Dimensions
- **Width**: [Number of cells, ≤64]
- **Height**: [Number of cells, ≤64]
- **Note**: Must be square grid (Width = Height)

### Color Palette
[List each color used and its meaning. Use indices 0-15 for ARC-AGI-3, or 0-9 for your current prototype]

| Color Index | Visual Color | Game Meaning | Behavior |
|-------------|--------------|--------------|----------|
| 0 | Black | Background/Empty Space | Passable |
| 3 | Green | Player Agent | Moves with arrow keys |
| 1 | Blue | Movable Block | Can be pushed |
| 2 | Red | Immovable Wall | Blocks movement |
| 4 | Yellow | Goal Target | Win condition |
| ... | ... | ... | ... |

### Object Behaviors

**[Object Type 1]**:
- Appearance: [Color, shape if relevant]
- Behavior: [How it acts/reacts]
- Interactions: [What happens when player/other objects touch it]

**[Object Type 2]**:
[Repeat for each object type]

### Hidden State (if any)
[Describe any information not immediately visible but discoverable]

**Example**:
- "Switches toggle invisible door states"
- "Player can discover this by activating switch and exploring"
- "Door state indicated by subtle color change (dark gray → light gray)"

**Important**: All hidden state must be discoverable through visual observation and experimentation.

---

## 4. Game Mechanics

### Core Rules

1. **[Rule 1 Name]**
   - Description: [What the rule does]
   - Discovery: [How players learn this]
   - Example: [Concrete example of rule in action]

2. **[Rule 2 Name]**
   [Repeat structure]

**Example**:
1. **Push Mechanics**
   - Description: Player can push blue blocks one space in movement direction
   - Discovery: First attempt to move through blue block results in push
   - Example: Player at (5,5) pressing RIGHT with blue block at (6,5) → Player moves to (6,5), block moves to (7,5)

### Action Mapping

| Action | Function | Required? |
|--------|----------|-----------|
| RESET | Restart current level | ✅ Yes |
| ACTION1 | [e.g., Move Up] | ✅ Yes |
| ACTION2 | [e.g., Move Down] | ✅ Yes |
| ACTION3 | [e.g., Move Left] | ✅ Yes |
| ACTION4 | [e.g., Move Right] | ✅ Yes |
| ACTION5 | [e.g., Activate/Interact] | ⬜ Optional |
| ACTION6 | [e.g., Click position] | ⬜ Optional |
| ACTION7 | Undo | ⬜ Optional |

---

## 5. Goal & Win Condition

### Success Criteria
[Precisely define what constitutes a win]

**Example**: "Player agent (green) occupies same cell as goal target (yellow)"

### Visual Win State
[Describe what the screen looks like when player wins]

**Example**:
- "Target square flashes bright white"
- "All cells briefly turn green"
- "Agent and target merge into single pulsing golden cell"

### Efficiency Metric
[How do you measure optimal play?]

**Options**:
- Minimum number of actions
- Fewest pushes/interactions
- Least backtracking
- Optimal path length

**Example**: "Optimal solution uses 12 actions. Human average: 15-20 actions."

### Loss Condition (if applicable)
[Define how a player can fail, if relevant]

**Example**: "Pushing block into corner where it can't be retrieved makes level unsolvable"

---

## 6. Level Generation

### Procedural Generation Approach
[Describe how levels are created to prevent memorization]

**Parameters That Vary**:
- [List what changes between instances]

**Example**:
- Grid size (12×12 to 24×24)
- Number of blocks (3-8)
- Block positions (random valid placements)
- Goal position (random corner)
- Obstacle configuration (ensures solvability)

### Difficulty Scaling
[How do levels get harder?]

**Example**:
- Level 1: 12×12 grid, 3 blocks, direct path possible
- Level 5: 20×20 grid, 6 blocks, requires planning sequence
- Level 10: 24×24 grid, 8 blocks, requires backtracking and multi-step thinking

### Solvability Guarantee
[How do you ensure generated levels are always solvable?]

**Example**:
- "A* pathfinding validates solution exists before presenting level"
- "Procedural generation uses constructive approach: start from goal, work backward"

---

## 7. Anti-Overfit Design

### Why This Resists Brute-Force

**Question**: Why can't an agent just try random actions until something works?

[Explain what prevents brute-forcing]

**Example**:
- "Random moves quickly create unsolvable states (blocks in corners)"
- "Action space is large (4 directions × ~50 valid cells = ~200 possible action sequences)"
- "Solution requires understanding push mechanics, not exhaustive search"

### Why Memorization Won't Work

**Question**: Why can't an agent memorize solutions?

[Explain variation between instances]

**Example**:
- "Procedural generation creates billions of possible level configurations"
- "Block positions, grid size, and goal location vary"
- "Solution strategy transfers but specific action sequence doesn't"

### Reasoning Requirements

**Question**: What understanding is necessary to solve efficiently?

[List the insights a solver must develop]

**Example**:
1. "Understand blocks can be pushed but not pulled"
2. "Recognize dead-end positions (blocks in corners)"
3. "Plan push sequences that don't create dead-ends"
4. "Work backward from goal to determine required block positions"

---

## 8. Core Priors Alignment

### Required Core Priors

[List ONLY the basic knowledge needed—no language, trivia, or culture]

**Spatial Reasoning**:
- [What spatial concepts are needed?]

**Mathematical**:
- [What math concepts are needed?]

**Other Core Priors**:
- [Any other fundamental reasoning abilities?]

**Example**:
- **Spatial**: Understanding adjacency, grid positions, movement direction
- **Mathematical**: Counting steps, recognizing geometric constraints
- **Other**: Object permanence (blocks don't disappear), causality (pushing causes movement)

### No Language/Culture Required

**Confirmation**: This game requires:
- ✅ NO reading or text interpretation
- ✅ NO cultural knowledge or symbols
- ✅ NO trivia or memorized facts
- ✅ NO language understanding

### Learnable Through Visual Observation

**Confirmation**:
- ✅ All rules discoverable by experimentation
- ✅ Visual feedback communicates all necessary information
- ✅ No external instructions needed

---

## 9. Implementation Notes

### Technical Complexity
[Rate and explain]

- **Grid Logic**: [Simple/Moderate/Complex]
- **Collision Detection**: [Simple/Moderate/Complex]
- **State Management**: [Simple/Moderate/Complex]
- **Rendering**: [Simple/Moderate/Complex]

### Estimated Development Time
[For creating MVP prototype]

**Example**: "~40 hours for working prototype with 3-5 sample levels"

### Dependencies
[What's needed to implement?]

**Example**:
- Grid/array manipulation
- Basic pathfinding (for validation)
- Sprite rendering or cell-based graphics

---

## 10. Novelty & Contribution

### What Makes This Unique?
[How is this different from existing ARC-AGI-3 games or common puzzle genres?]

**Example**:
- "Tests spatial planning + resource limitation simultaneously"
- "Introduces irreversible actions (block pushing) requiring look-ahead"
- "Combines sokoban-style mechanics with novel twist [describe twist]"

### What Reasoning Capability Does This Uniquely Test?
[What cognitive skill is underexplored in current benchmarks?]

**Example**:
- "Tests ability to recognize irreversible states and plan around them"
- "Probes forward chaining (working from current state) vs. backward chaining (working from goal)"

### Why This Advances ARC-AGI-3 Goals
[Connect to the benchmark's mission]

**Example**:
- "Current games focus on pattern recognition; this tests sequential planning"
- "Adds novel challenge in resource constraint reasoning"
- "Provides clear action-efficiency metric for AI evaluation"

---

## 11. Human Playtest Results (if available)

[If you've tested with humans, include findings]

### Participants
- Number: [How many people?]
- Background: [Technical/Non-technical?]

### Learning Time
- Average time to understand goal: [X seconds/minutes]
- Average time to first success: [X minutes]

### Enjoyment
- Rating: [X/10]
- Common feedback: [What did players say?]

### Action Efficiency
- Human optimal: [X actions]
- Human average: [Y actions]
- Human range: [Min-Max actions]

---

## 12. Demo Materials

### Repository
[Link to code repository if available]

### Video Demo
[Link to human playthrough video]

### Screenshots
[Include or link to key gameplay moments]

1. **Initial State**: [Screenshot of starting configuration]
2. **Mid-Game**: [Screenshot showing player solving]
3. **Win State**: [Screenshot of victory condition]

### Sample Replay
[Link to JSON action log if available]

---

## 13. Submission Checklist

Before submitting, verify:

### Design Constraints ✓
- [ ] Human can learn in < 1 minute
- [ ] Playable in 5-10 minutes
- [ ] No text/instructions required during gameplay
- [ ] Uses only core knowledge priors (no language/trivia/culture)
- [ ] Fun and engaging for humans
- [ ] Tests novel or underexplored reasoning skills

### Technical Requirements ✓
- [ ] Fits within 64×64 grid (square grid mandatory)
- [ ] Uses ≤16 colors from ARC palette
- [ ] Works with ACTION1-7 framework
- [ ] Deterministic behavior (same input → same output)
- [ ] Clear, visually obvious win condition
- [ ] Resists brute-force approaches
- [ ] Procedural level generation implemented

### Documentation ✓
- [ ] Complete GAME_SPEC.md (this document)
- [ ] Clear README.md in repository
- [ ] Demo video exists
- [ ] Sample gameplay footage or screenshots
- [ ] Code is clean and readable

### Testing ✓
- [ ] Prototype tested with humans
- [ ] Win condition triggers correctly
- [ ] Level generation produces valid puzzles
- [ ] Visual feedback is clear and understandable

---

## 14. Contact & Submission

### Author Information
- **Name**: [Your name]
- **Email**: [Your email]
- **GitHub**: [Your GitHub username]
- **Affiliation** (optional): [University/Organization]

### Submission Details
- **Submitted to**: [ARC Prize Form / Discord / Email]
- **Date**: [Submission date]
- **Version**: [Version number]

### License
[Specify license for your game code/design]

**Recommended**: MIT or Apache 2.0 (open source)

---

## Additional Notes

[Any other relevant information, considerations, or future development ideas]

---

**End of Game Specification**

*For questions about this template or the submission process, see [SUBMISSION_PROCESS.md](SUBMISSION_PROCESS.md) or contact team@arcprize.org*
