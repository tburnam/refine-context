# Context Refinement Report

**Project**: `{project_path}` | **Date**: {date} | **Sessions analyzed**: {session_count}

---

## Executive Summary

{executive_summary}

---

## Context Budget

| Source | Lines | Est. Tokens | Load Frequency |
|--------|------:|------------:|----------------|
| CLAUDE.md (global) | {global_claude_lines} | {global_claude_tokens} | Every session |
| CLAUDE.md (project) | {project_claude_lines} | {project_claude_tokens} | Every session |
| Rules (global-loading) | {global_rules_lines} | {global_rules_tokens} | Every session |
| Rules (path-scoped) | {scoped_rules_lines} | {scoped_rules_tokens} | On file match |
| Auto memory (MEMORY.md) | {memory_lines} | {memory_tokens} | First 200 lines |
| Skill descriptions | {skill_desc_lines} | {skill_desc_tokens} | Every session |
| Subdirectory CLAUDE.md | {subdir_claude_lines} | {subdir_claude_tokens} | On file access |
| **Total always-loaded** | **{total_always_lines}** | **{total_always_tokens}** | |

> Target: <=200 lines / ~800 tokens for main CLAUDE.md. Adherence drops from >92% to ~71% above 400 lines.

---

## Scores

| Area | Score | Grade |
|------|------:|-------|
| CLAUDE.md Quality | {claudemd_score}/100 | {claudemd_grade} |
| Skill Coverage | {skill_score}/100 | {skill_grade} |
| Config Optimization | {config_score}/100 | {config_grade} |
| Session Alignment | {session_score}/100 | {session_grade} |
| **Overall** | **{overall_score}/100** | **{overall_grade}** |

---

## Context Inventory

### CLAUDE.md Files

| File | Location | Lines | Est. Tokens | Load Trigger |
|------|----------|------:|------------:|--------------|
{claudemd_inventory_rows}

### Rules

| Rule | Scope | Lines | Est. Tokens | `paths:` Filter |
|------|-------|------:|------------:|-----------------|
{rules_inventory_rows}

### Skills

| Skill | Source | Lines | Est. Tokens | Auto-invocable | Notes |
|-------|--------|------:|------------:|:--------------:|-------|
{skills_inventory_rows}

### Agents

| Agent | Source | Model | Tools | Notes |
|-------|--------|-------|-------|-------|
{agents_inventory_rows}

### MCP Servers

| Server | Transport | Has Skill Docs | Tool Count | Notes |
|--------|-----------|:--------------:|----------:|-------|
{mcp_inventory_rows}

### Hooks

| Hook | Lifecycle Event | Source | Notes |
|------|----------------|--------|-------|
{hooks_inventory_rows}

### Plugins

| Plugin | Version | Scope | Provides |
|--------|---------|-------|----------|
{plugins_inventory_rows}

---

## Scrutiny Test Results

{scrutiny_results_per_file}

<!-- Repeat this block per file:

### {file_path}

| Section | Lines | Verdict | Recommended Destination | Evidence |
|---------|------:|---------|------------------------|----------|
| {section_name} | {lines} | {PASS/FAIL} | {destination_or_dash} | {evidence} |

-->

---

## Conversation Insights

### Tool Frequency

| Rank | Tool | Invocations |
|-----:|------|------------:|
{tool_frequency_rows}

### Skill Usage

| Skill | Invocations | Notes |
|-------|------------:|-------|
{skill_usage_rows}

### Query Archetypes

| Archetype | Frequency | Example |
|-----------|----------:|---------|
{query_archetype_rows}

### Repeated Questions

{repeated_questions}

### Context Failures

| Pattern | Occurrences | Example Session |
|---------|------------:|-----------------|
{context_failure_rows}

### Compaction Signals

{compaction_signals}

---

## Recommendations

### P0 -- High Impact, Easy

| # | Category | Recommendation | Evidence | Scrutiny Alignment | Token Impact |
|--:|----------|---------------|----------|-------------------|-------------:|
{p0_rows}

### P1 -- High Impact, Moderate Effort

| # | Category | Recommendation | Evidence | Scrutiny Alignment | Token Impact |
|--:|----------|---------------|----------|-------------------|-------------:|
{p1_rows}

### P2 -- Moderate Impact

| # | Category | Recommendation | Evidence | Scrutiny Alignment | Token Impact |
|--:|----------|---------------|----------|-------------------|-------------:|
{p2_rows}

### P3 -- Low Priority

| # | Category | Recommendation | Evidence | Scrutiny Alignment | Token Impact |
|--:|----------|---------------|----------|-------------------|-------------:|
{p3_rows}

---

*Run `/refine-context` again after implementing changes to measure improvement.*
