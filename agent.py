"""
Minimal agentic coding loop.

Loop: run tests -> if failing, show Claude the code + error -> apply Claude's
fix -> run tests again -> repeat until green or max iterations reached.

Setup:
    pip install anthropic python-dotenv pytest
    Create a .env file next to this script containing:
        ANTHROPIC_API_KEY=sk-ant-...

Run:
    python agent.py
"""

import json
import os
import re
import subprocess
import urllib.request
from pathlib import Path

from dotenv import load_dotenv
import anthropic

load_dotenv()  # reads ANTHROPIC_API_KEY (and anything else) from a .env file

# PROVIDER = "anthropic" (default, needs ANTHROPIC_API_KEY, costs money)
#          = "ollama"    (local, free, needs `ollama serve` running)
PROVIDER = os.environ.get("PROVIDER", "anthropic")
MODEL = "claude-sonnet-4-6"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:7b")
OLLAMA_URL = "http://localhost:11434/api/chat"

TASK_FILE = Path(__file__).parent / "tasks" / "buggy.py"
TEST_DIR = Path(__file__).parent / "tasks"
MAX_ITERATIONS = 6

if PROVIDER == "anthropic":
    _key = os.environ.get("ANTHROPIC_API_KEY")
    print(f"[debug] ANTHROPIC_API_KEY loaded: {'yes -> ' + _key[:10] + '...' if _key else 'NO — not found'}")
    client = anthropic.Anthropic()
else:
    client = None

print(f"[debug] Using provider: {PROVIDER} ({MODEL if PROVIDER == 'anthropic' else OLLAMA_MODEL})")


def run_tests() -> tuple[bool, str]:
    """Run pytest in the tasks dir. Returns (all_passed, output_text)."""
    result = subprocess.run(
        ["python", "-m", "pytest", "-v", "--tb=short"],
        cwd=TEST_DIR,
        capture_output=True,
        text=True,
    )
    output = result.stdout + result.stderr
    return result.returncode == 0, output


def ask_claude_for_fix(code: str, test_output: str) -> str:
    """Send the current code + failing test output to Claude, get back
    a full corrected version of the file."""

    system_prompt = (
        "You are an autonomous coding agent fixing a Python file so its "
        "test suite passes. You will be shown the current file content and "
        "the pytest output. Respond with ONLY a JSON object, no other text, "
        "no markdown fences, in this exact shape:\n"
        '{"reasoning": "one sentence on what was wrong", '
        '"new_file_content": "the full corrected file content"}\n'
        "The new_file_content must be the COMPLETE file (not a diff, not a "
        "snippet) — it will directly overwrite the existing file."
    )

    user_prompt = (
        f"Current file (tasks/buggy.py):\n```python\n{code}\n```\n\n"
        f"pytest output:\n```\n{test_output}\n```\n\n"
        "Fix ONLY what's needed to make the tests pass. Keep docstrings."
    )

    response = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = response.content[0].text.strip()
    # Strip accidental markdown fences just in case.
    raw = re.sub(r"^```(json)?|```$", "", raw.strip(), flags=re.MULTILINE).strip()

    parsed = json.loads(raw)
    print(f"    Claude's reasoning: {parsed['reasoning']}")
    return parsed["new_file_content"]


def ask_ollama_for_fix(code: str, test_output: str) -> str:
    """Same as ask_claude_for_fix, but calls a local Ollama server instead.
    Requires `ollama serve` running and the model pulled, e.g.:
        ollama pull qwen2.5-coder:7b
    """
    prompt = (
        "You are an autonomous coding agent fixing a Python file so its test "
        "suite passes. Respond with ONLY a JSON object, no other text, no "
        "markdown fences, in this exact shape:\n"
        '{"reasoning": "one sentence on what was wrong", '
        '"new_file_content": "the full corrected file content"}\n\n'
        f"Current file (tasks/buggy.py):\n```python\n{code}\n```\n\n"
        f"pytest output:\n```\n{test_output}\n```\n\n"
        "Fix ONLY what's needed to make the tests pass. Keep docstrings."
    )

    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
        "format": "json",
    }).encode()

    req = urllib.request.Request(
        OLLAMA_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        body = json.loads(resp.read())

    raw = body["message"]["content"].strip()
    raw = re.sub(r"^```(json)?|```$", "", raw, flags=re.MULTILINE).strip()

    parsed = json.loads(raw)
    print(f"    Ollama's reasoning: {parsed['reasoning']}")
    return parsed["new_file_content"]


def ask_llm_for_fix(code: str, test_output: str) -> str:
    """Dispatch to whichever provider is configured."""
    if PROVIDER == "ollama":
        return ask_ollama_for_fix(code, test_output)
    return ask_claude_for_fix(code, test_output)


def main():
    print(f"Starting agentic loop (max {MAX_ITERATIONS} iterations)\n")

    for i in range(1, MAX_ITERATIONS + 1):
        print(f"--- Iteration {i} ---")
        passed, output = run_tests()

        if passed:
            print("✅ All tests passing. Done.")
            print(output)
            return

        print(f"❌ Tests failing. Asking {PROVIDER} for a fix...")
        current_code = TASK_FILE.read_text()

        try:
            new_code = ask_llm_for_fix(current_code, output)
        except (json.JSONDecodeError, KeyError) as e:
            print(f"    Could not parse response: {e}")
            continue

        TASK_FILE.write_text(new_code)
        print("    Applied fix. Re-running tests...\n")

    print(f"⚠️ Gave up after {MAX_ITERATIONS} iterations without all tests passing.")
    _, final_output = run_tests()
    print(final_output)


if __name__ == "__main__":
    main()