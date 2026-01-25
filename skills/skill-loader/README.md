# Skill Loader

Load and manage Claude Code skills from external GitHub repositories.

## Quick Start

```
# Load skills from a GitHub repository
"Load skills from https://github.com/escotilha/skills"

# Add as persistent source (remembered across sessions)
"Always load skills from https://github.com/escotilha/skills"

# Update all skills from saved sources
"Update my skills"
```

## Features

- **One-time Install**: Load skills from any GitHub URL
- **Persistent Sources**: Save repositories as skill sources
- **Auto-Update**: Keep skills up-to-date from all sources
- **Smart Detection**: Automatically finds skills and agents in repositories

## Commands

| Command | Description |
|---------|-------------|
| `load skills from <url>` | Install skills from GitHub URL |
| `always load skills from <url>` | Add as persistent source |
| `update skills` | Refresh from all saved sources |
| `list skill sources` | Show configured sources |
| `remove skill source <name>` | Remove a saved source |

## Supported URL Formats

All these formats work:
- `https://github.com/owner/repo`
- `https://github.com/owner/repo.git`
- `github.com/owner/repo`
- `owner/repo` (shorthand)

## Configuration

Sources are saved to `~/.claude/skill-sources.json`:

```json
{
  "version": "1.0",
  "sources": [
    {
      "url": "https://github.com/escotilha/skills",
      "name": "escotilha-skills",
      "added": "2026-01-25T00:00:00Z",
      "enabled": true
    }
  ]
}
```

## Repository Requirements

For a repository to be a valid skill source, it must have:

```
repository/
├── skills/           # Required for skills
│   ├── skill-name/
│   │   └── SKILL.md  # Skill definition
│   └── ...
└── agents/           # Optional for agents
    ├── agent-name.md
    └── ...
```

## Installation Location

Skills are installed to:
- Skills: `~/.claude/skills/`
- Agents: `~/.claude/agents/`

## Examples

### Load from Escotilha Skills

```
User: Load skills from https://github.com/escotilha/skills

Claude: Cloning repository...
Found 6 skills:
  - autonomous-dev (v1.0.0)
  - claude-setup-optimizer (v1.0.0)
  - cpo-ai-skill (v2.1.0)
  - cto (v1.0.0)
  - fulltest-skill (v1.0.0)
  - worktree-scaffold (v1.0.0)

Found 6 agents:
  - frontend-agent
  - api-agent
  - database-agent
  - devops-agent
  - fulltesting-agent
  - orchestrator-fullstack

Installed to ~/.claude/skills/ and ~/.claude/agents/
```

### Add Persistent Source

```
User: Always load skills from github.com/escotilha/skills

Claude: Adding source "escotilha-skills"...
Source saved to ~/.claude/skill-sources.json
Installing skills...
Done! 6 skills and 6 agents installed.
```

### Update All Sources

```
User: Update my skills

Claude: Updating from 1 source...
- escotilha-skills: 2 skills updated
Update complete!
```

## Troubleshooting

### "Repository not found"
Ensure the URL is correct and the repository is public.

### "No skills found"
The repository must have a `skills/` directory with SKILL.md files.

### "Permission denied"
For private repositories, ensure your git credentials are configured.

## Related

- [Skill Creation Guide](../README.md)
- [Claude Code Documentation](https://docs.anthropic.com/claude-code)
