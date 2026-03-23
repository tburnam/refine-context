#!/usr/bin/env python3
"""Mine a Claude Code session JSONL file for usage patterns.

Parses a single session file and extracts tool usage, skill invocations,
and user prompts. Outputs structured JSON to stdout for aggregation by
the conversation-miner agent.

Usage:
    python3 mine_sessions.py <session.jsonl>

Output (JSON):
    {
        "tools": [["ToolName", count], ...],
        "skills": [["skill-name", count], ...],
        "prompts": ["first 200 chars of user message", ...]
    }
"""

import collections
import json
import sys


def mine_session(filepath: str) -> dict:
    """Parse a session JSONL file and return usage data."""
    tools = collections.Counter()
    skills = collections.Counter()
    user_prompts = []

    with open(filepath, encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                # Malformed line — skip and continue
                print(
                    f"Warning: skipping malformed JSON at line {line_num}",
                    file=sys.stderr,
                )
                continue

            msg_type = obj.get("type")
            message = obj.get("message", {})

            if msg_type == "assistant":
                for content_block in message.get("content", []):
                    if content_block.get("type") == "tool_use":
                        tool_name = content_block.get("name", "unknown")
                        tools[tool_name] += 1
                        if tool_name == "Skill":
                            skill_name = (
                                content_block.get("input", {}).get("skill", "unknown")
                            )
                            skills[skill_name] += 1

            elif msg_type == "user":
                content = message.get("content", "")
                if isinstance(content, str) and len(content) > 5:
                    user_prompts.append(content[:200])
                elif isinstance(content, list):
                    # Handle structured content blocks
                    for block in content:
                        if isinstance(block, dict) and block.get("type") == "text":
                            text = block.get("text", "")
                            if len(text) > 5:
                                user_prompts.append(text[:200])
                                break

    return {
        "tools": tools.most_common(30),
        "skills": skills.most_common(),
        "prompts": user_prompts[:50],
    }


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <session.jsonl>", file=sys.stderr)
        sys.exit(1)

    filepath = sys.argv[1]
    try:
        result = mine_session(filepath)
    except FileNotFoundError:
        print(f"Error: file not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: permission denied: {filepath}", file=sys.stderr)
        sys.exit(1)

    json.dump(result, sys.stdout, indent=2)
    print()  # trailing newline


if __name__ == "__main__":
    main()
