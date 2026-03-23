# Context Architecture Reference

Reference material for investigator agents auditing Claude Code context placement.

---

## 1. The Scrutiny Test

Every piece of context must justify its placement. The question is: **"Does every query in this scope need this information?"**

If you can't answer yes, the context is loaded too broadly — it wastes budget and degrades adherence for everything else.

| Answer | Belongs In |
|--------|-----------|
| Yes — all queries in this directory | CLAUDE.md at that directory level |
| Yes — all queries for a concept | A skill |
| Only when working with certain file types | `.claude/rules/` with `paths:` scope |
| Only in a subdirectory | Subdirectory CLAUDE.md |
| Discoverable from code/config at runtime | **Nowhere** — let Claude find it |

The last row is critical. Claude can read files, run commands, and explore codebases. Context that duplicates what's already in the code is pure waste — it burns budget and goes stale.

---

## 2. Context Layer Reference

Claude loads context in layers. Each layer has different loading behavior and budget cost. Understanding this is essential for deciding where to put things.

| Layer | Loads When | Budget Impact |
|-------|-----------|---------------|
| System prompt (~50 instructions) | Always | Fixed, ~700 tokens |
| CLAUDE.md (all levels) | Session start | Full size, every session |
| `.claude/rules/` (no `paths:`) | Session start | Full size, every session |
| `.claude/rules/` (with `paths:`) | On file match | On-demand |
| Auto memory (MEMORY.md) | Session start | First 200 lines |
| Skill descriptions | Session start | ~2% of context budget |
| Skill full content | On invocation | On-demand |
| Subdirectory CLAUDE.md | On file access | On-demand |
| MCP tool definitions | Deferred if >10% budget | On-demand via ToolSearch |

**Why this matters:** Everything in the top half of this table loads unconditionally. Every token there competes with every other token for adherence. The bottom half loads on-demand — it's essentially free until needed.

The architectural goal is simple: move as much as possible from always-loaded to on-demand.

---

## 3. Key Thresholds

These are empirical limits, not guidelines. Crossing them causes measurable degradation.

- **CLAUDE.md adherence**: >92% when under 200 lines. Drops to ~71% above 400 lines. This is not gradual — it's a cliff.
- **Target**: ≤200 lines for the main CLAUDE.md.
- **Instruction capacity**: Frontier models reliably follow ~150–200 distinct instructions. The system prompt consumes ~50, leaving **~100–150 for user instructions** across all always-loaded layers.
- **Always-loaded budget red line**: 800 lines (~3,200 tokens) across all always-loaded layers combined. Beyond this, you are actively degrading Claude's ability to follow any of your instructions.

The implication: if your CLAUDE.md is 400 lines and you have 200 lines of ungated rules and 200 lines in MEMORY.md, you've already blown past the red line. Something has to move or be deleted.

---

## 4. Progressive Disclosure

Progressive disclosure is not a nice-to-have — it's the core architectural principle.

**Why it matters:** Every always-loaded token degrades adherence for every other always-loaded token. This is a zero-sum game. A 50-line block about test conventions that only matters when editing tests is actively making Claude worse at following your build commands, code style rules, and everything else — on every single query.

**The principle:** Minimize what loads unconditionally. Maximize what loads on-demand.

Concretely:
- **Always-loaded** (CLAUDE.md, ungated rules, MEMORY.md): Only universal truths that apply to nearly every interaction. Build commands, critical invariants, project identity.
- **On-demand** (skills, gated rules, subdirectory CLAUDE.md): Everything scoped to a specific activity, file type, or part of the codebase.

The test is simple: if a piece of context applies to <80% of interactions, it should not be always-loaded. Move it to a skill, a gated rule, or a subdirectory CLAUDE.md.
