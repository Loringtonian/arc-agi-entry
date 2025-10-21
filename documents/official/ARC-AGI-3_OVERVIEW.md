# ARC-AGI-3 Official Overview

**Source**: [arcprize.org/arc-agi/3](https://arcprize.org/arc-agi/3/)
**Last Updated**: October 2025
**Status**: In Development (Launch: 2026)

## What is ARC-AGI-3?

ARC-AGI-3 is **the first interactive reasoning benchmark** designed to measure an AI Agent's ability to generalize in novel, unseen environments. Unlike the static puzzles of ARC-AGI-1 and ARC-AGI-2, ARC-AGI-3 uses video-game-like environments where agents and humans must perceive, plan, and act across multiple steps to achieve long-horizon goals.

### Key Characteristics

- **Hand-crafted novel environments**: ~100 unique games designed to test skill-acquisition efficiency
- **Interactive format**: Turn-based 2D grid games requiring exploration and adaptation
- **Zero-shot learning**: Agents evaluated on entirely new games never seen before
- **Human baseline**: Direct comparison of AI vs. human performance

## Timeline

- **Development Start**: Early 2025
- **Preview Competition**: August 2025 (Closed)
  - 6 games total: 3 public, 3 released in Aug 2025
  - Results announced Aug 19, 2025
- **Full Launch**: 2026
  - ~100 environments
  - Split between public and private evaluation sets

## Core Evaluation Pillars

ARC-AGI-3 evaluates five fundamental capabilities:

1. **Exploration** - Efficiently gather environmental information through strategic choices
2. **Percept → Plan → Action** - Process observations and execute purposeful actions
3. **Memory** - Store and apply previous experience effectively
4. **Goal Acquisition** - Set intermediate goals even when ultimate objectives are unclear
5. **Alignment** - Understand and pursue intended objectives

## Design Philosophy

### Core Knowledge Priors (Required)
- Basic mathematics
- Basic geometry
- Agent-ness (understanding entities that act)
- Object-ness (recognizing distinct objects)
- Spatial reasoning
- Temporal reasoning

### Explicitly Excluded
- Language or linguistic knowledge
- Cultural knowledge or symbols
- Trivia or memorized facts
- Domain-specific expertise
- Vast training datasets

## Game Submission Process

### Community Call

The ARC Prize Foundation actively seeks new game ideas from the community. Game submissions are a critical part of building the benchmark.

### Submission Method

**Official Form**: [https://forms.gle/aVD4L4xRaJqJoZvE6](https://forms.gle/aVD4L4xRaJqJoZvE6)

**Alternative Channels**:
- Discord: [https://discord.gg/9b77dPAmcA](https://discord.gg/9b77dPAmcA)
- Email: team@arcprize.org
- GitHub Issues: [arcprize/docs](https://github.com/arcprize/docs)

### Important Notes

- **No formal deadline**: Submissions accepted on rolling basis
- **No guarantee of implementation**: Not all submissions will be included
- **Curation process**: Expect iteration and back-and-forth with the team
- **No public SDK yet**: Game authoring tools not yet officially released

## Preview Competition Insights

### What Worked Well
- ✅ High human engagement and enjoyment
- ✅ Clear performance metrics via action efficiency
- ✅ Diverse game types (agentic, logic, orchestration)
- ✅ Measurable intelligence signal distinguishing AI from human capability

### Areas for Improvement
- ⚠️ Some games too friendly to brute-force/random search
- ⚠️ Needed clearer action availability communication
- ⚠️ Required better resistance to non-reasoning approaches

### Key Learning: Action Efficiency

**Action efficiency** emerged as foundational to evaluation:
- Measures how many moves agents require relative to human baselines
- Distinguishes exploration actions from execution actions
- Per-level scoring normalized across all games
- Provides quantitative intelligence metric

## Measurement Approach

Unlike traditional benchmarks, ARC-AGI-3 emphasizes:

1. **On-the-fly learning** - No memorization; adapt known concepts to novel situations
2. **Exploration efficiency** - How well agents discover game rules through experimentation
3. **Planning quality** - Ability to form and execute multi-step strategies
4. **Transfer learning** - Apply insights from one situation to another

## Community Resources

- **Website**: [https://arcprize.org](https://arcprize.org)
- **ARC-AGI-3 Portal**: [https://three.arcprize.org](https://three.arcprize.org)
- **Documentation**: [https://docs.arcprize.org](https://docs.arcprize.org)
- **GitHub Organization**: [https://github.com/arcprize](https://github.com/arcprize)
- **Newsletter**: [https://arcprize.kit.com/bc80575d89](https://arcprize.kit.com/bc80575d89)
- **Twitter/X**: [@arcprize](https://twitter.com/arcprize)

## For Game Designers

If you're interested in creating games for ARC-AGI-3:

1. Review the **Design Constraints** (see DESIGN_CONSTRAINTS.md)
2. Study the **Agent API Reference** (see AGENT_API_REFERENCE.md)
3. Create a **Game Specification** (see GAME_SPEC_TEMPLATE.md)
4. Build a minimal prototype
5. Submit via official form or contact team@arcprize.org

## Research Contact

For research inquiries, collaborations, or detailed technical questions:
**Email**: team@arcprize.org
