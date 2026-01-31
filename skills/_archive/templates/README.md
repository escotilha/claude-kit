# Skill Templates

This directory contains reusable templates for building Agent-native Architecture skills.

---

## Available Templates

### 1. context-template.md
**Purpose**: Session state and continuity management for skills

**Use When**:
- Building skills that need to remember state between sessions
- Creating multi-step workflows that span conversations
- Developing skills that make decisions that should be logged
- Working on projects with specific user preferences

**Key Sections**:
- Who I Am (skill identity)
- What I Know About This User (preferences)
- What Exists (filesystem cache)
- Recent Activity (action log)
- My Guidelines (project rules)
- Current State (pending tasks)

**See**: `context-usage-guide.md` for detailed integration instructions

---

## Quick Start

### For Skill Developers

1. **Copy the template**:
   ```bash
   cp ~/Library/Mobile\ Documents/com~apple~CloudDocs/claude-setup/skills/templates/context-template.md ./context.md
   ```

2. **Customize for your skill**:
   - Fill in "Who I Am" section with skill identity
   - Define what state needs to persist
   - Add skill-specific sections if needed

3. **Integrate into skill workflow**:
   ```markdown
   ## On Session Start
   1. Check for context.md in project root
   2. If exists, load and parse
   3. If not, create from template

   ## During Session
   - Update when significant actions occur
   - Log decisions in "Current State"

   ## On Session End
   - Update "Recent Activity"
   - Update "Last Sync" timestamp
   ```

4. **Reference the usage guide**:
   See `context-usage-guide.md` for:
   - Best practices
   - Integration patterns
   - Troubleshooting
   - Example implementations

---

## Template Philosophy

These templates follow **Agent-native Architecture** principles:

### 1. State Persistence
Skills should maintain continuity across sessions without requiring users to repeat context.

### 2. Memory Integration
Templates work alongside the memory system (see `memory-strategy.md`):
- **Context**: Session-specific, project-local state
- **Memory**: Long-term, cross-project learnings

### 3. Handoff Readiness
Templates enable smooth transitions between:
- Different skills working on the same project
- Sessions with time gaps
- Human and AI collaboration

### 4. Discovery Caching
Reduces redundant filesystem exploration by caching:
- File structure
- Project configuration
- Recent changes

### 5. Decision Logging
Captures the "why" behind actions:
- Architecture decisions
- Trade-offs considered
- User preferences applied

---

## Template Usage by Skill Type

### Long-running Development Skills
**Examples**: `cto`, `cpo-ai-skill`, `parallel-dev`

**Context Use**: Heavy
- Track architectural decisions
- Log multi-session progress
- Maintain feature state across worktrees

### Testing/QA Skills
**Examples**: `testing-agent`, `fulltest-skill`

**Context Use**: Moderate
- Track test coverage
- Log found bugs
- Remember flaky tests

### One-shot Utility Skills
**Examples**: `cp`, `maketree`

**Context Use**: Minimal/None
- Stateless operations
- No session continuity needed

### Research/Analysis Skills
**Examples**: `mna-triage-analyzer`, `financial-data-extractor`

**Context Use**: Moderate
- Cache analysis results
- Log evaluation criteria
- Track processed documents

---

## Directory Structure Recommendations

### Single Project
```
my-project/
├── context.md              # Primary context at root
├── .claude/
│   └── keybindings.json
├── src/
└── tests/
```

### Multi-skill Project
```
my-project/
├── .claude/
│   ├── context.md          # Shared context
│   └── skills/
│       ├── cto/
│       │   └── context.md  # CTO-specific state
│       └── testing-agent/
│           └── context.md  # Testing-specific state
├── src/
└── tests/
```

### Skill Discovery Priority
1. `./context.md` (project root)
2. `./.claude/context.md` (shared)
3. `./.claude/skills/{skill-name}/context.md` (skill-specific)

---

## Integration with Global Rules

Context templates complement global instructions:

| Global Rule | Context Section | Purpose |
|-------------|-----------------|---------|
| `coding-standards.md` | My Guidelines | Project-specific coding rules |
| `git-conventions.md` | Recent Activity | Log commits and branches |
| `memory-strategy.md` | What I Know | Reference memory entities |
| `security-rules.md` | My Guidelines | Security constraints |

### Example Integration
```markdown
## My Guidelines

### From Global Rules
- Follow coding-standards.md (TypeScript strict mode)
- Respect git-conventions.md (conventional commits)
- Apply security-rules.md (never commit secrets)

### From Memory
- pattern:early-returns (from cto skill)
- preference:async-await-over-promises (user preference)

### Project-Specific
- This project uses custom auth flow (see src/auth/README.md)
- Database migrations require manual approval
```

---

## Best Practices

### DO:
- ✅ Keep context.md under 500 lines
- ✅ Use timestamps for time-sensitive information
- ✅ Reference memory entities instead of duplicating
- ✅ Update "Last Sync" when modifying context
- ✅ Archive old activity logs when they grow large

### DON'T:
- ❌ Store sensitive information (credentials, API keys)
- ❌ Duplicate information from memory or codebase
- ❌ Create context for trivial one-off tasks
- ❌ Let context become stale (check timestamps)
- ❌ Ignore existing context when starting sessions

---

## Contributing New Templates

When creating new templates:

1. **Identify the pattern**: What problem does it solve?
2. **Design the structure**: What sections are needed?
3. **Write usage guide**: How should skills use it?
4. **Add examples**: Show real-world usage
5. **Test integration**: Verify with existing skills
6. **Document**: Update this README

### Template Checklist
- [ ] Clear purpose and use cases
- [ ] Commented sections explaining each part
- [ ] Integration instructions
- [ ] Example usage
- [ ] Best practices
- [ ] Troubleshooting guidance

---

## Future Templates (Roadmap)

### Planned Templates:
1. **skill-config-template.json** - Standardized skill configuration
2. **workflow-template.md** - Multi-stage workflow orchestration
3. **handoff-template.md** - Inter-skill communication
4. **test-report-template.md** - Standardized test reporting
5. **architecture-decision-template.md** - ADR format for context
6. **swarm-coordinator-template.md** - Swarm orchestration state

---

## Questions & Support

### Where to Learn More:
- **Usage Guide**: `context-usage-guide.md` (detailed integration)
- **Memory Strategy**: `../rules/memory-strategy.md` (memory vs context)
- **Example Skills**: Check `cto`, `testing-agent`, `cpo-ai-skill` implementations

### Common Questions:

**Q: When should I use context.md vs memory?**
A: Context is session-local and project-specific. Memory is long-term and cross-project. Use context for state, memory for learnings.

**Q: How often should context be updated?**
A: Update during session when significant actions occur. Always update on session end.

**Q: Can multiple skills share one context.md?**
A: Yes, use `.claude/context.md` for shared context. Skills can also have individual contexts in `.claude/skills/{name}/`.

**Q: What if context becomes too large?**
A: Archive old "Recent Activity" to `.claude/archive/` and keep only recent entries.

---

## Version History

- **v1.0** (2026-01-30): Initial release
  - context-template.md
  - context-usage-guide.md
  - This README

---

**Maintained By**: memory-consolidation skill
**Last Updated**: 2026-01-30
**Location**: `~/Library/Mobile Documents/com~apple~CloudDocs/claude-setup/skills/templates/`
