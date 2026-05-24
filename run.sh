#!/usr/bin/env bash
# Reproduce the tau2-bench airline e2e run that produced evidence/skillbook.json
# and evidence/result.json. ~31 minutes, ~$2 with claude-haiku-4-5 (agent) and
# claude-sonnet-4-6 (reflector + SkillManager) on Bedrock.
#
# Required env:
#   AWS credentials with Bedrock access for the agent + reflector
#   OPENAI_API_KEY for the tau2 user simulator (gpt-4o)
#
# Override AGENT_MODEL / REFLECTOR_MODEL via env if you want a different model.

set -euo pipefail

AGENT_MODEL="${AGENT_MODEL:-bedrock/eu.anthropic.claude-haiku-4-5-20251001-v1:0}"
REFLECTOR_MODEL="${REFLECTOR_MODEL:-bedrock/eu.anthropic.claude-sonnet-4-6}"
USER_MODEL="${USER_MODEL:-gpt-4o}"
OUTPUT_DIR="${OUTPUT_DIR:-results/luis-demo}"

# Expects to be run from the root of a checkout of agentic-context-engine
# (https://github.com/kayba-ai/agentic-context-engine). See the README for
# the clone-and-copy steps.
if [[ ! -d ace-eval/src/ace_eval ]]; then
  echo "Error: run this script from the root of an agentic-context-engine checkout."
  echo "       See README.md for setup steps."
  exit 1
fi

# Ensure the ace-eval submodule is checked out — ace-eval ships the CLI we use.
git submodule update --init --recursive

# tau2-bench's official 30 train / 20 test airline split is applied
# automatically when ace-eval finds it via the tau2 registry.
uv run --directory ace-eval ace-eval e2e \
  --benchmark tau-bench-airline \
  --agent-model "$AGENT_MODEL" \
  --reflector-model "$REFLECTOR_MODEL" \
  --skill-manager-model "$REFLECTOR_MODEL" \
  --reflector-type rr \
  --user-model "$USER_MODEL" \
  --max-num-steps 200 \
  --seed 42 \
  --num-trials 1 \
  --train-epochs 1 \
  --output-dir "$OUTPUT_DIR" \
  --verbose
