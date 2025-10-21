# ARC-AGI-3 Official Design Constraints

**Source**: [arcprize.org/arc-agi/3](https://arcprize.org/arc-agi/3/) & [30-Day Learnings Blog Post](https://arcprize.org/blog/arc-agi-3-preview-30-day-learnings)
**Last Updated**: October 2025

## Mandatory Requirements

All ARC-AGI-3 games MUST satisfy these constraints:

### 1. Human Accessibility

**"Easy for humans (can pick it up in <1 min of game play)"**

- Rules must be discoverable through play alone
- No tutorial or instructions required
- First-time players should grasp basic mechanics within 60 seconds
- Learning curve should be intuitive, not frustrating

**Playability Duration**: 5-10 minutes for competent human players

### 2. Core Knowledge Priors Only

**"Core Knowledge Priors (no language, trivia, cultural symbols)"**

Games MUST rely ONLY on:
- ✅ Basic mathematics (counting, arithmetic, modular math, etc.)
- ✅ Basic geometry (shapes, symmetry, distance, area, etc.)
- ✅ Object-ness (recognizing distinct entities)
- ✅ Agent-ness (understanding entities that act with purpose)
- ✅ Spatial reasoning (positions, adjacency, containment, etc.)
- ✅ Temporal reasoning (sequences, cause-effect, prediction)

Games MUST NOT require:
- ❌ Language or linguistic knowledge
- ❌ Cultural knowledge or symbols
- ❌ Trivia or memorized facts
- ❌ Domain-specific expertise
- ❌ Reading or text interpretation
- ❌ Cultural references or context

### 3. No Instructions Required

**"Should require no instructions to play"**

- Zero on-screen text during gameplay
- No tutorial levels that explicitly teach mechanics
- No written rules or guides
- Players learn by experimentation and observation
- Visual feedback must communicate all necessary information

### 4. Human Enjoyment

**"Should still be fun for humans"**

- Must be engaging, not tedious
- Should provide satisfying "aha!" moments
- Difficulty should feel fair, not arbitrary
- Success should feel earned

### 5. Novelty Encouraged

**Innovation in game mechanics is highly valued**

Specifically encouraged mechanics:
- Hidden state (information not immediately visible)
- Theory of Mind (reasoning about other agents' knowledge/intent)
- Long-horizon planning (multi-step strategies)
- Multi-agent interaction (cooperating or competing with NPCs)
- Emergent complexity (simple rules → deep gameplay)

## Technical Constraints

### Grid & Display

- **Grid Size**: 64×64 maximum
- **Colors**: 16 distinct colors available
- **Coordinate Range**: 0-63 inclusive (both X and Y axes)
- **Visual Only**: No text, numbers, or symbols on screen during play

### Deterministic Behavior

- Same inputs must produce same outputs
- No randomness during gameplay (procedural level generation allowed)
- Physics must be consistent and predictable
- Interactions must be mathematically precise

### Action Space

Games should work within the standard action framework:
- **RESET**: Restart level/game
- **ACTION1-4**: Typically directional movement (up/down/left/right)
- **ACTION5**: General interaction (select, rotate, attach, execute, etc.)
- **ACTION6**: Click action with X,Y coordinates (0-63 range)
- **ACTION7**: Undo (optional support)

## Design Principles from Preview Competition

### What Makes a Good ARC-AGI-3 Game

Based on the August 2025 preview competition findings:

#### ✅ DO: Resist Brute-Force Approaches

Games must require reasoning, not random search or exhaustive exploration.

**Good**: Goal requires understanding a pattern or rule
**Bad**: Goal can be found by trying every possible action

#### ✅ DO: Make Actions Clearly Available

Players should understand which actions are valid and what they do.

**Good**: Visual cues indicate interactive elements
**Bad**: Hidden mechanics with no discoverability path

#### ✅ DO: Reward Efficiency

Design should encourage optimal play, not just any solution.

**Good**: Minimal-move solutions require insight
**Bad**: Any random sequence eventually works

#### ✅ DO: Test Specific Reasoning Skills

Each game should probe particular cognitive capabilities.

**Examples**:
- **Exploration**: How efficiently do agents discover rules?
- **Memory**: Can they remember and apply past observations?
- **Planning**: Do they form multi-step strategies?
- **Abstraction**: Can they identify underlying patterns?

#### ❌ AVOID: Pure Trial-and-Error

If a game can be solved by randomly trying actions until something works, it's not testing reasoning.

#### ❌ AVOID: Ambiguous Win Conditions

Players should clearly know when they've succeeded.

**Good**: Visual state change that's obviously a win (all tiles same color, agent reaches goal, etc.)
**Bad**: Subtle change that could be missed

## Evaluation Criteria

Your game will be evaluated on:

### 1. Action Efficiency Metric

- How many actions do agents require vs. human baseline?
- Does the game distinguish skilled from unskilled play?
- Is there a clear "optimal" solution path?

### 2. Reasoning Requirements

- What cognitive skills does the game test?
- Can the game be brute-forced?
- Does success require understanding rules?

### 3. Human Playability

- Can a human learn it in < 1 minute?
- Is it completable in 5-10 minutes?
- Is it enjoyable to play?

### 4. Novelty

- Does it test something new?
- Does it introduce fresh mechanics?
- Does it probe underexplored reasoning capabilities?

### 5. Core Priors Alignment

- Uses only basic math/geometry/spatial reasoning?
- No language, cultural knowledge, or trivia required?
- Fully learnable through visual observation?

## Anti-Patterns to Avoid

Based on preview competition feedback:

### Too Friendly to Random Search

**Problem**: Agent can succeed by random exploration without understanding

**Example**: Grid with hidden goal that's found by clicking everywhere

**Solution**: Require pattern recognition or rule understanding to identify goal location

### Unclear Mechanics

**Problem**: Players don't know what actions do or what's interactive

**Example**: Objects that look identical but behave differently

**Solution**: Visual distinction for different object types, clear affordances

### Tedious Execution

**Problem**: Player understands solution but execution is repetitive

**Example**: Must click 50 identical tiles one-by-one

**Solution**: Design efficient interaction methods, avoid pure grinding

### Ambiguous Success

**Problem**: Player isn't sure if they won or what the goal was

**Example**: Goal is "maximize score" but no score is visible

**Solution**: Clear visual win state, obvious goal indication

## Submission Checklist

Before submitting your game idea, verify:

- [ ] Can a human learn the game in < 1 minute of play?
- [ ] Is it completable by a competent human in 5-10 minutes?
- [ ] Does it work with no text/instructions/tutorials?
- [ ] Does it use only core knowledge priors (no language/trivia/culture)?
- [ ] Is it fun and engaging for humans?
- [ ] Does it resist brute-force approaches?
- [ ] Does it require reasoning, not just random exploration?
- [ ] Are win conditions clear and obvious?
- [ ] Does it test specific cognitive capabilities?
- [ ] Is behavior deterministic and consistent?
- [ ] Does it fit within 64×64 grid and 16-color constraints?

## Resources

- **Official Design Constraints**: [arcprize.org/arc-agi/3](https://arcprize.org/arc-agi/3/)
- **30-Day Learnings**: [arcprize.org/blog/arc-agi-3-preview-30-day-learnings](https://arcprize.org/blog/arc-agi-3-preview-30-day-learnings)
- **Submit Game Ideas**: [https://forms.gle/aVD4L4xRaJqJoZvE6](https://forms.gle/aVD4L4xRaJqJoZvE6)
- **Contact**: team@arcprize.org
