# Context.md Usage Guide for Skills

This guide explains how skills should use the `context.md` file to maintain session state and provide continuity across conversations.

---

## Purpose

The `context.md` file serves as:

1. **Session Memory** - Preserves state between skill invocations
2. **Discovery Cache** - Reduces redundant filesystem exploration
3. **Decision Log** - Records what was decided and why
4. **Handoff Document** - Enables smooth transitions between skills/sessions

---

## When to Use Context.md

### ✅ Use Context for:
- Multi-session projects where state needs to persist
- Complex workflows with many steps
- Projects with specific user preferences to remember
- Collaborative work where multiple skills interact
- Long-running development tasks

### ❌ Skip Context for:
- One-off queries or simple tasks
- Stateless operations (searches, reads)
- Temporary/exploratory work
- User explicitly working in isolation mode

---

## Integration Pattern

Add this section to your skill's main instructions:

```markdown
## Context Management

### On Session Start
1. Check for existing `context.md` in project root or `.claude/` directory
2. If exists:
   - Read and parse for current state
   - Load relevant preferences and recent activity
   - Check for pending tasks
3. If not exists:
   - Decide if this project needs context (see criteria above)
   - If yes, create from template with initial discovery
   - If no, proceed without context file

### During Session
Update `context.md` when:
- **New files created**: Add to "What Exists" section
- **Significant actions complete**: Log in "Recent Activity"
- **User preferences learned**: Add to "What I Know About This User"
- **Decisions made**: Record in "Current State > Decisions Made This Session"
- **Tasks added/completed**: Update "Pending Items" and "Active Tasks"

### On Session End
1. Update "Recent Activity" with session summary
2. Update "Current State" with any pending items
3. Update "Last Sync" timestamp
4. If in git repo and context has changed:
   - Stage context.md
   - Consider auto-committing (based on user preference)
5. Clean up completed tasks from "Pending Items"
```

---

## File Location Strategy

### Priority Order:
1. **Project Root** (`./context.md`) - For single-project work
2. **Claude Directory** (`./.claude/context.md`) - For multi-skill projects
3. **Skill Directory** (`./.claude/skills/{skill-name}/context.md`) - For skill-specific state

### Discovery Logic:
```javascript
// Pseudo-code for context discovery
async function findContext(skillName) {
  const locations = [
    './context.md',
    './.claude/context.md',
    `./.claude/skills/${skillName}/context.md`
  ];

  for (const path of locations) {
    if (await exists(path)) {
      return await read(path);
    }
  }

  return null; // No context exists
}
```

---

## Context Sections Explained

### Who I Am
- **Static** - Set once when context is created
- Identifies which skill/agent owns this context
- Helps with handoffs between skills

### What I Know About This User
- **Dynamic** - Updated as preferences are learned
- Should query `mcp__memory__*` for user preferences
- Includes communication style, tool preferences, etc.

### What Exists
- **Semi-dynamic** - Updated when files are created/deleted
- Caches filesystem state to avoid repeated discovery
- Refresh when:
  - User explicitly asks to "refresh context"
  - Files are added/removed
  - More than 1 hour since last update

### Recent Activity
- **Dynamic** - Updated throughout session
- Append-only log of actions
- Keep last 10-20 entries, archive older ones

### My Guidelines
- **Semi-static** - Set from project config and user preferences
- References memory entities like `preference:*` and `pattern:*`
- Update when user provides new guidelines

### Current State
- **Dynamic** - Constantly updated
- Most important for session continuity
- Always update before ending session

---

## Best Practices

### DO:
- Keep context.md concise (under 500 lines)
- Use timestamps for all time-sensitive entries
- Reference memory entities instead of duplicating content
- Archive old "Recent Activity" to separate file if growing large
- Use bullet points and checkboxes for scannability

### DON'T:
- Duplicate information that exists in memory or codebase
- Store sensitive information (credentials, API keys)
- Create context for trivial/one-off tasks
- Let context become stale (update timestamps)
- Ignore existing context when starting a session

---

## Example: Context-Aware Session Start

```markdown
## On invocation, the skill should:

1. **Discover Context**
   ```bash
   # Check for context file
   if [ -f "./context.md" ]; then
     echo "Found existing context"
   fi
   ```

2. **Load User Preferences**
   ```javascript
   // Query memory for preferences
   const userPrefs = await mcp__memory__search_nodes({
     query: "preference:"
   });
   ```

3. **Resume State**
   ```markdown
   Based on context.md:
   - Last session: 2026-01-29 14:30
   - Pending: Fix authentication bug in login flow
   - Active project: contably
   - User preference: Prefers async/await over promises
   ```

4. **Acknowledge Continuity**
   ```
   "I see we were working on the authentication bug in contably.
   You prefer async/await syntax. Should I continue with the fix?"
   ```
```

---

## Context Lifecycle

```
┌─────────────────┐
│  Skill Invoked  │
└────────┬────────┘
         │
         ▼
    ┌─────────┐
    │ Context │ ─── No ──► Create Context?
    │ Exists? │               │
    └────┬────┘               │
         │                    │
        Yes              ┌────┴────┐
         │               │  Yes    │ No (skip)
         │               ▼         │
         │         ┌──────────┐    │
         │         │  Create  │    │
         │         │ from     │    │
         │         │ Template │    │
         │         └────┬─────┘    │
         │              │          │
         ▼              ▼          │
    ┌─────────────────────────┐   │
    │   Load & Parse Context  │◄──┘
    └───────────┬─────────────┘
                │
                ▼
    ┌─────────────────────────┐
    │   Work on User Task     │
    │   (Update as needed)    │
    └───────────┬─────────────┘
                │
                ▼
    ┌─────────────────────────┐
    │   Session End:          │
    │   - Update Recent       │
    │   - Update Current      │
    │   - Sync timestamp      │
    └─────────────────────────┘
```

---

## Integration with Memory System

Context.md **complements** the memory system, not replaces it:

| Context.md | Memory System |
|------------|---------------|
| Session-specific state | Long-term learnings |
| Project-local information | Cross-project patterns |
| Pending tasks & decisions | Validated best practices |
| File/directory structure | User preferences |
| Temporary notes | Mistakes to avoid |

**Golden Rule**: Context references memory entities, memory doesn't reference context.

Example in context.md:
```markdown
## My Guidelines
- Follow pattern:early-returns (from memory)
- User prefers preference:typescript-strict-mode (from memory)
- This project uses custom preference:contably-api-structure (project-specific)
```

---

## Troubleshooting

### Context is stale
- Check "Last Sync" timestamp
- If > 24 hours, ask user: "Context is from [date]. Should I refresh?"
- Refresh "What Exists" section

### Context is too large
- Archive old "Recent Activity" to `.claude/archive/activity-log.md`
- Keep only last 10 entries in context.md

### Multiple contexts found
- Prioritize: project root > .claude/ > skill-specific
- Ask user which to use if ambiguous

### Context conflicts with current state
- Git branch changed: Update context or ask which branch to work on
- Files missing: Refresh "What Exists" section
- User contradicts context preference: Update context, ask if permanent change

---

## Example Implementations

See these skills for reference implementations:
- `cto` - Uses context for architecture decisions tracking
- `website-design` - Uses context for design system evolution
- `testing-agent` - Uses context for test suite state
- `cpo-ai-skill` - Uses context for epic/milestone tracking

---

## Quick Reference

```bash
# Create context from template
cp ~/Library/Mobile\ Documents/com~apple~CloudDocs/claude-setup/skills/templates/context-template.md ./context.md

# Typical context locations
./context.md                              # Project root
./.claude/context.md                      # Claude directory
./.claude/skills/{skill-name}/context.md  # Skill-specific
```

```markdown
# Typical session flow comments in skill code
# 1. Load context if exists
# 2. Query memory for user preferences
# 3. Discover current state (git, files)
# 4. Present summary to user
# 5. Execute task
# 6. Update context with changes
# 7. Sync context before ending
```

---

**Last Updated**: 2026-01-30
**Version**: 1.0
**Maintained By**: memory-consolidation skill
