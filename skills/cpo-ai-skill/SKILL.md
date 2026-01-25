---
name: cpo-ai-skill
description: "Chief Product Officer AI that orchestrates entire product lifecycles. Receives product ideas, qualifies scope through discovery questions, creates strategic plans with epics/stages/stories, implements stage-by-stage with testing, and delivers production-ready products with documentation. Use when asked to: build a product from scratch, create a complete application, plan and implement a full project, orchestrate product development, go from idea to production. Triggers on: build this product, cpo mode, chief product officer, product lifecycle, idea to production, full product build, strategic planning, product roadmap."
user-invocable: true
context: fork
version: 2.1.0
tools: Task
model: opus
color: "#6366f1"
triggers:
  - "/cpo-go"
  - "/cpo-iterate"
  - "cpo mode"
  - "build this product"
  - "chief product officer"
  - "idea to production"
  - "full product build"
  - "product lifecycle"
dependencies:
  skills:
    - autonomous-dev
    - fulltest-skill
  subagents:
    - product-research-agent
    - cto-advisor-agent
    - frontend-design-agent
    - backend-api-agent
    - database-setup-agent
    - deployment-agent
  references:
    - phase-details
    - templates
    - environment-config
    - testing-integration
    - cost-estimation
    - rollback-mechanisms
    - memory-caching
    - visual-progress
    - iteration-support
    - production-monitoring
---

# Chief Product Officer AI Skill

A comprehensive orchestration skill that transforms product ideas into production-ready applications through structured discovery, strategic planning, iterative implementation, and rigorous testing.

---

## Quick Start: `/cpo-go` Command

### Command Syntax

```bash
/cpo-go <project-name> <description>

# Examples:
/cpo-go game create an interactive tic-tac-toe game
/cpo-go taskflow build a task management app for small teams
/cpo-go artmarket create a marketplace where artists can sell digital art
```

### Command Parsing

```
/cpo-go <name> <description...>
        │       │
        │       └── Everything after the name = product description
        └── First word after /cpo-go = project name (lowercase, no spaces)
```

### On Command Detection

When `/cpo-go` is invoked:

1. Parse project name and description
2. Create project directory: `./{project-name}/`
3. Initialize Git and GitHub repository
4. Initialize `master-project.json` with parsed name
5. Skip to streamlined discovery (fewer questions since context is provided)
6. Begin Phase 1 with the description as the product idea

**See:** [references/phase-details.md](references/phase-details.md) for complete workflow steps.

---

## Core Philosophy

**"From Vision to Production with Systematic Excellence"**

The CPO AI acts as a virtual Chief Product Officer, combining:
- **Product Strategy**: Qualifying ideas, defining scope, identifying MVP
- **Market Research**: Analyzing competitors, design patterns, and best practices
- **Technical Architecture**: Expert tech stack and deployment recommendations
- **World-Class Design**: Production-grade UI avoiding generic AI aesthetics
- **Project Management**: Sequential execution with quality gates
- **Quality Assurance**: Testing each stage before progression
- **Documentation**: Creating user guides and deployment docs

---

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CPO AI SKILL WORKFLOW                                │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  PHASE 1: DISCOVERY          PHASE 2: PLANNING         PHASE 3: EXECUTION   │
│  ┌──────────────────┐       ┌──────────────────┐       ┌──────────────────┐ │
│  │ Receive Idea     │──────►│ Strategic Plan   │──────►│ Stage-by-Stage   │ │
│  │ Ask Questions    │       │ Epics & Stages   │       │ Implementation   │ │
│  │ Define Scope     │       │ Story Breakdown  │       │ Test & Commit    │ │
│  │ Identify MVP     │       │ Master Project   │       │ Iterate Until    │ │
│  └──────────────────┘       └──────────────────┘       │ Complete         │ │
│                                                        └──────────────────┘ │
│                                                                 │            │
│  PHASE 4: VALIDATION        PHASE 5: DELIVERY                   │            │
│  ┌──────────────────┐       ┌──────────────────┐                │            │
│  │ Full Project     │◄──────│ User Guide       │◄───────────────┘            │
│  │ Testing          │       │ Documentation    │                             │
│  │ Fix Any Issues   │       │ Final Commit     │                             │
│  │ Quality Gate     │──────►│ Push & Go Live   │                             │
│  └──────────────────┘       └──────────────────┘                             │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Specialized Subagents

The CPO AI orchestrates **six specialized subagents** for best-in-class results:

| Agent | Phase | Purpose |
|-------|-------|---------|
| **Product Research Agent** | 1, 2 | Market research, competitor analysis, design references |
| **CTO Advisor Agent** | 2, 3.1 | Tech stack, architecture, deployment strategy |
| **Frontend Design Agent** | 3 (UI) | Distinctive, production-grade interfaces |
| **Backend API Agent** | 3 (API) | REST/GraphQL design, auth, error handling |
| **Database Setup Agent** | 3.1 | Schema design, migrations, Supabase/Neon setup |
| **Deployment Agent** | 5 | Vercel/Railway/DO deployment execution |

**See:** [subagents/](subagents/) directory for detailed agent definitions.

---

## Entry Point Detection

When this skill activates, check for existing project state:

| Condition | Action |
|-----------|--------|
| No `master-project.json` exists | Start Phase 1 (Discovery) |
| `master-project.json` exists, no stages completed | Start Phase 3 (Execute first stage) |
| `master-project.json` exists, some stages done | Resume Phase 3 (Next incomplete stage) |
| All stages complete, not tested | Start Phase 4 (Full Validation) |
| All complete and tested | Start Phase 5 (Documentation & Delivery) |

**First Action:** Check project state:

```bash
ls -la master-project.json cpo-progress.md docs/user-guide.md 2>/dev/null
```

---

## Phase Summaries

### Phase 1: Product Discovery

**Goal:** Transform a raw product idea into a qualified, scoped product definition.

**Key Steps:**
1. Receive and acknowledge the product idea
2. Ask 5-8 strategic discovery questions (target users, scope, tech constraints, success criteria)
3. Synthesize product definition with vision, features, and non-goals
4. Invoke Product Research Agent for competitor analysis and design inspiration
5. Get user approval on product definition

**Output:** Product definition document with research findings

**Detailed Steps:** [references/phase-details.md#phase-1](references/phase-details.md)

---

### Phase 2: Strategic Planning

**Goal:** Create a comprehensive, staged implementation plan.

**Key Steps:**
1. Invoke CTO Advisor Agent for tech stack recommendations and architecture
2. Decompose product into epics (major feature areas)
3. Break epics into stages (implementable chunks)
4. Define user stories for each stage
5. Generate `master-project.json` with complete plan
6. Initialize `cpo-progress.md` for tracking
7. Calculate cost estimates for MVP and scale
8. Present plan for user approval

**Output:** Complete project plan with epics, stages, stories, and cost estimates

**Detailed Steps:** [references/phase-details.md#phase-2](references/phase-details.md)

---

### Phase 3: Stage-by-Stage Implementation

**Goal:** Implement each stage sequentially with quality gates.

**Key Steps:**
1. Load project state and identify next pending stage
2. Determine stage type and select appropriate specialized agent
3. For Foundation: Invoke Database Setup Agent
4. For UI: Invoke Frontend Design Agent with research context
5. For API: Invoke Backend API Agent
6. Delegate implementation to autonomous-dev
7. Monitor progress and update tracking
8. Test stage with fulltest-skill
9. Commit and push if tests pass, fix and retry if tests fail
10. Repeat for all stages

**Output:** Fully implemented product with all stages complete and tested

**Detailed Steps:** [references/phase-details.md#phase-3](references/phase-details.md)

---

### Phase 4: Full Project Validation

**Goal:** Comprehensive testing of the complete integrated product.

**Key Steps:**
1. Merge all stage branches to main
2. Run full integration testing suite
3. Verify critical user journeys end-to-end
4. Categorize and fix any integration issues
5. Pass quality gate (all tests passing, no critical bugs)

**Output:** Fully validated, production-ready application

**Detailed Steps:** [references/phase-details.md#phase-4](references/phase-details.md)

---

### Phase 5: Documentation & Delivery

**Goal:** Create user documentation and deploy to production.

**Key Steps:**
1. Generate user guide with getting started, features, troubleshooting
2. Generate technical documentation with architecture, setup, API reference
3. Final commit with all documentation
4. Push to GitHub and create release tag
5. Invoke Deployment Agent for production deployment
6. Verify deployment with health checks
7. Generate go-live report with metrics and next steps

**Output:** Live production application with complete documentation

**Detailed Steps:** [references/phase-details.md#phase-5](references/phase-details.md)

---

## Quick Commands

| Command | Action |
|---------|--------|
| "status" | Show current phase and progress |
| "skip stage" | Skip current stage (mark as skipped) |
| "pause" | Stop execution, wait for input |
| "resume" | Continue from last checkpoint |
| "replan" | Go back to Phase 2 and adjust plan |
| "test only" | Run tests without implementing |
| "docs only" | Generate documentation only |

---

## Error Recovery

### Stage Implementation Fails

After max attempts, offer options:
1. Simplify stage (split into smaller stages)
2. Get manual assistance with blockers
3. Skip stage and continue (mark incomplete)
4. Restart stage with different approach

### Testing Keeps Failing

After 3 fix iterations, offer options:
1. Review test expectations (may be incorrect)
2. Simplify acceptance criteria
3. Get user input on expected behavior
4. Mark as known issue and continue

### Scope Creep Detected

If implementation expands beyond plan:
1. Return to plan (drop extra work)
2. Update plan to include new scope
3. Move extra work to future stage

**See:** [references/phase-details.md](references/phase-details.md) for detailed error handling.

---

## Key Files Reference

| File | Purpose | Created | Template |
|------|---------|---------|----------|
| `master-project.json` | Complete project state | Phase 2 | [templates.md](references/templates.md) |
| `cpo-progress.md` | Progress log | Phase 2 | [templates.md](references/templates.md) |
| `prd.json` | Current stage stories | Phase 3 (per stage) | [templates.md](references/templates.md) |
| `progress.md` | Stage-level progress | Phase 3 (per stage) | autonomous-dev format |
| `docs/user-guide.md` | End-user documentation | Phase 5 | [templates.md](references/templates.md) |
| `docs/technical-docs.md` | Developer documentation | Phase 5 | [templates.md](references/templates.md) |

---

## Integration with Other Skills & Agents

### Specialized Subagents

| Agent | When Invoked | Input | Output |
|-------|--------------|-------|--------|
| Product Research Agent | Phase 1, 2 | Product idea, market | competitor-analysis.md, design-references.md |
| CTO Advisor Agent | Phase 2, 3.1 | Product requirements | tech-stack-recommendation.md, adr/ |
| Frontend Design Agent | Phase 3 (UI) | Components, research | React/Vue component code |
| Backend API Agent | Phase 3 (API) | Endpoints, auth | API routes, middleware |
| Database Setup Agent | Phase 3.1 | Schema requirements | Prisma/Drizzle schema, migrations |
| Deployment Agent | Phase 5 | Platform, env vars | Live URL, health checks |

**Details:** [subagents/](subagents/) directory

### Dependent Skills

| Skill | Purpose | When Used |
|-------|---------|-----------|
| autonomous-dev | Story-level implementation | Phase 3 (every stage) |
| fulltest-skill | E2E testing | Phase 3 (after each stage), Phase 4 |

### Reference Documents

| Reference | Purpose | Link |
|-----------|---------|------|
| Phase Details | Complete step-by-step instructions | [references/phase-details.md](references/phase-details.md) |
| Templates | JSON/Markdown templates | [references/templates.md](references/templates.md) |
| Environment Config | .env templates for different stacks | [references/environment-config.md](references/environment-config.md) |
| Testing Integration | Testing strategy and commands | [references/testing-integration.md](references/testing-integration.md) |
| Cost Estimation | Infrastructure cost calculations | [references/cost-estimation.md](references/cost-estimation.md) |
| Examples | Complete workflow examples | [references/examples.md](references/examples.md) |

---

## Examples & Walkthroughs

**Complete Examples:**
- [Simple Game](references/examples.md#simple-game)
- [SaaS Task Manager](references/examples.md#saas-task-manager)
- [E-commerce Marketplace](references/examples.md#e-commerce-marketplace)

**See:** [references/examples.md](references/examples.md) for full walkthroughs with sample inputs/outputs.

---

## Version & Updates

**Current Version:** 2.0.0

**Recent Changes:**
- Added `/cpo-go` quick-start command
- Integrated specialized subagents for each domain
- Added cost estimation in planning phase
- Improved error recovery with multiple options
- Modular structure with detailed reference docs

**Roadmap:**
- Real-time collaboration features
- AI-powered cost optimization suggestions
- Automated monitoring setup post-deployment
- Multi-environment deployment (staging/prod)

---

**For detailed phase instructions, see:** [references/phase-details.md](references/phase-details.md)
**For all templates, see:** [references/templates.md](references/templates.md)
