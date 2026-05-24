<p align="center">
  <a href="https://kayba.ai"><img src="assets/kayba-banner.png" alt="Kayba" width="1080"/></a>
</p>

# Self-Improving Customer-Support Agent

**A [Kayba](https://kayba.ai) demo.** Open-source proof that an AI agent can read its own failed conversations, write a rulebook to fix them, and get measurably better, with no fine-tuning and no stack access.

| Benchmark | tau2-bench airline (20 held-out tasks) |
|---|---|
| Baseline pass@1 | 35% (7/20) |
| With learned rulebook | **55% (11/20)** |
| Strict consistency (pass^4) | **20% → 40% (2×)** all-4-attempts-correct rate |
| What's learned | 15 short rules in plain English |

> **Non-technical?** Read **[`ONE_PAGER.md`](ONE_PAGER.md)**: same numbers, plain language, forwardable. The rest of this README is engineer-facing: how to reproduce the run.

Built on [ACE (agentic-context-engine)](https://github.com/kayba-ai/agentic-context-engine), applied to [tau2-bench](https://github.com/sierra-research/tau2-bench)'s airline domain. 15 rules learned from 30 training conversations, evaluated on the 20-task test split.

## What's in here

```
kayba-customer-support-demo/
  README.md                     <- this file
  ONE_PAGER.md                  <- forwardable plain-language summary
  ATTRIBUTION.md                <- credits to tau2-bench / Sierra Research
  run.sh                        <- reproduce the run
  build_evidence.py             <- regenerate skills.md + injection text
  evidence/
    skillbook.json              <- 15 learned skills (verbatim run output)
    result.json                 <- run metadata + numbers
    skills.md                   <- skillbook rendered for humans
    external_agent_injection.txt  <- paste-into-any-agent prompt block
    traces/                     <- 5 pass + 5 fail multi-turn rollouts
```

## Results

From `evidence/result.json`:

| Field | Value |
|---|---|
| Benchmark | tau-bench-airline (full 20-task test split) |
| Agent model | `bedrock/eu.anthropic.claude-haiku-4-5` |
| Reflector + SkillManager | `bedrock/eu.anthropic.claude-sonnet-4-6` |
| User simulator | `gpt-4o`, seed 42 |
| Train / test split | 30 / 20 (tau2-airline's published split) |
| Trials per task | 1 |
| Baseline pass@1 | 35% (7 of 20) |
| With skillbook pass@1 | **55%** (11 of 20) |
| Newly passing | 5 tasks |
| Newly regressing | 1 task |
| Skills learned | 15 across 7 sections |

## How it works

1. ACE runs the haiku agent on the 30 training tasks against tau2's
   multi-turn simulator and records the rollouts.
2. The Reflector (sonnet) reads every rollout and identifies the failure
   modes, including the ones in tasks the agent passed by luck.
3. The SkillManager (also sonnet) distils those failure modes into 15
   short rules, saved to `evidence/skillbook.json`.
4. The haiku agent re-runs the 20 test tasks with the skillbook injected
   into its prompt. 5 new tasks pass, 1 regresses, net +20 pp.

The agent and the simulated customer are different LLMs with separate
system prompts. The agent sees the airline policy + tools. It never sees
the customer's hidden objectives. That's why the rules generalise
rather than memorise.

## Reproducing the run

The CLI (`ace-eval e2e`) lives in the
[agentic-context-engine](https://github.com/kayba-ai/agentic-context-engine)
repo. To reproduce:

```bash
# Clone the framework next to this repo
git clone https://github.com/kayba-ai/agentic-context-engine.git
cd agentic-context-engine
uv sync
git submodule update --init --recursive

# Copy run.sh in and execute
cp ../kayba-customer-support-demo/run.sh .
bash run.sh    # ~31 min, ~$2
```

> The `ace-eval` submodule on `agentic-context-engine`'s `main` is
> currently pinned at a commit that imports `ace.rr.*`; the parent ACE
> package has since moved that namespace to `ace.implementations.rr.*`.
> Fresh runs need the submodule bumped to a commit using the new path.
> The shipped `evidence/` artefacts are unaffected.

## Re-rendering the evidence files

```bash
uv run python build_evidence.py
```

The renderer reads `evidence/skillbook.json` directly so it stays robust
to schema changes in the live `ace.Skillbook` class.
