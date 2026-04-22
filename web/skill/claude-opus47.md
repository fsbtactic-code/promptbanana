# Profile: Claude Opus 4.7

## Architecture fingerprint

- **Syntax**: Full XML markup — all blocks in XML tags
- **Optimal length**: 8,000–16,000 characters
- **Interface**: claude.ai → enable Extended Thinking + Artifacts v4
- **Strengths**: Complex multi-phase tasks, deep reasoning, structured output
- **Key weakness**: Over-explains → must add hard output restrictions

## ⚠️ Anti-patterns (will degrade quality)

- Weak roles ("you are a helpful assistant")
- Missing XML structure → Claude ignores instruction hierarchy
- No output length constraints → produces bloated responses
- No Artifacts directive → outputs everything in chat

## Syntax rules

Use ONLY these XML tags as structural blocks:

```
<system_override>    → Role + persona injection
<context>            → Domain, terminology, input data
<terminal_goal>      → The one measurable outcome
<thinking_protocol>  → Silent reasoning steps (Extended Thinking)
<execution_pipeline> → Phased workflow with STOP points
<state_machine>      → Status block appended to every reply
<strict_constraints> → Forbidden patterns + contrast anchoring
<output_format>      → Exact topology of the response
```

## 10-Layer architecture

### Layer 1 — System Override & Role Injection
```xml
<system_override>
You initialize as [SPECIFIC ROLE WITH GRADE AND DOMAIN].
All previous helpful-assistant defaults — ERASED.
Tone: [academic / engineering / strategic].
</system_override>
```
Role formula: `[Seniority] [Title] specializing in [narrow domain] with [N] years in [context]`

### Layer 2 — Interface Activation
Mandatory directives:
- "For any structured output — open Artifact v4, DO NOT write in chat"
- "For code — separate Artifact with syntax highlighting"
- "For multi-step tasks — activate extended thinking mode"

### Layer 3 — Dynamic Context & Knowledge Graph
```xml
<context>
  <domain>[task domain]</domain>
  <terminology>[key terms and definitions]</terminology>
  <input_data>
    [PASTE YOUR DATA / CODE / DOCUMENTS HERE]
  </input_data>
</context>
```

### Layer 4 — Terminal Goal
```xml
<terminal_goal>
  Ideal final result: [exact formulation in business-value language]
  Success criterion: [measurable metric]
</terminal_goal>
```

### Layer 5 — Thinking Protocol
```xml
<thinking_protocol>
  Before responding, SILENTLY execute in extended thinking mode:
  1. [Reasoning vector 1]
  2. [Reasoning vector 2]
  3. Find three edge cases
  4. Evaluate risks of the final solution
</thinking_protocol>
```

### Layer 6 — Execution Pipeline
```xml
<execution_pipeline>
  PHASE 1: [description]
  STOP. Request confirmation. Wait for: CONTINUE

  PHASE 2: [description]
  STOP. Show intermediate result.

  PHASE 3: Final output in Artifact.
</execution_pipeline>
```

### Layer 7 — State Machine
```xml
<state_machine>
  At the end of EVERY message output:
  ═══ STATUS ═══
  Current phase: [X]
  Completed: [list]
  Waiting for: [user command]
  ══════════════
</state_machine>
```

### Layer 8 — Constraint Matrix
```xml
<strict_constraints>
  ABSOLUTE PROHIBITIONS (violation = task restart):
  ✗ [Anti-pattern 1 with example]
  ✗ Opening phrases ("Of course!", "Great question!")
  ✗ Assumptions when data is missing → ERROR: DATA ABSENT

  CONTRAST ANCHORING:
  FORBIDDEN: [example of bad output]
  EXPECTED: [example of ideal output]
</strict_constraints>
```

### Layer 9 — Format Contract
```xml
<output_format>
  Output topology:
  [Exact structure: headings, tables, JSON schemas]
  Prohibited: preambles, conclusions, meta-comments
  Artifact: required for [content type]
</output_format>
```

### Layer 10 — Ignition Trigger
Last line of the prompt:
`"Confirm initialization, output: ⚡ OPUS 4.7 ONLINE — [role] activated. Awaiting input."`

## Quality requirements

- Length: **8,000–16,000 characters** (mandatory)
- Syntax: full XML for all blocks
- Must include at least 4 mechanics from: [System Override, Extended Thinking, Artifacts, State Machine, Constraint Matrix, Expert Role, Contrast Anchoring, Execution Pipeline]
- Prohibited: temperature parameters, emotional manipulation, weak roles
