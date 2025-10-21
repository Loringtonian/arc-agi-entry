# Official ARC-AGI-3 Requirements for Game Submissions

**Purpose**: This document contains ONLY verified official requirements from ARC Prize Foundation sources.
**Last Verified**: October 2025
**Status**: All statements cited to official sources

---

## ⚠️ IMPORTANT NOTICE

**This document contains ONLY official requirements.**

Everything else in this repository (technical implementations, file structures, API specifications) represents either:
- **BEST PRACTICES** (industry-standard software engineering)
- **SPECULATION** (AI-generated assumptions and proposals)

If it's not in this document, **it's not officially required**.

---

## Official Sources

All information below is verified from these official ARC Prize Foundation sources:

1. **arcprize.org/arc-agi/3** - Official ARC-AGI-3 overview page
2. **arcprize.org/blog/arc-agi-3-preview-30-day-learnings** - Official blog post with design guidance
3. **docs.arcprize.org** - Official documentation (NOTE: For agent developers, not game authors)
4. **github.com/arcprize/ARC-AGI-3-Agents** - Official agent SDK (NOTE: For agents, not game submissions)

---

## OFFICIAL DESIGN CONSTRAINTS

**Source**: [arcprize.org/arc-agi/3](https://arcprize.org/arc-agi/3/)

All game submissions must meet these constraints (verbatim quotes from official site):

### 1. Human Accessibility
> **"Easy for humans (can pick it up in <1 min of game play)"**

- Players must be able to understand basic mechanics within one minute
- Rules must be discoverable through play alone

### 2. Playability Duration
> **"Should be fun for humans and playable in 5-10 minutes"**

- Games should be completable by competent humans within 5-10 minutes
- Must remain engaging, not tedious

### 3. Core Knowledge Priors Only
> **"Core Knowledge Priors (no language, trivia, cultural symbols)"**

Games must rely ONLY on:
- Basic mathematics
- Basic geometry
- Spatial reasoning
- Temporal reasoning

Games must NOT require:
- Language or linguistic knowledge
- Cultural knowledge or symbols
- Trivia or memorized facts
- Domain-specific expertise

### 4. No Instructions Required
> **"Should require no instructions to play"**

- No text displayed during gameplay
- No tutorial levels
- No written rules or guides
- Players learn purely through experimentation

### 5. Novel Mechanics Encouraged

**Source**: [arcprize.org/arc-agi/3](https://arcprize.org/arc-agi/3/)

The official site encourages:
> **"Innovative and novel game mechanics"**

Specifically mentioned:
- Hidden state
- Theory of mind
- Long-horizon planning
- Multi-agent navigation

---

## OFFICIAL DESIGN LEARNINGS

**Source**: [arcprize.org/blog/arc-agi-3-preview-30-day-learnings](https://arcprize.org/blog/arc-agi-3-preview-30-day-learnings)

The preview competition (August 2025) provided these insights:

### Avoid Brute-Force Vulnerability
> **"Some preview games were too friendly to random search"**

Games should resist being solved through:
- Random exploration
- Exhaustive trial-and-error
- Clicking everywhere without understanding

### Action Efficiency Matters
The foundation discovered that measuring:
> **"how efficiently environment information is converted into strategy"**

...provides the clearest signal of intelligence.

### Clear Action Affordances
> **"Developers requested explicit guidance about which actions work per game"**

Future games should make available actions visually clear to players.

---

## OFFICIAL SUBMISSION PROCESS

**Source**: [arcprize.org/arc-agi/3](https://arcprize.org/arc-agi/3/)

### Primary Submission Method

**Google Form**: [https://forms.gle/aVD4L4xRaJqJoZvE6](https://forms.gle/aVD4L4xRaJqJoZvE6)

Official prompt:
> **"Have a concept for an ARC-AGI-3 game? Submit your idea"**

### Contact Information

**Source**: [arcprize.org/blog/arc-agi-3-preview-30-day-learnings](https://arcprize.org/blog/arc-agi-3-preview-30-day-learnings)

**Email**: team@arcprize.org

The blog states they are:
> **"actively building the next wave of environments"**

And invites creators to:
> **"Submit new game ideas"**

### Community Channels

**Discord**: Available via official site (community discussion)
**Twitter**: @arcprize
**GitHub**: github.com/arcprize

---

## WHAT IS **NOT** OFFICIALLY REQUIRED

The following are NOT official requirements, despite appearing in other repository documentation:

### ❌ Technical Implementation
- NO official file format specified
- NO official repository structure required
- NO official API to implement
- NO official `reset()`/`step()` methods required
- NO official `env/` or `interface/` directories required

### ❌ Documentation
- NO official GAME_SPEC.md format required
- NO official documentation template required
- NO official specification structure required

### ❌ Testing & Packaging
- NO official testing requirements
- NO official CI/CD requirements
- NO official `pyproject.toml` or packaging requirements
- NO official LICENSE requirements

### ❌ Demos & Media
- NO official demo video requirement (though helpful)
- NO official replay JSON requirement
- NO official screenshot requirements

### ❌ Agent Integration
- NO requirement to integrate with ARC-AGI-3-Agents SDK
- NO requirement to provide agent adapters
- NO requirement for headless operation
- NO requirement for API compatibility

**Note**: The ARC-AGI-3-Agents repository and docs.arcprize.org are for **agent developers** (building AI to play games), NOT for game authors (creating games).

---

## OFFICIAL TECHNICAL DETAILS (FOR CONTEXT ONLY)

The following are mentioned in official agent documentation but are NOT explicitly stated as requirements for game submissions:

### Grid Size (From Agent Docs)
**Source**: [docs.arcprize.org/agents-quickstart](https://docs.arcprize.org/agents-quickstart)

Agent documentation mentions:
- Grid coordinates: "0-63 inclusive"
- This implies a 64×64 maximum grid

**NOTE**: This is stated for the agent API, not explicitly required for game submissions.

### Actions (From Agent Docs)
**Source**: [docs.arcprize.org/agents-quickstart](https://docs.arcprize.org/agents-quickstart)

The agent API defines:
- RESET: Start or restart game
- ACTION1-5: Single-parameter actions
- ACTION6: Click with X,Y coordinates (0-63 range)
- ACTION7: Undo (for supported games)

**NOTE**: This is the agent action framework. Games are NOT required to support all actions.

---

## TIMELINE

**Source**: [arcprize.org/arc-agi/3](https://arcprize.org/arc-agi/3/) & [arcprize.org/blog/arc-agi-3-preview-30-day-learnings](https://arcprize.org/blog/arc-agi-3-preview-30-day-learnings)

### Development History
- **Early 2025**: Development began
- **July 17, 2025**: ARC-AGI-3 Preview released (6 games: 3 public, 3 private)

### Preview Competition (Closed)
- **Competition Period**: July 17 - August 19, 2025
- **Results Announced**: August 19, 2025
- **Submissions**: 12 total, 8 tested
- **Winners**:
  - 1st: StochasticGoose (12.58% score)
  - 2nd: Blind Squirrel (6.71% score)

### ARC Prize 2025 (Kaggle Competition for AI Agents)
- **Competition Period**: March 26 - November 3, 2025
- **Purpose**: AI agents compete to solve ARC-AGI tasks
- **⚠️ IMPORTANT**: This is an **agent competition** (for building AI that plays games), NOT related to game submission process
- **Source**: arcprize.org/competitions/2025
- **Note**: Game authors should NOT confuse this with the game submission process described above

### Upcoming
- **Three private games**: "to be released in coming weeks" (after Aug 19)
- **Full benchmark launch**: 2026
- **Target size**: ~100 environments (mentioned in community discussions)

### Game Submission Deadline
- **NO deadline announced**
- Submissions accepted on **rolling basis**
- Team is "actively building the next wave of environments"

---

## SUBMISSION CHECKLIST

Based on official requirements ONLY:

### Design Constraints ✓
- [ ] Human can learn in < 1 minute of play
- [ ] Playable in 5-10 minutes
- [ ] No text, instructions, or tutorials
- [ ] Uses only core knowledge priors (no language/culture/trivia)
- [ ] Fun and engaging for humans
- [ ] Novel mechanics (encouraged but not required)
- [ ] Resists brute-force/random search approaches

### Submission ✓
- [ ] Submit via official form: https://forms.gle/aVD4L4xRaJqJoZvE6
- [ ] OR email team@arcprize.org with concept

**That's it.** Everything else is optional or helpful but not officially required.

---

## WHAT HELPS (BUT ISN'T REQUIRED)

The following are helpful for your submission but NOT official requirements:

- **Working prototype**: Proves feasibility, helps reviewers understand concept
- **Demo video**: Shows gameplay clearly without requiring code execution
- **Clear documentation**: Helps reviewers evaluate design
- **Playable implementation**: Allows testing and verification
- **Professional presentation**: Makes good impression

---

## FREQUENTLY ASKED QUESTIONS

### Q: Do I need to implement the agent API (reset/step methods)?
**A**: Not officially required. The agent API is for building AI agents, not for submitting games.

### Q: Do I need a specific repository structure?
**A**: Not officially required. No public specification exists for game submission packages.

### Q: Do I need to integrate with the ARC-AGI-3-Agents SDK?
**A**: Not officially required. That SDK is for agent developers, not game authors.

### Q: What file format should I use?
**A**: Not officially specified. Any format that clearly communicates your concept works.

### Q: Do I need tests, CI/CD, or a LICENSE file?
**A**: Not officially required. These are software engineering best practices but not submission requirements.

### Q: What technical specifications must I meet?
**A**: None explicitly stated for game submissions. Only the design constraints above are official requirements.

### Q: Can I submit just a concept without code?
**A**: Yes. The form says "Have a concept for an ARC-AGI-3 game? Submit your idea." A working prototype helps but isn't required.

---

## SUMMARY

### ✅ OFFICIAL REQUIREMENTS (3 things):
1. Meet design constraints (listed above)
2. Submit via form or email
3. That's it.

### ❌ NOT OFFICIAL REQUIREMENTS:
- Everything else (technical specs, file formats, API integration, etc.)

### 💡 HELPFUL BUT OPTIONAL:
- Working prototype
- Demo materials
- Clear documentation
- Professional packaging

---

## UPDATES TO THIS DOCUMENT

This document will be updated when:
- Official ARC Prize Foundation releases new requirements
- Official blog posts provide additional guidance
- Official documentation is updated

**Last Updated**: October 2025
**Next Review**: When official sources publish new information

---

## QUESTIONS?

**Official Channels**:
- Form: https://forms.gle/aVD4L4xRaJqJoZvE6
- Email: team@arcprize.org
- Discord: Via official website
- Site: arcprize.org/arc-agi/3

**Repository Documentation**:
See `official_scratch_pad.md` for detailed source analysis showing what is official vs speculation vs best practice.
