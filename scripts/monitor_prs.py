#!/usr/bin/env python3
"""
Hourly PR CI monitor. Checks all open contribution PRs, auto-fixes
ruff format/I001 failures in LiteLLM PRs, and writes /tmp/pr_status.md.
"""
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timezone

# ── PR manifest ──────────────────────────────────────────────────────────────

LITELLM_PRS = [
    ("BerriAI/litellm", 32198, "fix/stream-chunk-builder-missing-choices-key"),
    ("BerriAI/litellm", 32199, "fix/reasoning-tokens-zero-in-responses-api-output"),
    ("BerriAI/litellm", 32200, "fix/async-cache-streaming-drops-reasoning-content"),
    ("BerriAI/litellm", 32205, "fix/responses-api-previous-response-id-double-encode"),
]

OTHER_PRS = [
    ("EleutherAI/lm-evaluation-harness", 3913),
    ("vibrantlabsai/ragas", 2816),
    ("huggingface/peft", 3391),
    ("huggingface/trl", 6297),
    ("567-labs/instructor", 2412),
    ("stanfordnlp/dspy", 9979),
    ("vllm-project/vllm", 47662),
]

# Checks that always fail for external contributors — skip silently
LITELLM_KNOWN_UNFIXABLE = {
    "Verify PR source branch",
    "Guard main branch",
    "CodeQL",
    "codecov/patch",
    "CodSpeed Benchmarks",
    "Code scanning results / CodeQL",
}

FORK_USER = "shadowmodder"
WORK_DIR = Path(tempfile.mkdtemp(prefix="pr-monitor-"))
HAS_FORK_PAT = bool(os.environ.get("FORK_PAT"))


# ── Helpers ───────────────────────────────────────────────────────────────────

def run(cmd, **kwargs):
    kwargs.setdefault("capture_output", True)
    kwargs.setdefault("text", True)
    return subprocess.run(cmd, **kwargs)


def gh(*args):
    return run(["gh"] + list(args))


def get_pr_info(repo, number):
    r = gh("pr", "view", str(number), "--repo", repo,
           "--json", "state,mergedAt,title,headRefName")
    if r.returncode != 0:
        return None
    return json.loads(r.stdout)


def get_checks(repo, number):
    r = gh("pr", "checks", str(number), "--repo", repo)
    if r.returncode != 0 and not r.stdout:
        return []
    lines = r.stdout.strip().splitlines()
    checks = []
    for line in lines:
        parts = re.split(r'\t+', line.strip())
        if len(parts) >= 2:
            checks.append({"name": parts[0].strip(), "status": parts[1].strip()})
    return checks


def checks_summary(checks, skip_names=None):
    skip_names = skip_names or set()
    relevant = [c for c in checks if c["name"] not in skip_names]
    passing = sum(1 for c in relevant if c["status"] == "pass")
    failing = [c for c in relevant if c["status"] == "fail"]
    pending = sum(1 for c in relevant if c["status"] in ("pending", "in_progress", "queued", ""))
    return passing, failing, pending


# ── LiteLLM auto-fix ─────────────────────────────────────────────────────────

def clone_fork(repo_name, branch, clone_dir):
    if (clone_dir / ".git").exists():
        run(["git", "-C", str(clone_dir), "pull", "--ff-only"], capture_output=True)
        return True
    r = run(["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse",
             "--branch", branch,
             f"https://x-access-token:{os.environ['FORK_PAT']}@github.com/{FORK_USER}/{repo_name}.git",
             str(clone_dir)])
    return r.returncode == 0


def get_failing_lint_files(repo, run_id):
    """Parse log of a failed lint run for 'Would reformat' and I001 files."""
    r = gh("run", "view", run_id, "--repo", repo, "--log-failed")
    reformat = set(re.findall(r"Would reformat: (litellm/[^\s]+)", r.stdout))
    i001 = set(re.findall(r"(litellm/[^\s]+):\d+:\d+: I001", r.stdout))
    return reformat, i001


def get_latest_failed_lint_run(repo, branch):
    r = gh("run", "list", "--repo", repo, "--branch", branch,
           "--workflow", "test-linting.yml", "--limit", "5",
           "--json", "databaseId,status,conclusion")
    if r.returncode != 0:
        return None
    runs = json.loads(r.stdout)
    for run_obj in runs:
        if run_obj.get("conclusion") == "failure":
            return str(run_obj["databaseId"])
    return None


def autofix_litellm(repo, number, branch):
    """Returns a description of what was fixed, or None."""
    if not HAS_FORK_PAT:
        return None

    repo_name = repo.split("/")[1]
    clone_dir = WORK_DIR / repo_name / branch.replace("/", "_")
    clone_dir.mkdir(parents=True, exist_ok=True)

    if not clone_fork(repo_name, branch, clone_dir):
        return None

    run_id = get_latest_failed_lint_run(repo, branch)
    if not run_id:
        return None

    reformat_files, i001_files = get_failing_lint_files(repo, run_id)
    if not reformat_files and not i001_files:
        return None

    all_files = reformat_files | i001_files
    # Sparse-checkout all needed files
    run(["git", "-C", str(clone_dir), "sparse-checkout", "set", "--skip-checks"] +
        list(all_files))
    run(["git", "-C", str(clone_dir), "checkout"])

    fixed = []

    if reformat_files:
        r = run(["ruff", "format"] + list(reformat_files), cwd=clone_dir)
        if r.returncode == 0:
            fixed.append(f"ruff format: {', '.join(reformat_files)}")

    if i001_files:
        r = run(["ruff", "check", "--select", "I001", "--fix"] + list(i001_files),
                cwd=clone_dir)
        if r.returncode == 0:
            fixed.append(f"ruff I001: {', '.join(i001_files)}")

    if not fixed:
        return None

    # Check if anything actually changed
    diff = run(["git", "-C", str(clone_dir), "diff", "--name-only"])
    if not diff.stdout.strip():
        return None

    run(["git", "-C", str(clone_dir), "add", "-u"])
    run(["git", "-C", str(clone_dir), "commit",
         "-m", f"style: fix ruff lint in {repo}#{number}"])
    push = run(["git", "-C", str(clone_dir), "push", "origin", branch])
    if push.returncode != 0:
        return None

    return "; ".join(fixed)


# ── Main ─────────────────────────────────────────────────────────────────────

def check_pr(repo, number, branch=None, is_litellm=False):
    info = get_pr_info(repo, number)
    if not info:
        return {"repo": repo, "number": number, "status": "❓", "note": "could not fetch"}

    if info.get("mergedAt"):
        return {"repo": repo, "number": number, "status": "✅ Merged", "note": ""}

    if info.get("state") == "CLOSED":
        return {"repo": repo, "number": number, "status": "❌ Closed", "note": "needs human review"}

    checks = get_checks(repo, number)
    skip = LITELLM_KNOWN_UNFIXABLE if is_litellm else set()
    passing, failing, pending = checks_summary(checks, skip_names=skip)

    if failing:
        fail_names = [c["name"] for c in failing]
        # Check if auto-fixable lint failure
        lint_failing = any("lint" in n.lower() or "linting" in n.lower() for n in fail_names)
        if is_litellm and lint_failing and branch:
            fixed = autofix_litellm(repo, number, branch)
            if fixed:
                return {"repo": repo, "number": number, "status": "🔧 Fixed",
                        "note": f"pushed fix: {fixed} — CI re-running"}
        return {"repo": repo, "number": number, "status": "❌ Failing",
                "note": f"NEEDS HUMAN REVIEW: {', '.join(fail_names)}"}

    if pending:
        return {"repo": repo, "number": number, "status": "⏳ In progress",
                "note": f"{passing} pass, {pending} pending"}

    if passing:
        skip_note = " (guard/CodeQL unfixable skipped)" if is_litellm else ""
        return {"repo": repo, "number": number, "status": "🟢 Green",
                "note": f"all {passing} checks pass{skip_note}"}

    return {"repo": repo, "number": number, "status": "❓ Unknown", "note": "no checks found"}


def main():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    results = []

    print("Checking LiteLLM PRs...")
    for repo, number, branch in LITELLM_PRS:
        r = check_pr(repo, number, branch=branch, is_litellm=True)
        results.append(r)
        print(f"  {repo}#{number}: {r['status']} — {r['note']}")

    print("Checking other PRs...")
    for repo, number in OTHER_PRS:
        r = check_pr(repo, number, is_litellm=False)
        results.append(r)
        print(f"  {repo}#{number}: {r['status']} — {r['note']}")

    # Build markdown report
    lines = [
        f"## PR CI Status — {now}",
        "",
        "| Repo | PR | Status | Notes |",
        "|------|-----|--------|-------|",
    ]
    needs_attention = []
    for r in results:
        repo_short = r["repo"].split("/")[1]
        lines.append(f"| {repo_short} | #{r['number']} | {r['status']} | {r['note']} |")
        if "NEEDS HUMAN REVIEW" in r.get("note", "") or r["status"] == "❌ Closed":
            needs_attention.append(f"{r['repo']}#{r['number']}: {r['note']}")

    if needs_attention:
        lines += ["", "### ⚠️ Needs human review", ""]
        for item in needs_attention:
            lines.append(f"- {item}")

    auto_fixed = [r for r in results if r["status"] == "🔧 Fixed"]
    if auto_fixed:
        lines += ["", "### 🔧 Auto-fixed this run", ""]
        for r in auto_fixed:
            lines.append(f"- {r['repo']}#{r['number']}: {r['note']}")

    lines += ["", "---", f"*Monitoring {len(results)} PRs. Runs hourly.*"]

    report = "\n".join(lines)
    Path("/tmp/pr_status.md").write_text(report)
    print("\n" + report)

    # Exit 0 always — failures are reported via the issue, not the workflow status
    return 0


if __name__ == "__main__":
    sys.exit(main())
