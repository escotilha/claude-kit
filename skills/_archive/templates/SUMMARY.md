# Context Template System - Summary

Created: 2026-01-30

## What Was Created

This template system provides a standardized way for skills to maintain session state and continuity using the Agent-native Architecture pattern.

### Files Created

1. **context-template.md** (2.1KB)
   - Base template for creating context.md files
   - Standard sections: Who I Am, What I Know, What Exists, Recent Activity, My Guidelines, Current State
   - Ready to copy and customize for any skill

2. **context-usage-guide.md** (9.4KB)
   - Comprehensive integration guide
   - When to use context vs skip
   - Session lifecycle management
   - Memory integration patterns
   - Best practices and troubleshooting

3. **integration-example.md** (11KB+)
   - Before/after examples showing integration
   - Three detailed examples: simple dev skill, testing skill, orchestrator skill
   - Common patterns (progress tracking, decision logs, blockers)
   - Integration checklist
   - Troubleshooting guide

4. **README.md** (7.6KB)
   - Overview of template system
   - Quick start guide
   - Philosophy and principles
   - Usage by skill type
   - Directory structure recommendations

## Key Concepts

### Context vs Memory
- **Context**: Session-specific, project-local state (context.md)
- **Memory**: Long-term, cross-project learnings (MCP memory system)

### Context Locations (Priority Order)
1. `./context.md` - Project root (single project)
2. `./.claude/context.md` - Shared across skills
3. `./.claude/skills/{skill-name}/context.md` - Skill-specific

### Session Lifecycle
```
Session Start → Load Context → Query Memory → Work → Update Context → Session End
```

## When Skills Should Use Context

### ✅ Use Context For:
- Multi-session projects with persistent state
- Complex workflows with many steps
- Projects with specific user preferences
- Collaborative work between skills
- Long-running development tasks

### ❌ Skip Context For:
- One-off queries or simple tasks
- Stateless operations
- Temporary/exploratory work
- Explicitly isolated work

## Integration Pattern

Skills should add this section:

```markdown
## Context Management

### On Session Start
1. Check for context.md
2. If exists: Load and parse
3. If not: Create from template (if project needs it)

### During Session
Update when significant actions occur

### On Session End
1. Update Recent Activity
2. Update Current State
3. Update Last Sync timestamp
```

## Example Skills That Should Integrate

### High Priority (Long-running, stateful):
- `cto` - Track architecture decisions
- `cpo-ai-skill` - Track epic/stage progress
- `parallel-dev` - Track worktree states
- `testing-agent` - Track test coverage and bugs
- `fulltest-skill` - Track test results across sessions

### Medium Priority (Session state valuable):
- `website-design` - Track design decisions
- `mna-toolkit` - Track deal analysis state
- `run-local` - Track service health

### Low Priority (Mostly stateless):
- `cp` - Quick commit/push, no state
- `maketree` - One-off worktree creation
- `triage-analyzer` - Single analysis, no continuity

## Benefits of Using Context

1. **Session Continuity**: Resume work seamlessly after interruptions
2. **Decision Logging**: Audit trail of what was decided and why
3. **Reduced Redundancy**: No need to re-explain context each session
4. **Handoff Ready**: Easy transitions between skills or humans
5. **Progress Visibility**: Clear status of multi-stage work
6. **Blocker Tracking**: Document what's waiting and why

## Next Steps for Implementation

### For Skill Developers:
1. Review `integration-example.md` for your skill type
2. Copy `context-template.md` to project
3. Add Context Management section to skill
4. Test session resume functionality

### For Memory Consolidation:
1. Track which skills have integrated context
2. Monitor context health across projects
3. Consolidate patterns that emerge from context usage
4. Update memory-strategy.md with context patterns

### For Users:
1. No action required - skills will manage context automatically
2. If context feels stale, ask skill to "refresh context"
3. Context files are safe to read/edit manually
4. Can disable context per-project with `.claude/no-context` flag

## Integration Status

| Skill | Context Status | Priority |
|-------|---------------|----------|
| cto | ⏳ Not yet integrated | HIGH |
| cpo-ai-skill | ⏳ Not yet integrated | HIGH |
| testing-agent | ⏳ Not yet integrated | HIGH |
| fulltest-skill | ⏳ Not yet integrated | HIGH |
| parallel-dev | ⏳ Not yet integrated | HIGH |
| website-design | ⏳ Not yet integrated | MEDIUM |
| mna-toolkit | ⏳ Not yet integrated | MEDIUM |
| run-local | ⏳ Not yet integrated | MEDIUM |
| cp | N/A (stateless) | SKIP |
| maketree | N/A (one-off) | SKIP |

## Files Location

```
~/Library/Mobile Documents/com~apple~CloudDocs/claude-setup/skills/templates/
├── context-template.md         # Base template
├── context-usage-guide.md      # Integration guide
├── integration-example.md      # Before/after examples
├── README.md                   # System overview
└── SUMMARY.md                  # This file
```

## Usage Example

```bash
# For a skill developer
cd ~/my-skill-project
cp ~/Library/Mobile\ Documents/com~apple~CloudDocs/claude-setup/skills/templates/context-template.md ./context.md

# Edit context.md:
# 1. Fill in "Who I Am" section
# 2. Add custom sections if needed
# 3. Reference from skill instructions

# For a project using skills
cd ~/my-project
# Skill will auto-create context.md on first run (if configured)
# Or manually create:
cp ~/Library/Mobile\ Documents/com~apple~CloudDocs/claude-setup/skills/templates/context-template.md ./.claude/context.md
```

## Maintenance

This template system should be:
- Reviewed quarterly for improvements
- Updated when new patterns emerge
- Referenced in skill development guides
- Integrated with memory consolidation

---

**Created By**: Agent-native Architecture initiative
**Maintained By**: memory-consolidation skill
**Version**: 1.0
**Last Updated**: 2026-01-30
