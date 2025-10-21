# ARC-AGI-3 Official Compliance Verification Prompt

**Purpose**: Use this prompt with a fresh Claude Code instance to verify repository compliance against official ARC Prize Foundation sources.

---

## Prompt for Claude Code

```markdown
You are conducting an official compliance audit for an ARC-AGI-3 game development repository.

## Your Mission

Verify this repository's documentation and claims against ONLY official ARC Prize Foundation sources. Report facts, not opinions.

## Ground Truth Starting Point

Start with `/Users/lts/Desktop/arc agi entry/gpt5_on_arc.md` - this contains links to official documentation.

## Your Tasks

### 1. Verify Official Sources (30 minutes)

Visit EVERY link in gpt5_on_arc.md:
- arcprize.org/arc-agi/3
- arcprize.org/blog (especially 30-day learnings post)
- docs.arcprize.org
- github.com/arcprize/ARC-AGI-3-Agents
- github.com/arcprize/docs
- three.arcprize.org

Also search for ANY other official ARC Prize documentation we might have missed:
- Check arcprize.org for new pages
- Check docs.arcprize.org for new sections
- Check GitHub repos for README updates
- Look for official announcements, blog posts, or guidelines

### 2. Extract Official Requirements

From official sources ONLY, document:
- ✅ What IS officially required for game submissions
- ❌ What is NOT mentioned (gaps in official guidance)
- 🔍 What is ambiguous or unclear

Create three lists:
1. **OFFICIAL REQUIREMENTS** (with source citations)
2. **OFFICIAL GUIDANCE** (soft recommendations from official sources)
3. **NOT OFFICIALLY SPECIFIED** (things left to game authors)

### 3. Audit This Repository

Compare our documentation against official sources:

**Files to check**:
- `OFFICIAL_REQUIREMENTS.md` - Should contain ONLY official requirements
- `AGENT_INTEGRATION_GUIDE.md` - Should clearly label official vs speculation
- `rules.md` - Should separate official from best practices
- `arc_game_template.py` - Should not claim unofficial things are required
- `README.md` - Should not overstate compliance claims
- `documents/official/*` - Should all be verifiable

**For each file, report**:
- ✅ Claims that match official sources (with citations)
- ❌ Claims that contradict official sources (with corrections)
- ⚠️ Claims we can't verify (speculation presented as fact)
- 📝 Missing official information we should add

### 4. Check for Mismatches

Specifically verify:
- Grid size requirements (official vs our docs)
- Color palette requirements (official vs our docs)
- Action framework requirements (official vs our docs)
- Submission process (official vs our docs)
- Technical specifications (official vs our docs)
- Timeline and deadlines (official vs our docs)

### 5. Search for New Information

Look for official info we don't have yet:
- New blog posts since August 2025
- Updated documentation
- New game examples
- Clarifications on submission process
- Technical specification updates
- Community guidelines

## Output Format

Provide your findings in this structure:

### PART 1: Official Source Verification
```
Source: [URL]
Status: ✅ Verified / ❌ 404 / ⚠️ Changed
Last Updated: [Date if available]
Key Information: [Bullet points of official statements]
```

### PART 2: Official Requirements (Complete List)
```
REQUIREMENT: [Exact statement]
SOURCE: [URL + section]
EVIDENCE: [Quote from source]
```

### PART 3: Repository Compliance Report

**ACCURATE (✅)**
- [Claim from our docs] → Verified in [source]
- [Claim from our docs] → Verified in [source]

**INACCURATE (❌)**
- [Claim from our docs] → CONTRADICTS [source]
- Correction: [What official source actually says]

**UNVERIFIABLE (⚠️)**
- [Claim from our docs] → NOT found in official sources
- Classification: Speculation / Best Practice / Assumption

**MISSING (📝)**
- [Official info] from [source] → Not in our docs
- Recommended action: [Add to which file]

### PART 4: Gaps in Official Documentation

**What ARC Prize Has NOT Officially Specified**:
- [Topic] - No official guidance found
- [Topic] - Mentioned but not detailed
- [Topic] - Ambiguous or contradictory

### PART 5: Bottom Line Assessment

**Can the user proceed with confidence?**
- YES / NO / WITH CAVEATS

**Official Requirements Met**: X/Y
**Documentation Accuracy**: X%
**Critical Issues**: [Number]
**Recommended Actions**: [Priority list]

## Important Instructions

1. **ONLY cite official ARC Prize Foundation sources**:
   - arcprize.org domains
   - Official GitHub repos (arcprize organization)
   - Official documentation sites
   - Official blog posts

2. **DO NOT cite**:
   - Medium articles
   - Reddit posts
   - Third-party tutorials
   - Speculation or interpretations
   - AI-generated content (except official ARC Prize)

3. **Be precise with language**:
   - "OFFICIAL REQUIREMENT" = Explicitly stated in official docs
   - "OFFICIAL GUIDANCE" = Recommended in official docs
   - "SPECULATION" = Not found in official sources
   - "UNCLEAR" = Official sources are ambiguous

4. **Always provide source URLs** for every claim

5. **If unsure, say so** - Don't guess or infer

6. **Focus on facts, not opinions**:
   - ❌ "This seems reasonable"
   - ✅ "This is not mentioned in official sources"

## Success Criteria

Your audit is complete when you can answer:
1. What are ALL official requirements for game submissions? (with sources)
2. What does our repo claim that's not official? (with examples)
3. What official information are we missing? (with recommendations)
4. Can the user submit a game with confidence? (yes/no with reasoning)

## Time Estimate

- Source verification: 30 minutes
- Repository audit: 30 minutes
- Report writing: 30 minutes
- Total: ~90 minutes

## Start Now

Begin by reading `/Users/lts/Desktop/arc agi entry/gpt5_on_arc.md` to get the official link list, then systematically verify each source and audit our documentation.

Be thorough. Be precise. Be factual. The user needs to know they're on solid ground.
```

---

## How to Use This Prompt

1. **Open a fresh Claude Code session**
2. **Copy the entire prompt above** (everything in the markdown code block)
3. **Paste it as your first message**
4. **Let Claude work for ~90 minutes**
5. **Review the compliance report**

## What You'll Get

- Complete list of official requirements (with sources)
- Compliance report for all repo files
- List of inaccuracies to fix (if any)
- List of missing official information to add
- Clear YES/NO on whether you can proceed

## When to Run This

- Before major submissions
- After official documentation updates
- When you want to verify compliance
- Before making big architectural decisions
- When you see new ARC Prize announcements

---

**Last Updated**: October 2025
**Purpose**: Ensure repository aligns with official ARC Prize Foundation requirements only
