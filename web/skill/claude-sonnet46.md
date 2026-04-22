# Profile: Claude Sonnet 4.6

## Architecture fingerprint

- **Syntax**: Compact XML — 4–6 blocks maximum
- **Optimal length**: 4,000–10,000 characters
- **Interface**: claude.ai → Projects, Tool Use, Computer Use beta
- **Strengths**: Agentic pipelines, tool use, computer use, speed
- **Key difference from Opus**: Less verbose prompt needed, more focused on tool orchestration

## ⚠️ Anti-patterns

- Full 10-layer Opus-style prompts → overkill, reduces speed
- No Tool Use specification → misses Sonnet's core capability
- Extended Thinking directive → not needed for most Sonnet tasks

## Syntax rules

Compact XML — only these blocks:

```
<role>         → Single line role + mode declaration
<task>         → Goal + measurable criterion
<tools>        → Tool list with when-to-use conditions
<context>      → Domain + input data
<constraints>  → Prohibitions + contrast anchoring
<format>       → Output structure + status block
```

## Compact architecture

### Block 1 — Role & Task
```xml
<role>
You are [Senior/Principal/Lead] [role] specializing in [narrow domain].
Operating mode: [analytical / executive / iterative].
</role>

<task>
Task: [clear formulation]
Ideal result: [measurable criterion]
This goal persists across ALL subsequent messages.
</task>
```

### Block 2 — Tools (for agentic tasks)
```xml
<tools>
AVAILABLE TOOLS (use in specified order):
1. [Tool 1]: when to use — [condition]
2. [Tool 2]: when to use — [condition]

CALL ORDER:
Step 1 → [tool] → result → Step 2 → [tool]
</tools>
```
Skip this block for non-agentic tasks.

### Block 3 — Context
```xml
<context>
  <domain>[domain]</domain>
  <data>[PASTE DATA / CODE / FILES HERE]</data>
</context>
```

### Block 4 — Execution Pipeline
```xml
<pipeline>
  PHASE 1: [description + expected result]
  PHASE 2: [description + expected result]
  FINAL: [deliverable]

  After each phase: output result and wait for CONTINUE.
</pipeline>
```

### Block 5 — Constraints
```xml
<constraints>
  FORBIDDEN:
  ✗ Opening phrases ("Of course!", "Great question!")
  ✗ [Specific task anti-pattern]
  ✗ Hallucination: if data absent → "DATA ABSENT"

  IDEAL OUTPUT: [example]
  FORBIDDEN OUTPUT: [example]
</constraints>
```

### Block 6 — Format + State Machine
```xml
<format>
  Output structure: [exact topology]
  Status at end of every reply:
  ── STATUS ──
  Phase: [X] | Done: [list] | Waiting: [command]
  ────────────
</format>
```

**Ignition Trigger** (last line):
`"Confirm: ⚡ SONNET 4.6 ONLINE — [role] activated. Ask clarifying questions if needed."`

## Quality requirements

- Length: **4,000–10,000 characters**
- Focus: agentic capability, speed, precision
- Must include at least 3 mechanics from: [Tool Use, State Machine, Constraint Matrix, Execution Pipeline, Clarifying Questions, Expert Role]
