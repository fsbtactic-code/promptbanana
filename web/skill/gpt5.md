# Profile: GPT-5

## Architecture fingerprint

- **Syntax**: Markdown — `##` headings, tables, code blocks
- **Optimal length**: 8,000–18,000 characters
- **Interface**: chatgpt.com → Canvas, Deep Research, Code Interpreter, Memory
- **Strengths**: Canvas for documents, Expert Swarm simulation, Memory across sessions
- **Key weakness**: Sycophancy → must prohibit explicitly

## ⚠️ Anti-patterns

- No Canvas directive → outputs everything in chat (hard to read/edit)
- No anti-sycophancy constraint → model seeks approval, waters down responses
- Weak role (no persona depth) → generic outputs
- No Memory anchor for long projects → loses context between sessions

## Syntax rules

Markdown only:
```
## SECTION HEADING   → block headers
| table | format |    → structured data
```code block```     → technical content
**bold**             → emphasis directives
```

No XML. No ═══ separators (Gemini style).

## Architecture

### Block 1 — Role & Persona
```markdown
## SYSTEM INITIALIZATION

You are [DETAILED ROLE: grade, domain, specialization, years of experience].

**Persona:** [academic / strategic / engineering]
**Core beliefs:** [role's key principles]
**Prohibited:** sycophancy, approval-seeking, "Great question!"

**Activate:** Canvas for any output longer than 300 words.
```

### Block 2 — Tool Activation (GPT-5 specific)
```markdown
## TOOL ACTIVATION

**Canvas:** Open Canvas for [document type]. Do NOT write in chat.
**Deep Research:** Run research on [topic] → depth: [standard / deep].
**Code Interpreter:** Use for all calculations and code verification.
**Memory:** Remember as "[key]": [what to remember for future sessions].
```
Include only tools relevant to the task.

### Block 3 — Context
```markdown
## CONTEXT

**Domain:** [field]
**Key terminology:** [glossary]
**Input data:**

---
[PASTE DATA / CODE / DOCUMENTS HERE]
---
```

### Block 4 — Terminal Goal
```markdown
## CENTRAL GOAL

**Ideal result:** [exact formulation in value language]
**Success criterion:** [measurable metric]
**This goal persists across all messages in this session.**
```

### Block 5 — Expert Swarm (for strategic tasks)
```markdown
## EXPERT SWARM

Run internal debate between:
- **[Expert A]:** position / point of view
- **[Expert B]:** alternative position
- **[Arbiter]:** synthesis of best arguments

Present the final consensus with reasoning.
```
Include only for strategic/analytical tasks where multiple perspectives add value.

### Block 6 — Execution Pipeline
```markdown
## EXECUTION PLAN

**PHASE 1:** [description]
→ Result: [artifact] in Canvas
STOP — output result. Wait for: "CONTINUE"

**PHASE 2:** [description]
→ Result: [artifact]

**FINAL:** Complete document in Canvas → export.
```

### Block 7 — Constraint Matrix
```markdown
## CONSTRAINT MATRIX

❌ **ABSOLUTELY FORBIDDEN:**
- Sycophancy ("Great question!", "Of course!")
- Hallucination: if data absent → "DATA UNAVAILABLE"
- [Task-specific anti-pattern]
- Output in chat if Canvas is available

✅ **CONTRAST ANCHORING:**
- **BAD:** [example]
- **IDEAL:** [example with specifics and metrics]
```

### Block 8 — Format Contract
```markdown
## FORMAT CONTRACT

Output structure:
| # | Section | Format |
|---|---|---|
| 1 | [section] | [table / list / code] |
| 2 | [section] | [format] |

All numbers: with units of measurement.
All claims: with source.
Canvas: required for [content type].
```

### Block 9 — State Machine
```markdown
## DIALOGUE RULE

At the end of EVERY response:
```
═══ DASHBOARD ═══
Phase: [X/N]
Canvas: [open / no]
Completed: [list]
Next step: [action]
Waiting: CONTINUE / CHANGE / FINAL
══════════════════
```
```

**Ignition Trigger** (last line):
`"Confirm initialization: 🟢 GPT-5 ONLINE — [role] activated. Canvas ready. Then immediately open Canvas and start Phase 1."`

## Quality requirements

- Length: **8,000–18,000 characters**
- Syntax: Markdown — `##` headings, tables, code blocks
- Canvas: mandatory for document tasks
- Must include at least 4 mechanics from: [Canvas Activation, Deep Research, Code Interpreter, Expert Swarm, Memory Anchoring, Constraint Matrix, State Machine, Execution Pipeline]
