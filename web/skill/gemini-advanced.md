# Profile: Gemini 3.1 Advanced

## Architecture fingerprint

- **Syntax**: Structured text + ═══ separators — **NO XML**
- **Optimal length**: 8,000–15,000 characters
- **Interface**: gemini.google.com/advanced → Deep Research, Workspace
- **Strengths**: 20M token context, Deep Research (multi-step web), YouTube analysis, Workspace export
- **Key difference from Pro**: Deep Research parameters + Workspace integration + progressive disclosure

## ⚠️ Anti-patterns

- Same as Pro (no XML)
- Weak Deep Research parameters → vague research output
- Missing Workspace Export directive → user can't export results

## Additional capabilities (vs Pro)

### Deep Research Activation
```
DEEP RESEARCH:
Topic: [exact research topic]
Depth: [surface / standard / deep]
Source types: [academic / news / industry / all]
Time range: [last N years]
Exclude: [unwanted source types]
Output format: [structured report / table / theses]
```

### Multi-document Synthesis
```
SYNTHESIS TASK:
Documents: [N files uploaded]
Primary source: [main document]
Secondary sources: [supporting documents]
Synthesis goal: [what to extract across all sources]
```

### Workspace Export
```
EXPORT:
After final phase, export to: [Google Docs / Google Sheets / PDF]
Document title: [title template]
Structure: [heading hierarchy]
```

### YouTube / Video Analysis
```
VIDEO ANALYSIS:
URL: [YouTube link]
Analyze: EVERY frame relevant to [focus area]
Extract: [timestamps / quotes / visual elements]
```

## Full architecture (includes all Pro layers + Advanced additions)

### Block 1 — System Override
```
═══════════════════════════════════════════════════
SYSTEM OVERRIDE. PRIORITY: ABSOLUTE.
═══════════════════════════════════════════════════
You initialize as [ROLE + GRADE + DOMAIN].
Mode: Advanced Research / Analysis Mode.
Prohibited: surface conclusions, hallucinations, unsourced generalizations.
═══════════════════════════════════════════════════
```

### Block 2 — Advanced Capability Activation
```
CAPABILITY ACTIVATION:

[Include relevant capabilities from above: Deep Research, Multi-doc Synthesis, Video Analysis, Workspace Export]
```

### Block 3 — Context Anchoring (same as Pro — CRITICAL)
```
CONTEXT ANCHOR — READ FIRST:
[Same structure as gemini-pro.md Block 3]
```

### Block 4 — Terminal Goal
```
CENTRAL GOAL (unchanged for entire session):
Result: [exact formulation]
Quality criterion: [measurable metric]
Delivery format: [document type / structure]
```

### Block 5 — Research & Analysis Protocol
```
RESEARCH PROTOCOL:

STAGE 0: Read / index ALL input data.
  Create list: 1) key facts, 2) gaps, 3) contradictions

STAGE 1: [Analytical frame 1]
  → Sources: [data type for this stage]

STAGE 2: [Analytical frame 2]
  → Synthesis with Stage 1 results

STAGE 3: Verification — check all conclusions for contradictions.

ONLY after Stage 3 — form the final answer.
```

### Block 6 — Execution Pipeline with Delivery
```
DELIVERY PLAN:

PHASE 1: [Primary analysis]
→ Result: [structure / outline]
STOP. Show. Wait: CONTINUE

PHASE 2: [In-depth analysis / calculations]
→ Result: [detailed data]
STOP. Show. Wait: CONTINUE

FINAL: Complete document → export to [Google Docs / Sheets / PDF]
```

### Block 7 — Constraint Matrix
```
[Same structure as gemini-pro.md Block 7]
```

### Block 8 — Format Contract
```
FORMAT CONTRACT:
[1] Executive Summary: 3–5 key conclusions
[2] Main analysis: [structure]
[3] Data: tables with units of measurement
[4] Sources: numbered list with URLs/pages
[5] Next steps: specific recommendations

Prohibited: preambles, meta-comments, undefined terms
```

### Block 9 — State Machine
```
At the end of EVERY response:
━━━━━━━━━━━━━━━━━━━━━━━━
Phase: [X] | Sources: [N] | Data: [volume]
Completed: [list]
Next step: [action]
Waiting: CONTINUE / DEEPEN / FINAL
━━━━━━━━━━━━━━━━━━━━━━━━
```

**Ignition Trigger** (last line):
`"Confirm: 🟣 GEMINI ADVANCED ONLINE — [role] activated. Then immediately execute STAGE 0."`

## Quality requirements

- Length: **8,000–15,000 characters**
- Syntax: **NO XML** — structured text only
- Deep Research: maximally specific parameters
- Must include at least 4 mechanics from: [Deep Research, Context Anchoring, Multi-doc Synthesis, Workspace Export, Research Protocol, State Machine, Axiomatic Grounding]
