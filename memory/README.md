# Claude Code Memory System

A comprehensive guide to implementing persistent memory for Claude Code, enabling context that survives across sessions.

## Table of Contents

- [Why Memory Matters](#why-memory-matters)
- [Memory vs Skills vs Agents](#memory-vs-skills-vs-agents)
- [Memory Architecture](#memory-architecture)
- [Core Memory](#core-memory)
- [Session Context](#session-context)
- [Knowledge Graph (Memory MCP)](#knowledge-graph-memory-mcp)
- [Setup Guide](#setup-guide)
- [Memory Design Patterns](#memory-design-patterns)
- [Best Practices](#best-practices)
- [Advanced Configurations](#advanced-configurations)
- [Troubleshooting](#troubleshooting)

---

## Why Memory Matters

Every Claude Code session starts fresh. Without memory, Claude:

- Asks about your preferences repeatedly
- Doesn't know your project context
- Can't learn from past interactions
- Treats you like a stranger every time

With memory, Claude:

- Remembers your coding style and preferences
- Knows your active projects and tech stacks
- Recalls decisions made in previous sessions
- Builds understanding over time

**Memory transforms Claude from a stateless tool into a persistent collaborator.**

---

## Memory vs Skills vs Agents

These three components serve fundamentally different purposes:

| Component | Type | Purpose | Example |
|-----------|------|---------|---------|
| **Memory** | Nouns | Store facts and context | "Uses TypeScript strict mode" |
| **Skills** | Verbs | Define how to do tasks | `/commit` - how to make commits |
| **Agents** | Workers | Execute complex workflows | `frontend-agent` - builds UI |

### Analogy

Think of Claude as a new employee:

- **Memory** = Their notes about you, your preferences, past conversations
- **Skills** = Procedures they've learned (how to submit reports, run meetings)
- **Agents** = Specialists they can delegate to (accountant, designer, lawyer)

Memory is **what Claude knows**. Skills are **what Claude can do**. Agents are **who Claude can ask for help**.

---

## Memory Architecture

Claude Code memory operates on three layers:

```
┌─────────────────────────────────────────────────────────────┐
│                     MEMORY LAYERS                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Layer 1: CORE MEMORY (Static)                      │   │
│  │  ─────────────────────────────────────────────────  │   │
│  │  • User profile and identity                        │   │
│  │  • Stable preferences (rarely change)               │   │
│  │  • Coding beliefs and principles                    │   │
│  │  • Tool integrations                                │   │
│  │                                                     │   │
│  │  Loaded: Session start via hook                     │   │
│  │  Storage: JSON file                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Layer 2: SESSION CONTEXT (Dynamic)                 │   │
│  │  ─────────────────────────────────────────────────  │   │
│  │  • Current focus and working topic                  │   │
│  │  • Attention weights for relevance                  │   │
│  │  • Recent context window                            │   │
│  │  • Memory application tracking                      │   │
│  │                                                     │   │
│  │  Updated: Throughout session                        │   │
│  │  Storage: JSON file (ephemeral)                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                           │                                 │
│                           ▼                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  Layer 3: KNOWLEDGE GRAPH (Persistent)              │   │
│  │  ─────────────────────────────────────────────────  │   │
│  │  • Entities: people, projects, decisions            │   │
│  │  • Relations: connections between entities          │   │
│  │  • Observations: facts attached to entities         │   │
│  │                                                     │   │
│  │  Updated: As knowledge is gained                    │   │
│  │  Storage: Memory MCP (local or cloud database)      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Layer Responsibilities

| Layer | Volatility | Update Frequency | Best For |
|-------|------------|------------------|----------|
| Core Memory | Very stable | Monthly/quarterly | Identity, preferences, beliefs |
| Session Context | Ephemeral | Every session | Current focus, attention |
| Knowledge Graph | Semi-stable | As needed | Projects, decisions, learnings |

---

## Core Memory

Core memory is the foundation—stable facts about you that rarely change.

### Structure

```json
{
  "version": "1.0.0",
  "lastUpdated": "2026-01-28",

  "userProfile": {
    "name": "Your Name",
    "username": "github-username",
    "role": "Software Engineer at Company",
    "expertise": ["TypeScript", "React", "Node.js"],
    "workContext": "Building SaaS products",
    "communicationStyle": "direct, technical, minimal"
  },

  "preferences": {
    "packageManager": "pnpm",
    "deployment": {
      "primary": "Vercel",
      "alternatives": ["Railway", "Cloudflare"]
    },
    "database": {
      "primary": "PostgreSQL",
      "orm": "Prisma"
    },
    "codeStyle": {
      "principle": "simplicity over cleverness",
      "preferPatterns": ["early returns", "composition"],
      "avoidPatterns": ["deep nesting", "premature abstraction"]
    }
  },

  "beliefs": [
    "Simple solutions beat clever ones",
    "Delete code rather than comment it out",
    "Tests verify behavior, not implementation"
  ],

  "projectContext": {
    "activeProjects": ["ProjectA", "ProjectB"],
    "techStack": {
      "ProjectA": "Next.js + Supabase",
      "ProjectB": "Express + PostgreSQL"
    }
  }
}
```

### What Belongs in Core Memory

**Include:**
- Your name and professional identity
- Programming languages and frameworks you use
- Package manager preference (npm, pnpm, yarn, bun)
- Deployment platforms you use
- Database preferences
- Code style principles
- Active projects and their tech stacks
- Communication preferences

**Exclude:**
- Frequently changing information
- Project-specific details (use knowledge graph)
- Temporary decisions
- Session-specific context

### Loading Core Memory

Core memory loads at session start via a hook:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '=== CORE MEMORY ===' && cat ~/.claude/memory/core-memory.json"
          }
        ]
      }
    ]
  }
}
```

The `echo` prefix helps Claude recognize this as memory context.

---

## Session Context

Session context tracks the current session's state—what you're working on right now.

### Structure

```json
{
  "currentSession": {
    "startedAt": "2026-01-28T10:00:00Z",
    "project": "my-app",
    "workingDirectory": "/Users/me/code/my-app"
  },

  "currentFocus": {
    "topic": "authentication system",
    "since": "2026-01-28T10:15:00Z",
    "relatedFiles": [
      "src/auth/login.ts",
      "src/middleware/auth.ts"
    ],
    "keyDecisions": [
      "Using JWT with httpOnly cookies",
      "Refresh tokens stored in database"
    ]
  },

  "attentionWeights": {
    "weights": {
      "authentication": 1.0,
      "database": 0.7,
      "deployment": 0.2
    }
  },

  "recentContext": {
    "entries": [
      {"topic": "fixed login bug", "timestamp": "..."},
      {"topic": "added password reset", "timestamp": "..."}
    ]
  }
}
```

### Attention Weights

Attention weights help prioritize which memories are most relevant:

- **1.0** = Directly relevant to current work
- **0.5-0.9** = Related but not primary focus
- **0.1-0.4** = Background context
- **0.0** = Not relevant this session

### When to Update Session Context

- When switching projects
- When changing focus areas
- When making key decisions
- At session end (for continuity)

---

## Knowledge Graph (Memory MCP)

The knowledge graph stores structured knowledge as entities and relations.

### Concepts

**Entities** are things: people, projects, technologies, decisions.

```json
{
  "name": "authentication-system",
  "entityType": "feature",
  "observations": [
    "Uses JWT tokens",
    "Refresh tokens stored in PostgreSQL",
    "15-minute access token expiry"
  ]
}
```

**Relations** connect entities:

```
User --works_on--> Project
Project --uses--> Technology
Feature --depends_on--> Feature
Decision --affects--> Project
```

**Observations** are facts attached to entities:

```
Entity: "my-app"
Observations:
  - "Next.js 14 with App Router"
  - "Deployed on Vercel"
  - "Uses Supabase for auth and database"
```

### Entity Types

| Type | Purpose | Examples |
|------|---------|----------|
| `user` | People | You, team members |
| `project` | Codebases | my-app, api-service |
| `technology` | Tools and frameworks | React, PostgreSQL |
| `feature` | Specific functionality | auth-system, dashboard |
| `decision` | Architectural choices | "Use REST over GraphQL" |
| `pattern` | Recurring approaches | "Repository pattern" |
| `preference` | User preferences | code-style, tooling |
| `belief` | Principles | "Simplicity over cleverness" |
| `learning` | Lessons learned | "Avoid X because Y" |

### Relation Types

| Relation | Meaning | Example |
|----------|---------|---------|
| `works_on` | Active involvement | User --works_on--> Project |
| `uses` | Technology usage | Project --uses--> React |
| `has_preference` | User preference | User --has_preference--> pnpm |
| `depends_on` | Dependency | Feature --depends_on--> Auth |
| `believes` | Principle adherence | User --believes--> Simplicity |
| `learned_from` | Knowledge source | Learning --learned_from--> Project |
| `decided` | Decision made | User --decided--> Decision |
| `affects` | Impact relationship | Decision --affects--> Project |

### Memory MCP Tools

| Tool | Purpose | When to Use |
|------|---------|-------------|
| `create_entities` | Add new entities | Learning something new |
| `add_observations` | Add facts to entities | Gaining more detail |
| `create_relations` | Connect entities | Establishing relationships |
| `search_nodes` | Find relevant memories | Recalling information |
| `open_nodes` | Get full entity details | Deep dive on topic |
| `read_graph` | View entire graph | Understanding full context |
| `delete_entities` | Remove outdated info | Cleaning up |
| `delete_observations` | Remove specific facts | Correcting information |
| `delete_relations` | Remove connections | Updating relationships |

### Example Knowledge Graph

```
                    ┌─────────────┐
                    │    User     │
                    │  (Pierre)   │
                    └──────┬──────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │ Project  │    │ Project  │    │Preference│
    │(Contably)│    │(AgentApp)│    │(pnpm)    │
    └────┬─────┘    └────┬─────┘    └──────────┘
         │               │
    ┌────┴────┐     ┌────┴────┐
    ▼         ▼     ▼         ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Next.js│ │Supabase│ │Express│ │Postgres│
└───────┘ └───────┘ └───────┘ └───────┘
```

---

## Setup Guide

### Step 1: Create Directory Structure

```bash
mkdir -p ~/.claude/memory
```

### Step 2: Initialize Core Memory

Copy the template and customize:

```bash
cp core-memory-template.json ~/.claude/memory/core-memory.json
```

Edit with your information:

```bash
# Use your preferred editor
code ~/.claude/memory/core-memory.json
```

### Step 3: Initialize Session Context

```bash
cp session-context-template.json ~/.claude/memory/session-context.json
```

### Step 4: Configure Session Hook

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '=== CORE MEMORY ===' && cat ~/.claude/memory/core-memory.json 2>/dev/null || echo 'No core memory found'"
          }
        ]
      }
    ]
  }
}
```

### Step 5: Setup Memory MCP (Optional)

For knowledge graph persistence, add Memory MCP:

**Option A: Local file storage**

```json
{
  "mcp": {
    "mcpServers": {
      "memory": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"],
        "env": {
          "MEMORY_FILE_PATH": "~/.claude/memory/knowledge-graph.json"
        }
      }
    }
  }
}
```

**Option B: Cloud storage (Turso)**

For cross-device sync:

```json
{
  "mcp": {
    "mcpServers": {
      "memory": {
        "command": "node",
        "args": ["/path/to/memory-turso/dist/index.js"],
        "env": {
          "TURSO_DATABASE_URL": "libsql://your-db.turso.io",
          "TURSO_AUTH_TOKEN": "your-token"
        }
      }
    }
  }
}
```

### Step 6: Verify Setup

Start a new Claude Code session and verify:

1. Core memory loads at startup
2. Memory MCP tools are available (`/mcp` to check)
3. You can create and query entities

---

## Memory Design Patterns

### Pattern 1: Project Onboarding

When starting a new project, create entities:

```
Create entities:
- Project entity with tech stack observations
- Key feature entities
- Architecture decision entities
- Relations between them
```

### Pattern 2: Decision Recording

When making architectural decisions:

```
Create decision entity:
- Name: "use-jwt-authentication"
- Type: decision
- Observations:
  - "Chosen over session-based auth"
  - "Reason: stateless, works with microservices"
  - "Trade-off: larger request size"
- Relations:
  - affects -> project
  - decided_by -> user
```

### Pattern 3: Learning Capture

When learning something new:

```
Create learning entity:
- Name: "prisma-connection-pooling"
- Type: learning
- Observations:
  - "Must configure connection limit for serverless"
  - "Use pgbouncer for high concurrency"
  - "Learned from production incident"
- Relations:
  - learned_from -> project
  - relates_to -> PostgreSQL
```

### Pattern 4: Preference Evolution

When preferences change:

```
Add observation to existing entity:
- Entity: code-preferences
- New observation: "Switched from Zustand to Jotai for atomic state"
```

### Pattern 5: Memory Consolidation

Periodically consolidate memories:

1. Remove stale entities (unused for 90+ days)
2. Merge duplicate information
3. Promote frequently-used patterns to core memory
4. Archive completed project entities

---

## Best Practices

### DO

- **Keep core memory focused** - Only stable, essential information
- **Use descriptive entity names** - `auth-jwt-implementation` not `auth1`
- **Add context to observations** - "Uses pnpm (faster than npm, better monorepo support)"
- **Create relations** - Connections make knowledge retrievable
- **Review periodically** - Memories can become stale
- **Version your memory files** - Track changes over time

### DON'T

- **Don't store sensitive data** - No passwords, tokens, or secrets
- **Don't over-document** - Memory isn't a changelog
- **Don't create entities for everything** - Only meaningful knowledge
- **Don't skip relations** - Isolated entities are hard to find
- **Don't let memory grow unbounded** - Consolidate regularly

### Memory Hygiene

**Weekly:**
- Review recent entities for accuracy
- Remove temporary or test entities

**Monthly:**
- Update core memory if preferences changed
- Consolidate similar entities
- Review decision entities still relevant

**Quarterly:**
- Archive completed project entities
- Promote stable patterns to core memory
- Clean up unused relations

---

## Advanced Configurations

### Multi-Device Sync

Use cloud-backed storage for memories across devices:

1. **Turso** - Distributed SQLite
2. **Supabase** - PostgreSQL with real-time
3. **iCloud/Dropbox** - File sync for JSON storage

### Project-Specific Memory

Load different memories per project using hooks:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cat .claude/project-memory.json 2>/dev/null || cat ~/.claude/memory/core-memory.json"
          }
        ]
      }
    ]
  }
}
```

### Memory-Aware Skills

Skills can interact with memory:

```markdown
# My Skill

## Instructions

1. Search memory for relevant context:
   - `mcp__memory__search_nodes` with project name

2. Apply learned patterns from memory

3. Store new learnings:
   - Create entities for decisions made
   - Add observations to existing entities
```

### Attention-Weighted Retrieval

Query memories based on current focus:

```
Given attention weights:
  authentication: 1.0
  database: 0.7

Search for entities related to "authentication" first,
then "database" for supporting context.
```

---

## Troubleshooting

### Core Memory Not Loading

**Symptom:** Claude doesn't know your preferences at session start.

**Solutions:**
1. Check hook configuration in `~/.claude/settings.json`
2. Verify file exists: `cat ~/.claude/memory/core-memory.json`
3. Check for JSON syntax errors: `jq . ~/.claude/memory/core-memory.json`
4. Restart Claude Code session

### Memory MCP Not Connected

**Symptom:** Memory tools not available.

**Solutions:**
1. Run `/mcp` to check server status
2. Verify MCP configuration in settings
3. Check server logs for errors
4. Try reinstalling: `npx -y @modelcontextprotocol/server-memory`

### Search Returns Empty

**Symptom:** `search_nodes` finds nothing.

**Solutions:**
1. Check entities exist: `read_graph`
2. Try broader search terms
3. Verify entity names match search query
4. Check if using correct Memory MCP instance

### Memory Growing Too Large

**Symptom:** Slow queries, large file size.

**Solutions:**
1. Run memory consolidation
2. Delete stale entities
3. Archive old project data
4. Split into multiple memory files

### Sync Conflicts (Multi-Device)

**Symptom:** Different memories on different devices.

**Solutions:**
1. Use cloud-backed storage (Turso)
2. Always pull before starting session
3. Implement conflict resolution strategy
4. Keep critical info in core memory (file-synced)

---

## Memory MCP Tool Reference

### create_entities

Create new entities in the knowledge graph.

```json
{
  "entities": [
    {
      "name": "my-project",
      "entityType": "project",
      "observations": [
        "Next.js 14 application",
        "Uses App Router",
        "Deployed on Vercel"
      ]
    }
  ]
}
```

### add_observations

Add facts to existing entities.

```json
{
  "observations": [
    {
      "entityName": "my-project",
      "contents": [
        "Added authentication with Clerk",
        "Migrated to Drizzle ORM"
      ]
    }
  ]
}
```

### create_relations

Connect entities together.

```json
{
  "relations": [
    {
      "from": "User",
      "to": "my-project",
      "relationType": "works_on"
    },
    {
      "from": "my-project",
      "to": "Next.js",
      "relationType": "uses"
    }
  ]
}
```

### search_nodes

Find entities by query.

```json
{
  "query": "authentication"
}
```

Returns entities matching the query in name, type, or observations.

### open_nodes

Get full details of specific entities.

```json
{
  "names": ["my-project", "authentication-system"]
}
```

### read_graph

Get the entire knowledge graph.

```json
{}
```

Returns all entities and relations.

### delete_entities

Remove entities and their relations.

```json
{
  "entityNames": ["old-project", "deprecated-feature"]
}
```

### delete_observations

Remove specific observations from entities.

```json
{
  "deletions": [
    {
      "entityName": "my-project",
      "observations": ["Outdated fact to remove"]
    }
  ]
}
```

### delete_relations

Remove specific relations.

```json
{
  "relations": [
    {
      "from": "User",
      "to": "old-project",
      "relationType": "works_on"
    }
  ]
}
```

---

## Further Reading

- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [Memory MCP Server](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)

---

**Questions or improvements?** Open an issue at [github.com/escotilha/claude-kit](https://github.com/escotilha/claude-kit/issues)
