# Autonomous Agent Skill

A Claude Code skill that breaks features into small, testable user stories and implements them autonomously with fresh context per iteration. Features automatic learning from errors and patterns.

**Version:** 1.2.0

## Quick Start

```bash
git clone git@yourcompany.com:tools/autonomous-agent-skill.git
cd autonomous-agent-skill
./install.sh
```

## What It Does

Instead of trying to build an entire feature in one shot, this skill:

1. **Creates a PRD** - Asks clarifying questions, then generates a Product Requirements Document
2. **Splits into stories** - Breaks the feature into small, right-sized user stories
3. **Implements autonomously** - Works through each story one at a time, committing as it goes
4. **Self-verifies** - Runs typecheck/tests after each story, handles failures
5. **Learns automatically** - Captures error patterns and solutions, updates documentation

### Memory Between Iterations

The agent maintains state through files:

- `prd.json` - Task list with completion status and learning data
- `progress.md` - Learnings and implementation notes
- `AGENTS.md` - Long-term patterns for the repository (auto-updated)
- Git history - All code changes

## Usage

### Start with an inline goal (recommended)

Provide your goal directly with the command:

```
/autonomous-agent create a login system for this project
```

Or describe it naturally:

```
I want /autonomous-agent to add user notifications
```

**What happens:**

1. Agent analyzes your codebase for existing related code
2. Shows what it found (existing files, patterns, gaps)
3. Asks targeted clarifying questions based on findings
4. Generates a PRD tailored to your codebase

### Start without a goal (interactive)

```
/autonomous-agent
```

The agent will ask what you want to build, then proceed.

### Resume work

If you have an existing `prd.json`, the agent picks up where it left off.

### Commands during execution

| Command        | What it does                         |
| -------------- | ------------------------------------ |
| `status`       | Show current progress and next story |
| `skip`         | Skip current story, move to next     |
| `pause`        | Stop autonomous mode, wait for input |
| `retry`        | Retry the current story              |
| `parallel on`  | Enable parallel execution            |
| `parallel off` | Disable parallel execution           |
| `learning on`  | Enable auto-learning (default)       |
| `learning off` | Disable auto-learning                |

## How Stories Are Sized

Right-sized (1 iteration):

- Add a database column
- Create single API endpoint
- Add UI component to existing page

Too big (needs splitting):

- Build entire dashboard
- Add authentication system
- Complete feature end-to-end

**Rule:** If you can't describe the change in 2-3 sentences, split it.

## Example Flow

### With Inline Goal (Recommended)

```
You: /autonomous-agent create a login system

Agent: I'll help you create a login system. I analyzed the codebase and found:

Existing:
✓ Auth.js configured in lib/auth.ts
✓ User table with email/password columns
✓ Middleware for protected routes

Missing:
✗ Login page UI
✗ Registration flow

Based on this, a few questions:

1. Auth features?
   A. Login only (quick win)
   B. Login + Registration
   C. Full flow with password reset

2. UI approach?
   A. Dedicated pages at /login, /register (Recommended)
   B. Modal dialogs

Reply with: "1B, 2A"

You: 1B, 2A

Agent: Creating PRD with 4 user stories...
[Creates tasks/prd-login-system.md]

Please review. Reply "approved" to begin.

You: approved

Agent: Converting to prd.json, starting US-001...
[Implements each story, commits, moves to next]
...
Feature complete! 4 stories done in 4 commits.
```

### Without Inline Goal

```
You: /autonomous-agent

Agent: What feature would you like to build?

You: Add task priority to the app

Agent: I'll help you build task priority. First, a few questions:
[... continues with analysis and questions ...]
```

## Files Created

| File             | Purpose                                    |
| ---------------- | ------------------------------------------ |
| `tasks/prd-*.md` | Human-readable PRD                         |
| `prd.json`       | Machine-readable task list + learning data |
| `progress.md`    | Append-only learnings                      |
| `AGENTS.md`      | Long-term repo patterns (auto-updated)     |

## Auto-Learning

The agent automatically learns from its interactions and improves over time.

### What It Learns

| Trigger             | What Happens                               |
| ------------------- | ------------------------------------------ |
| Verification fails  | Parses error, captures solution when fixed |
| Same error 2+ times | Marks as recurring, applies known solution |
| Story completes     | Tracks file co-modification patterns       |
| New command used    | Offers to add to AGENTS.md                 |

### How It Works

```
Error Occurs → Parse & Classify → Check if Known → Apply or Learn

If NEW error:
  1. Attempt fix
  2. Capture what worked
  3. Add to AGENTS.md with (auto-learned) tag

If KNOWN error:
  1. Apply existing solution automatically
  2. Update occurrence count
```

### Auto-Generated AGENTS.md Entries

After running several stories, your AGENTS.md might include:

```markdown
## Gotchas

- Must run `npm run db:generate` after schema changes
- **[2024-01-15] US-003:** `Cannot find module '@/...'` → Check path aliases (auto-learned)
- **[2024-01-15] US-010:** Schema changes require type updates (auto-detected, 100% correlation)
```

### Learning Metrics

View learning progress:

```bash
cat prd.json | jq '.learning.metrics'
```

```json
{
  "totalErrorsEncountered": 18,
  "uniqueErrorPatterns": 6,
  "autoResolvedCount": 8,
  "learningEffectiveness": 0.78
}
```

### Configuration

Control auto-learning in prd.json:

```json
{
  "learning": {
    "enabled": true,
    "autoUpdateAgentsMd": true,
    "requireApprovalFor": ["commands"],
    "minOccurrencesForRecurring": 2
  }
}
```

## Uninstall

```bash
./uninstall.sh
```

Or manually:

```bash
rm -rf ~/.claude/skills/autonomous-agent
```

## Updating

Pull the latest and reinstall:

```bash
git pull
./install.sh
```

## Git Configuration

The autonomous agent creates working files that you may want to exclude from version control. Add to your `.gitignore`:

```gitignore
# Autonomous agent working files
prd.json
progress.md
tasks/
archive/
```

**Note:** You may want to commit `AGENTS.md` as it contains valuable project-specific patterns.

## Troubleshooting

**Skill not showing up?**

- Restart Claude Code after installation
- Check that `~/.claude/skills/autonomous-agent/SKILL.md` exists

**Agent stuck on a story?**

- Type `skip` to move to next story
- Type `pause` to stop and debug manually

**Want to start fresh?**

- Delete `prd.json` and `progress.md` from your project
- Run `/autonomous-agent` again
