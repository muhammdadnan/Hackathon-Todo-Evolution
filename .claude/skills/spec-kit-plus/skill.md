# SpecKitPlus Auto-Workflow Skill

---
name: spec-kit-plus
description: "Production-grade Spec-Driven Development (SDD) skill with Context7 integration, autonomous decision-making, and complete workflow from Constitution to Implementation."
version: "2.0.0"
---

## Description
Automates the complete Spec-Driven Development (SDD) workflow from specification to implementation. This skill intelligently detects and utilizes relevant skills from `.claude/skills` based on project requirements, uses Context7 for official documentation access, and maintains human control through checkpoints.

## Usage
```
/spec-auto "feature description"
```

---

## SDD Workflow Phases

| Phase | Command | Output |
|-------|---------|--------|
| 1. Constitution | `/sp.constitution` | `constitution.md` |
| 2. Specification | `/sp.specify` | `spec.md` |
| 3. Clarification | `/sp.clarify` | Updated spec |
| 4. Planning | `/sp.plan` | `plan.md` + ADRs |
| 5. Tasks | `/sp.tasks` | `tasks.md` |
| 6. Implementation | `/sp.implement` | Working code |

---

## Production-Grade Features

### 1. Context7 Integration
When creating skills or researching frameworks:
```
Library needed → Context7 MCP → Official Docs → Accurate Implementation
```
- `resolve-library-id` → Get library identifier
- `get-library-docs` → Fetch live, official documentation
- Ensures 100% accurate and up-to-date information

### 2. Auto-Skill Selection
- Scans `.claude/skills` for available skills
- Matches project requirements with appropriate skills:
  - Documentation skills for specs/plans
  - Code generation skills for implementation
  - Testing skills for validation
  - Integration skills for API contracts

### 3. Self-Decision Framework

| Confidence | Action | Examples |
|------------|--------|----------|
| **HIGH (>85%)** | Auto-proceed | Skill selection, phase transitions |
| **MEDIUM (50-85%)** | Proceed + Log | Implementation choices |
| **LOW (<50%)** | Ask User | Architecture, breaking changes |

### 4. Checkpoint Pattern (Human Control)
After every phase completion:
```
Agent: "✅ Phase [X] complete: [output]"
Human: Reviews → "APPROVE" → Git commit → "next"
```
Never proceed without human checkpoint approval.

### 5. Error Recovery System
```
On Error: Log → Classify → Self-Recover OR Escalate
Recovery: Retry alternative → Fallback skill → User guidance
```

---

## Advanced Execution Protocols

### 1. Task Atomicity & Lineage
**Atomicity Rules:**
- **Duration**: 15-30 minutes per task
- **Scope**: Single acceptance criterion
- **Dependencies**: Explicitly defined (blocking relationships)

**Lineage Tracing:**
- Every Task must trace back to a Plan Item
- Every Plan Item must trace back to a Spec Requirement
- Every Requirement must trace back to a Constitution Principle

### 2. Skill Fallback Chain
If a primary skill fails or is missing:
```
Primary Skill → Alternative Skill → Manual (Ask User)
```
**Mappings:**
- `doc-coauthoring` → `docx` → `internal-comms`
- `fetch-library-docs` → Context7 MCP → `browsing-with-playwright`
- `skill-creator-pro` → `skill-creator` → Manual

### 3. Iteration Loop Pattern
When output fails validation at any checkpoint:
1. **Identify Gap**: Compare output vs Spec Success Criteria
2. **Refine**: "Task X missed criterion Y. Adjust and retry."
3. **Re-execute**: Run task again with specific feedback
4. **Validate**: Re-check against spec (Do not accept "close enough")

### 4. SMART Specification Criteria
All specifications must be:
- **S**pecific: Unambiguous detail
- **M**easurable: Quantifiable success metrics
- **A**chievable: Technical feasibility confirmed
- **R**elevant: Aligns with project goals
- **T**ime-bound: Estimated duration defined

---

## Validation Checklists

### Per-Phase Validation
- **Constitution**: Quality standards enforceable?
- **Specification**: Success criteria testable?
- **Clarification**: Anything still ambiguous?
- **Plan**: Approach makes sense?
- **Tasks**: Can each be done in 30 minutes?
- **Implementation**: Meets spec exactly?

---

## Core Guarantees (Product Promise)

### PHR Recording
- Record every user input verbatim in `history/prompts/`
- Routing:
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`

### ADR Suggestions
- When architecturally significant decision detected:
- Suggest: "📋 Architectural decision detected: `<brief>`. Document? Run `/sp.adr <title>`"
- Never auto-create (user consent required)

### Action Logging
- All actions logged to `history/actions/`
- Format: `[timestamp] [action_type] [decision] [confidence] [outcome]`

---

## Project Auto-Discovery

On project load, automatically detect:

| File | Detection |
|------|-----------|
| `package.json` | Node.js |
| `requirements.txt` | Python |
| `Cargo.toml` | Rust |
| `.claude/` | Claude project |
| `specs/` | Existing SDD |

Select appropriate skills based on detected tech stack.

---

## Output Structure

```
specs/<feature-name>/
├── spec.md          # Feature specification
├── plan.md          # Implementation plan
└── tasks.md         # Atomic tasks

history/
├── prompts/         # PHR records
├── adr/             # Architectural decisions
└── actions/         # Action logs
```

---

## Requirements
- `.specify/memory/constitution.md` must exist
- Feature description as input
- Scans `.claude/skills` for available skills
- Human oversight via checkpoints
- **Brownfield Projects**: Use `init --here` with backup strategy (see `references/brownfield-adoption.md`)
- **Intelligence Acceleration**: Track skill reuse to measure time savings (refer to `Reference/how-spec-kit-plus-was-used.md`)

---

## Reference
See `Reference/how-spec-kit-plus-was-used.md` for real-world example.