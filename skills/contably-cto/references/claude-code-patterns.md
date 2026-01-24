# Claude Code Patterns for ContaBILY

## Context Management

### The Core Constraint
Claude's context window fills up fast. Performance degrades as it fills. Design everything around this constraint.

### CLAUDE.md Best Practices

Keep it concise and human-readable:

```markdown
# Project Name

## Commands
npm run build    # Build project
npm run test     # Run tests
npm run lint     # Lint code

## Code Style
- ES modules (import/export), not CommonJS
- Destructure imports when possible
- Portuguese for tax domain terms

## Key Patterns
- Money as integers (centavos)
- Dates in ISO 8601
- [Framework-specific patterns]

## Non-Obvious Behaviors
- [Edge cases]
- [Known issues]
```

### Hierarchical CLAUDE.md

```
project/
├── CLAUDE.md              # Global rules
├── src/
│   └── CLAUDE.md          # Source conventions
├── tests/
│   └── CLAUDE.md          # Test patterns
└── packages/tax-engine/
    └── CLAUDE.md          # Tax-specific rules
```

Claude merges these based on working directory.

## Thinking Levels

Trigger extended thinking with specific words:

| Keyword | Budget | Use Case |
|---------|--------|----------|
| "think" | Low | Standard tasks |
| "think hard" | Medium | Complex logic |
| "think harder" | High | Architecture decisions |
| "ultrathink" | Maximum | Critical system design |

Example:
> "I need to design the multi-tenant data isolation strategy. Ultrathink about the trade-offs between row-level security vs schema-per-tenant vs database-per-tenant."

## Subagents

Create specialized agents in `.claude/agents/`:

```yaml
# .claude/agents/security-reviewer.md
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---

You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

Invoke with: "Use a subagent to review this code for security issues."

### ContaBILY Subagent Suggestions

```
.claude/agents/
├── tax-compliance-reviewer.md    # Validate tax calculations
├── security-auditor.md           # Financial data security
├── database-architect.md         # Schema design review
├── api-designer.md               # REST/GraphQL patterns
└── brazil-regulations.md         # Compliance validation
```

## Workflow Patterns

### Test-Driven Development (TDD)

Powerful with agentic coding:

1. "Write tests for [feature] based on these expected behaviors. We're doing TDD, so don't create mock implementations."
2. "Run the tests and confirm they fail."
3. "Now implement the feature to make the tests pass."
4. "Commit the tests first, then the implementation."

### Plan-Then-Execute

For complex features:

1. "Read the relevant code and create a plan for implementing [feature]. Don't write any code yet."
2. "Think hard about edge cases and potential issues."
3. "Now implement phase 1 of the plan."
4. "Run tests and verify."
5. "Continue to phase 2..."

### Git Workflow

Claude handles 90%+ of git:

- "Create a branch for this feature"
- "What changes made it into v1.2.3?"
- "Write a commit message for these changes"
- "Rebase this onto main"

## Context Preservation

### For Long Sessions

Use `/clear` between different tasks to prevent context pollution.

### For Multi-Session Work

Maintain state in files:
- `progress.txt` - What was done, learnings
- `AGENTS.md` - Long-term patterns (repo-level)
- `prd.json` - Task status for autonomous loops

### Compaction Strategy

When context gets large:
1. Summarize completed work
2. Archive detailed logs
3. Keep only active context

## Multi-Agent Patterns

### Sequential Pipeline
```
Parser Agent → Extractor Agent → Validator Agent
```
Each writes to shared state, next reads from it.

### Parallel Execution
```
Tax Calculator Agent ─┐
                      ├→ Aggregator Agent
Report Generator Agent┘
```
Use git worktrees for parallel, isolated sessions.

### Human-in-the-Loop
For high-stakes actions (financial transactions, production deployments):
```
Agent works → Reaches checkpoint → Pauses for approval → Continues
```

## Automation Patterns

### Headless Mode
```bash
# For CI/CD pipelines
claude --dangerously-skip-permissions "Run tests and report results"
```
Only use in sandboxed environments.

### Hooks
Run scripts at lifecycle events:
- Pre-tool-use
- Post-tool-use
- Pre-commit
- Post-error

## Performance Tips

1. **Start fresh conversations** for each distinct task
2. **Be specific** about what you want
3. **Provide context upfront** rather than drip-feeding
4. **Use file references** instead of pasting large content
5. **Ask Claude to explore** the codebase for onboarding questions

## Common Mistakes to Avoid

| Mistake | Better Approach |
|---------|-----------------|
| Vague "fix this" prompts | Explain what went wrong and expected behavior |
| Accepting all changes blindly | Review Claude's explanations before approving |
| One giant prompt | Break into phases |
| Ignoring test failures | Stop and fix before continuing |
| Not using thinking levels | Match thinking to complexity |
