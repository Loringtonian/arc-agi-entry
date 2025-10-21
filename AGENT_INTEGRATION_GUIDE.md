# Agent Integration Guide

**Purpose**: Practical steps to make your ARC-AGI-3 games compatible with AI agents

⚠️ **IMPORTANT**: Agent integration is NOT required for game submissions. This guide is for when you're ready to test your games with AI agents.

**Official Requirements**: See `OFFICIAL_REQUIREMENTS.md` (just design constraints + form submission)
**This Guide**: 🟡 SPECULATION - Best practices for agent compatibility based on agent SDK analysis

---

## Why Agent Integration?

**Benefits**:
- Test your game with AI agents to see if it's challenging
- Measure action efficiency (AI actions vs human baseline)
- Validate game mechanics work as intended
- Get agent performance data before submission

**NOT Required**:
- You can submit games without agent integration
- ARC Prize Foundation will handle integration if your game is accepted
- Focus on human playability first

**Official Example Games** (to study):
- **ls20** - Agent reasoning game
- **ft09** - Elementary logic game
- **vc33** - Orchestration game

You can try these at [three.arcprize.org](https://three.arcprize.org) to see what ARC-AGI-3 games look like.

---

## Official Scoring Framework

🔵 **OFFICIAL** - From arcprize.org/blog/arc-agi-3-preview-30-day-learnings

**How Games Are Scored**:

```
Agent Score = (Agent Actions / Human Baseline Actions) × 100
```

**Score Range**: 0%-100%
- **Lower is better** (more efficient than humans)
- Score < 100 = More efficient than average human
- Score = 100 = Human-level efficiency
- Score > 100 = Less efficient than humans

**Details**:
- Measured **per-level**, then aggregated across all games
- Human baselines from **1,200+ players** who completed **3,900+ games**
- Persistent players found **theoretical minimum** action counts
- Tracks **exploration actions** vs **execution actions** separately

**Competition Performance Benchmarks**:
- **1st Place (StochasticGoose)**: 12.58% score (CNN-based RL)
- **2nd Place (Blind Squirrel)**: 6.71% score (state-graph exploration)

**What This Means**:
- If your game's agent score is ~10-15%, it's appropriately challenging
- If agents score >50%, game might be too hard or require better agents
- If agents score <5%, game might be too easy or exploitable

---

## Quick Decision Tree

```
Do I need agent integration NOW?
│
├─ Submitting game concept? → NO, just submit via form
├─ Want to test with AI? → YES, follow this guide
├─ Want performance metrics? → YES, follow this guide
└─ Just prototyping? → NO, focus on human play
```

---

## The Agent API (What You're Integrating With)

**Reference**: See `documents/official/AGENT_API_REFERENCE.md` for complete details

**Summary**: The official ARC-AGI-3-Agents SDK expects games to expose:

```python
# Environment interface
reset(seed: Optional[int]) -> observation
step(action) -> (observation, reward, done, info)

# Observation format
observation: Image or array representing game state

# Actions
ACTION1-7 + RESET (agents choose from these)
```

---

## Integration Steps

### Step 1: Understand Your Game's Current State

**Before integrating, you need**:
- ✅ Working game (human playable)
- ✅ Meets official design constraints
- ✅ Deterministic behavior (same input = same output)
- ✅ Clear win/loss conditions

**You don't need**:
- ❌ Specific file structure
- ❌ Specific code architecture
- ❌ Any particular framework

---

### Step 2: Create Environment Wrapper

**Goal**: Wrap your game in the agent API format

**Create**: `env/game.py` with:

```python
class YourGame:
    def reset(self, seed=None):
        """
        Start/restart game with optional seed for determinism

        Returns:
            observation: Current game state (grid as array or image)
        """
        if seed is not None:
            random.seed(seed)
        # Initialize your game
        return self._get_observation()

    def step(self, action):
        """
        Execute one action and return results

        Args:
            action: One of ACTION1-7 or RESET

        Returns:
            observation: New game state
            reward: 1 if won, 0 if ongoing, -1 if lost (or your scoring)
            done: True if game ended (win or loss)
            info: Dict with any extra data (optional)
        """
        # Execute action in your game
        # Update game state
        observation = self._get_observation()
        reward = self._calculate_reward()
        done = self._is_game_over()
        info = {"moves": self.move_count}  # Optional

        return observation, reward, done, info

    def _get_observation(self):
        """Convert your game grid to agent-friendly format"""
        # Return grid as numpy array with color indices 0-15
        return self.grid  # Shape: (height, width) with uint8 values
```

**Key Points**:
- `reset()` must be deterministic when given a seed
- `observation` should be grid with color indices (0-15)
- `done=True` when game ends (win or loss)
- `reward` can be simple (0/1) or complex (action efficiency)

---

### Step 3: Map Your Controls to Agent Actions

**Your game uses**: Keyboard controls (WASD, arrow keys, etc.)

**Agents use**: ACTION1-7 enum

**Create mapping**:

```python
from enum import Enum

class AgentAction(Enum):
    RESET = 0
    ACTION1 = 1  # Map to your UP
    ACTION2 = 2  # Map to your DOWN
    ACTION3 = 3  # Map to your LEFT
    ACTION4 = 4  # Map to your RIGHT
    ACTION5 = 5  # Map to your INTERACT (if applicable)
    ACTION6 = 6  # Map to your CLICK (if applicable)
    ACTION7 = 7  # Map to your UNDO (if applicable)

# In your step() method:
def step(self, action):
    if action == AgentAction.ACTION1:
        self._move_up()
    elif action == AgentAction.ACTION2:
        self._move_down()
    # ... etc
```

**Document your mapping** in a comment or README:
```
ACTION1 = Move Up
ACTION2 = Move Down
ACTION3 = Move Left
ACTION4 = Move Right
ACTION5 = Select/Interact (if your game needs it)
ACTION6 = Not used (or Click if applicable)
ACTION7 = Not used (or Undo if supported)
```

**Note on ACTION7** 🔵 **OFFICIAL UPDATE**:
- ACTION7 (undo) was **added in SDK v0.9.2** (Aug 19, 2025)
- Mentioned in changelog as "possible GameAction"
- Official blog states "undo functionality being implemented"
- **May not be widely supported yet** - treat as optional
- If you support undo, great! If not, that's also fine.

**Note on Game States** 🔵 **OFFICIAL**:
From docs.arcprize.org/games, the official state names are:
- `NOT_FINISHED` - Game in progress
- `WIN` - Player succeeded
- `GAME_OVER` - Player failed or reached action limit

Your code can use simplified names (like boolean `won`/`lost`), but official API uses these exact strings.

---

### Step 4: Create Adapter for Official SDK

**Goal**: Connect your environment to the official ARC-AGI-3-Agents SDK

**Create**: `interface/adapter_arc3.py`

```python
"""
Adapter to run your game with official ARC-AGI-3-Agents SDK
"""
from env.game import YourGame

class ARC3Adapter:
    def __init__(self):
        self.game = YourGame()

    def reset(self, seed=None):
        return self.game.reset(seed)

    def step(self, action):
        return self.game.step(action)

    def render(self):
        """Optional: Return visual representation"""
        return self.game.get_frame()  # Return image/array
```

**Usage**:
```python
# agents/test_agent.py
from interface.adapter_arc3 import ARC3Adapter

env = ARC3Adapter()
obs = env.reset(seed=42)

for step in range(100):
    action = agent.choose_action(obs)
    obs, reward, done, info = env.step(action)
    if done:
        break
```

---

### Step 5: Create Baseline Agents for Testing

**Random Agent** (`agents/random_agent.py`):
```python
import random
from enum import Enum

class AgentAction(Enum):
    ACTION1 = 1
    ACTION2 = 2
    ACTION3 = 3
    ACTION4 = 4
    # Add others if your game uses them

class RandomAgent:
    def choose_action(self, observation):
        """Pick random valid action"""
        valid_actions = [AgentAction.ACTION1, AgentAction.ACTION2,
                        AgentAction.ACTION3, AgentAction.ACTION4]
        return random.choice(valid_actions)
```

**Heuristic Agent** (`agents/heuristic_agent.py`):
```python
class HeuristicAgent:
    """Simple rule-based agent to test game mechanics"""

    def choose_action(self, observation):
        # Example: Move toward goal color
        if self._detect_goal_above(observation):
            return AgentAction.ACTION1  # UP
        elif self._detect_goal_below(observation):
            return AgentAction.ACTION2  # DOWN
        # ... etc

        # Fallback to random
        return random.choice([ACTION1, ACTION2, ACTION3, ACTION4])
```

---

### Step 6: Test Your Integration

**Create test script** (`test_agent_integration.py`):

```python
from interface.adapter_arc3 import ARC3Adapter
from agents.random_agent import RandomAgent

def test_random_agent(num_episodes=10):
    env = ARC3Adapter()
    agent = RandomAgent()

    results = []

    for episode in range(num_episodes):
        obs = env.reset(seed=episode)
        done = False
        steps = 0

        while not done and steps < 1000:
            action = agent.choose_action(obs)
            obs, reward, done, info = env.step(action)
            steps += 1

        results.append({
            'episode': episode,
            'steps': steps,
            'won': reward > 0,
            'info': info
        })

        print(f"Episode {episode}: {'WON' if reward > 0 else 'LOST'} in {steps} steps")

    return results

if __name__ == "__main__":
    results = test_random_agent()
    print(f"\nRandom agent won {sum(r['won'] for r in results)}/10 games")
```

**Run it**:
```bash
python test_agent_integration.py
```

**What to look for**:
- ✅ Episodes complete without errors
- ✅ Win/loss detection works
- ✅ Determinism: Same seed = same outcome
- ✅ Random agent rarely wins (game isn't trivial)
- ✅ No crashes or infinite loops

---

### Step 7: Create Replay/Recording System (Optional)

**Useful for debugging and demos**:

```python
import json

class ReplayRecorder:
    def __init__(self):
        self.actions = []
        self.observations = []

    def record_step(self, action, observation, reward, done):
        self.actions.append({
            'action': action.name,
            'reward': reward,
            'done': done
        })
        # Optionally save observation frames

    def save(self, filename):
        with open(filename, 'w') as f:
            json.dump({
                'actions': self.actions,
                'num_steps': len(self.actions)
            }, f, indent=2)
```

**Use it**:
```python
recorder = ReplayRecorder()

obs = env.reset(seed=42)
done = False

while not done:
    action = agent.choose_action(obs)
    obs, reward, done, info = env.step(action)
    recorder.record_step(action, obs, reward, done)

recorder.save('demos/episode_42.json')
```

---

## Minimal File Structure for Agent Integration

```
your-game-repo/
├── env/
│   ├── __init__.py
│   └── game.py              # Your game with reset/step
├── interface/
│   ├── __init__.py
│   └── adapter_arc3.py      # Adapter to official SDK
├── agents/
│   ├── __init__.py
│   ├── random_agent.py      # Baseline random
│   └── heuristic_agent.py   # Simple rule-based
├── demos/
│   └── episode_42.json      # Replay logs
├── test_agent_integration.py
└── good_games/
    └── your_game.py         # Original human-playable version
```

---

## Connecting to Official ARC-AGI-3-Agents SDK

**When you're ready to use the official SDK**:

1. **Clone official repo**:
```bash
git clone https://github.com/arcprize/ARC-AGI-3-Agents.git
cd ARC-AGI-3-Agents
```

2. **Set up environment**:
```bash
cp .env-example .env
# Edit .env and add your ARC_API_KEY from three.arcprize.org
```

3. **Add your game to their framework**:
   - Copy your `env/` and `interface/` folders
   - Register your game in their game list
   - Follow their docs: https://docs.arcprize.org/agents-quickstart

4. **Run agents against your game**:
```bash
uv run main.py --agent=random --game=your_game
```

### Important: Official API vs Local Testing

🔵 **OFFICIAL** - From arcprize.org blog

**Official Games (ls20, ft09, vc33)**:
- Run via **hosted API** at three.arcprize.org
- Requires **API key** (get from three.arcprize.org)
- **Rate limits** currently in place
- **Offline engine** being explored but not available yet
- For research/high-rate needs: contact team@arcprize.org

**Your Custom Games**:
- Can test **locally** without API
- No rate limits on your own machines
- Run offline as much as you want
- When ready, you can submit for official inclusion

**Versioned Game IDs** 🔵 **OFFICIAL**:
When games are officially added, they use format: `<game_name>-<version>`
- Example: "ls20" might be tracked as "ls20-v1", "ls20-v2" for updates
- Allows game improvements while maintaining stable names
- Your local games don't need this unless targeting official inclusion

---

## Testing Checklist

Before sharing your agent-integrated game:

**Functionality**:
- [ ] `reset()` works with and without seed
- [ ] `step()` handles all ACTION1-7 gracefully
- [ ] Observations are correct format (grid array)
- [ ] Win/loss detection works
- [ ] Invalid actions handled (don't crash)

**Determinism**:
- [ ] Same seed produces identical gameplay
- [ ] No randomness during gameplay (after reset)
- [ ] Replays are reproducible

**Performance**:
- [ ] Random agent rarely/never wins (game isn't trivial)
- [ ] Games complete in reasonable time (<1000 steps)
- [ ] No infinite loops or hangs

**Documentation**:
- [ ] ACTION mapping documented
- [ ] Win conditions clear
- [ ] Example replay saved

---

## Common Pitfalls

### 1. Non-Determinism
**Problem**: Same seed gives different results

**Solution**:
```python
def reset(self, seed=None):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    # All randomness must happen here, not during step()
```

### 2. Action Space Confusion
**Problem**: Agents use ACTION6 (click) but game doesn't support it

**Solution**:
```python
def step(self, action):
    if action in [ACTION6, ACTION7]:  # Not supported
        return self._get_observation(), 0, False, {'error': 'Action not supported'}
    # Handle valid actions
```

### 3. Observation Format Mismatch
**Problem**: Agents expect array but game returns image

**Solution**:
```python
def _get_observation(self):
    # Return grid as numpy array, shape (H, W) with uint8 color indices
    return np.array(self.grid, dtype=np.uint8)
```

### 4. Never-Ending Games
**Problem**: Game doesn't set `done=True`

**Solution**:
```python
def step(self, action):
    # ... execute action
    done = self._check_win() or self._check_loss() or self.steps > MAX_STEPS
    return obs, reward, done, info
```

---

## When to Integrate vs When to Submit

**Submit WITHOUT agent integration**:
- ✅ You have a working prototype
- ✅ Human playable and fun
- ✅ Meets official design constraints
- ✅ Want feedback from ARC Prize team

**Integrate BEFORE submitting**:
- ✅ You want to test game difficulty with AI
- ✅ You want action efficiency metrics
- ✅ You want to prove agent compatibility
- ✅ You're submitting a polished, final version

**Remember**: Agent integration is NOT required for submission. Many successful games may be submitted as human-playable prototypes only.

---

## Resources

**Official Documentation**:
- Agent SDK: https://github.com/arcprize/ARC-AGI-3-Agents
- Agent Quickstart: https://docs.arcprize.org/agents-quickstart
- API Reference: `documents/official/AGENT_API_REFERENCE.md`

**This Repository**:
- Design constraints: `OFFICIAL_REQUIREMENTS.md`
- Game template: `arc_game_template.py`
- Implementation ideas: `codecsubmissiongaps.markdown` (archived)

**Questions?**
- Discord: https://discord.gg/9b77dPAmcA
- Email: team@arcprize.org

---

## Summary

**Three-tier approach**:

1. **Prototype** (human playable) → Submit via form
2. **Agent-ready** (reset/step API) → Test with agents locally
3. **SDK-integrated** (fully compatible) → Run with official agents

**Start at level 1, progress when ready. You don't need level 3 to submit.**

Good luck! 🎮
