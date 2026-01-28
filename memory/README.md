# Claude Code Memory System

Persistent memory for Claude Code using knowledge graphs and structured context files.

## Overview

Memory in Claude Code serves a different purpose than skills:

| Concept | Purpose | Example |
|---------|---------|---------|
| **Memory** | Store facts, preferences, context | "Uses pnpm", "Prefers Tailwind" |
| **Skills** | Define how to perform tasks | `/commit`, `/deploy` |

**Memory = nouns (what you know). Skills = verbs (what you do).**

## Components

### 1. Core Memory (`core-memory.json`)

Static file loaded at session start containing:

- **User profile** - Name, role, expertise, communication style
- **Preferences** - Package manager, deployment, database, styling
- **Beliefs** - Coding principles and philosophies
- **Project context** - Active projects and tech stacks
- **Tool integrations** - Configured services and MCP servers

### 2. Session Context (`session-context.json`)

Dynamic file for tracking current session state:

- **Current focus** - What topic you're working on
- **Attention weights** - Relevance scores for different topics
- **Recent context** - Rolling window of recent work
- **Memory application log** - Track which memories were useful

### 3. Memory MCP (Knowledge Graph)

Persistent database for entities and relations:

- **Entities** - People, projects, preferences, patterns
- **Relations** - Connections between entities
- **Observations** - Facts attached to entities

## Setup

### Step 1: Create Memory Directory

```bash
mkdir -p ~/.claude/memory
cp core-memory-template.json ~/.claude/memory/core-memory.json
cp session-context-template.json ~/.claude/memory/session-context.json
```

### Step 2: Configure Session Hook

Add to `~/.claude/settings.json`:

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

### Step 3: Setup Memory MCP (Optional)

For persistent knowledge graph storage, add Memory MCP:

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

Or use a cloud-backed memory server like Turso for cross-device sync.

## Usage

### Populating Core Memory

Edit `core-memory.json` with your information:

```json
{
  "userProfile": {
    "name": "Your Name",
    "role": "Software Engineer",
    "expertise": ["TypeScript", "React", "Node.js"],
    "communicationStyle": "direct, technical"
  },
  "preferences": {
    "packageManager": "pnpm",
    "deployment": {
      "primary": "Vercel"
    }
  }
}
```

### Using Memory MCP

Query memories:
```
"What do you know about my preferences?"
```

Create entities:
```
"Remember that Project X uses PostgreSQL"
```

Search memories:
```
"What projects am I working on?"
```

### Memory Consolidation

Periodically consolidate memories to:
- Remove stale or unused entries
- Promote frequently-used patterns to core memory
- Clean up duplicate information

## Best Practices

1. **Keep core memory focused** - Only essential, stable information
2. **Use entities for dynamic knowledge** - Projects, learnings, decisions
3. **Review periodically** - Prune outdated information
4. **Separate concerns** - Core memory (static) vs MCP (dynamic)

## Memory MCP Tools

| Tool | Purpose |
|------|---------|
| `create_entities` | Create new memory entities |
| `search_nodes` | Search memories by query |
| `open_nodes` | Get full details of specific entities |
| `add_observations` | Add facts to existing entities |
| `create_relations` | Create relationships between entities |
| `delete_entities` | Remove memory entities |
| `delete_relations` | Remove relationships |
| `read_graph` | Get entire knowledge graph |

## Example Entities

```
User (entity) --has_preference--> code-preferences (entity)
User (entity) --works_on--> Project (entity)
Project (entity) --uses--> tech-stack (entity)
```

## Troubleshooting

**Memory not loading at session start:**
- Check hook configuration in settings.json
- Verify file paths are correct
- Run `cat ~/.claude/memory/core-memory.json` to test

**Memory MCP not working:**
- Run `/mcp` to check connected servers
- Verify MCP server configuration
- Check for errors in Claude Code logs
