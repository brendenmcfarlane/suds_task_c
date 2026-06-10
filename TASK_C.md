# Task: Simple AFlow-Style Topology Search for GSM8K

## Goal

Implement a small **from-scratch** multi-agent topology optimizer for math problems, inspired by **AFlow**. Do **not** use the AFlow GitHub code.

We want to test whether changing the agent graph improves accuracy and how the answer trajectory changes when an agent or edge is added or removed.

## Dataset

Use a very small GSM8K subset to control API cost:

- 5 problems for topology search
- 5 held-out problems for final testing

Do not rerun experiments unnecessarily. Use the same questions for all topology comparisons.

## Agents

Use simple prompt-wrapper agents:

```text
Planner
Solver
Checker
Reflector
ArithmeticChecker
```

Start with this base topology:

```text
Planner -> Solver -> Checker
```

Represent each topology as nodes and directed edges:

```json
{
  "nodes": ["Planner", "Solver", "Checker"],
  "edges": [["Planner", "Solver"], ["Solver", "Checker"]]
}
```

## Topology Changes

Try small acyclic graph changes only:

1. Add one agent, such as `ArithmeticChecker` or `Reflector`.
2. Remove one optional agent.
3. Add one edge.
4. Remove one edge.

Keep each topology small. The goal is interpretability, not a large search.

## Search Loop

Implement a minimal AFlow-style loop:

```text
for iteration in 1..5:
    propose 2 mutated topologies
    run each topology on the 5 dev problems
    score = accuracy - 0.02 * average_agent_calls
    keep the best topology
```

Then run only the best 2 or 3 topologies on the 5 held-out test problems.

## Trajectory Inspection

Do **not** save full traces for every topology/problem. During search, only keep the score needed for comparison.

After the search, pick 2 or 3 representative examples and record only those trajectories in the report:

```json
{
  "topology": "Planner -> Solver -> ArithmeticChecker -> Checker",
  "question": "...",
  "steps": [
    {"agent": "Planner", "output": "..."},
    {"agent": "Solver", "output": "..."},
    {"agent": "ArithmeticChecker", "output": "..."},
    {"agent": "Checker", "output": "..."}
  ],
  "final_answer": "...",
  "correct": true,
  "agent_calls": 4
}
```

## Simple Viewer

Make a very small Streamlit viewer only for the selected representative examples, not for all runs.

The viewer should show:

1. The topology graph.
2. The step-by-step agent messages.
3. A before/after comparison for one topology mutation.
4. Accuracy and average agent calls for the tested topologies.

The purpose is to visually inspect how adding or removing an agent/edge changes the reasoning path.

## Final Report

Write a short report, maximum 1 page:

1. Which topologies were tested?
2. Which topology worked best on dev and test?
3. Did `ArithmeticChecker` or `Reflector` help?
4. Show 2 short trajectory examples where topology changed the reasoning.
5. Show 1 short example where a topology made the result worse.
6. Include 1 or 2 screenshots from the viewer.
