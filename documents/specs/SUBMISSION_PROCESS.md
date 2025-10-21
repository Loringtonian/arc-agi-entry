# Game Submission Process for ARC-AGI-3

⚠️ **DISCLAIMER**: This document contains OFFICIAL sources + SPECULATION about best practices

**For official requirements ONLY**: See `../../OFFICIAL_REQUIREMENTS.md`
**Legend**: 🔵 = OFFICIAL | 🟡 = SPECULATION | 🟢 = BEST PRACTICE

**Source**: Compiled from [gpt5_on_arc.md](../../gpt5_on_arc.md) and official ARC Prize resources
**Last Updated**: October 2025

## Important: Current Status

### What EXISTS
- ✅ Active call for community game submissions
- ✅ Official submission form
- ✅ Team contact for proposals
- ✅ Agent interface specification (for agents, not game authoring)
- ✅ Discord community for discussion

### What DOES NOT EXIST (Yet)
- ❌ Public game-authoring SDK or templates
- ❌ Formal submission deadline
- ❌ Public submission portal with automatic acceptance
- ❌ Game schema or package format specification

### Reality Check

**The submission process is collaborative and curatorial**, not automated. Think of it like:
- Proposing a conference paper (pitch + iterate)
- Contributing to an open-source project (submit + refine)

NOT like:
- Kaggle competition submission (automated upload)
- App store submission (publish and done)

## Recommended Submission Path

Based on the official guidance and current best practices, follow this 5-step process:

### Step 1: Mirror the Agent Interface

**Why**: Your game needs to fit into the existing ARC-AGI-3 environment framework.

**Action**: Study the official agent repository to understand the observation/action contract:
- Repository: [github.com/arcprize/ARC-AGI-3-Agents](https://github.com/arcprize/ARC-AGI-3-Agents)
- Documentation: [docs.arcprize.org/agents-quickstart](https://docs.arcprize.org/agents-quickstart)

**Key Specifications to Match**:
- 64×64 grid maximum
- 16 color palette
- 7 core actions (RESET + ACTION1-6, with ACTION7 for undo)
- Frame-based observation format
- Session management via GUID

### Step 2: Build a Minimum Viable Environment (MVE)

**Goal**: Create a playable prototype that demonstrates your game concept.

**Required Components**:

1. **Environment Class** with standard methods:
   ```python
   def reset() -> observation
       """Initialize or restart game, return starting state"""

   def step(action) -> (observation, reward, done, info)
       """Execute action, return new state"""
   ```

2. **Observation Format**:
   - Visual frame (64×64 grid or smaller)
   - Rendered as image or array
   - Color indices 0-15

3. **Action Space**:
   - Support relevant subset of ACTION1-7
   - RESET always required
   - ACTION6 (click) with X,Y coordinates 0-63 if needed

4. **Replay/Recording System**:
   - Generate GIF or MP4 of gameplay
   - Save JSON log of action sequences
   - Allow reviewers to understand without running code

**Implementation Note**: You don't need to integrate with the full ARC-AGI-3 API yet. Build a standalone environment that could be wrapped/adapted later.

### Step 3: Package a Game Specification

**Create a GAME_SPEC.md** document with:

#### Required Sections

**1. Game Overview**
- Name
- One-sentence description
- Skill(s) under test (exploration, memory, planning, abstraction, etc.)

**2. Human Intuitiveness**
- Describe what a human intuits in the first 30-60 seconds
- How do they discover the rules? (no instructions allowed!)
- What makes the goal obvious without text?

**3. Visual Design**
- Color meanings (what each color represents)
- Object behaviors (how things move/interact)
- Grid layout and typical dimensions
- Hidden state (if any) and how it's discoverable

**4. Goal & Win Condition**
- What constitutes success?
- How is it visually obvious?
- What's the efficiency metric? (minimum actions, optimal path, etc.)

**5. Action Mapping**
- What does each ACTION1-7 do in your game?
- Which actions are essential vs. optional?

**6. Anti-Overfit Design**
- How do you procedurally generate levels?
- What parameters vary between instances?
- Why can't this be brute-forced or memorized?

**7. Core Priors Alignment**
- Confirm: No language, trivia, or cultural knowledge required
- List the core priors needed (basic math, geometry, spatial reasoning, etc.)
- Explain why it's learnable through visual observation alone

#### Example Structure

See [GAME_SPEC_TEMPLATE.md](../specs/GAME_SPEC_TEMPLATE.md) for a complete template.

### Step 4: Create a Developer-Friendly Repository

**Recommended Structure**:

```
arc3-game-[your-game-name]/
├── README.md                    # Overview and quick start
├── GAME_SPEC.md                 # Detailed specification
├── LICENSE                      # Open source license
├── env/
│   ├── __init__.py
│   ├── game.py                  # Core game logic (reset/step)
│   ├── levels.py                # Procedural level generator
│   └── renderer.py              # Visual rendering
├── interface/
│   └── adapter_arc3.py          # Wrapper to ARC-AGI-3 API format
├── demos/
│   ├── human_play.mp4           # Video of human playthrough
│   ├── sample_replay.json       # Logged action sequence
│   └── screenshots/             # Key gameplay moments
├── tests/
│   ├── test_reset_step.py       # Basic environment tests
│   └── test_levels.py           # Level generation tests
├── agents/
│   ├── random_agent.py          # Baseline: random actions
│   └── heuristic_agent.py       # Simple rule-based agent
└── pyproject.toml               # Dependencies (keep minimal)
```

**Why This Structure?**

- Clear separation of concerns
- Easy for AI agents (and humans) to understand
- Testable and maintainable
- Shows your game works end-to-end

**Key Files**:

1. **README.md** - Quick overview, how to run, what it tests
2. **GAME_SPEC.md** - Complete specification
3. **demos/** - Visual proof of playability
4. **agents/** - Proof that your game works with agent framework

### Step 5: Submit and Socialize

**Primary Submission Method**:

📋 **Official Form**: [https://forms.gle/aVD4L4xRaJqJoZvE6](https://forms.gle/aVD4L4xRaJqJoZvE6)

**Supporting Channels** (use in addition to form):

1. **Discord Community**
   - Join: [https://discord.gg/9b77dPAmcA](https://discord.gg/9b77dPAmcA)
   - Share in appropriate channel
   - Ask moderators where game prototypes should be posted
   - Engage with community feedback

2. **Email Contact**
   - Send to: team@arcprize.org
   - Include: Link to repo, GAME_SPEC.md, demo video
   - Reference: "Game submission per arcprize.org/arc-agi/3 'Submit your idea' call"

3. **GitHub Issues** (optional)
   - Repository: [github.com/arcprize/docs](https://github.com/arcprize/docs)
   - Create issue with: Proposal summary + link to your repo
   - Tag: [game-proposal] or similar

**What to Include in Submission**:

- Link to your game repository
- Link to GAME_SPEC.md
- Link to demo video (human_play.mp4)
- Brief explanation (2-3 paragraphs) of:
  - What reasoning skill your game tests
  - Why it's novel/interesting
  - How it satisfies ARC-AGI-3 constraints

## What Happens After Submission

**Expect**:
- Curation and review (may take weeks/months)
- Back-and-forth iteration on design
- Possible requests for modifications
- No guaranteed timeline for inclusion

**Don't Expect**:
- Immediate acceptance/rejection
- Automated evaluation
- Guaranteed inclusion in ARC-AGI-3

The team is building toward ~100 environments for the 2026 launch, so they're selectively curating high-quality, diverse games.

## Preparation Checklist

Before submitting, ensure:

### Design Constraints ✓
- [ ] Human can learn in < 1 minute
- [ ] Playable in 5-10 minutes
- [ ] No text/instructions required
- [ ] Uses only core knowledge priors
- [ ] Fun for humans to play
- [ ] Novel or tests underexplored reasoning skills

### Technical Requirements ✓
- [ ] Fits within 64×64 grid
- [ ] Uses ≤16 colors
- [ ] Works with ACTION1-7 framework
- [ ] Deterministic behavior
- [ ] Clear win condition
- [ ] Resists brute-force approaches

### Documentation ✓
- [ ] Complete GAME_SPEC.md
- [ ] Clear README.md
- [ ] Demo video exists
- [ ] Sample replay JSON exists
- [ ] Code is clean and readable

### Testing ✓
- [ ] Environment reset/step works
- [ ] Levels generate correctly
- [ ] Baseline agents can play (random, heuristic)
- [ ] Win condition triggers appropriately
- [ ] Visual rendering is clear

## FAQ

**Q: Do I need to integrate with the full ARC-AGI-3 API?**
A: No. Build a standalone environment first. Provide an adapter or notes on how it could integrate, but full API integration isn't required for submission.

**Q: What if I don't have a working implementation?**
A: You can submit a detailed concept without code, but a minimal prototype significantly increases your chances. Visual mockups + GAME_SPEC.md is better than nothing.

**Q: How polished does my submission need to be?**
A: Focus on:
1. Clear game concept
2. Demonstrated novelty
3. Obvious fit with ARC-AGI-3 goals
4. Working prototype (even if rough)

Don't worry about: Production-quality graphics, perfect code, comprehensive test coverage.

**Q: Can I submit multiple game ideas?**
A: Yes, but each should be a separate submission with its own repo/spec.

**Q: What's the timeline for the 2026 launch?**
A: Not publicly specified. Development started early 2025, full launch targeted for 2026. No specific date announced.

**Q: Will I be compensated if my game is included?**
A: Not specified publicly. Ask team@arcprize.org about collaboration terms.

**Q: Can I make my submission public before the team reviews it?**
A: Yes. The team encourages open sharing. Make your repo public, share on Discord, etc.

## Resources

### Official Documentation
- **ARC-AGI-3 Overview**: [arcprize.org/arc-agi/3](https://arcprize.org/arc-agi/3/)
- **Design Constraints**: See [DESIGN_CONSTRAINTS.md](../official/DESIGN_CONSTRAINTS.md)
- **Agent API Reference**: See [AGENT_API_REFERENCE.md](../official/AGENT_API_REFERENCE.md)
- **30-Day Learnings**: [arcprize.org/blog/arc-agi-3-preview-30-day-learnings](https://arcprize.org/blog/arc-agi-3-preview-30-day-learnings)

### Code & Templates
- **Agent Repository**: [github.com/arcprize/ARC-AGI-3-Agents](https://github.com/arcprize/ARC-AGI-3-Agents)
- **Game Spec Template**: [GAME_SPEC_TEMPLATE.md](../specs/GAME_SPEC_TEMPLATE.md)
- **Our Game Template**: [../../arc_game_template.py](../../arc_game_template.py)

### Community
- **Discord**: [discord.gg/9b77dPAmcA](https://discord.gg/9b77dPAmcA)
- **Twitter**: [@arcprize](https://twitter.com/arcprize)
- **Newsletter**: [arcprize.kit.com/bc80575d89](https://arcprize.kit.com/bc80575d89)
- **Email**: team@arcprize.org

## Bottom Line

**Yes**: You can design and submit games for ARC-AGI-3.

**Process**: Propose + prototype + share via form/Discord/email.

**No**: There's no public SDK, formal deadline, or guaranteed acceptance yet.

**Best Approach**: Build a compelling prototype with clear documentation, then submit through official channels and engage with the community for feedback.
