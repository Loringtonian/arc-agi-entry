Game mechanic types 

Below is a grab‑bag of 40 mechanics you can mix‑and‑match. Each description is short but concrete enough that you—and anyone trying to build an automated solver—can formalize the rules on a 10‑color, ≤ 64 × 64 square grid.

#	Mechanic (suggested name)	Core idea (one‑liner)	Why it’s interesting for solvers
State & Movement			
1	Sliding Token	A single “agent” color slides one step per tick; walls are other colors; reach the goal.	Algorithms must handle path‑planning with changing obstacles.
2	Wrap‑Around Runner	Exiting the grid on one edge re‑enters on the opposite (toroidal space).	Introduces modulo arithmetic and global reasoning.
3	Color Conveyor Belts	Squares cycle their color rightward each tick, acting like belts.	Requires predicting future positions, not just present state.
4	Push‑Block Sokoban	Agent pushes colored crates onto matching target pads.	Classic NP‑hard puzzle—good for heuristic search.
5	Momentum Glide	Once moving, the agent continues until hitting a wall.	Demands look‑ahead and inevitable‑state detection.
Timing & Rhythm			
6	Beat Sequencer	Only every k‑th tick can you act; other ticks are skipped.	Forces temporal planning and modular arithmetic.
7	Fading Trails	Recently visited squares fade through a color gradient before clearing.	Memory of the past influences legal moves.
8	Pendulum Gates	Gates open/close on a global sine‑wave schedule.	Synchronization and phase prediction are required.
9	Cascade Reaction	Performing an action starts a countdown (displayed as shade) that triggers a board‑wide effect.	Chains of delayed consequences test causal reasoning.
Memory & Sequence			
10	Simon Path	Grid flashes a sequence of positions you must repeat exactly.	Solvers need short‑term sequence memory.
11	Lock‑Key Pairs	Collect keys (colored squares) in a required order to unlock doors.	Permutation reasoning & ordering constraints.
12	Echo Maze	Stepping on a tile creates a clone that retraces your past n moves behind you. Avoid collisions.	Requires anticipating multiple intertwined histories.
Pattern Formation			
13	Color Flood Fill	Change the color of the starting corner; goal is to flood the grid with a target pattern in ≤ m moves.	Relates to graph coloring & BFS.
14	Symmetry Painter	Every paint action is mirrored across one or more axes; produce a goal pattern.	Touches on group theory and constraint satisfaction.
15	Life‑Like Automaton	Each tick, colors update by Conway‑style rules; you seed the initial pattern.	Solvers must learn emergent dynamics.
16	Tiling Constraints	Only certain 2 × 2 color blocks are legal; fill the grid completely.	Reduces to exact‑cover / constraint propagation.
17	Fractal Growth	Each colored seed replicates outward following L‑system rules until halted by blockers.	Requires predicting recursive expansion.
Resource & Optimization			
18	Energy Budget	Each move costs energy, shown as a diminishing color bar; maximize score before depletion.	Poses a shortest‑path with weighted costs.
19	Harvest & Convert	Collect resource tiles, then drop them on converters to upgrade score‑multiplier colors.	Introduces inventory management.
20	Risk‑Reward Gradient	High‑value colors appear near hazards that erase you on contact.	Balances exploration vs. safety.
Multi‑Agent / Adversarial			
21	Chaser & Runner	An AI “monster” color moves greedily toward you; survive T ticks.	Invokes pursuit‑evasion algorithms.
22	Swarm Herding	Lead multiple wandering agents into goal zones by blocking paths.	Multi‑body coordination and flocking dynamics.
23	Territory Claim	Two colors expand one square per tick; you place walls to maximize your color’s area.	Competitive influence‑maximization.
Topology & Geometry			
24	Elevated Layers	Color encodes height; only ascend/descend one unit per move.	Converts 2‑D grid into discretized 3‑D terrain.
25	Mirror World	The board displays both the “real” layer and a mirrored phantom layer; moves affect both in inverse ways.	Dual‑state reasoning.
26	Portal Pairs	Stepping on a portal instantly teleports to its partner of same color.	Non‑local connectivity challenges path‑finding heuristics.
Signal Processing & Waves			
27	Color Wavefronts	Selected tiles emit concentric rings of alternating colors each tick; align rings to hit targets.	Spatial–temporal interference prediction.
28	Harmonic Locks	A gate opens only when three oscillating color signals align on the same tick.	Requires computing least‑common multiples.
29	Phase Shift Terrain	Land tiles cyclically shift through a 3‑color palette; only specific phases are passable.	Demands phase tracking.
Stochastic & Hidden Information			
30	Fog of War	Unseen squares reveal color only when adjacent; finish with limited peeks.	Combines exploration with inference.
31	Probabilistic Walls	A “quantum” wall turns solid with probability p each tick, shown as a flickering shade.	Solvers must reason over expected value and risk.
32	Hidden Mines	Certain colors indicate probability of adjacent mines (classic Minesweeper logic).	Deductive reasoning under uncertainty.
Transformation & Rewriting			
33	Color Cyclic Permute	A global “clock” rotates all colors (0→1→2…). Your actions must account for future rotations.	Adds modular arithmetic to state space.
34	Swap‑Rule Grammar	Specified 3×3 patterns auto‑swap to new colors each tick (Wang‑tile style).	Equivalent to local string‑rewrite systems.
35	Repaint Ray	Fire a beam that converts every nth square to a chosen color until blocked.	Line‑of‑sight computation.
Score‑Chasing Variants			
36	Combo Chains	Removing a block triggers gravity; cascading clears multiply score.	Promotes search for high‑yield configurations.
37	Time‑Attack Dash	Points decay exponentially with time; finish objectives ASAP.	Pushes greedy vs. full‑search trade‑offs.
38	Precision Paint	Score equals the count of correctly colored squares minus mis‑colored ones. Perfect accuracy matters.	Fine‑grained evaluation for learning agents.
Meta / Learning Mechanics			
39	Rule Discovery	The update rule itself (e.g., which neighborhood triggers a color change) is hidden; infer by observing a few ticks.	Encourages hypothesis‑testing and adaptive algorithms.
40	Curriculum Unlock	Completing easy boards unlocks new colors or larger grids in the same episode.	Requires long‑term skill accumulation and transfer.

How to Use This List
	1.	Compose hybrids – e.g., combine Momentum Glide with Pendulum Gates for timed ice‑slides.
	2.	Vary grid scale – some mechanics shine on 8 × 8, others need 64 × 64 room to breathe.
	3.	Tune color semantics – the same RGB value can be “agent,” “wall,” “resource,” or “timer” depending on the rule set.
	4.	Expose parameters – solvers learn faster when each instance supplies its k, p, or sequence length explicitly.

With these mechanics you can craft hundreds of distinct puzzle instances, each challenging a different slice of reasoning—from pure search, through probabilistic inference, all the way up to incremental rule discovery.

additionally: 

Below are 15 mechanics that respect your hard constraints — exactly 10 discrete colors, a square grid ≤ 64 × 64, no sound or hue‑shifting, no textual symbols, no cultural knowledge needed — and emphasize basic math, basic geometry, agent‑ness and object‑ness.
For each I give a concise description and why it’s interesting for program‑solvers.

⸻

1. Parity Painter
	•	Core idea: Two colors represent bits (0/1). Stepping on a cell toggles its bit and the four orthogonal neighbors. Win by driving every bit to 0.
	•	Solver challenge: Classic “Lights Out” linear‑algebra problem on GF(2); finding a minimum toggle set requires reasoning about parity and matrix rank.

2. Vector Slide
	•	Core idea: Eight arrow colors encode unit vectors (N, S, E, W, NE, NW, SE, SW) and one color is “agent,” one is “goal.” When the agent enters an arrow square, it is teleported one step in that vector (wrapping at edges).
	•	Solver challenge: Path‑finding in a directed graph with deterministic teleports; must reason with modular arithmetic on coordinates.

3. Modular Collector
	•	Core idea: Six token colors represent the integers 0‑5. A door color opens only when (sum of collected tokens) mod 6 equals the door’s color‑value.
	•	Solver challenge: Knapsack‑style planning under modular constraints; requires keeping a running residue class.

4. Voronoi Claim
	•	Core idea: You may drop up to k “seed” colors. On the final tick every empty tile adopts the color of its nearest seed (Manhattan distance). Score is your total claimed area.
	•	Solver challenge: Geometric partitioning and distance minimization; algorithms must search seed placements that maximize Voronoi cells.

5. Centroid Balancer
	•	Core idea: Five block colors encode weights 1‑5. Place exactly n blocks so that the discrete center‑of‑mass of all blocks lands on a marked target cell.
	•	Solver challenge: Basic coordinate geometry and integer‑weighted averaging; solvers need to enumerate weight configurations efficiently.

6. Spiral Enumerator
	•	Core idea: The board specifies a start color and a spiral direction (clockwise or counter). The agent must visit every cell in exact spiral order without revisiting.
	•	Solver challenge: Deriving the mathematical rule for the target permutation of coordinates and planning a Hamiltonian path that matches it.

7. Collision Sum
	•	Core idea: Colored “balls” slide simultaneously one step per tick. When two collide, they merge into a new color whose numeric value is (a + b) mod 10. Reach a prescribed final multiset.
	•	Solver challenge: Predicting pairwise collisions, conservation of momentum, and modular arithmetic on color‑values.

8. Color Parasite (works unchanged)
	•	Core idea: A special parasite color overwrites any adjacent color, but decays after three ticks unless it infects another square. Victory = full infection or full containment.
	•	Solver challenge: Spatiotemporal spread vs. blocking—object interaction and epidemic modeling within discrete steps.

9. Polarity Chain (refined)
	•	Core idea: Two charge colors (+, –). A neutral object moves one step each tick in the direction of the net adjacent charge vector (sum of neighboring + minus –). Rearrange charges to guide the object to a goal.
	•	Solver challenge: Continuous‑valued vector reasoning emerging from discrete local sums; feedback is fully visible, no hidden state.

10. Inkblot Symmetry Prison (works unchanged)
	•	Core idea: The board enforces mirror symmetry across a moving axis; any move that breaks the symmetry is cloned to restore it, often in an unexpected spot. Escape by exploiting the axis shift to reach an asymmetrical goal region.
	•	Solver challenge: High‑order spatial symmetry prediction and exploiting transformation rules.

11. Time‑Lapse Garden (works unchanged)
	•	Core idea: Plant colored seeds that grow into deterministic fractal shapes after n ticks. You can’t prune. Match a target end‑state.
	•	Solver challenge: Recursive growth forecasting and combinatorial seed placement.

12. Inter‑Dimensional Swap Grid (works unchanged)
	•	Core idea: Every m ticks the visible grid swaps with a “ghost” grid that obeys inverted motion rules (e.g., agents move oppositely). Both persist between swaps. Achieve a goal in either reality.
	•	Solver challenge: Dual‑state planning with periodic rule alternation; timestep synchronization.

13. Gravity Lens (works unchanged)
	•	Core idea: Four gravity‑well colors exert a constant pull (N, S, E, W). Free objects drift one cell per tick toward the nearest well unless acted upon.
	•	Solver challenge: Combining straight‑line planning with predictable but inexorable drift vectors.

14. Color Logic Gates (works unchanged)
	•	Core idea: Colored wires carry binary signals (ON/OFF). Overlapping specific color pairs realizes AND, OR, XOR gates. Activate a goal register.
	•	Solver challenge: Map a visual circuit to Boolean algebra and search for a placement satisfying given truth conditions.

15. Reality Glitch (works unchanged)
	•	Core idea: Every g ticks, a pseudo‑random 3 × 3 patch reverts to its state g ticks ago. Pattern is fixed per instance and fully visible.
	•	Solver challenge: Temporal planning that is robust to deterministic partial rollbacks—requires storing and replaying local history.

⸻

Why these fit your brief
	•	Only 10 colors are ever referenced; where numbers or states are needed they are encoded directly as distinct colors (e.g., weights 1‑5, token values 0‑5, arrow directions, charges).
	•	Mechanics rely on counting, parity, modular arithmetic, spatial symmetry, vector addition, area maximization, center‑of‑mass, fractal growth, dual‑state reasoning—all squarely in “basic math & geometry.”
	•	Each scenario features clear agents and objects interacting through deterministic, local rules.
	•	No symbols, language cues, or cultural trivia are required for a solver to infer or exploit the rules.

Feel free to ask for concrete rule formalizations, example boards, or difficulty estimates for any of the above.
