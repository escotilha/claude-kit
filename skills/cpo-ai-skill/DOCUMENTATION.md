# CPO AI Skill - Complete Documentation

**Version:** 2.1.0
**Model:** Claude Opus 4.5
**Repository:** [github.com/escotilha/skills](https://github.com/escotilha/skills/tree/master/skills/cpo-ai-skill)

---

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Commands](#commands)
4. [Workflow Phases](#workflow-phases)
5. [Specialized Subagents](#specialized-subagents)
6. [Project Artifacts](#project-artifacts)
7. [Tech Stack Templates](#tech-stack-templates)
8. [Cost Estimation](#cost-estimation)
9. [Templates & Schemas](#templates--schemas)
10. [Integration Points](#integration-points)
11. [Advanced Features](#advanced-features)
12. [Examples](#examples)
13. [Troubleshooting](#troubleshooting)
14. [Architecture](#architecture)

---

## Overview

The **CPO AI Skill** (Chief Product Officer AI) is a comprehensive orchestration system that transforms product ideas into production-ready, deployed applications. It acts as a virtual Chief Product Officer, combining product strategy, market research, technical architecture, project management, and quality assurance into a single automated workflow.

### Core Philosophy

> **"From Vision to Production with Systematic Excellence"**

The CPO AI combines:
- **Product Strategy** - Qualifying ideas, defining scope, identifying MVP
- **Market Research** - Analyzing competitors, design patterns, and best practices
- **Technical Architecture** - Expert tech stack and deployment recommendations
- **World-Class Design** - Production-grade UI avoiding generic AI aesthetics
- **Project Management** - Sequential execution with quality gates
- **Quality Assurance** - Testing each stage before progression
- **Documentation** - Creating user guides and deployment docs

### What Makes It Different

| Traditional Approach | CPO AI Approach |
|---------------------|-----------------|
| Separate planning and execution | Integrated end-to-end workflow |
| Generic templates | Research-driven, context-aware design |
| Manual deployment | Automated production deployment |
| Single-shot generation | Iterative implementation with testing |
| No cost visibility | Infrastructure cost estimation upfront |

---

## Quick Start

### New Project: `/cpo-go`

```bash
/cpo-go <project-name> <description>
```

**Examples:**
```bash
/cpo-go game create an interactive tic-tac-toe game
/cpo-go taskflow build a task management app for small teams
/cpo-go artmarket create a marketplace where artists can sell digital art
```

**Fast Mode:** Reply `"go"` to use defaults:
- Creates **public GitHub repo** with project name
- **MVP** scope
- **Web app** (Next.js + Supabase)
- **Speed** priority
- **Auto-deploys** to Vercel

### Existing Project: `/cpo-iterate`

```bash
/cpo-iterate <description of changes>
```

**Examples:**
```bash
/cpo-iterate add user profile editing and avatar uploads
/cpo-iterate fix the checkout flow bug and improve error messages
/cpo-iterate add dark mode support across all pages
```

---

## Commands

### Primary Commands

| Command | Purpose | When to Use |
|---------|---------|-------------|
| `/cpo-go <name> <desc>` | Start new project from scratch | Beginning a new product |
| `/cpo-iterate <desc>` | Add features to existing project | Evolving a launched product |

### Quick Commands

| Command | Action |
|---------|--------|
| `"status"` | Show current phase and progress |
| `"skip stage"` | Skip current stage (mark as skipped) |
| `"pause"` | Stop execution, wait for input |
| `"resume"` | Continue from last checkpoint |
| `"replan"` | Go back to Phase 2 and adjust plan |
| `"test only"` | Run tests without implementing |
| `"docs only"` | Generate documentation only |
| `"costs"` | Show detailed cost breakdown |

### Natural Language Triggers

The skill also activates on natural language phrases:
- "build this product"
- "chief product officer"
- "idea to production"
- "full product build"
- "product lifecycle"
- "cpo mode"

---

## Workflow Phases

The CPO AI executes a structured 5-phase workflow:

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

### Phase 1: Product Discovery

**Goal:** Transform a raw product idea into a qualified, scoped product definition.

**Steps:**
1. Receive and acknowledge the product idea
2. Ask 5-8 strategic discovery questions
3. Synthesize product definition
4. Invoke Product Research Agent for competitor analysis
5. Get user approval on product definition

**Discovery Questions Cover:**
- Target users & market (B2C, B2B, developers, internal)
- Core problem statement
- Scope & complexity (MVP, feature-complete, enterprise)
- Technical constraints
- Data & persistence requirements
- Authentication requirements
- Deployment target
- Success criteria

**Output:** Product definition document with research findings

### Phase 2: Strategic Planning

**Goal:** Create a comprehensive, staged implementation plan.

**Steps:**
1. Invoke CTO Advisor Agent for tech stack recommendations
2. Decompose product into epics (major feature areas)
3. Break epics into stages (implementable chunks)
4. Define user stories for each stage
5. Generate `master-project.json` with complete plan
6. Initialize `cpo-progress.md` for tracking
7. Calculate cost estimates for MVP and scale
8. Present plan for user approval

**Stage Sizing Rules:**

| Right-sized Stage | Too Big (Split) |
|-------------------|-----------------|
| 3-7 user stories | More than 10 stories |
| 1-3 hours work | Full day or more |
| Single feature area | Multiple unrelated features |
| Clear completion criteria | Vague "make it work" |

**Output:** Complete project plan with epics, stages, stories, and cost estimates

### Phase 3: Stage-by-Stage Implementation

**Goal:** Implement each stage sequentially with quality gates.

**Steps:**
1. Load project state and identify next pending stage
2. Determine stage type and select appropriate specialized agent
3. Delegate implementation based on stage type:
   - **Foundation** → Database Setup Agent
   - **UI** → Frontend Design Agent
   - **API** → Backend API Agent
4. Monitor progress and update tracking
5. Test stage with fulltest-skill
6. Commit and push if tests pass
7. Repeat for all stages

**Quality Gate:** Tests must pass before committing. After 3 failed fix attempts, user is offered options.

### Phase 4: Full Project Validation

**Goal:** Comprehensive testing of the complete integrated product.

**Steps:**
1. Merge all stage branches to main
2. Run full integration testing suite
3. Verify critical user journeys end-to-end
4. Categorize and fix any integration issues
5. Pass quality gate (all tests passing, no critical bugs)

**Quality Gate Criteria:**
- [ ] All unit tests pass
- [ ] All integration tests pass
- [ ] Build completes successfully
- [ ] Critical user journeys work
- [ ] No critical or high severity bugs

### Phase 5: Documentation & Delivery

**Goal:** Create user documentation and deploy to production.

**Steps:**
1. Generate user guide with getting started, features, troubleshooting
2. Generate technical documentation with architecture, setup, API reference
3. Final commit with all documentation
4. Push to GitHub and create release tag
5. Invoke Deployment Agent for production deployment
6. Verify deployment with health checks
7. Generate go-live report with metrics and next steps

**Output:** Live production application with complete documentation

---

## Specialized Subagents

The CPO AI orchestrates **six specialized subagents** for domain-specific excellence:

### 1. Product Research Agent

**Model:** Sonnet
**Purpose:** Market research, competitor analysis, design references

**Capabilities:**
- Analyze competing products and their features
- Identify market gaps and opportunities
- Benchmark pricing and positioning strategies
- Find best-in-class UI/UX examples
- Collect design system references
- Identify interaction patterns from successful products

**Outputs:**
- `competitor-analysis.md`
- `design-references.md`
- `market-insights.md`

**Invoked During:** Phase 1 (Discovery), Phase 2 (Planning)

### 2. CTO Advisor Agent

**Model:** Opus
**Purpose:** Tech stack selection, architecture, deployment strategy

**Capabilities:**
- Evaluate frameworks, languages, and tools
- Design system architecture for scalability
- Define service boundaries and data flow
- Plan security, reliability, and performance
- Document architectural decisions (ADRs)
- Recommend hosting platforms and infrastructure

**Outputs:**
- `tech-stack-recommendation.md`
- `architecture-overview.md`
- `deployment-guide.md`
- `adr/` (Architecture Decision Records)

**Tech Stack Templates:**
- **SaaS Application** - Next.js + Tailwind + Prisma + PostgreSQL + Vercel
- **High-Scale Application** - Go/Rust backend + Kubernetes + Redis
- **MVP / Rapid Prototype** - Next.js + Supabase (BaaS)
- **Mobile Application** - React Native/Flutter + Firebase

**Invoked During:** Phase 2 (Planning), Phase 3.1 (Foundation)

### 3. Frontend Design Agent

**Model:** Opus
**Purpose:** Distinctive, production-grade UI implementation

Based on [Anthropic's Frontend Design Skill](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design).

**Core Philosophy:**
> "Choose a clear conceptual direction and execute it with precision. Bold maximalism and refined minimalism both work—the key is intentionality, not intensity."

**Aesthetic Directions Supported:**
| Direction | Characteristics | Best For |
|-----------|-----------------|----------|
| Brutalist | Raw, bold, unconventional | Developer tools, creative agencies |
| Minimalist | Clean, spacious, focused | Productivity apps, enterprise |
| Maximalist | Rich, layered, expressive | Creative platforms, entertainment |
| Glassmorphism | Frosted glass, depth, blur | Modern dashboards, iOS-style |
| Neubrutalism | Bold colors, hard shadows | Creative tools, startups |

**Anti-Patterns Avoided:**
- Generic purple gradients (AI cliché)
- System fonts without intentionality
- Centered everything
- Stock photo headers
- Cookie-cutter card grids

**Requirements:**
- Research input from Product Research Agent
- Dark mode support
- Mobile responsive
- WCAG 2.1 AA accessibility

**Invoked During:** Phase 3 (UI stages)

### 4. Backend API Agent

**Model:** Opus
**Purpose:** REST/GraphQL design, authentication, error handling

**Capabilities:**
- RESTful API endpoint design
- GraphQL schema and resolvers
- JWT/OAuth/API key authentication
- Input validation with Zod
- Error handling patterns
- Rate limiting implementation
- Database query optimization
- DataLoader for N+1 prevention

**Framework Support:**
- Next.js API Routes
- Next.js Server Actions
- Express.js
- tRPC

**Security Patterns:**
- Input validation on all inputs
- Output encoding (XSS prevention)
- SQL injection prevention (parameterized queries)
- CSRF protection
- Rate limiting on APIs
- Secure session management

**Invoked During:** Phase 3 (API stages)

### 5. Database Setup Agent

**Model:** Sonnet
**Purpose:** Schema design, migrations, database provisioning

**Supported Providers:**
- **Supabase** - PostgreSQL with auth, storage, realtime
- **Neon** - Serverless PostgreSQL with branching
- **PostgreSQL** - Via Docker for local development

**ORM Support:**
- **Prisma** - Type-safe, schema-first
- **Drizzle** - Lightweight, SQL-like

**Schema Patterns:**
- User & Auth tables with profile triggers
- Multi-tenancy (organization-based)
- Audit logging
- Soft deletes
- Timestamps convention

**Security:**
- Row Level Security (RLS) policies
- Role-based access patterns
- Multi-tenant data isolation

**Outputs:**
- ORM schema files
- SQL migrations
- Seed scripts
- TypeScript types
- `.env.example` configuration
- RLS policies

**Invoked During:** Phase 3.1 (Foundation stage)

### 6. Deployment Agent

**Model:** Sonnet
**Purpose:** Production deployment execution

**Supported Platforms:**

| Platform | Use Case | Strengths |
|----------|----------|-----------|
| Vercel | Next.js, React, static sites | Zero-config, edge functions |
| Railway | Full-stack apps, databases | Simple, built-in Postgres/Redis |
| DigitalOcean | App Platform, Droplets | Flexible, Kubernetes support |
| Cloudflare | Pages, Workers, edge compute | Global CDN, R2 storage |

**Capabilities:**
- Pre-deployment verification (build, tests, env vars)
- Platform CLI configuration
- Environment variable setup
- Domain configuration
- SSL/TLS certificate verification
- Post-deployment health checks
- Rollback procedures

**Deployment Workflow:**
1. Pre-flight checks (build, tests, health endpoint)
2. Environment setup (production env vars)
3. Deploy (platform-specific)
4. Verify (health check, smoke tests, DNS, SSL)
5. Finalize (documentation, monitoring setup)

**Invoked During:** Phase 5 (Delivery)

---

## Project Artifacts

### Files Generated

| File | Purpose | Created In |
|------|---------|------------|
| `master-project.json` | Complete project state and plan | Phase 2 |
| `cpo-progress.md` | Detailed progress log | Phase 2 |
| `prd.json` | Current stage stories | Phase 3 (per stage) |
| `.env.example` | Environment configuration template | Phase 3.1 |
| `.gitignore` | Git configuration | Phase 3.1 |
| `docs/user-guide.md` | End-user documentation | Phase 5 |
| `docs/technical-docs.md` | Developer documentation | Phase 5 |
| `CHANGELOG.md` | Version history | Phase 5 |

### Research Artifacts

| File | Purpose |
|------|---------|
| `competitor-analysis.md` | Competitive landscape analysis |
| `design-references.md` | Visual design inspiration |
| `market-insights.md` | Market validation findings |
| `tech-stack-recommendation.md` | CTO-level tech guidance |
| `architecture-overview.md` | System architecture design |
| `adr/` | Architecture Decision Records |

### Directory Structure

```
./{project-name}/
├── master-project.json          # Complete project state
├── cpo-progress.md              # Detailed progress log
├── .env.example                 # Environment template
├── .gitignore                   # Git configuration
├── prd.json                     # Stage-specific PRD
├── competitor-analysis.md       # Research: competitors
├── design-references.md         # Research: design
├── market-insights.md           # Research: market
├── tech-stack-recommendation.md # CTO recommendations
├── architecture-overview.md     # System architecture
├── adr/                         # Architecture Decision Records
├── docs/
│   ├── user-guide.md           # End-user documentation
│   └── technical-docs.md       # Developer documentation
├── src/                         # Application source code
├── prisma/                      # Database schema (if Prisma)
├── supabase/                    # Supabase config (if Supabase)
└── {framework files}            # Next.js, React, etc.
```

---

## Tech Stack Templates

### Standard SaaS Stack (Most Common)

```yaml
frontend:
  framework: Next.js 14 (App Router)
  styling: Tailwind CSS + shadcn/ui
  state: Zustand or React Query
  rationale: "Server components, excellent DX, Vercel deployment"

backend:
  runtime: Node.js 20 LTS
  framework: Next.js API Routes or tRPC
  validation: Zod
  rationale: "Unified stack, type-safety, rapid development"

database:
  primary: PostgreSQL (via Neon or Supabase)
  orm: Prisma or Drizzle
  cache: Redis (Upstash)
  rationale: "Relational integrity, serverless-friendly"

auth:
  provider: Clerk or NextAuth.js
  rationale: "Managed auth reduces complexity"

hosting:
  platform: Vercel
  database: Neon / Supabase
  storage: Cloudflare R2 or AWS S3
  rationale: "Optimized for Next.js, global edge"

monitoring:
  errors: Sentry
  analytics: PostHog or Mixpanel
  logs: Axiom or Datadog
```

### High-Scale Application

```yaml
frontend:
  framework: Next.js 14 or Remix
  styling: Tailwind CSS
  cdn: Cloudflare

backend:
  language: Go or Rust (performance-critical) + Node.js (API)
  framework: Fiber (Go) or Axum (Rust)
  api: GraphQL (Apollo) or REST
  queue: BullMQ / AWS SQS

database:
  primary: PostgreSQL (RDS/Cloud SQL)
  read-replicas: Yes
  cache: Redis Cluster
  search: Elasticsearch or Meilisearch

hosting:
  compute: AWS ECS/EKS or GCP Cloud Run
  cdn: Cloudflare
  storage: S3 + CloudFront

infrastructure:
  iac: Terraform or Pulumi
  containers: Docker
  orchestration: Kubernetes (if needed)
```

### MVP / Rapid Prototype

```yaml
frontend:
  framework: Next.js 14
  styling: Tailwind + shadcn/ui
  rationale: "Fastest to production-quality UI"

backend:
  baas: Supabase (auth, database, storage, realtime)
  rationale: "Minimal backend code, focus on product"

database:
  provider: Supabase PostgreSQL
  rationale: "Built-in auth, realtime, storage"

hosting:
  platform: Vercel (frontend) + Supabase (backend)
  rationale: "Free tier, instant deployment"

skip_for_mvp:
  - Kubernetes
  - Microservices
  - Custom auth
  - Complex CI/CD
```

---

## Cost Estimation

CPO AI provides infrastructure cost projections at the end of Phase 2 (Planning).

### When Shown

1. **End of Phase 2** - Before user approves strategic plan
2. **Significant scope changes** - When epics/stages are added/removed
3. **On explicit request** - User asks "show costs"
4. **Before deployment** - Final cost verification in Phase 5

### Cost Estimate Format

```markdown
## Resource Estimate: [Project Name]

### Development Scope
| Metric | Value |
|--------|-------|
| Epics | 4 |
| Stages | 12 |
| User Stories | 36 |
| Estimated Complexity | Medium |

### Infrastructure Costs (Monthly)

#### MVP / Launch Phase
| Service | Tier | Cost | Notes |
|---------|------|------|-------|
| Vercel | Hobby | $0 | 100GB bandwidth |
| Supabase | Free | $0 | 500MB DB, 1GB storage |
| Domain | - | ~$1/month | ~$12/year amortized |
| **Total** | | **~$1/month** | |

#### Growth Phase (1K-10K users)
| Service | Tier | Cost | Notes |
|---------|------|------|-------|
| Vercel | Pro | $20/month | Unlimited bandwidth |
| Supabase | Pro | $25/month | 8GB DB, 100GB storage |
| Domain | - | ~$1/month | Same domain |
| **Total** | | **~$46/month** | |

#### Scale Phase (10K+ users)
| Service | Tier | Cost | Notes |
|---------|------|------|-------|
| Vercel | Pro | $20/month | May need multiple seats |
| Supabase | Pro | $25-100/month | Based on DB size |
| CDN/Extras | - | $10-50/month | Images, caching |
| **Total** | | **~$55-170/month** | |
```

### Provider Cost Reference

**Hosting Platforms:**
| Provider | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| Vercel | 100GB bandwidth | $20/seat/month | Next.js |
| Railway | $5 credit/month | Usage-based | Full-stack |
| Cloudflare Pages | Unlimited | $5/month (Workers) | Static + edge |

**Database Services:**
| Provider | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| Supabase | 500MB DB | $25/month | All-in-one |
| Neon | 0.5GB storage | $19/month | Serverless Postgres |
| PlanetScale | 1B row reads | $29/month | High-scale MySQL |

**Authentication:**
| Provider | Free Tier | Paid Tier | Best For |
|----------|-----------|-----------|----------|
| Clerk | 10K MAU | $25/month | React/Next.js |
| Supabase Auth | Unlimited | Included | All-in-one |
| NextAuth.js | Self-hosted | Free (OSS) | Most flexible |

---

## Templates & Schemas

### master-project.json

```json
{
  "project": {
    "name": "[Product Name]",
    "description": "[Product description]",
    "version": "0.1.0",
    "createdAt": "[ISO timestamp]",
    "status": "planning"
  },
  "productDefinition": {
    "vision": "[Vision statement]",
    "targetUser": "[User persona]",
    "problemStatement": "[Core problem]",
    "scope": "[MVP|Feature-complete|Enterprise]",
    "techStack": {
      "frontend": "[framework]",
      "backend": "[framework]",
      "database": "[database]",
      "hosting": "[platform]",
      "authentication": "[auth solution]",
      "orm": "[Prisma|Drizzle]"
    },
    "successMetrics": ["[metric 1]", "[metric 2]"],
    "nonGoals": ["[explicitly out of scope]"]
  },
  "epics": [
    {
      "id": "E1",
      "name": "Foundation",
      "description": "Project setup, auth, database",
      "priority": 0,
      "status": "pending",
      "dependsOn": []
    }
  ],
  "stages": [
    {
      "id": "S1",
      "epicId": "E1",
      "name": "Project Initialization",
      "description": "Set up project structure",
      "status": "pending",
      "dependsOn": [],
      "stories": [
        {
          "id": "S1-US-001",
          "title": "Initialize Next.js project",
          "description": "As a developer...",
          "acceptanceCriteria": ["Criterion 1", "Typecheck passes"],
          "priority": 1,
          "dependsOn": []
        }
      ]
    }
  ],
  "verification": {
    "typecheck": "npm run typecheck",
    "test": "npm run test",
    "lint": "npm run lint",
    "build": "npm run build"
  },
  "repository": {
    "url": null,
    "branch": "main",
    "lastCommit": null
  },
  "costs": {
    "mvp": { "total": 0 },
    "scale": { "total": 45 }
  }
}
```

### Stage PRD (prd.json)

```json
{
  "project": "[Product Name]",
  "branchName": "feature/stage-[N]-[name]",
  "description": "[Stage description]",
  "createdAt": "[ISO timestamp]",
  "verification": {
    "typecheck": "npm run typecheck",
    "test": "npm run test",
    "lint": "npm run lint"
  },
  "userStories": [
    {
      "id": "S[N]-US-001",
      "title": "[Story title]",
      "description": "As a [user], I want [capability] so that [benefit]",
      "acceptanceCriteria": ["Criterion 1", "Typecheck passes"],
      "priority": 1,
      "dependsOn": [],
      "passes": false,
      "attempts": 0,
      "notes": ""
    }
  ]
}
```

---

## Integration Points

### Dependent Skills

| Skill | Purpose | When Used |
|-------|---------|-----------|
| **autonomous-dev** | Story-level implementation | Phase 3 (every stage) |
| **fulltest-skill** | Comprehensive E2E testing | Phase 3 (after each stage), Phase 4 |
| **worktree-scaffold** | Isolated stage development | Optional for parallel work |

### MCP Integrations

| MCP Server | Purpose |
|------------|---------|
| **Memory MCP** | Cache research results across projects |
| **Chrome DevTools** | E2E testing via browser automation |
| **GitHub** | Repository management |

### Tools Used

- **Task** - Subagent coordination
- **WebSearch/WebFetch** - Research
- **Bash** - Git operations, CLI tools
- **Read/Write/Edit** - File operations
- **Glob/Grep** - Code search

---

## Advanced Features

### Iteration Support (v2.1.0+)

The `/cpo-iterate` command enables post-launch development:

**What It Does:**
1. Loads existing `master-project.json`
2. Creates iteration branch (`iteration/v1.1-feature`)
3. Adds new epic(s) to the project
4. Runs mini-discovery for the new feature
5. Generates stages for the new epic
6. Implements stages incrementally
7. Tests new + existing features (regression)
8. Updates version number
9. Updates changelog

**Feature Flags:**
```typescript
// lib/feature-flags.ts
export const FEATURES = {
  TEAM_COLLABORATION: process.env.NEXT_PUBLIC_FEATURE_TEAM_COLLABORATION === 'true',
  DARK_MODE: process.env.NEXT_PUBLIC_FEATURE_DARK_MODE === 'true',
} as const;
```

**Semantic Versioning:**
- **MAJOR** - Breaking changes
- **MINOR** - New features (backward compatible)
- **PATCH** - Bug fixes

### Rollback Mechanisms

Git-based checkpoints with automatic and manual recovery:

**Automatic Checkpoints:**
- Commit after each passing stage
- Tag releases at milestones

**Manual Recovery:**
```bash
# Identify last working version
git log --oneline -10

# Checkout that version
git checkout <commit-hash>

# Redeploy
vercel --prod
```

### Memory Caching

Research results cached via Memory MCP for cross-project reuse:
- Competitor analysis
- Design references
- Tech patterns

### Visual Progress

**ASCII Dashboard:**
```
┌─────────────────────────────────────────────────┐
│  TaskFlow - Stage Progress                       │
├─────────────────────────────────────────────────┤
│  S1: Foundation      ██████████████████ DONE    │
│  S2: Authentication  ██████████████████ DONE    │
│  S3: Core Features   █████████░░░░░░░░░ 50%     │
│  S4: UI Polish       ░░░░░░░░░░░░░░░░░░ PENDING │
└─────────────────────────────────────────────────┘
```

### Production Monitoring

Automatic setup for:
- **Sentry** - Error tracking
- **PostHog** - Product analytics
- **BetterStack** - Uptime monitoring

---

## Examples

### Example 1: Task Management App

```bash
/cpo-go taskflow build a task management app for small teams
```

**CPO AI Workflow:**
1. **Discovery** - Quick questions (fewer due to context)
2. **Research** - Analyzes Asana, Linear, Notion
3. **CTO Recommendation** - Next.js + Supabase + Vercel
4. **Planning** - 5 epics, 12 stages
5. **Cost Estimate** - ~$0/month (MVP) → ~$45/month (at scale)
6. **Database Setup** - Supabase + Prisma schema
7. **Environment** - `.env.example` generated
8. **Implementation** - Stage-by-stage with testing
9. **Documentation** - User guide + technical docs
10. **Deployment** - Live on Vercel

### Example 2: E-commerce Marketplace

**Discovery Questions:**
- Marketplace model (listings, auctions, NFT)
- Target sellers (hobbyist, professional, AI)
- Content types (downloads, print-on-demand, commissions)
- Revenue model (transaction fee, subscription, ads)
- Payment processing (Stripe, PayPal, crypto)

**Typical Epics:**
1. Foundation (auth, database)
2. Catalog (products, categories, search)
3. Shopping (cart, checkout, payments)
4. Order Management
5. User Experience (reviews, wishlist)
6. Admin (dashboard, inventory)
7. Production (testing, docs, deploy)

### Example 3: SaaS Dashboard

**Design Brief (from Research):**
```markdown
### Research Summary
**Competitor Analysis:**
- Linear: Clean, minimal, keyboard-first
- Notion: Flexible but can feel cluttered
- Asana: Feature-rich but overwhelming

**Design References:**
1. Raycast - Command palette, dark mode
2. Vercel Dashboard - Sophisticated gradients
3. Stripe Dashboard - Data density done right

**Market Insights:**
- 78% prefer dark mode
- Top request: Keyboard shortcuts
- Pain point: Too many clicks

### Design Direction
- **Aesthetic:** Modern minimalist with depth
- **Differentiator:** Cmd+K command palette
- **Typography:** Inter + JetBrains Mono
- **Colors:** Deep indigo (differentiate from Linear)
```

---

## Troubleshooting

### Error Recovery

#### Stage Implementation Fails

After max attempts, options offered:
1. Simplify stage (split into smaller stages)
2. Get manual assistance with blockers
3. Skip stage and continue (mark incomplete)
4. Restart stage with different approach

#### Testing Keeps Failing

After 3 fix iterations, options offered:
1. Review test expectations (may be incorrect)
2. Simplify acceptance criteria
3. Get user input on expected behavior
4. Mark as known issue and continue

#### Scope Creep Detected

If implementation expands beyond plan:
1. Return to plan (drop extra work)
2. Update plan to include new scope
3. Move extra work to future stage

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| Build fails | TypeScript errors | Run `npm run typecheck` locally |
| Tests fail | Missing dependencies | Check `package.json`, run `npm install` |
| DB connection fails | Wrong connection string | Verify `DATABASE_URL` in `.env` |
| Deploy fails | Missing env vars | Check platform env var configuration |
| Stage stuck | Circular dependencies | Review stage dependencies in plan |

### Entry Point Detection

When the skill activates, it checks project state:

| Condition | Action |
|-----------|--------|
| No `master-project.json` | Start Phase 1 (Discovery) |
| `master-project.json` exists, no stages completed | Start Phase 3 (Execute first stage) |
| Some stages done | Resume Phase 3 (Next incomplete stage) |
| All stages complete, not tested | Start Phase 4 (Full Validation) |
| All complete and tested | Start Phase 5 (Documentation & Delivery) |

---

## Architecture

### Skill Metadata

```yaml
name: cpo-ai-skill
description: "Chief Product Officer AI..."
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
```

### File Structure

```
cpo-ai-skill/
├── README.md                    # Quick start guide
├── SKILL.md                     # Complete skill specification
├── DOCUMENTATION.md             # This file
├── subagents/
│   ├── product-research-agent.md
│   ├── cto-advisor-agent.md
│   ├── frontend-design-agent.md
│   ├── backend-api-agent.md
│   ├── database-setup-agent.md
│   └── deployment-agent.md
└── references/
    ├── phase-details.md         # Step-by-step phase instructions
    ├── templates.md             # JSON/Markdown templates
    ├── environment-config.md    # .env templates
    ├── testing-integration.md   # Testing strategy
    ├── cost-estimation.md       # Infrastructure cost calculations
    ├── rollback-mechanisms.md   # Git checkpoints, recovery
    ├── memory-caching.md        # Research caching via Memory MCP
    ├── visual-progress.md       # ASCII/HTML progress displays
    ├── iteration-support.md     # /cpo-iterate command details
    ├── production-monitoring.md # Sentry, PostHog, uptime setup
    └── examples.md              # Complete workflow examples
```

---

## Resources

### Official Sources
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Anthropic Frontend Design Plugin](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design)
- [Frontend Aesthetics Cookbook](https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb)
- [Claude Agent SDK Demos](https://github.com/anthropics/claude-agent-sdk-demos)

### Framework Documentation
- [Next.js Documentation](https://nextjs.org/docs)
- [Prisma Documentation](https://www.prisma.io/docs)
- [Supabase Documentation](https://supabase.com/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui Components](https://ui.shadcn.com/)
- [tRPC Documentation](https://trpc.io/docs)
- [Zod Schema Validation](https://zod.dev/)

### Security
- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [PostgreSQL RLS](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)

### Community
- [VoltAgent Awesome Subagents](https://github.com/VoltAgent/awesome-claude-code-subagents)

---

## Version History

### v2.1.0 (Current)
- `/cpo-iterate` command for existing projects
- Git-based rollback mechanisms
- Memory caching via Memory MCP
- ASCII/HTML progress dashboards
- Automatic Sentry, PostHog, uptime setup
- Modular reference document architecture

### v2.0.0
- Backend API Agent
- Database Setup Agent (Supabase/Neon provisioning)
- Deployment Agent (actual deployment execution)
- Infrastructure cost projections
- Automatic `.env.example` generation
- Tighter integration with fulltest-skill

### v1.0.0
- Initial release
- 5-phase workflow
- Product Research Agent
- CTO Advisor Agent
- Frontend Design Agent
- Basic documentation generation

---

**CPO AI Skill v2.1.0** | Built for [Claude Code](https://claude.com/claude-code)
