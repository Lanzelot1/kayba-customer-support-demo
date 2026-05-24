# Self-Improving Customer-Support Agent: One-Pager

> **From [Kayba](https://kayba.ai): open-source learning layer for AI agents.**
>
> Demo repo: https://github.com/Lanzelot1/kayba-customer-support-demo  
> Framework: https://github.com/kayba-ai/agentic-context-engine  
> Book a call: https://zcal.co/kayba/30min

We built a learning layer (the **agentic-context-engine**) that observes
a customer-support agent handling recorded conversations, identifies
where it's getting things wrong, and writes a short rulebook the agent
reads on the next run. No fine-tuning, no access to your stack. Just
the conversations and your policy doc.

## What we tested it on

A public customer-service benchmark for an airline call-center: 50
multi-turn conversations between an AI agent and a simulated customer,
with real tool calls (look up customer, find reservation, modify
booking, process refund, transfer to human). Each conversation is
graded pass/fail by an external test suite. The setup mirrors a real
call-center workflow: identify the customer, look up records, apply
policy, take an action, escalate when needed.

## Results

15 rules learned from 30 training conversations, then injected into the
agent's instructions at run time. Two views of the same benchmark:

On a single run across the 20 held-out tasks, the agent passed
**7 of 20 (35%)** before the rulebook and **11 of 20 (55%)** after.

Each task was sampled 4 times independently (temperature > 0) to separate consistent improvement from sampling noise.

| Consistency metric | Baseline | With rulebook | Relative |
|---|---|---|---|
| pass on 1 attempt | 41.2% | 52.5% | +27% |
| pass on 2 attempts | 28.3% | 44.2% | +56% |
| pass on 3 attempts | 22.5% | 41.2% | +83% |
| **pass on all 4 attempts** | **20.0%** | **40.0%** | **2×** |

The headline number is the bottom row: **the rulebook doubles the rate
at which the agent gets the task right on every single one of four
independent attempts.** "pass on k attempts" means succeeding on all k
independent tries at the same task; the stricter the consistency bar,
the larger the lift.

(Claude Haiku 4.5 on tau-bench airline; 15 learned strategies;
leaderboard configuration.)

## What the rulebook looks like

Three of the 15 rules, paraphrased:

- *Basic Economy refunds:* always issue a travel certificate, not cash,
  unless one of four specific exceptions applies (24-hour window,
  airline-cancelled, business class, covered insurance), and disclose
  the policy before doing it.
- *Delay-compensation claims:* check the actual flight status with the
  tool before processing the request, not just the customer's word.
- *Transfer to human:* include a structured summary (user ID,
  reservation ID, reason, policy status, membership tier, insurance).

Every rule cites the recorded conversation that motivated it, so your
team can keep, edit, or drop each one.

## How it works

Three steps, run automatically:

1. **Read the failures.** A model reads every recorded conversation
   and pinpoints what went wrong, including in conversations the
   agent technically passed but got lucky on.
2. **Write the rules.** A second model turns those failure patterns
   into 15 short rules in plain English.
3. **Use the rules.** The agent runs again with the rules added to
   its instructions. That's where the lift comes from.

The simulated customer in the benchmark is a separate AI with a
hidden script: a backstory, goal, and constraints the agent never
sees. The agent only sees the airline's policy and its tools. So
when the agent improves, it's getting better at applying the policy
itself, not memorising answers from the test.

## Next steps

The same approach transfers to any agent with recorded conversations
and a policy doc, not just customer support. Everything's also in the
demo repo above. Happy to jump on a call to walk through your use case.

Best,  
Sven & Filip, Kayba
