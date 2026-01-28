# Claude Kit

Open source toolkit for Claude Code CLI: skills, agents, and memory.

## What's Included

| Component | Purpose |
|-----------|---------|
| **Skills** | Reusable task instructions (`/commit`, `/deploy`, `/test`) |
| **Agents** | Specialized subagents for complex tasks |
| **Memory** | Persistent knowledge and context across sessions |

## Quick Install

```bash
# Clone repository
git clone https://github.com/escotilha/claude-kit.git
cd claude-kit

# Install skills
cp -r skills/* ~/.claude/skills/

# Install agents
cp -r agents/* ~/.claude/agents/

# Install memory templates
mkdir -p ~/.claude/memory
cp memory/core-memory-template.json ~/.claude/memory/core-memory.json
cp memory/session-context-template.json ~/.claude/memory/session-context.json
```

---

## Skills

### Autonomous Dev (`autonomous-dev`)

Autonomous coding agent that breaks features into user stories and implements them iteratively.

```
"Build a user authentication system"
"Create a PRD for dashboard feature"
```

### Claude Setup Optimizer (`claude-setup-optimizer`)

Analyzes Claude Code changelog and recommends improvements to your setup.

```
"Optimize my claude setup"
"/optimize-setup"
```

### Full-Spectrum Testing (`fulltest-skill`)

Maps sites, spawns parallel testers, auto-fixes issues.

```
"Test http://localhost:3000 and fix issues"
"/fulltest"
```

### CTO Advisor (`cto`)

Technical leadership: architecture, security, performance, code quality.

```
/cto
"Do a security audit"
"Review this codebase"
```

### CPO AI (`cpo-ai-skill`)

Chief Product Officer AI - from idea to production-ready application.

```
/cpo-go my-app Create a task management application
```

### Skill Loader (`skill-loader`)

Load skills from external GitHub repositories.

```
"Load skills from github.com/owner/repo"
"Update my skills"
```

### Worktree Scaffold (`worktree-scaffold`)

Parallel feature development with git worktrees.

```
"Create worktree for feature-name"
```

---

## Agents

| Agent | Purpose |
|-------|---------|
| `fulltesting-agent` | Full E2E testing with Chrome DevTools |
| `frontend-agent` | React, Vue, Angular, Next.js, Svelte |
| `api-agent` | REST/GraphQL API design and implementation |
| `database-agent` | Schema design, migrations, query optimization |
| `devops-agent` | CI/CD, Docker, cloud deployments |
| `orchestrator-fullstack` | Multi-layer feature coordination |

---

## Memory

Memory provides persistent knowledge across Claude Code sessions.

### Components

1. **Core Memory** (`core-memory.json`) - Static user profile, preferences, beliefs
2. **Session Context** (`session-context.json`) - Dynamic session state
3. **Memory MCP** - Knowledge graph for entities and relations

### Setup

1. Copy templates to `~/.claude/memory/`
2. Edit `core-memory.json` with your information
3. Add session hook to load memory at startup

See [memory/README.md](memory/README.md) for detailed setup instructions.

### Memory vs Skills

| Memory | Skills |
|--------|--------|
| Facts and context | Task instructions |
| "Uses pnpm" | "How to commit" |
| Nouns | Verbs |

---

## Configuration

### Memory Hook

Add to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cat ~/.claude/memory/core-memory.json"
          }
        ]
      }
    ]
  }
}
```

### Memory MCP

```json
{
  "mcp": {
    "mcpServers": {
      "memory": {
        "command": "npx",
        "args": ["-y", "@modelcontextprotocol/server-memory"]
      }
    }
  }
}
```

### Chrome DevTools MCP (for testing)

```json
{
  "mcp": {
    "mcpServers": {
      "chrome-devtools": {
        "command": "npx",
        "args": ["-y", "chrome-devtools-mcp"]
      }
    }
  }
}
```

---

## Repository Structure

```
claude-kit/
├── README.md
├── skills/
│   ├── autonomous-dev/
│   ├── claude-setup-optimizer/
│   ├── cto/
│   ├── skill-loader/
│   ├── cpo-ai-skill/
│   ├── fulltest-skill/
│   └── worktree-scaffold/
├── agents/
│   ├── fulltesting-agent.md
│   ├── frontend-agent.md
│   ├── api-agent.md
│   ├── database-agent.md
│   ├── devops-agent.md
│   └── orchestrator-fullstack.md
├── memory/
│   ├── README.md
│   ├── core-memory-template.json
│   └── session-context-template.json
└── LICENSE
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

MIT License - see LICENSE file.

---

**Repository:** [github.com/escotilha/claude-kit](https://github.com/escotilha/claude-kit)
