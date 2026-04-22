# Profile: DeepSeek R3

## Architecture fingerprint

- **Syntax**: Plain text — ultra-minimal
- **Optimal length**: 1,500–5,000 characters (shorter = better than o4)
- **Interface**: chat.deepseek.com → enable "DeepThink (R1)" mode
- **Strengths**: Algorithms, math, code — often beats o4 on competitive programming
- **Core principle**: GRPO/RL reasoning — shows `<think>...</think>` block automatically

## ⚠️ CRITICAL RULES — stricter than o4

DeepSeek R3 is a **GRPO reasoning model**. The `<think>` block is visible in the interface — it's normal.

**ABSOLUTELY FORBIDDEN:**
- Any chain-of-thought instructions
- "Think step by step" / "Reason through this"
- Reasoning examples in the prompt
- Multi-step meta-instructions
- Verbose constraint explanations

**DeepSeek degrades MORE than o4 from prompt overload.**

## What WORKS for DeepSeek

Only 4 sections — use R-Rules instead of CoT:

### R-Rules (key differentiator)
Instead of explaining HOW to think, write explicit rules:
```
R1: [Rule 1]
R2: [Rule 2]
R3: [Boundary case]
R4: If data absent → NULL
R5: [Verification criterion]
```

## The 4-section template

### Section 1 — Role (minimum)
```
[Role] specializing in [narrow domain]. Working in maximum accuracy mode.
```

### Section 2 — Task
```
TASK: [extremely precise formulation]

Input data:
[PASTE DATA / CODE / PROBLEM CONDITIONS HERE]

Ideal result: [measurable criterion]
```

### Section 3 — R-Rules (instead of CoT)
```
RULES (R-RULES):
R1: [Constraint 1]
R2: [Constraint 2]
R3: [Boundary case]
R4: If data absent → output NULL
R5: [Verification criterion]
```

### Section 4 — Output Format
```
OUTPUT FORMAT:
[JSON schema / table / list — exact structure]
Result only. No explanations of reasoning process.
```

## Key differences from o4

| | o4 | DeepSeek R3 |
|---|---|---|
| Max length | 6,000 chars | 5,000 chars |
| Best for | General reasoning | Competitive algorithms |
| R-Rules | Optional | Preferred over constraints |
| Ignition trigger | Skip | Skip |
| Think block | Hidden | Visible in UI |

## What NOT to add

Same prohibitions as o4, plus:
- Do NOT add verification triggers
- Do NOT add status blocks
- Do NOT add phased workflows

## Quality requirements

- Length: **1,500–5,000 characters** (critical maximum)
- Only 4 sections: Role + Task + R-Rules + Format
- R-Rules over narrative constraints
- No CoT, no reasoning instructions, no meta-layers
- If in doubt — make it shorter
