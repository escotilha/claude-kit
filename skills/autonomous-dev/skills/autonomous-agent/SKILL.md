---
name: autonomous-agent
version: "2.0.0"
description: "Autonomous coding agent that breaks features into small user stories and implements them iteratively with fresh context per iteration. Supports parallel execution and smart delegation. Use when asked to: build a feature autonomously, create a PRD, implement a feature from scratch, run an autonomous coding loop, break down a feature into user stories. Triggers on: autonomous agent, build this autonomously, autonomous mode, implement this feature, create prd, prd to json, user stories, iterative implementation, ralph."
author: "Nuvini"
last-updated: "2025-01-28"
user-invocable: true
context: fork
---

# Autonomous Coding Agent

## Quick Start: Check Status First

```bash
if [ -f prd.json ]; then
  jq -r '(.userStories | map(select(.passes)) | length) as $done | (.userStories | length) as $total |
    if $done == $total then "COMPLETE" else "IN_PROGRESS: \($done)/\($total)" end' prd.json
else
  echo "NO_PRD"
fi
```

**If COMPLETE:** Report completion, offer to create PR or start new feature.
**If IN_PROGRESS:** Jump to [Phase 3](#phase-3-autonomous-loop).
**If NO_PRD:** Start [Phase 1](#phase-1-prd-generation).

---

## Architecture

**State persists in files:**
- `prd.json` - Task list with status
- `progress.md` - Implementation learnings
- `AGENTS.md` - Repository patterns
- Memory MCP - Cross-project learnings

**Each iteration is stateless** - read files to restore context.

**Execution Modes:**
| Mode | When | Speedup |
|------|------|---------|
| Sequential | Default | 1x |
| Parallel | `delegation.parallel.enabled: true` | 2-3x |
| Swarm | `swarm.enabled: true`, 10+ stories | 3-5x |

---

## Phase 1: PRD Generation

**Goal:** Create PRD from feature idea.

### 1.1 Load Preferences
```
mcp__memory__search_nodes({ query: "preference" })
mcp__memory__search_nodes({ query: "pattern" })
```

### 1.2 Codebase Discovery
- Detect stack: `package.json`, `requirements.txt`, etc.
- Check `AGENTS.md` for existing patterns
- Query memory for stack-specific insights

### 1.3 Clarifying Questions
Ask 3-5 questions with lettered options:
```
I'll help you build [feature]. Quick questions:

1. Primary goal?
   A. [Goal 1]  B. [Goal 2]  C. Other

2. Scope?
   A. MVP  B. Full-featured  C. Backend only

Reply: "1A, 2B" or type answers
```

### 1.4 Generate PRD
Create `tasks/prd-[name].md`:
```markdown
# PRD: [Feature Name]

## Overview
Brief description.

## User Stories

### US-001: [Title]
**Description:** As a [user], I want [feature] so that [benefit].
**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Typecheck passes
```

**Complexity scoring (1-10):**
| Score | Description |
|-------|-------------|
| 1-3 | Simple, 1 file |
| 4-6 | Moderate, 2-4 files |
| 7-8 | Complex, multiple systems |
| 9-10 | Split it |

### 1.5 Get Approval
```
PRD created: tasks/prd-[name].md
[N] stories, total complexity: [X]

Reply:
- "approved" - Begin implementation
- "edit US-X" - Modify story
- "expand US-X" - Split complex story
```

---

## Phase 2: JSON Conversion

**Goal:** Convert PRD to `prd.json`.

### 2.1 Create Branch
```bash
git checkout -b feature/[name]
```

### 2.2 Generate prd.json
```json
{
  "project": "[Name]",
  "branchName": "feature/[name]",
  "createdAt": "2024-01-15T10:00:00Z",
  "verification": {
    "typecheck": "npm run typecheck",
    "test": "npm run test"
  },
  "delegation": {
    "enabled": false,
    "fallbackToDirect": true
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "[Title]",
      "description": "As a [user]...",
      "acceptanceCriteria": ["Criterion 1", "Typecheck passes"],
      "priority": 1,
      "complexity": 4,
      "dependsOn": [],
      "status": "pending",
      "passes": false,
      "attempts": 0
    }
  ]
}
```

**Status values:** `pending` | `blocked` | `in_progress` | `completed` | `skipped` | `expanded`

### 2.3 Initialize Progress
Create `progress.md`:
```markdown
# Progress: [Feature]
Branch: `feature/[name]`
Started: [Date]
---
```

---

## Phase 3: Autonomous Loop

**Goal:** Implement stories one at a time until complete.

### 3.0 Load Context
```bash
cat prd.json
cat AGENTS.md 2>/dev/null
cat progress-summary.md 2>/dev/null || head -100 progress.md
```

Query memory:
```
mcp__memory__search_nodes({ query: "[detected-stack]" })
mcp__memory__search_nodes({ query: "mistake" })
```

### 3.1 Find Next Story

```javascript
// Update blocked status
stories.forEach(story => {
  if (story.passes || story.status === 'skipped') return;
  const blocked = story.dependsOn?.some(depId => {
    const dep = stories.find(s => s.id === depId);
    return dep && !dep.passes;
  });
  story.status = blocked ? 'blocked' : 'pending';
});

// Get next available
const next = stories
  .filter(s => !s.passes && s.status !== 'blocked' && s.status !== 'skipped')
  .sort((a, b) => a.priority - b.priority)[0];
```

If blocked stories exist:
```
⚠ 2 stories blocked:
  - US-004: waiting on US-002, US-003
Next available: US-002 (priority 2, complexity 5)
```

### 3.2 Announce Task
```
## Starting: US-XXX - [Title]

**Goal:** [Description]
**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Typecheck passes

**Approach:** [2-3 sentences]
```

### 3.3 Implement

**If `delegation.enabled: true`:**
1. Detect story type (frontend/api/database/devops/fullstack/general)
2. Select agent: `frontend-agent`, `api-agent`, `database-agent`, `devops-agent`, or `general-purpose`
3. Delegate with structured prompt (see delegation section below)
4. Parse result, fallback to direct if fails

**If `delegation.enabled: false` (default):**
1. Read existing code patterns
2. Make minimal changes for this story only
3. Don't refactor unrelated code

### 3.4 Verify
```bash
npm run typecheck
npm run test
```

### 3.5 Handle Results

**If passes:**
```javascript
story.passes = true;
story.status = 'completed';
story.completedAt = new Date().toISOString();
```

1. Update prd.json
2. Commit: `git commit -m "feat(US-XXX): [Title]"`
3. Update progress.md:
   ```markdown
   ## [Date] - US-XXX: [Title]

   **Implementation:**
   - [What was done]
   - [Files changed]

   **Learnings:**
   - [Patterns discovered]
   ---
   ```
4. Continue to next story

**If fails:**
1. Increment `attempts`
2. Log error and analysis
3. If attempts < 3: Fix and retry
4. If attempts >= 3 and complexity >= 6: Suggest `expand US-XXX`
5. If attempts >= 3: Ask user for help

### 3.6 Completion
When all stories pass:
```
===== FEATURE COMPLETE =====

Branch: feature/[name]
Stories: [N]/[N]

Options:
A. Create PR
B. Show summary
C. Start new feature
```

---

## Commands

| Command | Action |
|---------|--------|
| `status` | Show progress and next story |
| `skip` | Skip current story |
| `pause` | Stop autonomous mode |
| `expand US-X` | Split complex story into 2-4 pieces |
| `retry` | Retry current story |
| `summarize` | Regenerate progress-summary.md |

### Status Output
```
Stories: 4/8 (50%)

| ID | Title | C | Status |
|----|-------|---|--------|
| US-001 | Create page | 3 | ✓ |
| US-002 | Add form | 4 | → |
| US-003 | Add API | 5 | ○ |
| US-004 | Connect | 4 | ⊘ |

Legend: ✓ done, → active, ○ pending, ⊘ blocked

Blocked: US-004 waiting on US-002
Next: US-002 (complexity: 4)
```

### Expand Command
```
> expand US-005

Expanding: "Add OAuth login" (complexity: 8)

Proposed:
- US-005.1: OAuth callback endpoint (3)
- US-005.2: OAuth initiation (2)
- US-005.3: Login button component (3)
- US-005.4: Auth context provider (4)

Dependencies: US-005.1 → US-005.2 → US-005.3, US-005.4

Apply? (yes/no)
```

After expansion:
```json
{
  "id": "US-005",
  "status": "expanded",
  "expandedInto": ["US-005.1", "US-005.2", "US-005.3", "US-005.4"]
}
```

---

## Delegation

Enable smart delegation to specialized agents:

```json
{
  "delegation": {
    "enabled": true,
    "fallbackToDirect": true
  }
}
```

### Story Type Detection
```javascript
function detectStoryType(story) {
  const text = [story.title, story.description, ...story.acceptanceCriteria].join(' ').toLowerCase();

  if (/component|ui|page|form|button|modal|css|style/.test(text)) return 'frontend';
  if (/endpoint|route|api|rest|graphql|middleware/.test(text)) return 'api';
  if (/database|schema|migration|table|query|sql/.test(text)) return 'database';
  if (/deploy|ci\/cd|docker|kubernetes|github actions/.test(text)) return 'devops';
  if (/end.to.end|full.stack|frontend.*backend/.test(text)) return 'fullstack';
  return 'general';
}
```

### Agent Mapping
| Type | Agent |
|------|-------|
| frontend | frontend-agent |
| api | api-agent |
| database | database-agent |
| devops | devops-agent |
| fullstack | orchestrator-fullstack |
| general | general-purpose |

### Subagent Prompt Template
```markdown
# Story Implementation Task

**ONLY implement this specific story.** Do not:
- Implement other stories
- Refactor unrelated code
- Add features beyond acceptance criteria

## Story: ${story.id} - ${story.title}

${story.description}

**Acceptance Criteria:**
${story.acceptanceCriteria.map(c => `- [ ] ${c}`).join('\n')}

**Verification:** ${Object.entries(prd.verification).map(([k,v]) => `${k}: \`${v}\``).join(', ')}

## Required Output Format
RESULT: [SUCCESS|FAILURE]

Files changed:
- path/to/file.ts (new/modified)

Verification:
- Typecheck: [PASS|FAIL]
- Tests: [PASS|FAIL]

Implementation notes:
[2-3 sentences]
```

### Fallback Handling
If delegation fails (agent not found, returned FAILURE, verification failed):
```
⚠ Delegation to api-agent failed.
Reason: [error]

Falling back to direct implementation...
```

---

## Parallel Execution

Run multiple independent stories concurrently:

```json
{
  "delegation": {
    "enabled": true,
    "parallel": {
      "enabled": true,
      "maxConcurrent": 3
    }
  }
}
```

### Flow
1. Find stories with no unmet dependencies
2. Detect potential file conflicts
3. Select non-conflicting batch (up to maxConcurrent)
4. Launch all agents in single message (enables true parallelism)
5. Collect results, handle failures individually

### Expected Speedups
| Independent | Sequential | Parallel (3) | Speedup |
|-------------|------------|--------------|---------|
| 2 | ~6 min | ~3 min | 2x |
| 3 | ~9 min | ~3 min | 3x |
| 5 | ~15 min | ~5 min | 3x |

---

## Swarm Mode

For large PRDs (10+ stories), use TeammateTool for persistent workers:

```json
{
  "swarm": {
    "enabled": true,
    "teamName": "feature-auth",
    "workers": {
      "maxWorkers": 5,
      "types": ["frontend", "api", "database"]
    }
  }
}
```

See [references/swarm-orchestration-design.md](references/swarm-orchestration-design.md) for full protocol.

---

## Memory Integration

**Query at phase start:**
```
mcp__memory__search_nodes({ query: "preference" })
mcp__memory__search_nodes({ query: "[stack]" })  // e.g., "nextjs"
mcp__memory__search_nodes({ query: "mistake" })
```

**Save after successful stories (if broadly applicable):**
```javascript
mcp__memory__create_entities({
  entities: [{
    name: "pattern:descriptive-name",
    entityType: "pattern",  // or: mistake, tech-insight, preference
    observations: ["What", "When to use", "Applies to: [stack]"]
  }]
})
```

**Entity types:** `pattern` | `mistake` | `preference` | `tech-insight` | `architecture-decision`

---

## File Reference

| File | Purpose |
|------|---------|
| `tasks/prd-*.md` | Human-readable PRD |
| `prd.json` | Machine-readable tasks |
| `progress.md` | Full implementation log |
| `progress-summary.md` | Compact context (auto-generated) |
| `AGENTS.md` | Repository patterns |

## Reference Docs

| File | Content |
|------|---------|
| [references/schemas.md](references/schemas.md) | Full prd.json schema |
| [references/examples.md](references/examples.md) | Complete examples |
| [references/swarm-orchestration-design.md](references/swarm-orchestration-design.md) | Swarm protocol |
| [references/smart-delegation-design.md](references/smart-delegation-design.md) | Delegation architecture |
