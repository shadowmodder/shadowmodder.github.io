# Session Notes

The canonical portfolio lives at **[github.com/shadowmodder](https://github.com/shadowmodder)** (the profile README). That's the single source of truth for repos, PRs, and blog posts. Update it, not this file.

---

## Active PRs — quick reference

| PR | Repo | Notes |
|---|---|---|
| [#3913](https://github.com/EleutherAI/lm-evaluation-harness/pull/3913) | lm-evaluation-harness | |
| [#2816](https://github.com/vibrantlabsai/ragas/pull/2816) | ragas | |
| [#32198](https://github.com/BerriAI/litellm/pull/32198) | litellm | Benchmarks CI timeout — not our code. Commented asking maintainer to rerun. |
| [#32199](https://github.com/BerriAI/litellm/pull/32199) | litellm | Same benchmarks timeout. |
| [#32200](https://github.com/BerriAI/litellm/pull/32200) | litellm | |
| [#32205](https://github.com/BerriAI/litellm/pull/32205) | litellm | |
| [#38680](https://github.com/langchain-ai/langchain/pull/38680) | langchain | Resubmit of #38678 (auto-closed: no issue). Links to issue #38679. |
| [#3391](https://github.com/huggingface/peft/pull/3391) | peft | |
| [#6297](https://github.com/huggingface/trl/pull/6297) | trl | Resubmit of #6296 (auto-closed: wrong template). |

## Blog repo ops

- Commits go to `master`. GitHub Pages serves from `main`.
- Always push both: `git push origin master && git push origin master:main`
- New posts go in `posts/`, update `index.html` to add card at top of list.

## Investigated — no PR needed

| Repo | Issue | Reason |
|---|---|---|
| UKPLab/sentence-transformers | #3722 | Fixed in PR #3792 (June 2026) |
| BerriAI/litellm | #32004 | Already fixed in current codebase |
