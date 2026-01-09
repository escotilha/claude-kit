# Ralph Agent Examples & Patterns

## Story Splitting Examples

### Example: Notification System

**Original (too big):**
> "Add user notification system"

**Split into:**
1. US-001: Add notifications table to database
2. US-002: Create notification service for sending notifications
3. US-003: Add notification bell icon to header
4. US-004: Create notification dropdown panel
5. US-005: Add mark-as-read functionality
6. US-006: Add notification preferences page

### Example: Task Priority Feature

**Original (too big):**
> "Add task priority system"

**Split into:**
1. US-001: Add `priority` column to tasks table (high/medium/low, default: medium)
2. US-002: Create server action to update task priority
3. US-003: Add priority dropdown to task edit form
4. US-004: Add priority badge display on task cards
5. US-005: Add filter by priority on task list
6. US-006: Add sort by priority option

### Example: Dashboard

**Original (too big):**
> "Build the admin dashboard"

**Split into:**
1. US-001: Create dashboard page route and layout
2. US-002: Add user count stats query
3. US-003: Add user count card component
4. US-004: Add revenue stats query
5. US-005: Add revenue card component
6. US-006: Add recent activity query
7. US-007: Add activity list component

---

## Acceptance Criteria Patterns

### Database Stories
```
- Add `[column]` column to `[table]` table with type `[type]`
- Default value is `[value]`
- Migration runs successfully
- Typecheck passes
```

### Server Action Stories
```
- Action accepts `[params]` and returns `[type]`
- Action validates `[validation rules]`
- Action handles error case: `[error scenario]`
- Typecheck passes
- Tests pass
```

### UI Component Stories
```
- Component renders `[elements]`
- Clicking `[element]` triggers `[behavior]`
- Component shows loading state while fetching
- Component shows error state on failure
- Typecheck passes
- Verify in browser using dev-browser skill
```

### Filter/Sort Stories
```
- Dropdown shows options: `[option1]`, `[option2]`, `[option3]`
- Selecting `[option]` filters list to show only `[criteria]`
- Default selection is `[default]`
- Filter persists on page refresh (if applicable)
- Typecheck passes
- Verify in browser using dev-browser skill
```

---

## Complete prd.json Example

```json
{
  "project": "TaskApp",
  "branchName": "ralph/task-priority",
  "description": "Add priority levels to tasks with filtering capability",
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
      "passes": false,
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
      "passes": false,
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
        "Verify in browser using dev-browser skill"
      ],
      "priority": 3,
      "passes": false,
      "notes": ""
    },
    {
      "id": "US-004",
      "title": "Display priority badge on task cards",
      "description": "As a user, I want to see task priority at a glance",
      "acceptanceCriteria": [
        "Badge shows on each task card",
        "High = red badge, Medium = yellow badge, Low = green badge",
        "Badge shows priority text",
        "Typecheck passes",
        "Verify in browser using dev-browser skill"
      ],
      "priority": 4,
      "passes": false,
      "notes": ""
    }
  ]
}
```

---

## progress.txt Template

```
# Progress Log - [Feature Name]
Branch: ralph/[feature-name]

---

## 2024-01-15 14:30 - US-001: Add priority column to database
- **Implementation**: Added priority enum column to tasks table via migration
- **Files changed**: 
  - `db/migrations/20240115_add_priority.sql`
  - `db/schema.ts`
- **Learnings:**
  - Database requires explicit enum definition before column creation
  - Need to run `db:generate` after schema changes

---

## 2024-01-15 15:00 - US-002: Create updateTaskPriority server action
- **Implementation**: Created server action with validation
- **Files changed**:
  - `app/actions/tasks.ts`
  - `tests/actions/tasks.test.ts`
- **Learnings:**
  - Server actions need revalidatePath for cache updates
  - Zod schema used for priority validation

---
```

---

## Common Gotchas

1. **Context overflow**: Story too big → LLM runs out of context → broken code. Split it.

2. **Wrong ordering**: UI before schema → imports fail → wasted iteration. Always: schema → backend → frontend.

3. **Vague criteria**: "Works correctly" → no way to verify → story never completes. Be specific.

4. **Missing typecheck**: Forgot "Typecheck passes" → broken types slip through → cascading failures.

5. **UI not verified**: Code looks right but renders wrong → always include browser verification for UI stories.

6. **Giant PRD**: 20+ stories in one prd.json → overwhelming. Consider splitting into multiple features/branches.
