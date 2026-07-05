# Portfolio Tracker

**Canonical profile:** [github.com/shadowmodder](https://github.com/shadowmodder) — repos, merged PRs, blog links  
**This file:** Active open PRs under review + session ops notes  
**LinkedIn:** [linkedin.com/in/sudhirvissa](https://linkedin.com/in/sudhirvissa)  
**Blog:** [shadowmodder.github.io](https://shadowmodder.github.io)

---

## Active PRs — under review

When a PR merges, move it to the profile README and remove it here.

| PR | Repo | Bug fixed | LinkedIn post |
|---|---|---|---|
| [#3913](https://github.com/EleutherAI/lm-evaluation-harness/pull/3913) | lm-evaluation-harness | ECE + RMS calibration metrics | — |
| [#2816](https://github.com/vibrantlabsai/ragas/pull/2816) | ragas | NDCG, MRR, Precision@K, Recall@K retrieval metrics | [post](https://www.linkedin.com/feed/update/urn:li:share:7479612239688433665/) |
| [#32198](https://github.com/BerriAI/litellm/pull/32198) | litellm | `stream_chunk_builder` KeyError on missing `choices` | — |
| [#32199](https://github.com/BerriAI/litellm/pull/32199) | litellm | `reasoning_tokens` forced to `0` in Responses API proxy | — |
| [#32200](https://github.com/BerriAI/litellm/pull/32200) | litellm | Async cache streaming drops `reasoning_content` | — |
| [#32205](https://github.com/BerriAI/litellm/pull/32205) | litellm | `previous_response_id` double-encoded in MCP tool loops | — |
| [issue #38682](https://github.com/langchain-ai/langchain/issues/38682) | langchain | Streaming tool call fires prematurely with empty args | [post](https://www.linkedin.com/posts/sudhirvissa_langchain-llm-opensource-activity-7346287543816716288-) |
| [#3391](https://github.com/huggingface/peft/pull/3391) | peft | `update_and_allocate` unreachable after `inject_adapter_in_model` | — |
| [#6297](https://github.com/huggingface/trl/pull/6297) | trl | NaN logprobs crash in GRPO trainer with vLLM importance sampling | — |
| [#2412](https://github.com/567-labs/instructor/pull/2412) | instructor | `Optional[NestedModel]` fields stored as raw dicts in streaming partials | — |
| [#9979](https://github.com/stanfordnlp/dspy/pull/9979) | dspy | MIPROv2 silently discards hand-labeled demos — proposer sees "No task demos provided" | — |
| [#47662](https://github.com/vllm-project/vllm/pull/47662) | vllm | `/v1/responses` endpoint rejects valid `input_audio` content parts with 422 | — |

### CI notes
- **#32198, #32199** — LiteLLM benchmarks CI times out at GitHub's 15-min limit (CodSpeed). Not our code. Commented on both asking maintainer to rerun.
- **LangChain** — Issue #38682 open (Type: Bug set via web form — bot should not auto-close). Approach commented, waiting for maintainer assignment. Fix ready on fork branch `fix/streaming-tool-call-empty-args-sse-fragmentation`.
- **#6297** — Resubmit of #6296 (auto-closed: wrong PR template). Now uses full TRL template.

---

## Blog posts

| Post | URL | LinkedIn post |
|---|---|---|
| Your Fraud Model's Scores Are Not Probabilities | [link](https://shadowmodder.github.io/posts/calibration-in-production.html) | [post](https://www.linkedin.com/feed/update/urn:li:share:7479612239688433665/) |
| RAG Retrieval Isn't a Similarity Problem | [link](https://shadowmodder.github.io/posts/rag-retrieval-isnt-similarity.html) | [post](https://www.linkedin.com/posts/sudhirvissa_rag-llm-machinelearning-activity-7346287105668108288-) |
| Running an LLM Gateway in Production | [link](https://shadowmodder.github.io/posts/llm-gateway-production.html) | [post](https://www.linkedin.com/posts/sudhirvissa_llm-mlops-aiinfrastructure-activity-7346287277908844544-) |
| Streaming LLMs in Production | [link](https://shadowmodder.github.io/posts/streaming-llms-production.html) | [post](https://www.linkedin.com/posts/sudhirvissa_llm-mlops-python-activity-7346287476332371968-) · [post 2](https://www.linkedin.com/posts/sudhirvissa_langchain-llm-opensource-activity-7346287543816716288-) |
| Fine-Tuning vs. Prompting | [link](https://shadowmodder.github.io/posts/finetuning-vs-prompting.html) | [post](https://www.linkedin.com/posts/sudhirvissa_llm-finetuning-machinelearning-activity-7346287610684338176-) |

---

## Blog repo ops

- Commits go to `master`. Pages serves from `main`. Always push both:
  ```
  git push origin master && git push origin master:main
  ```
- New posts: add HTML to `posts/`, add card at top of `index.html`.

## Investigated — no PR needed

| Repo | Issue | Finding |
|---|---|---|
| UKPLab/sentence-transformers | #3722 | Fixed in PR #3792 (June 2026) |
| BerriAI/litellm | #32004 | Already fixed in current codebase |
