# Autonomous Agent Examples & Patterns

## Inline Goal Example (End-to-End Flow)

This example shows the complete flow when a user provides an inline goal.

### User Input

```
/autonomous-agent create a login system for this project
```

### Step 0.1: Parse Inline Goal

```
INLINE_GOAL: "create a login system for this project"
```

### Step 1.1.6: Goal-Specific Codebase Analysis

**Keywords extracted:** auth, login, user, session, password, signin, signup

**Search results:**

```bash
# Files found with auth-related code
lib/auth.ts                           # Auth.js configuration
app/api/auth/[...nextauth]/route.ts   # NextAuth API route
db/schema.ts                          # Contains User table
middleware.ts                         # Route protection

# Database schema inspection
User table: id, email, password, name, createdAt
Session table: id, userId, expires
```

**CODEBASE_CONTEXT built:**

```
existingFiles:
  - lib/auth.ts (Auth.js with credentials provider skeleton)
  - db/schema.ts (User table with email/password)
  - middleware.ts (protects /dashboard routes)

existingPatterns:
  - Next.js 14 App Router
  - Auth.js (NextAuth v5)
  - Drizzle ORM
  - Server Actions for mutations

integrationPoints:
  - Auth config ready, needs custom pages
  - User table ready for auth
  - Middleware configured for protected routes

gaps:
  - No login page (/login)
  - No registration page (/register)
  - No password reset flow
  - No email verification
```

### Step 1.2: Context-Aware Questions

```
I'll help you create a login system. I analyzed the codebase and found:

Existing:
✓ Auth.js configured in lib/auth.ts
✓ User table with email/password columns in db/schema.ts
✓ Auth API route at /api/auth/[...nextauth]
✓ Middleware protecting /dashboard routes

Missing:
✗ Login page UI
✗ Registration page
✗ Password reset flow

Based on this, a few questions:

1. Auth features to build?
   A. Login page only (quick win - auth backend exists)
   B. Login + Registration pages
   C. Full flow (login, register, forgot password)

2. Should registration require email verification?
   A. No - immediate access after signup
   B. Yes - verify email before login allowed

3. UI style?
   A. Dedicated pages at /login, /register (Recommended - matches Next.js patterns)
   B. Modal dialogs from any page
   C. Sidebar/drawer approach

Reply with: "1B, 2A, 3A" (or type your own answers)
```

### User Response

```
1C, 2B, 3A
```

### Step 1.3: Generate PRD

Creates `tasks/prd-login-system.md`:

```markdown
# PRD: Login System

## Overview

Complete authentication UI for the existing Auth.js backend, including login,
registration with email verification, and password reset functionality.

## Goals

- Enable users to create accounts and sign in
- Verify email addresses before granting access
- Allow password recovery via email

## Non-Goals

- OAuth/social login (can be added later)
- Two-factor authentication
- Admin user management

## User Stories

### US-001: Create login page UI

**Description:** As a user, I want a login page so I can sign into my account.

**Scope:** `app/(auth)/login/page.tsx`, `components/auth/LoginForm.tsx`
**Domain:** frontend
**Depends on:** None

**Acceptance Criteria:**

- [ ] Login page at /login with email/password form
- [ ] Form validates email format and required fields
- [ ] Shows error messages for invalid credentials
- [ ] Redirects to /dashboard on success
- [ ] Uses existing Auth.js signIn() function
- [ ] Typecheck passes

### US-002: Create registration page UI

**Description:** As a visitor, I want to create an account.

**Scope:** `app/(auth)/register/page.tsx`, `components/auth/RegisterForm.tsx`, `actions/auth.ts`
**Domain:** frontend, backend
**Depends on:** None

**Acceptance Criteria:**

- [ ] Registration page at /register
- [ ] Form collects email, password, confirm password, name
- [ ] Password strength validation (min 8 chars)
- [ ] Server action creates user in database (password hashed)
- [ ] Sends verification email after signup
- [ ] Shows "check your email" message
- [ ] Typecheck passes

### US-003: Implement email verification

**Description:** As a user, I need to verify my email before accessing the app.

**Scope:** `app/(auth)/verify/page.tsx`, `actions/auth.ts`, `lib/email.ts`
**Domain:** backend, frontend
**Depends on:** US-002

**Acceptance Criteria:**

- [ ] Verification token generated and stored on signup
- [ ] Email sent with verification link
- [ ] /verify?token=xxx page validates token
- [ ] User marked as verified in database
- [ ] Unverified users cannot sign in
- [ ] Typecheck passes

### US-004: Create password reset flow

**Description:** As a user, I want to reset my password if I forget it.

**Scope:** `app/(auth)/forgot-password/page.tsx`, `app/(auth)/reset-password/page.tsx`, `actions/auth.ts`
**Domain:** frontend, backend
**Depends on:** US-003 (reuses email infrastructure)

**Acceptance Criteria:**

- [ ] /forgot-password page with email input
- [ ] Sends reset link to email
- [ ] /reset-password?token=xxx page for new password
- [ ] Token expires after 1 hour
- [ ] Password updated in database (hashed)
- [ ] Typecheck passes

### US-005: Add auth navigation links

**Description:** As a user, I want easy access to login/logout.

**Scope:** `components/Header.tsx`
**Domain:** frontend
**Depends on:** US-001

**Acceptance Criteria:**

- [ ] Header shows Login/Register when logged out
- [ ] Header shows user name and Logout when logged in
- [ ] Logout clears session and redirects to home
- [ ] Typecheck passes

## Technical Approach

- Extend existing Auth.js setup in lib/auth.ts
- Create (auth) route group for login/register pages
- Use server actions for form submissions
- Reuse existing User table, add emailVerified and resetToken columns
- Use existing email service pattern (or add Resend if none exists)
```

### Resulting prd.json

```json
{
  "project": "MyApp",
  "branchName": "feature/login-system",
  "description": "Complete auth UI with login, registration, email verification, password reset",
  "parallelConfig": {
    "enabled": true,
    "maxConcurrent": 3
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "Create login page UI",
      "dependsOn": [],
      "scope": {
        "files": ["app/(auth)/login/*", "components/auth/LoginForm.tsx"],
        "domains": ["frontend"],
        "exclusive": false
      }
    },
    {
      "id": "US-002",
      "title": "Create registration page UI",
      "dependsOn": [],
      "scope": {
        "files": [
          "app/(auth)/register/*",
          "components/auth/RegisterForm.tsx",
          "actions/auth.ts"
        ],
        "domains": ["frontend", "backend"],
        "exclusive": false
      }
    },
    {
      "id": "US-003",
      "title": "Implement email verification",
      "dependsOn": ["US-002"],
      "scope": {
        "files": ["app/(auth)/verify/*", "actions/auth.ts", "lib/email.ts"],
        "domains": ["backend", "frontend"],
        "exclusive": false
      }
    },
    {
      "id": "US-004",
      "title": "Create password reset flow",
      "dependsOn": ["US-003"],
      "scope": {
        "files": [
          "app/(auth)/forgot-password/*",
          "app/(auth)/reset-password/*",
          "actions/auth.ts"
        ],
        "domains": ["frontend", "backend"],
        "exclusive": false
      }
    },
    {
      "id": "US-005",
      "title": "Add auth navigation links",
      "dependsOn": ["US-001"],
      "scope": {
        "files": ["components/Header.tsx"],
        "domains": ["frontend"],
        "exclusive": false
      }
    }
  ]
}
```

### Wave Planning

```
Wave 0: US-001, US-002 (parallel - no dependencies, non-overlapping scope)
Wave 1: US-003, US-005 (parallel - US-003 depends on US-002, US-005 depends on US-001)
Wave 2: US-004 (sequential - depends on US-003)
```

---

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

### prd.json with Dependencies (Sequential)

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

## Parallel Execution Examples

### Dependency Graph Visualization

Understanding how stories can be parallelized based on dependencies:

```
Example: Task Priority Feature

                    US-001 (Database)
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
        US-002       US-004       US-005
       (Backend)   (Frontend)   (Frontend)
            │            │
            ▼            ▼
        US-003       US-006
       (Frontend)   (Frontend)
                         │
                         ▼
                     US-007
                    (Frontend)

Wave 0: US-001 (sequential - database is exclusive)
Wave 1: US-002, US-004, US-005 (parallel - different domains)
Wave 2: US-003, US-006 (parallel - non-overlapping files)
Wave 3: US-007 (sequential - single story)
```

### Parallelization Patterns

**Star Pattern (Best for Parallelization):**

```
         US-001
        /  |  \
    US-002 US-003 US-004
```

All child stories can run in parallel after US-001 completes.

**Chain Pattern (No Parallelization):**

```
US-001 → US-002 → US-003 → US-004
```

Each story depends on the previous - must run sequentially.

**Diamond Pattern (Partial Parallelization):**

```
         US-001
        /      \
    US-002    US-003
        \      /
         US-004
```

US-002 and US-003 can run in parallel; US-004 waits for both.

**Forest Pattern (Maximum Parallelization):**

```
US-001    US-002    US-003
   │         │         │
US-004    US-005    US-006
```

Independent chains - all roots can run in parallel, then all children.

---

## Complete prd.json Example (with Parallel Config)

```json
{
  "project": "TaskApp",
  "branchName": "feature/task-priority",
  "description": "Add priority levels to tasks with filtering capability",
  "createdAt": "2024-01-15T10:00:00Z",

  "parallelConfig": {
    "enabled": true,
    "maxConcurrent": 3,
    "conflictStrategy": "git-merge-fallback",
    "verificationMode": "per-wave",
    "scopeAnalysis": "auto",
    "retryFailedSequentially": true,
    "waveTimeout": 300000
  },

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
      "scope": {
        "files": ["db/schema.ts", "db/migrations/*.sql"],
        "domains": ["database"],
        "exclusive": true
      },
      "passes": false,
      "attempts": 0,
      "waveId": null,
      "agentId": null,
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
      "scope": {
        "files": ["src/actions/tasks.ts", "tests/actions/tasks.test.ts"],
        "domains": ["backend"],
        "exclusive": false
      },
      "passes": false,
      "attempts": 0,
      "waveId": null,
      "agentId": null,
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
      "scope": {
        "files": ["src/components/TaskForm.tsx"],
        "domains": ["frontend"],
        "exclusive": false
      },
      "passes": false,
      "attempts": 0,
      "waveId": null,
      "agentId": null,
      "notes": ""
    },
    {
      "id": "US-004",
      "title": "Create priority badge component",
      "description": "As a developer, I need a reusable badge component for priority",
      "acceptanceCriteria": [
        "Badge component created with high/medium/low variants",
        "High = red, Medium = yellow, Low = green",
        "Component exports PriorityBadge",
        "Typecheck passes"
      ],
      "priority": 2,
      "dependsOn": ["US-001"],
      "scope": {
        "files": ["src/components/PriorityBadge.tsx"],
        "domains": ["frontend"],
        "exclusive": false
      },
      "passes": false,
      "attempts": 0,
      "waveId": null,
      "agentId": null,
      "notes": ""
    },
    {
      "id": "US-005",
      "title": "Display priority badge on task cards",
      "description": "As a user, I want to see task priority at a glance",
      "acceptanceCriteria": [
        "Badge shows on each task card",
        "Badge reflects current task priority",
        "Typecheck passes",
        "Verify in browser"
      ],
      "priority": 4,
      "dependsOn": ["US-004"],
      "scope": {
        "files": ["src/components/TaskCard.tsx"],
        "domains": ["frontend"],
        "exclusive": false
      },
      "passes": false,
      "attempts": 0,
      "waveId": null,
      "agentId": null,
      "notes": ""
    },
    {
      "id": "US-006",
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
      "dependsOn": ["US-005"],
      "scope": {
        "files": [
          "src/components/TaskList.tsx",
          "src/components/PriorityFilter.tsx"
        ],
        "domains": ["frontend"],
        "exclusive": false
      },
      "passes": false,
      "attempts": 0,
      "waveId": null,
      "agentId": null,
      "notes": ""
    }
  ],

  "waves": []
}
```

---

## Wave History Examples

### Example: Completed Feature with Wave History

After a feature is fully implemented, the prd.json includes complete wave history:

```json
{
  "project": "TaskApp",
  "branchName": "feature/task-priority",
  "description": "Add priority levels to tasks with filtering capability",
  "createdAt": "2024-01-15T10:00:00Z",

  "parallelConfig": {
    "enabled": true,
    "maxConcurrent": 3,
    "conflictStrategy": "git-merge-fallback",
    "verificationMode": "per-wave"
  },

  "verification": {
    "typecheck": "npm run typecheck",
    "test": "npm run test",
    "lint": "npm run lint"
  },

  "userStories": [
    {
      "id": "US-001",
      "title": "Add priority column to database",
      "passes": true,
      "attempts": 1,
      "waveId": "wave-0",
      "agentId": null,
      "completedAt": "2024-01-15T10:15:00Z"
    },
    {
      "id": "US-002",
      "title": "Create updateTaskPriority server action",
      "passes": true,
      "attempts": 1,
      "waveId": "wave-1",
      "agentId": "agent-abc123",
      "completedAt": "2024-01-15T10:16:30Z"
    },
    {
      "id": "US-003",
      "title": "Add priority dropdown to task form",
      "passes": true,
      "attempts": 1,
      "waveId": "wave-2",
      "agentId": "agent-def456",
      "completedAt": "2024-01-15T10:18:00Z"
    },
    {
      "id": "US-004",
      "title": "Create priority badge component",
      "passes": true,
      "attempts": 1,
      "waveId": "wave-1",
      "agentId": "agent-ghi789",
      "completedAt": "2024-01-15T10:16:15Z"
    },
    {
      "id": "US-005",
      "title": "Display priority badge on task cards",
      "passes": true,
      "attempts": 2,
      "waveId": "wave-2",
      "agentId": "agent-jkl012",
      "completedAt": "2024-01-15T10:18:45Z",
      "notes": "First attempt failed due to missing import, fixed on retry"
    },
    {
      "id": "US-006",
      "title": "Add filter by priority",
      "passes": true,
      "attempts": 1,
      "waveId": "wave-3",
      "agentId": null,
      "completedAt": "2024-01-15T10:20:00Z"
    }
  ],

  "waves": [
    {
      "id": "wave-0",
      "stories": ["US-001"],
      "parallel": false,
      "status": "completed",
      "startedAt": "2024-01-15T10:00:00Z",
      "completedAt": "2024-01-15T10:15:00Z",
      "duration": 900000,
      "results": {
        "US-001": {
          "success": true,
          "filesChanged": [
            "db/schema.ts",
            "db/migrations/20240115_add_priority.sql"
          ],
          "learnings": [
            "Database requires explicit enum definition before column creation"
          ]
        }
      }
    },
    {
      "id": "wave-1",
      "stories": ["US-002", "US-004"],
      "parallel": true,
      "status": "completed",
      "startedAt": "2024-01-15T10:15:00Z",
      "completedAt": "2024-01-15T10:16:30Z",
      "duration": 90000,
      "results": {
        "US-002": {
          "success": true,
          "agentId": "agent-abc123",
          "agentType": "Backend Agent",
          "filesChanged": [
            "src/actions/tasks.ts",
            "tests/actions/tasks.test.ts"
          ],
          "learnings": ["Server actions need revalidatePath for cache updates"]
        },
        "US-004": {
          "success": true,
          "agentId": "agent-ghi789",
          "agentType": "Frontend Agent",
          "filesChanged": ["src/components/PriorityBadge.tsx"],
          "learnings": ["Using shadcn/ui Badge component with custom colors"]
        }
      },
      "verification": {
        "typecheck": "passed",
        "test": "passed",
        "lint": "passed"
      }
    },
    {
      "id": "wave-2",
      "stories": ["US-003", "US-005"],
      "parallel": true,
      "status": "completed",
      "startedAt": "2024-01-15T10:16:30Z",
      "completedAt": "2024-01-15T10:18:45Z",
      "duration": 135000,
      "results": {
        "US-003": {
          "success": true,
          "agentId": "agent-def456",
          "agentType": "Frontend Agent",
          "filesChanged": ["src/components/TaskForm.tsx"],
          "learnings": []
        },
        "US-005": {
          "success": true,
          "agentId": "agent-jkl012",
          "agentType": "Frontend Agent",
          "filesChanged": ["src/components/TaskCard.tsx"],
          "learnings": ["Must import PriorityBadge before using"],
          "retries": 1,
          "firstAttemptError": "TS2307: Cannot find module './PriorityBadge'"
        }
      },
      "verification": {
        "typecheck": "passed",
        "test": "passed",
        "lint": "passed"
      }
    },
    {
      "id": "wave-3",
      "stories": ["US-006"],
      "parallel": false,
      "status": "completed",
      "startedAt": "2024-01-15T10:18:45Z",
      "completedAt": "2024-01-15T10:20:00Z",
      "duration": 75000,
      "results": {
        "US-006": {
          "success": true,
          "filesChanged": [
            "src/components/TaskList.tsx",
            "src/components/PriorityFilter.tsx"
          ],
          "learnings": [
            "URL search params need useSearchParams hook in client components"
          ]
        }
      }
    }
  ],

  "summary": {
    "totalStories": 6,
    "completedStories": 6,
    "totalWaves": 4,
    "parallelWaves": 2,
    "sequentialWaves": 2,
    "totalDuration": 1200000,
    "estimatedSequentialDuration": 2700000,
    "speedup": "2.25x"
  }
}
```

### Example: Partial Completion with Failures

When some stories fail and need retry:

```json
{
  "waves": [
    {
      "id": "wave-0",
      "stories": ["US-001"],
      "parallel": false,
      "status": "completed",
      "startedAt": "2024-01-15T10:00:00Z",
      "completedAt": "2024-01-15T10:15:00Z",
      "duration": 900000
    },
    {
      "id": "wave-1",
      "stories": ["US-002", "US-004", "US-005"],
      "parallel": true,
      "status": "partial",
      "startedAt": "2024-01-15T10:15:00Z",
      "completedAt": "2024-01-15T10:17:00Z",
      "duration": 120000,
      "results": {
        "US-002": {
          "success": true,
          "agentId": "agent-abc123",
          "agentType": "Backend Agent",
          "filesChanged": ["src/actions/tasks.ts"]
        },
        "US-004": {
          "success": true,
          "agentId": "agent-def456",
          "agentType": "Frontend Agent",
          "filesChanged": ["src/components/PriorityBadge.tsx"]
        },
        "US-005": {
          "success": false,
          "agentId": "agent-ghi789",
          "agentType": "Frontend Agent",
          "error": "TS2322: Type 'string' is not assignable to type 'Priority'",
          "filesChanged": ["src/components/TaskCard.tsx"],
          "rollbackApplied": true
        }
      },
      "verification": {
        "typecheck": "failed",
        "failingStory": "US-005",
        "error": "src/components/TaskCard.tsx:15 - Type error"
      },
      "commit": {
        "hash": "abc1234",
        "message": "feat(wave-1): US-002, US-004 (US-005 rolled back)",
        "storiesIncluded": ["US-002", "US-004"]
      }
    },
    {
      "id": "wave-2",
      "stories": ["US-005"],
      "parallel": false,
      "status": "pending",
      "note": "US-005 queued for sequential retry after wave-1 partial failure"
    }
  ]
}
```

### Example: Wave with Merge Conflict

When parallel stories create a merge conflict:

```json
{
  "waves": [
    {
      "id": "wave-1",
      "stories": ["US-002", "US-003"],
      "parallel": true,
      "status": "conflict",
      "startedAt": "2024-01-15T10:15:00Z",
      "completedAt": "2024-01-15T10:17:00Z",
      "duration": 120000,
      "results": {
        "US-002": {
          "success": true,
          "agentId": "agent-abc123",
          "filesChanged": ["src/types/task.ts", "src/actions/tasks.ts"]
        },
        "US-003": {
          "success": true,
          "agentId": "agent-def456",
          "filesChanged": ["src/types/task.ts", "src/components/TaskForm.tsx"]
        }
      },
      "conflict": {
        "file": "src/types/task.ts",
        "stories": ["US-002", "US-003"],
        "resolution": "fallback-sequential",
        "resolvedBy": "US-002 committed first, US-003 re-queued"
      },
      "commit": {
        "hash": "def5678",
        "message": "feat(wave-1): US-002 (US-003 re-queued due to conflict)",
        "storiesIncluded": ["US-002"]
      }
    },
    {
      "id": "wave-2",
      "stories": ["US-003"],
      "parallel": false,
      "status": "completed",
      "note": "Re-run after merge conflict resolution",
      "startedAt": "2024-01-15T10:17:00Z",
      "completedAt": "2024-01-15T10:19:00Z"
    }
  ]
}
```

---

## progress.md Format

### Sequential Execution Format

```markdown
# Progress Log: Task Priority Feature

Branch: `feature/task-priority`
Started: 2024-01-15
Mode: Sequential

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

### Parallel Execution Format (Wave-based)

```markdown
# Progress Log: Task Priority Feature

Branch: `feature/task-priority`
Started: 2024-01-15
Mode: Parallel (max 3 agents)

---

## 2024-01-15 10:00 - Wave 0 (Sequential)

**Story:** US-001 - Add priority column to database

**Implementation:**

- Added priority enum type to schema
- Created migration file
- Updated Task type

**Files changed:**

- `db/schema.ts`
- `db/migrations/20240115_add_priority.sql`

**Learnings:**

- Database requires explicit enum definition before column creation

**Duration:** 15 minutes

---

## 2024-01-15 10:15 - Wave 1 (Parallel)

**Stories Executed:**

| Story  | Title                      | Agent          | Status |
| ------ | -------------------------- | -------------- | ------ |
| US-002 | Server action for priority | Backend Agent  | Pass   |
| US-004 | Priority badge component   | Frontend Agent | Pass   |

**Execution Time:** 90s (vs ~6min sequential)
**Speedup:** 4x

**Files Changed:**

- `src/actions/tasks.ts` (US-002)
- `tests/actions/tasks.test.ts` (US-002)
- `src/components/PriorityBadge.tsx` (US-004)

**Learnings:**

- US-002: Server actions need revalidatePath for cache updates
- US-004: Using shadcn/ui Badge with custom color variants

**Verification:** All passed (typecheck, test, lint)

---

## 2024-01-15 10:17 - Wave 2 (Parallel)

**Stories Executed:**

| Story  | Title                     | Agent          | Status  |
| ------ | ------------------------- | -------------- | ------- |
| US-003 | Priority dropdown in form | Frontend Agent | Pass    |
| US-005 | Badge on task cards       | Frontend Agent | Retry 1 |

**Execution Time:** 135s
**Note:** US-005 failed first attempt, succeeded on retry

**Files Changed:**

- `src/components/TaskForm.tsx` (US-003)
- `src/components/TaskCard.tsx` (US-005)

**Failures:**

- US-005 (attempt 1): `TS2307: Cannot find module './PriorityBadge'`
  - Fix: Added missing import statement
  - Retry: Passed

**Learnings:**

- US-005: Must verify imports when using components created in same wave

---

## 2024-01-15 10:20 - Wave 3 (Sequential)

**Story:** US-006 - Add filter by priority

**Implementation:**

- Created PriorityFilter component
- Integrated with TaskList using URL params
- Added useSearchParams for state persistence

**Files changed:**

- `src/components/TaskList.tsx`
- `src/components/PriorityFilter.tsx`

**Learnings:**

- URL search params require useSearchParams in client components
- Filter state should persist across navigation

**Duration:** 75 seconds

---

## Summary

| Metric               | Value       |
| -------------------- | ----------- |
| Total Stories        | 6           |
| Total Waves          | 4           |
| Parallel Waves       | 2           |
| Sequential Waves     | 2           |
| Total Time           | ~20 minutes |
| Est. Sequential Time | ~45 minutes |
| Speedup              | 2.25x       |
| Retries              | 1 (US-005)  |
| Conflicts            | 0           |

---
```

### Wave with Conflict Resolution

```markdown
## 2024-01-15 10:15 - Wave 1 (Parallel - Conflict Resolved)

**Stories Attempted:**

| Story  | Title                 | Agent          | Status   |
| ------ | --------------------- | -------------- | -------- |
| US-002 | Update task types     | Backend Agent  | Pass     |
| US-003 | Task form integration | Frontend Agent | Conflict |

**Conflict Detected:**
```

File: src/types/task.ts
Stories: US-002, US-003
Both agents modified the Task interface

```

**Resolution:** Fallback to sequential

- US-002 committed (earlier completion time)
- US-003 re-queued for Wave 2

**Files Committed:**

- `src/types/task.ts` (US-002 version)
- `src/actions/tasks.ts` (US-002)

**Wave 2 Note:** US-003 will run sequentially and merge its type changes

---

## 2024-01-15 10:18 - Wave 2 (Sequential - Post-Conflict)

**Story:** US-003 - Task form integration (retry after conflict)

**Implementation:**

- Merged type changes with US-002's updates
- Added form field for priority

**Files changed:**

- `src/types/task.ts` (merged changes)
- `src/components/TaskForm.tsx`

**Learnings:**

- Stories modifying shared type files should use `scope.exclusive: true`
- Updated prd.json scope for future runs

---
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

## AGENTS.md Templates

Three templates for different project needs. The agent auto-generates Template 1 when no AGENTS.md exists.

### Template 1: Auto-Generated Starter (Default)

This is generated automatically during Phase 1 when no AGENTS.md exists:

```markdown
# AGENTS.md - [Project Name]

> Auto-generated by autonomous-agent on [YYYY-MM-DD]
> Review and customize. This file will be updated during implementation.

## Source

| Type          | Location         |
| ------------- | ---------------- |
| Global rules  | ~/.claude/rules/ |
| Auto-detected | [timestamp]      |

## Quick Commands

| Action    | Command             | Required |
| --------- | ------------------- | -------- |
| Typecheck | `npm run typecheck` | Yes      |
| Test      | `npm run test`      | Yes      |
| Lint      | `npm run lint`      | Yes      |
| Build     | `npm run build`     | No       |
| Dev       | `npm run dev`       | -        |

## Stack

- **Runtime:** Node.js 20.x
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript (strict mode)
- **Database:** PostgreSQL with Drizzle ORM
- **Styling:** Tailwind CSS
- **Testing:** Vitest

## Directory Structure

src/
├── app/ # Next.js pages and routes
├── components/ # React components
├── actions/ # Server actions
├── lib/ # Utility functions
└── db/
├── schema.ts # Database schema
└── migrations/ # SQL migrations

## Conventions

### From Global Rules (~/.claude/rules/)

**Coding Standards:**

- Prefer `const` over `let`, avoid `var`
- Use async/await over raw promises
- Prefer named exports over default exports

**Git Conventions:**

- Commit format: `type(scope): description`
- Branch format: `feature/description`, `fix/description`

**Security:**

- Never commit secrets or API keys
- Validate all user input
- Use parameterized queries

### Project-Specific

- Server actions return `{ success: boolean, data?: T, error?: string }`
- Components use Props interface naming: `[ComponentName]Props`
- API routes follow REST conventions

## Gotchas

> Entries are auto-appended during implementation

- Must run `npm run db:generate` after schema changes
- Server actions need `revalidatePath()` after mutations

---

_Last updated: [timestamp]_
```

### Template 2: Minimal (For simple projects)

Use for smaller projects with straightforward setup:

```markdown
# AGENTS.md

## Commands

- Typecheck: `npm run typecheck`
- Test: `npm run test`
- Lint: `npm run lint`

## Conventions

- Follow existing patterns in codebase
- See ~/.claude/rules/ for global standards

## Gotchas

[Will be populated during implementation]
```

### Template 3: Full Custom (For complex projects)

Comprehensive template for large or complex projects:

```markdown
# AGENTS.md - [Project Name]

## Overview

[Brief project description and architecture overview]

## Commands

### Required Before Commit

1. `npm run typecheck` - TypeScript compilation
2. `npm run lint` - ESLint checks
3. `npm run test` - Unit tests
4. `npm run test:e2e` - E2E tests (on feature branches)

### Development

- `npm run dev` - Start development server
- `npm run db:studio` - Open Drizzle Studio
- `npm run db:generate` - Generate migrations from schema
- `npm run db:migrate` - Run pending migrations

### Deployment

- `npm run build` - Production build
- `npm run start` - Start production server

## Architecture

### State Management

- Server state: React Query
- Client state: Zustand
- Forms: React Hook Form + Zod

### API Design

- REST endpoints in `/api/v1/*`
- GraphQL endpoint at `/api/graphql` (if applicable)
- WebSocket at `/api/ws` (if applicable)

## Conventions

### Coding Standards

[Project-specific coding standards]

### File Naming

- Components: PascalCase (`UserProfile.tsx`)
- Utilities: camelCase (`formatDate.ts`)
- Constants: SCREAMING_SNAKE (`API_BASE_URL`)

### Testing

- Unit tests: `*.test.ts` alongside source
- Integration: `tests/integration/*.test.ts`
- E2E: `e2e/*.spec.ts`

## Environment

Required environment variables:

- `DATABASE_URL` - PostgreSQL connection string
- `NEXTAUTH_SECRET` - Auth secret
- `NEXTAUTH_URL` - Canonical URL

## Gotchas

- After schema changes: run `db:generate` then `db:migrate`
- Server components can't use client hooks
- Middleware only runs on Edge runtime

## Changelog

| Date       | Change             | Story |
| ---------- | ------------------ | ----- |
| YYYY-MM-DD | Initial generation | -     |
```

---

## AGENTS.md Update Patterns

How to update AGENTS.md during Phase 3 implementation:

### Pattern 1: Adding a Gotcha

When you encounter an unexpected issue during implementation:

```markdown
## Gotchas

- [existing entries...]
- **[YYYY-MM-DD] US-XXX:** [Concise description of issue and solution]
```

**Example:**

```markdown
- **2024-01-15 US-003:** Form validation errors don't clear on submit - must call `reset()` after successful submission
```

### Pattern 2: Documenting a New Pattern

When you establish a pattern not previously documented:

```markdown
## Conventions

### Project-Specific

- [existing entries...]
- **[Pattern Name]:** [Description] _(discovered US-XXX)_
```

**Example:**

```markdown
- **Modal Pattern:** All modals use `@radix-ui/dialog` with controlled state _(discovered US-007)_
```

### Pattern 3: Adding a Command

When you discover or create a useful script:

```markdown
## Commands

### Development

- [existing entries...]
- `npm run [script]` - [Description] _(added US-XXX)_
```

---

## Rules Merging Examples

How project AGENTS.md merges with global ~/.claude/rules/:

### Example 1: Command Override (Project Wins)

**Global rules (~/.claude/rules/coding-standards.md):**

```markdown
## Testing

- Run tests with `npm test`
```

**Project AGENTS.md:**

```markdown
## Commands

- Test: `pnpm test:ci`
```

**Effective rule:** Use `pnpm test:ci` (AGENTS.md wins for commands)

### Example 2: Convention Merge (Combine with Override)

**Global rules:**

```markdown
- Prefer named exports over default exports
```

**Project AGENTS.md:**

```markdown
- Page components use default exports (Next.js requirement)
```

**Effective rules:**

- Use named exports (general case from global)
- Use default exports for page components (exception from project)

### Example 3: Security Never Overridden

**Global rules (~/.claude/rules/security-rules.md):**

```markdown
- NEVER commit secrets, API keys, passwords, or credentials
```

**Project AGENTS.md:**

```markdown
## Conventions

- Store API keys in `.env.local`
```

**Effective rules:**

- NEVER commit secrets (always enforced - global security can't be overridden)
- Store API keys in `.env.local` (location guidance from project)

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

### 7. Scope Overlap in Parallel

**Symptom:** Merge conflicts during wave execution
**Solution:** Mark overlapping stories with `scope.exclusive: true` or add explicit dependency

### 8. Missing Import in Parallel

**Symptom:** Story fails because it depends on component from same wave
**Solution:** Add dependency or ensure imports reference committed code only

---

## Auto-Learning Examples

### Example 1: Learning from TypeScript Errors

When a TypeScript error occurs during verification, the auto-learning system captures and documents it:

**Scenario:** Story US-003 fails with a missing module error

```
Verification Output:
src/components/TaskCard.tsx:5:18 - error TS2307: Cannot find module '@/components/ui/badge'

AUTO-LEARNING TRACE:
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Parse Error                                              │
├─────────────────────────────────────────────────────────────────┤
│ error_type: typescript                                           │
│ error_code: TS2307                                               │
│ category: missing-module                                         │
│ file: src/components/TaskCard.tsx                                │
│ line: 5                                                          │
│ message: Cannot find module '@/components/ui/badge'              │
│ signature: hash("typescript-TS2307-module-@/components")         │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Check Existing Knowledge                                 │
├─────────────────────────────────────────────────────────────────┤
│ Searching AGENTS.md Gotchas... NOT FOUND                         │
│ Searching progress.md... NOT FOUND                               │
│ Searching prd.json learning.errorPatterns... NOT FOUND           │
│ Result: NEW ERROR PATTERN                                        │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Attempt Fix                                              │
├─────────────────────────────────────────────────────────────────┤
│ Analyzing error category: missing-module                         │
│ Common solutions:                                                │
│   1. Check if file exists at path                                │
│   2. Verify tsconfig.json path aliases                           │
│   3. Install missing package                                     │
│                                                                  │
│ Attempting: Create missing component file                        │
│ Result: VERIFICATION PASSED                                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Capture Solution                                         │
├─────────────────────────────────────────────────────────────────┤
│ git diff analysis:                                               │
│   + src/components/ui/badge.tsx (new file)                       │
│                                                                  │
│ Solution recorded:                                               │
│ {                                                                │
│   "signature": "ts2307-module-components-ui",                    │
│   "solution_type": "create-file",                                │
│   "solution": "Create missing component file",                   │
│   "files_created": ["src/components/ui/badge.tsx"]               │
│ }                                                                │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Update AGENTS.md                                         │
├─────────────────────────────────────────────────────────────────┤
│ Section: Gotchas                                                 │
│ Entry added:                                                     │
│ - **[2024-01-15] US-003:** `Cannot find module '@/components/...'`│
│   → Verify component exists or create missing file (auto-learned)│
└─────────────────────────────────────────────────────────────────┘
```

**Resulting prd.json learning section:**

```json
{
  "learning": {
    "errorPatterns": [
      {
        "signature": "ts2307-module-components-ui",
        "category": "missing-module",
        "message": "Cannot find module '@/components/ui/badge'",
        "occurrences": 1,
        "firstSeen": "2024-01-15T10:30:00Z",
        "solution": "Create missing component file",
        "solutionType": "create-file",
        "storiesAffected": ["US-003"]
      }
    ]
  }
}
```

---

### Example 2: Recurring Error Detection

When the same error pattern occurs multiple times:

**Scenario:** Same TS2307 error occurs in US-005 after being learned in US-003

```
Verification Output:
src/components/TaskList.tsx:8:22 - error TS2307: Cannot find module '@/components/ui/card'

AUTO-LEARNING TRACE:
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Parse Error                                              │
├─────────────────────────────────────────────────────────────────┤
│ signature: hash("typescript-TS2307-module-@/components")         │
│ (Normalized signature matches previous pattern)                  │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Check Existing Knowledge                                 │
├─────────────────────────────────────────────────────────────────┤
│ Searching prd.json learning.errorPatterns...                     │
│ MATCH FOUND:                                                     │
│   signature: ts2307-module-components-ui                         │
│   solution: "Create missing component file"                      │
│   occurrences: 1                                                 │
│                                                                  │
│ Result: KNOWN ERROR - APPLY SOLUTION                             │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Apply Known Solution                                     │
├─────────────────────────────────────────────────────────────────┤
│ Applying: Create missing component file                          │
│ Created: src/components/ui/card.tsx                              │
│ Result: VERIFICATION PASSED                                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Update Learning Data                                     │
├─────────────────────────────────────────────────────────────────┤
│ occurrences: 1 → 2                                               │
│ solutionAppliedCount: 0 → 1                                      │
│ storiesAffected: ["US-003"] → ["US-003", "US-005"]               │
│                                                                  │
│ Threshold met (occurrences >= 2): Mark as RECURRING              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Update AGENTS.md (Escalate)                              │
├─────────────────────────────────────────────────────────────────┤
│ Original entry:                                                  │
│ - **[2024-01-15] US-003:** ... (auto-learned)                    │
│                                                                  │
│ Updated entry:                                                   │
│ - **[2024-01-15] US-003:** `Cannot find module '@/components/...'`│
│   → Create missing component file (recurring, 2 occurrences)     │
└─────────────────────────────────────────────────────────────────┘

Console output:
🔄 Recurring pattern detected: TS2307 missing-module
   Automatically applying known solution from US-003
   ✓ Solution applied successfully (2nd occurrence)
```

---

### Example 3: File Co-modification Pattern Detection

The system detects when files are frequently modified together:

**Scenario:** After 5 stories, pattern emerges that schema changes require type updates

```
Historical Data (from prd.json waves):
┌──────────┬───────────────────────────────────────────────────────┐
│ Story    │ Files Modified                                        │
├──────────┼───────────────────────────────────────────────────────┤
│ US-001   │ db/schema.ts, src/types/task.ts                       │
│ US-003   │ db/schema.ts, src/types/user.ts, src/lib/db.ts        │
│ US-006   │ src/components/Form.tsx                               │
│ US-008   │ db/schema.ts, src/types/project.ts                    │
│ US-010   │ db/schema.ts, src/types/task.ts, prisma/schema.prisma │
└──────────┴───────────────────────────────────────────────────────┘

AUTO-LEARNING TRACE:
┌─────────────────────────────────────────────────────────────────┐
│ Pattern Analysis (after US-010 completion)                       │
├─────────────────────────────────────────────────────────────────┤
│ Analyzing file co-modification patterns...                       │
│                                                                  │
│ db/schema.ts modified in: US-001, US-003, US-008, US-010         │
│ Co-modified files:                                               │
│   - src/types/*.ts: 4/4 stories (100% correlation)               │
│   - src/lib/db.ts: 1/4 stories (25% correlation)                 │
│   - prisma/schema.prisma: 1/4 stories (25% correlation)          │
│                                                                  │
│ Pattern detected:                                                │
│   db/schema.ts → src/types/*.ts (correlation: 1.0)               │
│                                                                  │
│ Threshold check: 1.0 > 0.7 (patternCorrelationThreshold)         │
│ Result: SIGNIFICANT PATTERN                                      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Check Existing Documentation                                     │
├─────────────────────────────────────────────────────────────────┤
│ Searching AGENTS.md for "schema" + "types"...                    │
│ Result: NOT DOCUMENTED                                           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Update AGENTS.md                                                 │
├─────────────────────────────────────────────────────────────────┤
│ Section: Gotchas                                                 │
│ Entry added:                                                     │
│ - **[2024-01-15] US-010:** Schema changes (`db/schema.ts`)       │
│   require updating type definitions in `src/types/`              │
│   (auto-detected, 100% correlation across 4 stories)             │
└─────────────────────────────────────────────────────────────────┘

Console output:
📊 Pattern detected: File co-modification
   db/schema.ts → src/types/*.ts (100% correlation)
   Added to AGENTS.md Gotchas: "Schema changes require type updates"
```

**Resulting prd.json learning section:**

```json
{
  "learning": {
    "patternsDiscovered": [
      {
        "type": "file-co-modification",
        "sourceFile": "db/schema.ts",
        "targetPattern": "src/types/*.ts",
        "correlation": 1.0,
        "observedIn": ["US-001", "US-003", "US-008", "US-010"],
        "recommendation": "Schema changes require updating type definitions",
        "discoveredAt": "2024-01-15T14:30:00Z"
      }
    ]
  }
}
```

---

### Example 4: Command Discovery

When a new command is used that's not documented:

**Scenario:** During US-007, developer runs `npm run db:seed` which isn't in AGENTS.md

```
Command Execution:
$ npm run db:seed

AUTO-LEARNING TRACE:
┌─────────────────────────────────────────────────────────────────┐
│ Step 1: Track Command Usage                                      │
├─────────────────────────────────────────────────────────────────┤
│ Command detected: npm run db:seed                                │
│ Context: US-007 implementation                                   │
│ Exit code: 0 (success)                                           │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Step 2: Check Documentation                                      │
├─────────────────────────────────────────────────────────────────┤
│ Searching AGENTS.md Commands section...                          │
│ Found commands: typecheck, test, lint, build, dev                │
│ "db:seed" NOT FOUND                                              │
│                                                                  │
│ Verify in package.json:                                          │
│   "scripts": {                                                   │
│     "db:seed": "tsx scripts/seed.ts"  ← EXISTS                   │
│   }                                                              │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Step 3: Check Learning Config                                    │
├─────────────────────────────────────────────────────────────────┤
│ requireApprovalFor: ["commands"]                                 │
│ Result: REQUIRES USER APPROVAL                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│ Step 4: Prompt User                                              │
├─────────────────────────────────────────────────────────────────┤
│ 📝 New command discovered: `npm run db:seed`                     │
│                                                                  │
│ This command was used during US-007 but isn't documented in      │
│ AGENTS.md. Would you like to add it?                             │
│                                                                  │
│ A. Add to Commands section                                       │
│ B. Skip (don't add)                                              │
│ C. Add and mark as "Development only"                            │
└─────────────────────────────────────────────────────────────────┘

User selects: A

┌─────────────────────────────────────────────────────────────────┐
│ Step 5: Update AGENTS.md                                         │
├─────────────────────────────────────────────────────────────────┤
│ Section: Commands                                                │
│ Entry added:                                                     │
│ | Seed DB | `npm run db:seed` | No | _(discovered US-007)_ |     │
└─────────────────────────────────────────────────────────────────┘

Console output:
📝 Command documented: `npm run db:seed` added to AGENTS.md Commands
```

---

### Example 5: Learning Metrics Dashboard

After completing a feature, view learning progress:

```bash
$ cat prd.json | jq '.learning'
```

```json
{
  "enabled": true,
  "autoUpdateAgentsMd": true,
  "errorPatterns": [
    {
      "signature": "ts2307-module-components",
      "category": "missing-module",
      "message": "Cannot find module '@/components/...'",
      "occurrences": 4,
      "solutionAppliedCount": 3,
      "storiesAffected": ["US-003", "US-005", "US-008", "US-012"]
    },
    {
      "signature": "ts2339-property-undefined",
      "category": "missing-property",
      "message": "Property 'X' does not exist on type",
      "occurrences": 2,
      "solutionAppliedCount": 1,
      "storiesAffected": ["US-006", "US-009"]
    }
  ],
  "patternsDiscovered": [
    {
      "type": "file-co-modification",
      "sourceFile": "db/schema.ts",
      "targetPattern": "src/types/*.ts",
      "correlation": 1.0
    },
    {
      "type": "import-pattern",
      "pattern": "@radix-ui/dialog",
      "usedIn": ["src/components/Modal.tsx", "src/components/Confirm.tsx"]
    }
  ],
  "metrics": {
    "totalErrorsEncountered": 18,
    "uniqueErrorPatterns": 6,
    "autoResolvedCount": 8,
    "newGotchasAdded": 5,
    "newConventionsAdded": 2,
    "commandsDiscovered": 1,
    "learningEffectiveness": 0.78
  }
}
```

**Visual Summary:**

```
╔═══════════════════════════════════════════════════════════════════╗
║                    AUTO-LEARNING SUMMARY                           ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                    ║
║  Errors Encountered:    18                                         ║
║  Unique Patterns:       6                                          ║
║  Auto-Resolved:         8 (44%)                                    ║
║                                                                    ║
║  AGENTS.md Updates:                                                ║
║    • Gotchas added:     5                                          ║
║    • Conventions added: 2                                          ║
║    • Commands added:    1                                          ║
║                                                                    ║
║  Top Recurring Issues:                                             ║
║    1. Missing module imports (4 occurrences)                       ║
║    2. Missing property on type (2 occurrences)                     ║
║                                                                    ║
║  Patterns Discovered:                                              ║
║    • Schema → Types co-modification (100% correlation)             ║
║    • @radix-ui/dialog import pattern                               ║
║                                                                    ║
║  Learning Effectiveness: 78%                                       ║
║  (Auto-resolved / Total errors where solution was available)       ║
║                                                                    ║
╚═══════════════════════════════════════════════════════════════════╝
```

---

### Example 6: AGENTS.md After Auto-Learning

After running multiple stories with auto-learning enabled:

```markdown
<!-- Auto-Learning Enabled: Entries tagged (auto-learned) are added automatically -->

# AGENTS.md - TaskApp

## Quick Commands

| Action    | Command             | Required | Notes                 |
| --------- | ------------------- | -------- | --------------------- |
| Typecheck | `npm run typecheck` | Yes      |                       |
| Test      | `npm run test`      | Yes      |                       |
| Lint      | `npm run lint`      | Yes      |                       |
| Build     | `npm run build`     | No       |                       |
| Seed DB   | `npm run db:seed`   | No       | _(discovered US-007)_ |

## Stack

- **Runtime:** Node.js 20.x
- **Framework:** Next.js 14 (App Router)
- **Database:** PostgreSQL with Drizzle ORM

## Conventions

### Project-Specific

- Server actions return `{ success: boolean, data?: T, error?: string }`
- **Modal Components:** Use `@radix-ui/dialog` with controlled state _(auto-detected from US-007)_
- **Form Validation:** Use Zod schemas shared between client/server _(auto-detected from US-004)_

## Gotchas

- Must run `npm run db:generate` after schema changes
- Server actions need `revalidatePath()` after mutations
- **[2024-01-15] US-003:** `Cannot find module '@/components/...'` → Verify component exists or create missing file (recurring, 4 occurrences)
- **[2024-01-15] US-006:** Property does not exist on type → Check type definitions match database schema (auto-learned)
- **[2024-01-15] US-010:** Schema changes (`db/schema.ts`) require updating type definitions in `src/types/` (auto-detected, 100% correlation across 4 stories)
- **[2024-01-16] US-014:** Form validation errors don't clear on submit → Call `reset()` after successful submission (auto-learned)

---

_Last updated: 2024-01-16 (includes 5 auto-learned entries)_
```

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

### Enable Parallel Mode

```bash
# Add parallelConfig to existing prd.json
cat prd.json | jq '. + {
  "parallelConfig": {
    "enabled": true,
    "maxConcurrent": 3,
    "conflictStrategy": "git-merge-fallback"
  }
}' > prd.json.tmp && mv prd.json.tmp prd.json
```

### Check Wave Status

```bash
# View completed waves
cat prd.json | jq '.waves[] | {id, status, stories, duration}'

# View current wave progress
cat prd.json | jq '.waves[] | select(.status == "in_progress")'
```

### View Parallelization Stats

```bash
# Calculate speedup
cat prd.json | jq '{
  totalWaves: (.waves | length),
  parallelWaves: ([.waves[] | select(.parallel == true)] | length),
  totalDuration: ([.waves[].duration] | add),
  storiesPerWave: ([.waves[].stories | length] | add / (.waves | length))
}'
```
