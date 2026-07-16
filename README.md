# Minimal Agentic Coding Demo

This is the smallest possible version of the loop that powers tools like
Claude Code: **act → observe real feedback → fix → repeat**.

## What's here

- `tasks/buggy.py` — three functions, each with one intentional bug
- `tasks/test_buggy.py` — pytest tests that define correct behavior
- `agent.py` — the loop: run tests, show Claude the failure, apply its fix, repeat

## Setup

```bash
pip install anthropic pytest
export ANTHROPIC_API_KEY=sk-...   # your key
```

## Run

```bash
source path/to/venv/bin/activate
python agent.py
PROVIDER=anthropic python agent.py
```

You'll see it:
1. Run pytest — see 3 failures
2. Send the code + error output to Claude
3. Get back a corrected file, write it to disk
4. Re-run pytest
5. Repeat until green (usually 1–2 iterations for this example)

## Why this counts as "agentic"

The key thing is: **you never told it what the bugs were.** It only saw
pytest's output — real, ground-truth feedback from actually running the
code — and used that to correct itself. That feedback loop is the whole
idea. A plain "ask Claude to write code" call has no way to know if its
answer was even right.

## Things to try next (each teaches a real agentic concept)

1. **Make it worse first.** Add a 4th function with a trickier bug (off-by-one,
   wrong edge case) and watch it take more iterations — see the reasoning
   printed at each step.
2. **Add a tool instead of hardcoding the file.** Give Claude a `list_files`
   and `read_file` tool call instead of always handing it `buggy.py` directly.
   Now it has to *decide* what to look at — real tool use instead of
   spoon-fed context.
3. **Add a budget.** Track total tokens or API cost and stop early if it
   exceeds a limit — a real guardrail.
4. **Two-agent review.** Before accepting a fix, send the new code to a
   second Claude call: "does this look correct and minimal?" Only apply it
   if that reviewer agrees. This is the seed of multi-agent orchestration.
5. **Let it write the tests too.** Give it only a plain-English spec
   ("add_numbers should sum two numbers") and have it write both the
   implementation and the tests — now it's planning, not just reacting.
