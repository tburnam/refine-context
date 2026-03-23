---
name: refine-context
description: Audits and refines Claude Code context quality across all layers — CLAUDE.md files, rules, skills, memory, MCP servers, hooks, settings, and agents. Analyzes conversation history to find patterns and gaps. Use when the user wants to optimize their Claude Code setup, reduce context bloat, fix skill triggering issues, improve instruction adherence, audit progressive disclosure, or when they mention "refine", "context", "optimize setup", or complain that Claude ignores instructions.
argument-hint: "[audit|conversations] [directory]"
effort: max
context: fork
allowed-tools: [Read, Glob, Grep, Bash, Agent]
---

# /refine-context — Context Refinement Audit

Audit all Claude Code context sources and conversation history. Produce a prioritized report for improving progressive disclosure.

## Why This Matters

Context is finite. CLAUDE.md adherence drops from >92% under 200 lines to ~71% above 400 lines. The system prompt consumes ~50 of ~150-200 reliable instruction slots. Every unnecessary token in always-loaded context degrades everything else. Read `references/context-architecture.md` for the full framework.

## Before Starting

Detect environment:
- Working directory: !`pwd`
- Claude Code version: !`claude --version 2>/dev/null || echo "not detected"`

## Parse Scope

Parse `$ARGUMENTS` for:
- **Phase**: `audit` (static only) | `conversations` (session mining only) | default: both
- **Directory**: explicit path or cwd

Resolve the project session key: absolute path of target directory with `/` replaced by `-`. Session index lives at `~/.claude/projects/{key}/sessions-index.json`.

## Orchestration

### Phase 1 — Investigate (parallel subagents)

Spawn agents as parallel background subagents. Each is **read-only** — never modifies files. Full instructions for each agent are in `agents/`:

| # | Agent | File | Runs When |
|---|-------|------|-----------|
| 1 | claude-md-auditor | `agents/claude-md-auditor.md` | audit or both |
| 2 | skill-auditor | `agents/skill-auditor.md` | audit or both |
| 3 | infra-auditor | `agents/infra-auditor.md` | audit or both |
| 4 | codebase-scanner | `agents/codebase-scanner.md` | audit or both |
| 5 | conversation-miner | `agents/conversation-miner.md` | conversations or both |

Launch all applicable agents simultaneously — parallel execution minimizes wall-clock time and keeps each agent's file reads isolated from the main context.

Pass each agent the target directory and project session key.

### Phase 2 — Synthesize

Once all investigators complete, spawn the synthesizer agent. Instructions: `agents/synthesizer.md`. Report template: `templates/report-template.md`.

Feed ALL investigator outputs to the synthesizer. It cross-references findings, scores the setup, deduplicates, and produces the final report.

### Present the Report

Display the synthesizer's output directly to the user. The report is self-contained and follows the template structure. Share the filepath to the full report with the user.

## Graceful Degradation

| Condition | Response |
|-----------|----------|
| No `sessions-index.json` | Skip conversation mining, note as gap in report |
| No `.claude/` directory | Note as "unconfigured project", audit what exists |
| No skills installed | Score skill coverage as 0, recommend a starting set |
| No CLAUDE.md files | Note as gap, focus on infra + codebase scan |
| Session JSONL corrupt | Skip that session, mine the rest |
| Individual agent fails | Report partial results, note which agent failed |

## Gotchas

Known failure modes — add to this list as they surface:

- **Conversation miner reads too many sessions**: Cap at 15 sessions. Large JSONL files can exhaust context. If a session file is >5MB, skip it and note in output.
- **Synthesizer ignores low-scoring areas**: Explicitly instruct it to report ALL areas, even those scoring well — the user needs the full picture.
- **Stale path detection false positives**: Some CLAUDE.md references use glob patterns or relative paths that look wrong but resolve correctly. The codebase scanner should verify before marking STALE.
- **MCP tool count explosion**: Projects with many MCP servers can have 100+ tool definitions. The infra auditor should summarize by server, not list every tool.
- **Memory file proliferation**: Some projects have dozens of memory files. The auditor should count and summarize, not read every one — focus on MEMORY.md index and total line count.
