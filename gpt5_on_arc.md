⚠️ **DISCLAIMER**: This document mixes OFFICIAL sources with SPECULATION about implementation

**For official requirements ONLY**: See `OFFICIAL_REQUIREMENTS.md`
**Legend**: 🔵 = OFFICIAL | 🟡 = SPECULATION | 🟢 = BEST PRACTICE

---

Short version: you can design and submit a game idea for ARC-AGI-3, but there is no public, formal "game-author SDK" or deadline right now. The public SDK and docs are aimed at agents (players), not game authors. The ARC team is actively soliciting game ideas and invites you to pitch them; the current, best-practice path is: share a well-specified proposal + (ideally) a minimal prototype, then contact them via Discord / email / GitHub issues. I'll give you the exact links and a repo starter so you can set a coding agent loose.

What exists (official) 🔵 **OFFICIAL**
	•	ARC-AGI-3 overview and the explicit "Got Game Ideas?" call for community submissions (design constraints listed). No deadline posted.  ￼
	•	"Time to build" post: they're actively building the next wave of environments and invite new game ideas; contact email listed. Still no dates.  ￼
	•	Docs site (Mintlify) is an Agents Quickstart / API for running agents 🟡 (NOTE: for agent developers, NOT game authors)  ￼
	•	Official GitHub:
	•	arcprize/ARC-AGI-3-Agents (reference for the environment/agent interface; latest release v0.9.2 on Aug 19 2025). 🟡 For agents, NOT games  ￼
	•	arcprize/docs (public docs repo; has contributing guidance).  ￼
	•	Community touchpoints to route your proposal / questions: Discord (linked from Resources/Guide) and team@arcprize.org.  ￼

What does not exist (publicly) 🔵 **OFFICIAL** (verified absence)
	•	No published game-authoring SDK, templates, or schema for third-party environment packages.
	•	No public submission deadline or portal specifically for "submit your environment to be included in ARC-AGI-3."
	•	The only dated thing was the Agent Preview Competition (closed Aug 2025) — that was for agents, not game submissions.  ￼

Design constraints you must obey (from ARC page) 🔵 **OFFICIAL**
	•	Easy for humans (pick up in <1 min; playable in 5–10 min).
	•	No language/trivia/cultural symbols (focus on core knowledge priors).
	•	No instructions required; should still be fun for humans; novelty encouraged (hidden state, ToM, long-horizon planning, multi-agent, etc.).  ￼

How to proceed (practical path to a credible submission) 🟡 **SPECULATION** - Suggested approach, NOT official requirements

1) Mirror their interface so your prototype "fits" 🟡 **SPECULATION**

🟡 **SPECULATION**: Study and clone the Agents repo to mirror the observations/actions contract in your environment prototype (e.g., 64×64 grid, ~16 colours; 7 actions total: ACTION1-7 + RESET in the agent framework). This lets you demo your game with existing agents.  ￼

Key references
	•	Agents Quickstart + repo: adds/implements agent methods & run loops.  ￼
	•	Third-party write-ups describe the grid + actions used in preview, which you can emulate.  ￼

2) Build a minimum viable environment (MVE)

Implement a tiny environment that exposes:
	•	reset() → observation (64×64×C array or equivalent image)
	•	step(action) → observation, reward, done, info (align names to what their agents expect)
	•	Action space matching preview conventions: RESET, UP/DOWN/LEFT/RIGHT, INTERACT, CLICK(x,y) (keep CLICK in 0–63).  ￼
	•	Replay/recording (GIF/MP4 + JSON of actions) so reviewers can grok the mechanic without code. Their docs discuss recordings & replays; mimic that.  ￼

3) Package a crisp game spec

Write a GAME_SPEC.md describing:
	•	Name & skill under test (exploration, memory, planning, abstraction, objectness, ToM…).
	•	Human pick-up: one-paragraph “what a human intuits in 30–60 s” (no text instructions in-game).
	•	State & assets: visual alphabet, colours used, object behaviours, hidden state (if any).
	•	Goal & scoring: success condition; efficiency metrics (steps/time/levels).
	•	Anti-overfit: generate levels procedurally from a seed; explain parameter ranges.
	•	Safety & priors: confirm no language/trivia/symbols, only core priors.  ￼

4) Create a Dev-friendly repo your agent can traverse

Proposed structure (works cross-platform; minimal friction for Cursor/agents):

arc3-game-<slug>/
  README.md
  GAME_SPEC.md
  LICENSE
  env/
    __init__.py
    game.py            # reset/step; observation renderer
    levels.py          # seedable level generator
    sprites.py         # if you use tiles; otherwise simple primitives
  interface/
    adapter_arc3.py    # wraps your env to ARC-AGI-3 Agents expectations
  demos/
    human_play.mp4
    sample_replay.json
  tests/
    test_reset_step.py
  pyproject.toml       # uv/pdm/poetry ok; keep install simple
  .github/workflows/ci.yml

Add a tiny “baseline random” and “naive heuristic” agent script to show playability via the official Agents loop.  ￼

5) Submit / Socialize it the way ARC asks today
	•	Post your proposal + repo in the ARC Prize Discord (ask where to share game-idea prototypes), and tag moderators. The Resources/Guide explicitly route people to Discord; they also give team@arcprize.org.  ￼
	•	Open a GitHub Issue in arcprize/docs (or in ARC-AGI-3-Agents if your issue is interface-related) linking your repo, replay, and GAME_SPEC. Their docs welcome issues/PRs for ideas.  ￼
	•	Email team@arcprize.org with the same package; reference the “Got Game Ideas?” call.  ￼

Reality check: there’s no public cut-off date for game submissions yet. They’re building toward a ~2026 full release (~100 environments). Expect curation, iteration, and back-and-forth rather than a Kaggle-style portal.  ￼

Repo bootstrap (copy/paste into your README)
	•	Purpose: Proposed ARC-AGI-3 environment “<Name>” that tests <skill(s)> while satisfying ARC constraints (human-intuitive, 5–10 min, no language/trivia).  ￼
	•	Run (agent loop):

git clone https://github.com/arcprize/ARC-AGI-3-Agents.git
cd ARC-AGI-3-Agents && cp .env-example .env
# set ARC_API_KEY in .env

Then import interface/adapter_arc3.py from this repo to run our environment under the standard loop.  ￼

	•	Replay: demos/human_play.mp4 + demos/sample_replay.json show solvability and goal structure.  ￼
	•	Contact to submit: Discord (ARC Prize server) or email team@arcprize.org.  ￼

Useful links (so your agent can fetch context fast)
	•	ARC-AGI-3 overview & “Got Game Ideas?” blurb.  ￼
	•	30-Day Learnings post (explicitly invites new game ideas + lists email).  ￼
	•	Docs (Agents Quickstart) and Quickstart home.  ￼
	•	Official GitHub org and ARC-AGI-3-Agents repo.  ￼
	•	Docs repo (for issues/PRs).  ￼
	•	Competitions page (Agent Preview is past; confirms it was agents only).  ￼

Bottom line
	•	Yes: you can design/submit a game (problem).
	•	No public deadline/SDK for authors yet; process = propose + prototype + share via Discord/email/GitHub.  ￼
	•	If you want, I’ll draft a GAME_SPEC.md skeleton and a Python env/game.py stub aligned to the preview obs/actions so you can drop it into a repo and point Cursor/agents at it immediately.