# Minimal Agentic Coding Demo

This is the smallest possible version of the loop that powers tools like
Claude Code: **act → observe real feedback → fix → repeat**.

## What's here

- `tasks/buggy.py` — three functions, each with one intentional bug
- `tasks/test_buggy.py` — pytest tests that define correct behavior
- `agent.py` — the loop: run tests, show Claude the failure, apply its fix, repeat

## Setup

**1. Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

You'll know it worked because your prompt will show `(venv)` at the start.

**2. Install dependencies (inside the venv)**

```bash
pip install anthropic python-dotenv pytest
```

**3. Choose a provider — Anthropic (cloud, needs a key) or Ollama (local, free)**

### Option A: Anthropic (default)

Create a `.env` file in this folder (copy `.env.example`) with your key:

```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

`agent.py` loads this automatically via `python-dotenv` — no need to
`export` anything in your shell.

**Don't commit `.env` to git.** If this becomes a real repo, add a
`.gitignore` with `.env` in it — `.env.example` is safe to commit since it
has no real key.

### Option B: Ollama (runs locally, no API key, no cost)

Install Ollama from [ollama.com](https://ollama.com) if you haven't, then:

```bash
ollama serve                        # in one terminal, keep it running
ollama pull qwen2.5-coder:7b        # once, downloads the model (~5GB)
```

No `.env` needed for this path.

## Run

Make sure your venv is activated (`(venv)` showing in your prompt) before
running either of these.

**With Anthropic:**
```bash
python agent.py
```

```bash
USE_TOOLS=1 PROVIDER=anthropic python agent.py;  
```

**With Ollama:**
```bash
PROVIDER=ollama python agent.py
```
On Windows PowerShell:
```powershell
$env:PROVIDER="ollama"; python agent.py
```
To use a different local model: `OLLAMA_MODEL=llama3.1 PROVIDER=ollama python agent.py`

You'll see it:
1. Run pytest — see 3 failures
2. Send the code + error output to the model
3. Get back a corrected file, write it to disk
4. Re-run pytest
5. Repeat until green (usually 1–2 iterations for this example)

## Why this counts as "agentic"

The key thing is: **you never told it what the bugs were.** It only saw
pytest's output — real, ground-truth feedback from actually running the
code — and used that to correct itself. That feedback loop is the whole
idea. A plain "ask Claude to write code" call has no way to know if its
answer was even right.

## Version control safety net

The agent now git-commits its own progress:

- On first run, it `git init`s this folder and commits the buggy starting state as a baseline.
- Each fix attempt is left **uncommitted** until the *next* iteration confirms it didn't make things worse (compares failure counts before/after).
- If a fix **improves or holds steady** → it gets committed with a message like `attempt 2: failures 3 -> 1`.
- If a fix **regresses** (more failures than before) → `git checkout -- tasks/` discards it and restores the last good commit, and the agent tries again from that known-good state instead of compounding a bad edit.

Run `git log --oneline` afterward in this folder to see every kept attempt —
a real audit trail of what the agent tried and which fixes stuck.

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