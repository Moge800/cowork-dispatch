---
name: cowork-dispatch
description: "Use when: delegating bounded coding drafts, test drafts, or quick local verification to the cowork-dispatch MCP server backed by local Ollama."
---

# cowork-dispatch

Use this skill when the workspace has the `cowork-dispatch` MCP server available and you want to use a local Ollama model as a bounded helper for low-risk generation or verification tasks.

The local model is a coworker, not the final decision maker. Use it to draft, summarize, or run narrow checks, then inspect the result before applying it.

## Available Tools

- `ask_ollama`: Sends a prompt to local Ollama and returns its text response.
- `run_pytest`: Runs `uv run pytest` in the workspace and returns the output.

## Good Delegation Targets

- Drafting a small function from clear requirements.
- Drafting pytest cases for a known behavior.
- Producing boilerplate that follows an existing pattern.
- Summarizing a short error log or test failure.
- Suggesting a small refactor for a localized block of code.
- Drafting documentation wording for an already-decided behavior.

## Avoid Delegating

- Final architecture or design decisions.
- Security-sensitive changes.
- Large cross-module refactors.
- Ambiguous requirements that need product judgment.
- Applying code without review.
- Treating local model output as authoritative.

## Workflow

1. Define a narrow task with explicit constraints and expected output format.
2. Ask `ask_ollama` for a draft, keeping prompts short and specific.
3. Review the draft against the repository's existing style and behavior.
4. Apply only the parts that are correct and useful.
5. Run focused tests, or use `run_pytest` when a full pytest run is appropriate.
6. Report what was delegated, what was accepted, and what was verified.

## Prompt Pattern

Use prompts that constrain scope and output shape:

```text
Given this existing Python function and behavior requirement, draft only the replacement function body. Do not include markdown. Preserve the existing public API. Requirement: ...
```

For tests:

```text
Draft pytest tests for this behavior. Return only test functions. Use the existing test style. Do not invent external services or network calls.
```

For summaries:

```text
Summarize this failure output in three bullets: likely cause, relevant line, and next check. Do not propose code changes unless the cause is explicit.
```

## Review Rules

- Prefer repository patterns over the draft's style.
- Check imports, error handling, and edge cases yourself.
- Run generated Python snippets or tests before trusting them.
- Keep edits smaller than the draft when possible.
- Do not paste secrets, tokens, private logs, or proprietary context into local model prompts unless the user explicitly allows it.

## Success Criteria

The skill is being used well when the local coworker handles low-level drafting or repetition, while the main agent keeps responsibility for judgment, edits, and verification.