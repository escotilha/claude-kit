# CPO AI Skill

**Chief Product Officer AI** - Transform product ideas into production-ready applications.

## Quick Start: `/cpo-go`

```bash
/cpo-go <project-name> <description>   # Start new product
/cpo-go help                            # Show quick reference
/cpo-go status                          # Show project progress
```

### Examples

```bash
/cpo-go game create an interactive tic-tac-toe game
/cpo-go taskflow build a task management app for small teams
/cpo-go artmarket create a marketplace where artists can sell digital art
```

### Fast Mode

Reply `"go"` to use defaults and start immediately:
- Creates **public GitHub repo** with project name
- **MVP** scope
- **Web app** (Next.js + Supabase)
- **Speed** priority

### Commands During Execution

| Command | Action |
|---------|--------|
| `go` | Use defaults, start immediately |
| `approved` | Approve phase, continue |
| `pause` | Stop execution |
| `resume` | Continue from checkpoint |
| `skip stage` | Skip current stage |
| `replan` | Go back and adjust plan |

---

## Overview

The CPO AI Skill orchestrates the entire product development lifecycle:

1. **Discovery** - Qualify ideas through strategic questions
2. **Planning** - Break down into epics, stages, and stories
3. **Execution** - Implement stage-by-stage with testing
4. **Validation** - Full project integration testing
5. **Delivery** - Documentation and go-live

## Alternative Triggers

You can also activate with:
- "cpo mode"
- "build this product"
- "chief product officer"
- "idea to production"

Then describe your product idea.

## Workflow

```
Product Idea → Discovery Questions → Strategic Plan → Stage Implementation → Testing → Documentation → Go Live
```

## Key Files Generated

| File | Purpose |
|------|---------|
| `master-project.json` | Complete project state and progress |
| `cpo-progress.md` | Detailed progress log |
| `docs/user-guide.md` | End-user documentation |
| `docs/technical-docs.md` | Developer documentation |

## Specialized Subagents

The CPO AI orchestrates three specialized agents for best-in-class results:

| Agent | Purpose | Based On |
|-------|---------|----------|
| **Product Research Agent** | Market research, competitor analysis, design references | [Anthropic Research Agent](https://github.com/anthropics/claude-agent-sdk-demos) |
| **CTO Advisor Agent** | Tech stack selection, architecture, deployment strategy | Best practices from [wshobson/agents](https://github.com/wshobson/agents) |
| **Frontend Design Agent** | Distinctive, production-grade UI | [Anthropic Frontend Design Plugin](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) |

## Integration

Works with:
- **autonomous-dev** - Story-level implementation
- **fulltest-skill** - Comprehensive testing
- **worktree-scaffold** - Isolated stage development

## Example

```
User: /cpo-go taskflow build a task management app for small teams

CPO AI: Quick Discovery for "taskflow"...
User: go

CPO AI:
1. [Research Agent] Analyzes Asana, Linear, Notion for best practices
2. [Research Agent] Collects design references and UI patterns
3. [CTO Agent] Recommends Next.js + Supabase stack with deployment guide
4. Creates strategic plan with 5 epics, 12 stages
5. Implements Stage 1: Project Setup
6. [Frontend Agent] Creates distinctive dashboard UI (not generic AI look)
7. Tests Stage 1
8. Commits and moves to Stage 2
9. ... continues until complete
10. Generates user guide
11. Pushes to GitHub and goes live
```

## Documentation

- [SKILL.md](./SKILL.md) - Full skill specification
- [subagents/](./subagents/) - Specialized agent definitions
  - [product-research-agent.md](./subagents/product-research-agent.md)
  - [cto-advisor-agent.md](./subagents/cto-advisor-agent.md)
  - [frontend-design-agent.md](./subagents/frontend-design-agent.md)
- [templates/](./templates/) - Project and documentation templates
- [references/examples.md](./references/examples.md) - Comprehensive examples

## Sources

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Anthropic Frontend Design Plugin](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design)
- [Claude Agent SDK Demos](https://github.com/anthropics/claude-agent-sdk-demos)
- [VoltAgent Awesome Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)

## Version

1.1.0
