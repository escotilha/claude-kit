# Context Template System - Visual Guide

A visual overview of how the context template system works.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Context Template System                       │
│                                                                  │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────┐  │
│  │ context-template │  │ context-usage-   │  │ integration- │  │
│  │     .md          │  │    guide.md      │  │  example.md  │  │
│  │                  │  │                  │  │              │  │
│  │  Base structure  │  │  How to use      │  │  Real        │  │
│  │  for creating    │  │  and integrate   │  │  examples    │  │
│  │  context files   │  │  into skills     │  │  & patterns  │  │
│  └──────────────────┘  └──────────────────┘  └──────────────┘  │
│           │                      │                     │         │
│           └──────────────────────┴─────────────────────┘         │
│                                  │                               │
│                                  ▼                               │
│                    ┌──────────────────────────┐                  │
│                    │      README.md           │                  │
│                    │  (System Overview)       │                  │
│                    └──────────────────────────┘                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Session Lifecycle with Context

```
┌─────────────────────────────────────────────────────────────────┐
│                        Session Start                             │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌────────────────────────┐
                    │  Check for context.md  │
                    │  in priority order:    │
                    │  1. ./context.md       │
                    │  2. ./.claude/         │
                    │  3. ./.claude/skills/  │
                    └───────────┬────────────┘
                                │
                    ┌───────────┴────────────┐
                    │                        │
                ┌───▼───┐              ┌────▼─────┐
                │ Found │              │ Not Found│
                └───┬───┘              └────┬─────┘
                    │                       │
                    ▼                       ▼
        ┌───────────────────────┐  ┌────────────────────┐
        │   Load & Parse        │  │ Should create one? │
        │   - Current State     │  │ (based on criteria)│
        │   - Recent Activity   │  └────────┬───────────┘
        │   - Preferences       │           │
        └───────────┬───────────┘     ┌─────┴─────┐
                    │                 │           │
                    │                Yes         No
                    │                 │           │
                    │                 ▼           │
                    │     ┌──────────────────┐   │
                    │     │ Create from      │   │
                    │     │ template.md      │   │
                    │     └─────────┬────────┘   │
                    │               │            │
                    └───────────────┴────────────┘
                                    │
                                    ▼
                    ┌────────────────────────────┐
                    │  Query Memory for          │
                    │  - preferences             │
                    │  - patterns                │
                    │  - mistakes to avoid       │
                    └────────────┬───────────────┘
                                 │
                                 ▼
                    ┌────────────────────────────┐
                    │  Present Context Summary   │
                    │  to User:                  │
                    │  "I see we were working    │
                    │   on X. Should I continue?"│
                    └────────────┬───────────────┘
                                 │
┌────────────────────────────────▼────────────────────────────────┐
│                         Work Session                             │
│                                                                  │
│  User Task → Skill Action → Update Context → Continue           │
│     │            │               │                               │
│     │            │               ▼                               │
│     │            │    ┌──────────────────────┐                  │
│     │            │    │ Update sections:     │                  │
│     │            │    │ - Recent Activity    │                  │
│     │            │    │ - Current State      │                  │
│     │            │    │ - What Exists        │                  │
│     │            │    │ - Decisions Made     │                  │
│     │            │    └──────────────────────┘                  │
│     │            │                                               │
│     └────────────┴───────────────┐                              │
│                                  │                               │
└──────────────────────────────────┼───────────────────────────────┘
                                   │
                                   ▼
┌─────────────────────────────────────────────────────────────────┐
│                         Session End                              │
│                                                                  │
│  1. Update "Recent Activity" with session summary               │
│  2. Update "Current State" with pending items                   │
│  3. Update "Last Sync" timestamp                                │
│  4. Stage context.md (if in git repo)                           │
│  5. Optional: Commit context changes                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## Context vs Memory Decision Tree

```
                    ┌──────────────────────┐
                    │  Need to store       │
                    │  information?        │
                    └──────────┬───────────┘
                               │
                    ┌──────────▼───────────┐
                    │ Is it session-       │
                    │ specific or project- │
                    │ local?               │
                    └──────────┬───────────┘
                               │
                    ┌──────────┴───────────┐
                    │                      │
                   Yes                    No
                    │                      │
                    ▼                      ▼
        ┌────────────────────┐  ┌────────────────────┐
        │                    │  │                    │
        │  Use CONTEXT.MD    │  │  Use MEMORY MCP    │
        │                    │  │                    │
        │  Examples:         │  │  Examples:         │
        │  - Pending tasks   │  │  - User prefs      │
        │  - Stage progress  │  │  - Best practices  │
        │  - Files created   │  │  - Patterns        │
        │  - This session's  │  │  - Mistakes to     │
        │    decisions       │  │    avoid           │
        │  - Blockers        │  │  - Tech insights   │
        │                    │  │                    │
        │  Lifetime:         │  │  Lifetime:         │
        │  Session/project   │  │  Permanent         │
        │                    │  │                    │
        │  Scope:            │  │  Scope:            │
        │  This project      │  │  Cross-project     │
        │                    │  │                    │
        └────────────────────┘  └────────────────────┘
                    │                      │
                    │                      │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Context REFERENCES  │
                    │  memory entities     │
                    │                      │
                    │  Example:            │
                    │  "Follow             │
                    │   pattern:early-     │
                    │   returns"           │
                    └──────────────────────┘
```

---

## Directory Structure Patterns

### Pattern 1: Single Project (Simple)
```
my-project/
├── context.md              ← Context at root
├── src/
│   ├── index.ts
│   └── utils.ts
├── tests/
└── package.json
```

### Pattern 2: Multi-Skill Project
```
my-project/
├── .claude/
│   ├── context.md          ← Shared context
│   └── skills/
│       ├── cto/
│       │   └── context.md  ← CTO-specific state
│       ├── testing-agent/
│       │   └── context.md  ← Testing-specific state
│       └── archive/
│           └── old-activity.md
├── src/
├── tests/
└── package.json
```

### Pattern 3: Complex Project with Archives
```
my-project/
├── .claude/
│   ├── context.md          ← Current context
│   ├── archive/
│   │   ├── 2026-01-activity.md
│   │   └── decisions-log-2025.md
│   └── skills/
│       └── cpo-ai-skill/
│           ├── context.md
│           └── epic-progress.md
├── src/
└── package.json
```

---

## Integration Complexity Levels

```
┌─────────────────────────────────────────────────────────────────┐
│  Level 1: Basic (5 min integration)                             │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Check if context.md exists                                  │
│  2. If yes, load it                                             │
│  3. If no, continue without                                     │
│                                                                  │
│  No creation, no updates, just reading.                         │
│  Good for: One-off utilities, simple readers                    │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Level 2: Standard (20 min integration)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Session Start:                                                 │
│    1. Check for context                                         │
│    2. Load if exists, create if needed                          │
│    3. Present summary to user                                   │
│                                                                  │
│  During Session:                                                │
│    - Update Recent Activity when actions occur                  │
│    - Update Current State when decisions made                   │
│                                                                  │
│  Session End:                                                   │
│    - Update Last Sync timestamp                                 │
│                                                                  │
│  Good for: Most development skills, testing skills              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  Level 3: Advanced (60 min integration)                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Everything from Level 2, plus:                                 │
│                                                                  │
│  - Custom context sections for skill-specific state             │
│  - Memory integration (query preferences, patterns)             │
│  - Progress tracking with percentages                           │
│  - Decision logging with rationales                             │
│  - Blocker tracking                                             │
│  - Archive management (move old data)                           │
│  - Multi-location context discovery                             │
│  - Context health checks                                        │
│                                                                  │
│  Good for: Orchestrators, multi-stage workflows, CPO/CTO        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Skill Type → Context Usage Matrix

```
┌──────────────────────┬─────────────┬──────────────┬─────────────┐
│ Skill Type           │ Should Use  │ Complexity   │ Priority    │
│                      │ Context?    │ Level        │             │
├──────────────────────┼─────────────┼──────────────┼─────────────┤
│ Long-running Dev     │ ✅ YES      │ Advanced     │ HIGH        │
│ (cto, cpo-ai-skill)  │             │ (Level 3)    │             │
├──────────────────────┼─────────────┼──────────────┼─────────────┤
│ Multi-stage Build    │ ✅ YES      │ Advanced     │ HIGH        │
│ (parallel-dev)       │             │ (Level 3)    │             │
├──────────────────────┼─────────────┼──────────────┼─────────────┤
│ Testing/QA           │ ✅ YES      │ Standard     │ HIGH        │
│ (testing-agent)      │             │ (Level 2)    │             │
├──────────────────────┼─────────────┼──────────────┼─────────────┤
│ Design/Creative      │ ✅ YES      │ Standard     │ MEDIUM      │
│ (website-design)     │             │ (Level 2)    │             │
├──────────────────────┼─────────────┼──────────────┼─────────────┤
│ Analysis/Research    │ ⚠️  MAYBE   │ Standard     │ MEDIUM      │
│ (triage-analyzer)    │             │ (Level 2)    │             │
├──────────────────────┼─────────────┼──────────────┼─────────────┤
│ One-off Utilities    │ ❌ NO       │ N/A          │ SKIP        │
│ (cp, maketree)       │             │              │             │
└──────────────────────┴─────────────┴──────────────┴─────────────┘
```

---

## Context Sections Explained

```
┌─────────────────────────────────────────────────────────────────┐
│                         CONTEXT.MD                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ## Who I Am                                                     │
│  ┌────────────────────────────────────────────────────┐         │
│  │ STATIC - Set once                                  │         │
│  │ Identifies which skill/agent owns this context     │         │
│  │ Helps with handoffs between skills                 │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
│  ## What I Know About This User                                 │
│  ┌────────────────────────────────────────────────────┐         │
│  │ DYNAMIC - Updated as learned                       │         │
│  │ User preferences from memory + this session        │         │
│  │ Communication style, tool preferences              │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
│  ## What Exists                                                 │
│  ┌────────────────────────────────────────────────────┐         │
│  │ SEMI-DYNAMIC - Refresh periodically                │         │
│  │ Filesystem cache to avoid repeated discovery       │         │
│  │ Files, directories, configuration                  │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
│  ## Recent Activity                                             │
│  ┌────────────────────────────────────────────────────┐         │
│  │ DYNAMIC - Append only                              │         │
│  │ Log of actions with timestamps                     │         │
│  │ Keep last 10-20, archive older                     │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
│  ## My Guidelines                                               │
│  ┌────────────────────────────────────────────────────┐         │
│  │ SEMI-STATIC - From config + preferences            │         │
│  │ Project-specific rules                             │         │
│  │ References to memory entities                      │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
│  ## Current State                                               │
│  ┌────────────────────────────────────────────────────┐         │
│  │ DYNAMIC - Most important for continuity            │         │
│  │ Pending tasks, active work, blockers               │         │
│  │ Always update before session end                   │         │
│  └────────────────────────────────────────────────────┘         │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Quick Reference Commands

```bash
# Create context from template
cp ~/Library/Mobile\ Documents/com~apple~CloudDocs/claude-setup/skills/templates/context-template.md ./context.md

# Check if context exists
test -f ./context.md && echo "Context exists" || echo "No context"

# View context
cat ./context.md

# Archive old activity (manual)
tail -n 10 ./context.md > temp.md
mv temp.md ./context.md

# Find all contexts in project
find . -name "context.md" -type f
```

---

## Common Workflows

### Workflow 1: First-time Context Creation
```
User starts skill
    ↓
Skill checks for context
    ↓
None found
    ↓
Skill asks: "Should I create context.md?"
    ↓
User: "Yes"
    ↓
Skill copies template
    ↓
Skill fills in "Who I Am"
    ↓
Skill discovers files → fills "What Exists"
    ↓
Skill queries memory → fills "My Guidelines"
    ↓
Context ready for use
```

### Workflow 2: Resume from Context
```
User starts skill (return visit)
    ↓
Skill loads context.md
    ↓
Parses "Current State" section
    ↓
Sees: "Pending: Fix auth bug"
    ↓
Skill: "I see we were working on the auth bug.
       Should I continue?"
    ↓
User: "Yes"
    ↓
Skill resumes work with full context
```

### Workflow 3: Multi-skill Collaboration
```
CTO Skill creates architecture
    ↓
Updates .claude/context.md with decisions
    ↓
User invokes Testing Agent
    ↓
Testing Agent loads .claude/context.md
    ↓
Sees CTO's architecture decisions
    ↓
Tests according to those decisions
    ↓
Updates context with test results
    ↓
Both skills share state seamlessly
```

---

**Created**: 2026-01-30
**For**: Context Template System v1.0
**Maintained By**: memory-consolidation skill
