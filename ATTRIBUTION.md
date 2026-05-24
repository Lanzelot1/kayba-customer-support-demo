# Attribution

This demo runs end-to-end against an open-source benchmark. The
benchmark, its data, its policy, its tools, its user simulator, and its
reward function come from upstream. ACE adds the skillbook-learning
layer.

## Source

- **TAU-bench / tau2-bench** — Sierra Research
- Repository: https://github.com/sierra-research/tau2-bench
- License: **MIT** © 2025 Sierra Research
- Leaderboard: https://tau-bench.github.io

## What comes from tau2-bench

- The airline policy used as the agent's system prompt
- The airline reservation database and tool definitions
- The 50 airline tasks and the published 30 / 20 train/test split
- The user-simulator implementation and its global guidelines
- The reward function (database-state match + natural-language and
  communicate assertions)

ACE consumes all of this through `tau2.run.run_task` (wrapped by
`ace_eval.e2e.benchmarks.tau_bench.TauBenchRunner`). tau2 is not forked
or modified.

## What ACE adds

- The Reflector that reads each baseline rollout and identifies failure
  modes
- The SkillManager that distils those failures into reusable rules
- The Skillbook (`evidence/skillbook.json`)
- The injection mechanism that puts the learned rules into the agent's
  prompt at inference time

## Evidence shipped here

The skillbook and traces come from an end-to-end run on the open-source
[agentic-context-engine](https://github.com/kayba-ai/agentic-context-engine)
repo. Specific run identifier is recorded in
`evidence/result.json::run_id`.

- `evidence/skillbook.json` — verbatim output of the e2e run
- `evidence/result.json` — verbatim output of the same run, containing
  the numbers cited in `README.md` and `ONE_PAGER.md`
- `evidence/traces/*.json` — 10-trace subset (5 pass, 5 fail) of the
  haiku baseline rollouts on the airline train split. Each file is
  tau2's native simulation record with `info`, `task`, and `simulation`
  keys.

## License notice

The MIT license requires the copyright notice be retained; the original
`LICENSE` is in the tau2-bench repository linked above. This demo ships
under the same license as the
[agentic-context-engine](https://github.com/kayba-ai/agentic-context-engine)
framework.
