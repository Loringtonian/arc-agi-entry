# Game Mechanics Library for ARC-AGI-3

**Purpose**: Reference library of 55+ game mechanics suitable for ARC-AGI-3 puzzle games
**Updated**: October 2025 to align with official ARC-AGI-3 specifications
**Status**: Community-generated mechanics catalog

## ARC-AGI-3 Alignment Notes

These mechanics were originally designed for a 10-color, 64×64 grid system. **ARC-AGI-3 officially supports**:
- **Grid**: Up to 64×64 cells (square grids mandatory)
- **Colors**: 16 distinct colors (indices 0-15)
- **Actions**: 7 core actions (RESET + ACTION1-7)
- **Design Constraints**:
  - Easy for humans (< 1 min to learn)
  - Playable in 5-10 minutes
  - No text/instructions required
  - Uses only core knowledge priors (no language/trivia/culture)
  - Deterministic behavior
  - Resists brute-force approaches

All mechanics below are **compatible with ARC-AGI-3 requirements** and can be adapted to the 16-color palette and 7-action framework.

---

## How to Use This Library

1. **Compose Hybrids** - Combine mechanics (e.g., Momentum Glide + Pendulum Gates = timed ice-slides)
2. **Vary Grid Scale** - Some mechanics shine on 8×8, others need 64×64
3. **Tune Color Semantics** - Same color can be "agent," "wall," "resource," or "timer" depending on rules
4. **Expose Parameters** - Solvers learn faster when instances supply k, p, or sequence length explicitly
5. **Map to Actions** - Define which ACTION1-7 controls do what in your game

With these mechanics you can craft hundreds of distinct puzzle instances, each challenging a different slice of reasoning—from pure search, through probabilistic inference, all the way up to incremental rule discovery.

---

## Core Mechanics Collection (40 Base Mechanics)

Below is a collection of 40 mechanics you can mix-and-match. Each description is concrete enough that you—and anyone trying to build an automated solver—can formalize the rules on a ≤64×64 square grid.

### State & Movement

**#1 - Sliding Token**
- **Core Idea**: A single "agent" color slides one step per tick; walls are other colors; reach the goal
- **Why Interesting**: Algorithms must handle path-planning with changing obstacles
- **ARC-AGI-3 Fit**: ✅ Tests exploration, planning, spatial reasoning

**#2 - Wrap-Around Runner**
- **Core Idea**: Exiting the grid on one edge re-enters on the opposite (toroidal space)
- **Why Interesting**: Introduces modulo arithmetic and global reasoning
- **ARC-AGI-3 Fit**: ✅ Tests spatial reasoning with non-Euclidean topology

**#3 - Color Conveyor Belts**
- **Core Idea**: Squares cycle their color rightward each tick, acting like belts
- **Why Interesting**: Requires predicting future positions, not just present state
- **ARC-AGI-3 Fit**: ✅ Tests temporal prediction and planning

**#4 - Push-Block Sokoban**
- **Core Idea**: Agent pushes colored crates onto matching target pads
- **Why Interesting**: Classic NP-hard puzzle—good for heuristic search
- **ARC-AGI-3 Fit**: ✅ Tests planning, irreversible actions, spatial reasoning

**#5 - Momentum Glide**
- **Core Idea**: Once moving, the agent continues until hitting a wall
- **Why Interesting**: Demands look-ahead and inevitable-state detection
- **ARC-AGI-3 Fit**: ✅ Tests planning with constrained control

### Timing & Rhythm

**#6 - Beat Sequencer**
- **Core Idea**: Only every k-th tick can you act; other ticks are skipped
- **Why Interesting**: Forces temporal planning and modular arithmetic
- **ARC-AGI-3 Fit**: ✅ Tests temporal reasoning and synchronization

**#7 - Fading Trails**
- **Core Idea**: Recently visited squares fade through a color gradient before clearing
- **Why Interesting**: Memory of the past influences legal moves
- **ARC-AGI-3 Fit**: ✅ Tests memory and spatial awareness

**#8 - Pendulum Gates**
- **Core Idea**: Gates open/close on a global sine-wave schedule
- **Why Interesting**: Synchronization and phase prediction are required
- **ARC-AGI-3 Fit**: ✅ Tests temporal prediction and timing

**#9 - Cascade Reaction**
- **Core Idea**: Performing an action starts a countdown (displayed as shade) that triggers a board-wide effect
- **Why Interesting**: Chains of delayed consequences test causal reasoning
- **ARC-AGI-3 Fit**: ✅ Tests causal reasoning and delayed planning

### Memory & Sequence

**#10 - Simon Path**
- **Core Idea**: Grid flashes a sequence of positions you must repeat exactly
- **Why Interesting**: Solvers need short-term sequence memory
- **ARC-AGI-3 Fit**: ✅ Tests memory and sequence reproduction

**#11 - Lock-Key Pairs**
- **Core Idea**: Collect keys (colored squares) in a required order to unlock doors
- **Why Interesting**: Permutation reasoning & ordering constraints
- **ARC-AGI-3 Fit**: ✅ Tests planning with ordering constraints

**#12 - Echo Maze**
- **Core Idea**: Stepping on a tile creates a clone that retraces your past n moves behind you. Avoid collisions
- **Why Interesting**: Requires anticipating multiple intertwined histories
- **ARC-AGI-3 Fit**: ✅ Tests memory, prediction, and spatial reasoning

### Pattern Formation

**#13 - Color Flood Fill** ⭐ *Implemented in good_games/*
- **Core Idea**: Change the color of the starting corner; goal is to flood the grid with a target pattern in ≤m moves
- **Why Interesting**: Relates to graph coloring & BFS
- **ARC-AGI-3 Fit**: ✅ Tests graph reasoning and optimization

**#14 - Symmetry Painter**
- **Core Idea**: Every paint action is mirrored across one or more axes; produce a goal pattern
- **Why Interesting**: Touches on group theory and constraint satisfaction
- **ARC-AGI-3 Fit**: ✅ Tests symmetry reasoning and planning

**#15 - Life-Like Automaton**
- **Core Idea**: Each tick, colors update by Conway-style rules; you seed the initial pattern
- **Why Interesting**: Solvers must learn emergent dynamics
- **ARC-AGI-3 Fit**: ⚠️ May need adaptation (cellular automata can be hard to discover visually)

**#16 - Tiling Constraints**
- **Core Idea**: Only certain 2×2 color blocks are legal; fill the grid completely
- **Why Interesting**: Reduces to exact-cover / constraint propagation
- **ARC-AGI-3 Fit**: ✅ Tests constraint satisfaction and pattern matching

**#17 - Fractal Growth**
- **Core Idea**: Each colored seed replicates outward following L-system rules until halted by blockers
- **Why Interesting**: Requires predicting recursive expansion
- **ARC-AGI-3 Fit**: ✅ Tests recursive reasoning and prediction

### Resource & Optimization

**#18 - Energy Budget**
- **Core Idea**: Each move costs energy, shown as a diminishing color bar; maximize score before depletion
- **Why Interesting**: Poses a shortest-path with weighted costs
- **ARC-AGI-3 Fit**: ✅ Tests resource management and optimization

**#19 - Harvest & Convert**
- **Core Idea**: Collect resource tiles, then drop them on converters to upgrade score-multiplier colors
- **Why Interesting**: Introduces inventory management
- **ARC-AGI-3 Fit**: ✅ Tests planning with resource collection

**#20 - Risk-Reward Gradient**
- **Core Idea**: High-value colors appear near hazards that erase you on contact
- **Why Interesting**: Balances exploration vs. safety
- **ARC-AGI-3 Fit**: ✅ Tests risk assessment and planning

### Multi-Agent / Adversarial

**#21 - Chaser & Runner**
- **Core Idea**: An AI "monster" color moves greedily toward you; survive T ticks
- **Why Interesting**: Invokes pursuit-evasion algorithms
- **ARC-AGI-3 Fit**: ✅ Tests evasion planning and agent reasoning

**#22 - Swarm Herding**
- **Core Idea**: Lead multiple wandering agents into goal zones by blocking paths
- **Why Interesting**: Multi-body coordination and flocking dynamics
- **ARC-AGI-3 Fit**: ✅ Tests multi-agent reasoning and coordination

**#23 - Territory Claim**
- **Core Idea**: Two colors expand one square per tick; you place walls to maximize your color's area
- **Why Interesting**: Competitive influence-maximization
- **ARC-AGI-3 Fit**: ✅ Tests strategic planning and area control

### Topology & Geometry

**#24 - Elevated Layers**
- **Core Idea**: Color encodes height; only ascend/descend one unit per move
- **Why Interesting**: Converts 2-D grid into discretized 3-D terrain
- **ARC-AGI-3 Fit**: ✅ Tests spatial reasoning with height constraints

**#25 - Mirror World**
- **Core Idea**: The board displays both the "real" layer and a mirrored phantom layer; moves affect both in inverse ways
- **Why Interesting**: Dual-state reasoning
- **ARC-AGI-3 Fit**: ✅ Tests dual-state tracking and planning

**#26 - Portal Pairs**
- **Core Idea**: Stepping on a portal instantly teleports to its partner of same color
- **Why Interesting**: Non-local connectivity challenges path-finding heuristics
- **ARC-AGI-3 Fit**: ✅ Tests spatial reasoning with non-Euclidean connectivity

### Signal Processing & Waves

**#27 - Color Wavefronts**
- **Core Idea**: Selected tiles emit concentric rings of alternating colors each tick; align rings to hit targets
- **Why Interesting**: Spatial-temporal interference prediction
- **ARC-AGI-3 Fit**: ✅ Tests wave mechanics and timing

**#28 - Harmonic Locks**
- **Core Idea**: A gate opens only when three oscillating color signals align on the same tick
- **Why Interesting**: Requires computing least-common multiples
- **ARC-AGI-3 Fit**: ✅ Tests synchronization and mathematical reasoning

**#29 - Phase Shift Terrain**
- **Core Idea**: Land tiles cyclically shift through a 3-color palette; only specific phases are passable
- **Why Interesting**: Demands phase tracking
- **ARC-AGI-3 Fit**: ✅ Tests temporal prediction and planning

### Stochastic & Hidden Information

**#30 - Fog of War**
- **Core Idea**: Unseen squares reveal color only when adjacent; finish with limited peeks
- **Why Interesting**: Combines exploration with inference
- **ARC-AGI-3 Fit**: ⚠️ ARC-AGI-3 prefers deterministic games; use sparingly

**#31 - Probabilistic Walls**
- **Core Idea**: A "quantum" wall turns solid with probability p each tick, shown as a flickering shade
- **Why Interesting**: Solvers must reason over expected value and risk
- **ARC-AGI-3 Fit**: ❌ Violates determinism requirement (not ARC-AGI-3 compliant)

**#32 - Hidden Mines**
- **Core Idea**: Certain colors indicate probability of adjacent mines (classic Minesweeper logic)
- **Why Interesting**: Deductive reasoning under uncertainty
- **ARC-AGI-3 Fit**: ⚠️ Only if mine placement is deterministic and discoverable

### Transformation & Rewriting

**#33 - Color Cyclic Permute**
- **Core Idea**: A global "clock" rotates all colors (0→1→2…). Your actions must account for future rotations
- **Why Interesting**: Adds modular arithmetic to state space
- **ARC-AGI-3 Fit**: ✅ Tests modular math and prediction

**#34 - Swap-Rule Grammar**
- **Core Idea**: Specified 3×3 patterns auto-swap to new colors each tick (Wang-tile style)
- **Why Interesting**: Equivalent to local string-rewrite systems
- **ARC-AGI-3 Fit**: ✅ Tests pattern recognition and prediction

**#35 - Repaint Ray**
- **Core Idea**: Fire a beam that converts every nth square to a chosen color until blocked
- **Why Interesting**: Line-of-sight computation
- **ARC-AGI-3 Fit**: ✅ Tests geometric reasoning and planning

### Score-Chasing Variants

**#36 - Combo Chains**
- **Core Idea**: Removing a block triggers gravity; cascading clears multiply score
- **Why Interesting**: Promotes search for high-yield configurations
- **ARC-AGI-3 Fit**: ⚠️ Score-focused; ensure clear win condition beyond score

**#37 - Time-Attack Dash**
- **Core Idea**: Points decay exponentially with time; finish objectives ASAP
- **Why Interesting**: Pushes greedy vs. full-search trade-offs
- **ARC-AGI-3 Fit**: ⚠️ Time pressure may conflict with action efficiency metric

**#38 - Precision Paint**
- **Core Idea**: Score equals the count of correctly colored squares minus mis-colored ones. Perfect accuracy matters
- **Why Interesting**: Fine-grained evaluation for learning agents
- **ARC-AGI-3 Fit**: ✅ Tests precision and planning

### Meta / Learning Mechanics

**#39 - Rule Discovery**
- **Core Idea**: The update rule itself (e.g., which neighborhood triggers a color change) is hidden; infer by observing a few ticks
- **Why Interesting**: Encourages hypothesis-testing and adaptive algorithms
- **ARC-AGI-3 Fit**: ✅ Perfect for ARC-AGI-3! Tests meta-learning

**#40 - Curriculum Unlock**
- **Core Idea**: Completing easy boards unlocks new colors or larger grids in the same episode
- **Why Interesting**: Requires long-term skill accumulation and transfer
- **ARC-AGI-3 Fit**: ✅ Tests long-horizon planning and skill transfer

---

## Refined Mechanics Collection (15 Additional)

These 15 mechanics emphasize the core constraints: exactly 16 discrete colors max, square grid ≤64×64, no sound or text, no cultural knowledge—relying on basic math, geometry, agent-ness, and object-ness.

### Refined Mechanics

**#41 - Parity Painter**
- **Core Idea**: Two colors represent bits (0/1). Stepping on a cell toggles its bit and the four orthogonal neighbors. Win by driving every bit to 0
- **Why Interesting**: Classic "Lights Out" linear-algebra problem on GF(2); finding minimum toggle set requires reasoning about parity and matrix rank
- **ARC-AGI-3 Fit**: ✅ Tests mathematical reasoning (modular arithmetic, linear algebra)

**#42 - Vector Slide**
- **Core Idea**: Eight arrow colors encode unit vectors (N, S, E, W, NE, NW, SE, SW), one color is "agent," one is "goal." When agent enters an arrow square, it teleports one step in that vector (wrapping at edges)
- **Why Interesting**: Path-finding in a directed graph with deterministic teleports; requires reasoning with modular arithmetic on coordinates
- **ARC-AGI-3 Fit**: ✅ Tests spatial reasoning and vector math

**#43 - Modular Collector**
- **Core Idea**: Six token colors represent integers 0-5. A door opens only when (sum of collected tokens) mod 6 equals the door's color-value
- **Why Interesting**: Knapsack-style planning under modular constraints; requires keeping running residue class
- **ARC-AGI-3 Fit**: ✅ Tests modular arithmetic and planning

**#44 - Voronoi Claim**
- **Core Idea**: You may drop up to k "seed" colors. On final tick every empty tile adopts the color of its nearest seed (Manhattan distance). Score is your total claimed area
- **Why Interesting**: Geometric partitioning and distance minimization; algorithms must search seed placements that maximize Voronoi cells
- **ARC-AGI-3 Fit**: ✅ Tests geometric reasoning and area optimization

**#45 - Centroid Balancer**
- **Core Idea**: Five block colors encode weights 1-5. Place exactly n blocks so that the discrete center-of-mass of all blocks lands on a marked target cell
- **Why Interesting**: Basic coordinate geometry and integer-weighted averaging; solvers need to enumerate weight configurations efficiently
- **ARC-AGI-3 Fit**: ✅ Tests mathematical reasoning (center of mass, weighted averages)

**#46 - Spiral Enumerator**
- **Core Idea**: The board specifies a start color and a spiral direction (clockwise or counter). Agent must visit every cell in exact spiral order without revisiting
- **Why Interesting**: Deriving the mathematical rule for the target permutation of coordinates and planning a Hamiltonian path that matches it
- **ARC-AGI-3 Fit**: ✅ Tests pattern recognition and path planning

**#47 - Collision Sum**
- **Core Idea**: Colored "balls" slide simultaneously one step per tick. When two collide, they merge into a new color whose numeric value is (a + b) mod 10 [or mod 16]. Reach a prescribed final multiset
- **Why Interesting**: Predicting pairwise collisions, conservation of momentum, and modular arithmetic on color-values
- **ARC-AGI-3 Fit**: ✅ Tests physics simulation and modular math

**#48 - Color Parasite**
- **Core Idea**: A special parasite color overwrites any adjacent color, but decays after three ticks unless it infects another square. Victory = full infection or full containment
- **Why Interesting**: Spatiotemporal spread vs. blocking—object interaction and epidemic modeling within discrete steps
- **ARC-AGI-3 Fit**: ✅ Tests spreading dynamics and strategic blocking

**#49 - Polarity Chain**
- **Core Idea**: Two charge colors (+, –). A neutral object moves one step each tick in the direction of the net adjacent charge vector (sum of neighboring + minus –). Rearrange charges to guide object to goal
- **Why Interesting**: Continuous-valued vector reasoning emerging from discrete local sums; feedback is fully visible, no hidden state
- **ARC-AGI-3 Fit**: ✅ Tests vector math and force reasoning

**#50 - Inkblot Symmetry Prison**
- **Core Idea**: Board enforces mirror symmetry across a moving axis; any move that breaks symmetry is cloned to restore it, often in unexpected spot. Escape by exploiting axis shift to reach asymmetrical goal region
- **Why Interesting**: High-order spatial symmetry prediction and exploiting transformation rules
- **ARC-AGI-3 Fit**: ✅ Tests symmetry reasoning and constraint exploitation

**#51 - Time-Lapse Garden**
- **Core Idea**: Plant colored seeds that grow into deterministic fractal shapes after n ticks. You can't prune. Match a target end-state
- **Why Interesting**: Recursive growth forecasting and combinatorial seed placement
- **ARC-AGI-3 Fit**: ✅ Tests recursive reasoning and prediction

**#52 - Inter-Dimensional Swap Grid**
- **Core Idea**: Every m ticks the visible grid swaps with a "ghost" grid that obeys inverted motion rules (e.g., agents move oppositely). Both persist between swaps. Achieve goal in either reality
- **Why Interesting**: Dual-state planning with periodic rule alternation; timestep synchronization
- **ARC-AGI-3 Fit**: ✅ Tests dual-state tracking and temporal reasoning

**#53 - Gravity Lens**
- **Core Idea**: Four gravity-well colors exert a constant pull (N, S, E, W). Free objects drift one cell per tick toward nearest well unless acted upon
- **Why Interesting**: Combining straight-line planning with predictable but inexorable drift vectors
- **ARC-AGI-3 Fit**: ✅ Tests physics simulation and planning under constraints

**#54 - Color Logic Gates**
- **Core Idea**: Colored wires carry binary signals (ON/OFF). Overlapping specific color pairs realizes AND, OR, XOR gates. Activate a goal register
- **Why Interesting**: Map visual circuit to Boolean algebra and search for placement satisfying given truth conditions
- **ARC-AGI-3 Fit**: ✅ Tests logical reasoning and circuit design

**#55 - Reality Glitch**
- **Core Idea**: Every g ticks, a pseudo-random 3×3 patch reverts to its state g ticks ago. Pattern is fixed per instance and fully visible
- **Why Interesting**: Temporal planning that is robust to deterministic partial rollbacks—requires storing and replaying local history
- **ARC-AGI-3 Fit**: ✅ Tests temporal reasoning and state prediction

---

## Implementation Guidance for ARC-AGI-3

### Adapting Mechanics to ARC-AGI-3

When implementing any of these mechanics for ARC-AGI-3 submission:

1. **Color Mapping**: Use indices 0-15 (16 colors available)
   - Reserve color 0 for background/empty
   - Assign semantic meaning to each color used
   - Document color meanings in your GAME_SPEC.md

2. **Action Mapping**: Define what each ACTION1-7 does
   - ACTION1-4: Typically directional movement (Up/Down/Left/Right)
   - ACTION5: General interaction (activate, select, rotate, etc.)
   - ACTION6: Click/target with X,Y coordinates
   - ACTION7: Undo (optional)
   - RESET: Always required (restart level)

3. **Grid Constraints**: Ensure square grids only
   - Minimum: 8×8 (recommended for simplicity)
   - Maximum: 64×64 (official limit)
   - Width must equal height

4. **Deterministic Behavior**: Remove any randomness during play
   - Procedural generation for level creation is OK
   - But once a level starts, behavior must be deterministic
   - Same action sequence = same outcome every time

5. **Visual Discovery**: All rules must be learnable visually
   - No hidden mechanics impossible to discover
   - Visual feedback for all state changes
   - Clear cause-and-effect relationships

6. **Brute-Force Resistance**: Design to require insight
   - Large action space (hard to try everything)
   - Irreversible actions (mistakes have consequences)
   - Pattern recognition rewarded over exhaustive search

### Prohibited Mechanics for ARC-AGI-3

Avoid these characteristics:

- ❌ **Randomness during play** (e.g., #31 Probabilistic Walls)
- ❌ **Requiring cultural knowledge** (e.g., chess piece movements)
- ❌ **Text or symbols** (no letters, numbers on screen)
- ❌ **Audio cues** (visual only)
- ❌ **Rectangular grids** (must be square)
- ❌ **Ambiguous goals** (win must be visually obvious)

### Recommended Mechanics for First Submissions

**Excellent starting points** (well-aligned with ARC-AGI-3 goals):

1. **Sliding Token** (#1) - Classic spatial planning
2. **Push-Block Sokoban** (#4) - Irreversible actions + planning
3. **Color Flood Fill** (#13) - Graph reasoning + optimization
4. **Symmetry Painter** (#14) - Constraint satisfaction
5. **Parity Painter** (#41) - Mathematical reasoning
6. **Vector Slide** (#42) - Spatial + modular math
7. **Voronoi Claim** (#44) - Geometric optimization
8. **Rule Discovery** (#39) - Meta-learning

---

## Resources

### For Game Design
- **Official Constraints**: See documents/official/DESIGN_CONSTRAINTS.md
- **Agent API Reference**: See documents/official/AGENT_API_REFERENCE.md
- **Submission Process**: See documents/specs/SUBMISSION_PROCESS.md
- **Game Spec Template**: See documents/specs/GAME_SPEC_TEMPLATE.md

### Official ARC-AGI-3 Links
- **Overview**: https://arcprize.org/arc-agi/3/
- **Submit Form**: https://forms.gle/aVD4L4xRaJqJoZvE6
- **Documentation**: https://docs.arcprize.org
- **GitHub**: https://github.com/arcprize/ARC-AGI-3-Agents
- **Discord**: https://discord.gg/9b77dPAmcA
- **Contact**: team@arcprize.org

---

**End of Mechanics Library**

*This is a living document. Mechanics marked with ⭐ have been implemented in our good_games/ folder.*
