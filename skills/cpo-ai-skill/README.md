# CPO AI Skill

**Chief Product Officer AI** - Transform product ideas into production-ready applications.

## Overview

The CPO AI Skill orchestrates the entire product development lifecycle:

1. **Discovery** - Qualify ideas through strategic questions
2. **Planning** - Break down into epics, stages, and stories
3. **Execution** - Implement stage-by-stage with testing
4. **Validation** - Full project integration testing
5. **Delivery** - Documentation and go-live

## Quick Start

Activate the skill by saying:
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

## Integration

Works with:
- **autonomous-dev** - Story-level implementation
- **fulltest-skill** - Comprehensive testing
- **worktree-scaffold** - Isolated stage development

## Example

```
User: "Build a task management app for small teams"

CPO AI:
1. Asks discovery questions about users, scope, tech stack
2. Creates strategic plan with 5 epics, 12 stages
3. Implements Stage 1: Project Setup
4. Tests Stage 1
5. Commits and moves to Stage 2
6. ... continues until complete
7. Generates user guide
8. Pushes to GitHub
```

## Documentation

- [SKILL.md](./SKILL.md) - Full skill specification
- [templates/](./templates/) - Project and documentation templates
- [references/examples.md](./references/examples.md) - Comprehensive examples

## Version

1.0.0
