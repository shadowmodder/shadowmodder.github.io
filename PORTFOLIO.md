# ML/LLM Portfolio — Open Source Contributions

Active sprint tracking. Updated each session.

---

## Open Source PRs

| PR | Repo | Status | Bug Fixed |
|---|---|---|---|
| [#3913](https://github.com/EleutherAI/lm-evaluation-harness/pull/3913) | EleutherAI/lm-evaluation-harness | Open | Added ECE + RMS calibration metrics |
| [#2816](https://github.com/vibrantlabsai/ragas/pull/2816) | vibrantlabsai/ragas | Open | Added NDCG, MRR, Precision@K, Recall@K retrieval metrics |
| [#32198](https://github.com/BerriAI/litellm/pull/32198) | BerriAI/litellm | Open — benchmarks timeout (not our code) | `stream_chunk_builder` KeyError on missing `choices` key |
| [#32199](https://github.com/BerriAI/litellm/pull/32199) | BerriAI/litellm | Open — benchmarks timeout (not our code) | `reasoning_tokens` forced to `0` in Responses API proxy |
| [#32200](https://github.com/BerriAI/litellm/pull/32200) | BerriAI/litellm | Open | Async cache streaming silently drops `reasoning_content` |
| [#32205](https://github.com/BerriAI/litellm/pull/32205) | BerriAI/litellm | Open | `previous_response_id` double-encoded in MCP tool loops |
| [#38678](https://github.com/langchain-ai/langchain/pull/38678) | langchain-ai/langchain | Open | Streaming tool call fires prematurely with empty args `{}` |
| [#3391](https://github.com/huggingface/peft/pull/3391) | huggingface/peft | Open | `update_and_allocate` unreachable after `inject_adapter_in_model` |
| [#6296](https://github.com/huggingface/trl/pull/6296) | huggingface/trl | Open | NaN logprobs crash in GRPO trainer with vLLM importance sampling |

### Investigated — no PR needed
| Repo | Issue | Finding |
|---|---|---|
| UKPLab/sentence-transformers | #3722 | Already fixed in PR #3792 (June 2026) |
| BerriAI/litellm | #32004 | Bedrock streaming already fixed in current codebase |

---

## Blog Posts

All live at [shadowmodder.github.io](https://shadowmodder.github.io)

| Post | URL | Published |
|---|---|---|
| Your Fraud Model's Scores Are Not Probabilities | [calibration-in-production.html](https://shadowmodder.github.io/posts/calibration-in-production.html) | Jul 2026 |
| RAG Retrieval Isn't a Similarity Problem | [rag-retrieval-isnt-similarity.html](https://shadowmodder.github.io/posts/rag-retrieval-isnt-similarity.html) | Jul 2026 |
| Running an LLM Gateway in Production | [llm-gateway-production.html](https://shadowmodder.github.io/posts/llm-gateway-production.html) | Jul 2026 |
| Streaming LLMs in Production: The Edge Cases That Break Your App | [streaming-llms-production.html](https://shadowmodder.github.io/posts/streaming-llms-production.html) | Jul 2026 |
| Fine-Tuning vs. Prompting: A Decision Framework That Doesn't Lie to You | [finetuning-vs-prompting.html](https://shadowmodder.github.io/posts/finetuning-vs-prompting.html) | Jul 2026 |

---

## LinkedIn Posts

| Post | Linked to |
|---|---|
| Calibration: fraud model scores aren't probabilities | Blog post 1 |
| RAG retrieval is a relevance problem, not similarity | Blog post 2 + ragas PR #2816 |
| LLM API costs are 3x higher than they need to be | Blog post 3 |
| Streaming breaks in 6 specific ways in production | Blog post 4 |
| Fine-tuning vs. prompting decision tree | Blog post 5 |
| LangChain streaming bug — real-world example | Blog post 4 + langchain PR #38678 |

---

## Notes

- LiteLLM benchmark CI failures (#32198, #32199): CodSpeed job times out at GitHub's 15-min limit. Not caused by our changes. Commented on both PRs asking maintainers to rerun.
- Blog repo uses `master` branch for commits; `main` branch is what GitHub Pages serves. Both must stay in sync — push to both with `git push origin master` then `git push origin master:main`.
