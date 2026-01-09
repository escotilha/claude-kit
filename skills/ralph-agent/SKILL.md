---
name: ralph-agent
description: "Autonomous AI coding agent that breaks features into small user stories and implements them iteratively. Use when asked to build a feature autonomously, create a PRD, convert a PRD to JSON, or run an autonomous coding loop. Triggers on: ralph, autonomous agent, build this feature, create prd, convert prd to json, implement autonomously, autonomous loop, autonomous coding, user stories."
---

# Ralph Wiggum Autonomous Agent

An autonomous coding workflow that breaks features into small, testable user stories and implements them one at a time in a loop.

## Core Concept

Each iteration spawns a **fresh context**. Memory between iterations is:
- Git history (commits)
- `progress.txt` (learnings)
- `prd.json` (story status)

## Workflow Overview

```
Feature Idea → PRD → prd.json → Autonomous Loop → COMPLETE
```

**Three Phases:**
1. **PRD Generation** — Create requirements document with user stories
2. **JSON Conversion** — Convert PRD to `prd.json` task list
3. **Autonomous Loop** — Implement one story per iteration until done

---

## Phase 1: PRD Generation

When given a feature idea, create a PRD first. Do NOT start coding.

### Step 1: Ask Clarifying Questions

Ask 3-5 essential questions with lettered options for quick responses:

```
1. What is the primary goal?
   A. Improve onboarding  B. Increase retention  C. Reduce support  D. Other

2. Who is the target user?
   A. New users  B. Existing users  C. All users  D. Admins

3. What is the scope?
   A. MVP  B. Full-featured  C. Backend only  D. Frontend only
```

User can respond: "1A, 2C, 3B"

### Step 2: Generate PRD

Create markdown PRD with these sections:

| Section | Content |
|---------|---------|
| **Introduction** | Brief feature description |
| **Goals** | Specific, measurable objectives |
| **User Stories** | Small, independent stories (see format below) |
| **Non-Goals** | What this will NOT include |
| **Success Metrics** | How to measure success |

**User Story Format:**
```md
### US-001: [Title]
**Description:** As a [user], I want [feature] so that [benefit].

**Acceptance Criteria:**
- [ ] Specific verifiable criterion
- [ ] Another criterion
- [ ] Typecheck passes
- [ ] [UI only] Verify in browser
```

Save to: `tasks/prd-[feature-name].md`

---

## Phase 2: PRD to JSON Conversion

Convert approved PRD to `prd.json`:

```json
{
  "project": "[Project Name]",
  "branchName": "ralph/[feature-name]",
  "description": "[Feature description]",
  "userStories": [
    {
      "id": "US-001",
      "title": "[Title]",
      "description": "As a [user], I want [feature] so that [benefit]",
      "acceptanceCriteria": ["Criterion 1", "Typecheck passes"],
      "priority": 1,
      "passes": false,
      "notes": ""
    }
  ]
}
```

### Critical Rules

**Story Size — ONE iteration max:**
| ✅ Right-sized | ❌ Too big (split these) |
|----------------|-------------------------|
| Add a database column | Build entire dashboard |
| Add UI component to existing page | Add authentication |
| Update server action with new logic | Refactor the API |
| Add filter dropdown | Complete feature end-to-end |

**Rule:** If you can't describe the change in 2-3 sentences, it's too big.

**Story Ordering — Dependencies first:**
1. Schema/database (migrations)
2. Server actions/backend
3. UI components using backend
4. Dashboard/summary views

**Acceptance Criteria — Must be verifiable:**
| ✅ Good | ❌ Bad |
|---------|--------|
| Add `status` column with default 'pending' | Works correctly |
| Filter has options: All, Active, Completed | Good UX |
| Clicking delete shows confirmation | Handles edge cases |

**Always include:** `"Typecheck passes"` (and `"Tests pass"` for testable logic)

---

## Phase 3: Autonomous Loop

Process **one story per turn**:

### Loop Steps

1. **Announce Task**
   > "Now starting US-001: Add priority field to database."

2. **Implement Code**
   Write code for ONLY that user story.

3. **Request Verification**
   > "I've implemented US-001. Please run tests and confirm if they pass."

4. **Await Confirmation**
   - Tests pass → Continue
   - Tests fail → Fix and retry step 3

5. **Update prd.json**
   Set `"passes": true` for completed story.

6. **Log Progress**
   ```
   ## Log: US-001
   - **Implementation**: Added `priority` column with default `medium`
   - **Learnings**: Migration library requires explicit null handling
   ```

7. **Check Completion**
   - All stories `passes: true` → Output `COMPLETE` and stop
   - Stories remain → Go to step 1 for next priority story

---

## Key Files

| File | Purpose |
|------|---------|
| `prd.json` | Task list with `passes` status |
| `progress.txt` | Append-only learnings |
| `AGENTS.md` | Long-term patterns across repo |

### progress.txt Format
```
## [Date] - [Story ID]
- What was implemented
- Files changed
- **Learnings:** Patterns, gotchas, useful context
---
```

### AGENTS.md Content
- API patterns/conventions
- Non-obvious requirements
- File dependencies
- Testing approaches

---

## Archiving Previous Runs

Before writing new `prd.json`, if existing one has different `branchName`:
1. Create: `archive/YYYY-MM-DD-feature-name/`
2. Copy: `prd.json` and `progress.txt`
3. Reset: `progress.txt` with fresh header

---

## Quick Reference

See [references/examples.md](references/examples.md) for story splitting examples and common patterns.
