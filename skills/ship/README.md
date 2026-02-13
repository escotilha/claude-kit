# /ship — End-to-End Feature Shipping Skill

## What it does

Takes a feature from idea to production in one command. You describe what you want built, and it handles everything — product spec, tech spec, planning, implementation, testing, bug fixes, and documentation. Resumable across sessions.

## The 8 Phases

### Phase 0: Project Detection

Auto-detects your project on first run — package manager (pnpm/npm/yarn/bun/cargo/pip), language, framework, monorepo setup, available scripts (build, test, typecheck, lint), and which QA skill to use. Works with TypeScript, Python, Go, Rust — any project.

### Phase 1: Product Spec (CPO mindset)

Analyzes the feature as a product manager: who's the user, what problem does this solve, what's MVP scope vs nice-to-have, success metrics, risks. Writes `product-spec.md`. If you give it a detailed brief, it condenses and moves on.

### Phase 2: Tech Spec (CTO mindset)

Deep-reads your codebase to understand existing patterns, then designs the technical approach: database schema changes, API endpoints, frontend components, service layer, dependencies, implementation order. Writes `tech-spec.md`.

### Phase 3: Implementation Plan (Sequential Thinking)

Breaks the tech spec into dependency-aware tasks using sequential thinking. Each task gets classified by complexity for model routing:

- **Simple (haiku)** — boilerplate, config, translations, re-exports
- **Moderate (sonnet)** — business logic, API routes, React components, hooks
- **Complex (opus)** — novel algorithms, state machines, architectural decisions

Before planning, queries past learnings from `learnings.json` and MCP Memory to adjust model routing based on previous mis-routes and add warnings for known failure areas.

### Phase 4: Execution (Swarm)

Creates a team and spawns parallel agents matched to task complexity. Each agent gets the task, relevant file contents, codebase conventions, and learnings from past runs (e.g., "API routes without validation fail QA 80% of the time"). After each group completes: typecheck, fix if needed, commit, update state.

If context approaches 80% capacity, it commits everything and tells you to run `/ship --resume`.

### Phase 5: QA Testing

Runs typecheck, tests, and lint using detected project commands. Then dispatches to the appropriate QA skill (auto-detected) or falls back to Chrome DevTools browser testing. Collects results into `qa-report.md`.

### Phase 6: Fix Cycle

If QA finds issues, fixes them in up to 3 iterations. Checks `learnings.json` for known fix patterns first before investigating from scratch. Records every error type and successful fix back to learnings. Re-runs QA after each iteration.

### Phase 7: Documentation + Retrospective

Writes `ship-log.md` with summary, all files created/modified, dependencies added, QA results, and commits.

Then runs an automatic retrospective:

- Which model routes were wrong? (haiku task that needed sonnet)
- Which QA failures were found?
- Which fix patterns worked?
- Any dependency gotchas?

Saves everything to two places.

## Two-Layer Learning System

Every `/ship` run makes the next one smarter.

### Layer 1: Project-local (`.claude/ship/learnings.json`)

Stores model routing corrections, QA failure patterns, fix solutions, and dependency gotchas specific to this project. Read by Phase 3 (planning), Phase 4 (agent prompts), and Phase 6 (fix cycle).

### Layer 2: Cross-project (MCP Memory `ship-learning:*` entities)

Generalizes patterns that apply across all projects. E.g., "React hooks with useEffect are moderate, not simple" or "API routes without zod validation fail QA 80% of the time." Portable across every project you work on.

## Key Features

- **Resumable** — All state persisted to `.claude/ship/{feature}/state.json`. Context clears? Just run `/ship --resume`.
- **Project-agnostic** — Detects your stack automatically. Works with any language, framework, or monorepo setup.
- **Cost-optimized** — Routes simple tasks to cheap/fast models, saves expensive models for complex work.
- **Self-improving** — Each run feeds learnings back. Model routing gets more accurate, QA failures get prevented, known fixes get applied instantly.

## Commands

```bash
/ship "Add user notifications with email and in-app channels"  # Full run
/ship --resume                    # Continue from last checkpoint
/ship --phase=qa                  # Run QA only
/ship --phase=fix                 # Run fix cycle only
/ship --phase=doc                 # Generate docs only
```

Quick commands during a run: `status`, `skip`, `pause`, `replan`, `qa only`, `doc only`.
