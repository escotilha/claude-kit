# Autonomous Agent Examples & Patterns

## Story Splitting Examples

### Example: Notification System

**Original (too big):**

> "Add user notification system"

**Split into:**

1. US-001: Add notifications table with schema (id, userId, message, read, createdAt)
2. US-002: Create sendNotification server action
3. US-003: Create getNotifications server action with pagination
4. US-004: Add notification bell icon to header (static, no data)
5. US-005: Connect bell icon to notifications data
6. US-006: Create notification dropdown panel UI
7. US-007: Add mark-as-read functionality
8. US-008: Add notification preferences to user settings

### Example: Task Priority Feature

**Original (too big):**

> "Add task priority system"

**Split into:**

1. US-001: Add `priority` enum column to tasks table (high/medium/low, default: medium)
2. US-002: Update task types to include priority field
3. US-003: Create updateTaskPriority server action
4. US-004: Add priority dropdown to task edit form
5. US-005: Add priority badge component
6. US-006: Display priority badge on task cards
7. US-007: Add filter by priority on task list
8. US-008: Add sort by priority option

### Example: Dashboard

**Original (too big):**

> "Build the admin dashboard"

**Split into:**

1. US-001: Create dashboard page route and base layout
2. US-002: Add user count query to data layer
3. US-003: Create StatsCard component
4. US-004: Add user count stats card to dashboard
5. US-005: Add revenue stats query
6. US-006: Add revenue stats card to dashboard
7. US-007: Create activity list component
8. US-008: Add recent activity query and display

---

## Dependency Ordering

Stories should be ordered so dependencies come first:

```
US-001: Schema/Database changes
    ↓
US-002: Type definitions (if separate from schema)
    ↓
US-003: Server actions/API endpoints
    ↓
US-004: Reusable UI components (no data fetching)
    ↓
US-005: Connected components (with data fetching)
    ↓
US-006: Page integration
    ↓
US-007: Enhancement features (filters, sorts, etc.)
```

### prd.json with Dependencies

```json
{
  "userStories": [
    {
      "id": "US-001",
      "title": "Add priority column to database",
      "priority": 1,
      "dependsOn": [],
      "passes": false
    },
    {
      "id": "US-002",
      "title": "Create updateTaskPriority server action",
      "priority": 2,
      "dependsOn": ["US-001"],
      "passes": false
    },
    {
      "id": "US-003",
      "title": "Add priority dropdown to task form",
      "priority": 3,
      "dependsOn": ["US-002"],
      "passes": false
    }
  ]
}
```

---

## Acceptance Criteria Templates

### Database Stories

```markdown
**Acceptance Criteria:**

- [ ] Add `[column]` column to `[table]` table with type `[type]`
- [ ] Default value is `[value]`
- [ ] Migration file created and runs successfully
- [ ] Schema types updated
- [ ] Typecheck passes
```

### Server Action Stories

```markdown
**Acceptance Criteria:**

- [ ] Action accepts `[params]` parameters
- [ ] Action validates: [validation rules]
- [ ] Action returns `[return type]`
- [ ] Action handles error case: [specific error]
- [ ] Typecheck passes
- [ ] Tests pass
```

### UI Component Stories (No Data)

```markdown
**Acceptance Criteria:**

- [ ] Component accepts props: [prop list]
- [ ] Component renders [elements]
- [ ] Component has correct styling
- [ ] Typecheck passes
```

### Connected Component Stories

```markdown
**Acceptance Criteria:**

- [ ] Component fetches data from [source]
- [ ] Component shows loading state
- [ ] Component shows error state on failure
- [ ] Component displays data correctly
- [ ] Typecheck passes
- [ ] Verify in browser
```

### Filter/Sort Stories

```markdown
**Acceptance Criteria:**

- [ ] Dropdown shows options: [option1], [option2], [option3]
- [ ] Selecting [option] filters/sorts list correctly
- [ ] Default selection is [default]
- [ ] Filter state persists in URL (if applicable)
- [ ] Typecheck passes
- [ ] Verify in browser
```

---

## Complete prd.json Example

```json
{
  "project": "TaskApp",
  "branchName": "feature/task-priority",
  "description": "Add priority levels to tasks with filtering capability",
  "createdAt": "2024-01-15T10:00:00Z",
  "verification": {
    "typecheck": "npm run typecheck",
    "test": "npm run test",
    "lint": "npm run lint",
    "build": "npm run build"
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "Add priority column to database",
      "description": "As a developer, I need to store task priority so it persists",
      "acceptanceCriteria": [
        "Add `priority` column to tasks table (enum: high, medium, low)",
        "Default value is 'medium'",
        "Migration created and runs successfully",
        "Typecheck passes"
      ],
      "priority": 1,
      "dependsOn": [],
      "passes": false,
      "attempts": 0,
      "notes": ""
    },
    {
      "id": "US-002",
      "title": "Create updateTaskPriority server action",
      "description": "As a developer, I need an action to update task priority",
      "acceptanceCriteria": [
        "Action accepts taskId and priority parameters",
        "Action validates priority is one of: high, medium, low",
        "Action returns updated task object",
        "Typecheck passes",
        "Tests pass"
      ],
      "priority": 2,
      "dependsOn": ["US-001"],
      "passes": false,
      "attempts": 0,
      "notes": ""
    },
    {
      "id": "US-003",
      "title": "Add priority dropdown to task form",
      "description": "As a user, I want to set task priority when creating/editing tasks",
      "acceptanceCriteria": [
        "Dropdown appears in task create/edit form",
        "Dropdown has options: High, Medium, Low",
        "Selected value saves correctly via server action",
        "Typecheck passes",
        "Verify in browser"
      ],
      "priority": 3,
      "dependsOn": ["US-002"],
      "passes": false,
      "attempts": 0,
      "notes": ""
    },
    {
      "id": "US-004",
      "title": "Display priority badge on task cards",
      "description": "As a user, I want to see task priority at a glance",
      "acceptanceCriteria": [
        "Badge component created with high/medium/low variants",
        "High = red, Medium = yellow, Low = green",
        "Badge shows on each task card",
        "Typecheck passes",
        "Verify in browser"
      ],
      "priority": 4,
      "dependsOn": ["US-001"],
      "passes": false,
      "attempts": 0,
      "notes": ""
    },
    {
      "id": "US-005",
      "title": "Add filter by priority",
      "description": "As a user, I want to filter tasks by priority level",
      "acceptanceCriteria": [
        "Filter dropdown on task list page",
        "Options: All, High, Medium, Low",
        "Selecting option filters displayed tasks",
        "Filter value persists in URL query param",
        "Typecheck passes",
        "Verify in browser"
      ],
      "priority": 5,
      "dependsOn": ["US-004"],
      "passes": false,
      "attempts": 0,
      "notes": ""
    }
  ]
}
```

---

## progress.md Format

```markdown
# Progress Log: Task Priority Feature

Branch: `feature/task-priority`
Started: 2024-01-15

---

## 2024-01-15 10:30 - US-001: Add priority column to database

**Implementation:**

- Added priority enum type to schema
- Created migration file: `db/migrations/20240115_add_priority.sql`
- Updated Task type in `types/task.ts`

**Files changed:**

- `db/schema.ts`
- `db/migrations/20240115_add_priority.sql`
- `types/task.ts`

**Learnings:**

- Database requires explicit enum definition before column creation
- Need to run `db:generate` after schema changes

---

## 2024-01-15 11:00 - US-002: Create updateTaskPriority server action

**Implementation:**

- Created server action with zod validation
- Added revalidatePath for cache invalidation
- Added unit test for validation

**Files changed:**

- `app/actions/tasks.ts`
- `tests/actions/tasks.test.ts`

**Learnings:**

- Server actions need revalidatePath for cache updates
- Zod schema can be reused for both client and server validation

---
```

---

## AGENTS.md Template

Create this file when you discover patterns:

```markdown
# Repository Patterns

Last updated: 2024-01-15

## Stack

- Framework: Next.js 14 (App Router)
- Database: PostgreSQL with Drizzle ORM
- Styling: Tailwind CSS
- Testing: Vitest

## Directory Structure
```

src/
app/ # Next.js pages and routes
components/ # React components
actions/ # Server actions
lib/ # Utility functions
db/
schema.ts # Database schema
migrations/ # SQL migrations
tests/ # Test files

```

## API Conventions
- Server actions in `src/actions/[domain].ts`
- Return `{ success: boolean, data?: T, error?: string }`
- Use Zod for validation

## Component Patterns
- Client components marked with "use client"
- Props interfaces named `[Component]Props`
- Export default for page components, named for reusables

## Database
- Schema changes require running `npm run db:generate`
- Migrations auto-apply in dev, manual in prod
- Use transactions for multi-table operations

## Testing
- Unit tests: `*.test.ts` alongside source
- Integration: `tests/integration/`
- Run with `npm run test`

## Common Gotchas
- Must run `db:generate` after schema changes
- Server actions need `revalidatePath()` for cache
- Client components can't import server-only code
```

---

## Common Failure Patterns

### 1. Story Too Big

**Symptom:** Implementation takes many files, running out of context
**Solution:** Split into smaller stories, commit progress

### 2. Missing Dependency

**Symptom:** Import fails, type doesn't exist
**Solution:** Check `dependsOn`, reorder if needed

### 3. Wrong Order

**Symptom:** Frontend before backend, UI fails to compile
**Solution:** Always: schema -> types -> backend -> frontend

### 4. Vague Criteria

**Symptom:** "Works correctly" - can't verify
**Solution:** Rewrite with specific, testable criteria

### 5. Missing Typecheck

**Symptom:** Type errors accumulate
**Solution:** Always include "Typecheck passes" in criteria

### 6. UI Not Verified

**Symptom:** Code compiles but renders wrong
**Solution:** Include "Verify in browser" for UI stories

---

## Quick Reference

### Starting Fresh

```bash
# No prd.json -> Phase 1
ls prd.json 2>/dev/null || echo "Start Phase 1"
```

### Resuming Work

```bash
# Has prd.json with pending stories -> Phase 3
cat prd.json | jq '.userStories[] | select(.passes == false)'
```

### Checking Status

```bash
# Count remaining stories
cat prd.json | jq '[.userStories[] | select(.passes == false)] | length'
```

### Force Complete

```bash
# Mark story as done (use with caution)
cat prd.json | jq '.userStories[0].passes = true' > prd.json.tmp && mv prd.json.tmp prd.json
```
