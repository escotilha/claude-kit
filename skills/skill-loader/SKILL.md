---
name: skill-loader
description: "Load and install skills from external GitHub repositories. Manages skill sources and keeps local skills up-to-date."
user-invocable: true
context: keep
version: 1.0.0
tools: [Bash, Read, Write, Glob, Grep, Task, WebFetch]
model: sonnet
color: "#6366F1"
triggers:
  - "load skills from"
  - "install skills from"
  - "add skill source"
  - "update skills"
  - "list skill sources"
  - "/load-skills"
  - "/skill-loader"
---

# Skill Loader

Load and install Claude Code skills from external GitHub repositories.

## Overview

This skill manages external skill sources, allowing you to:
- Load skills from any GitHub repository containing Claude Code skills
- Maintain a list of trusted skill sources
- Update skills from all configured sources
- Install individual skills or entire collections

## Activation

This skill activates when the user wants to:
- Load skills from a GitHub URL
- Add a new skill source
- Update existing skills
- List configured sources

## Workflow

### 1. Load Skills from URL

When user provides a GitHub URL:

```
User: "Load skills from https://github.com/escotilha/skills"
```

**Steps:**
1. Parse and validate the GitHub URL
2. Check if repository contains skills (look for `skills/` directory)
3. Clone repository to temporary location
4. Copy skills to `~/.claude/skills/`
5. Copy agents to `~/.claude/agents/`
6. Optionally save source to `~/.claude/skill-sources.json`
7. Report installed skills

### 2. Add Skill Source (Persistent)

Save a repository as a trusted source:

```
User: "Add skill source https://github.com/escotilha/skills"
```

**Steps:**
1. Validate repository URL
2. Add to `~/.claude/skill-sources.json`
3. Optionally install skills immediately

### 3. Update All Skills

Refresh skills from all sources:

```
User: "Update skills" or "/update-skills"
```

**Steps:**
1. Read `~/.claude/skill-sources.json`
2. For each source, pull latest changes
3. Copy updated skills/agents
4. Report what changed

### 4. List Sources

Show configured sources:

```
User: "List skill sources"
```

## Implementation

### Parsing GitHub URLs

Accept these formats:
- `https://github.com/owner/repo`
- `https://github.com/owner/repo.git`
- `github.com/owner/repo`
- `owner/repo` (shorthand)

Extract: `owner` and `repo` name

### Directory Structure

Skills are installed to:
```
~/.claude/
├── skills/              # Skill definitions
│   ├── skill-name/
│   │   └── SKILL.md
│   └── ...
├── agents/              # Agent definitions
│   ├── agent-name.md
│   └── ...
└── skill-sources.json   # Configured sources
```

### skill-sources.json Format

```json
{
  "version": "1.0",
  "sources": [
    {
      "url": "https://github.com/escotilha/skills",
      "name": "escotilha-skills",
      "added": "2026-01-25T00:00:00Z",
      "lastUpdated": "2026-01-25T00:00:00Z",
      "enabled": true
    }
  ],
  "settings": {
    "autoUpdate": false,
    "backupBeforeUpdate": true
  }
}
```

### Clone and Install Process

```bash
# Create temp directory
TEMP_DIR=$(mktemp -d)

# Clone repository (shallow for speed)
git clone --depth 1 https://github.com/owner/repo.git "$TEMP_DIR"

# Check for skills directory
if [ -d "$TEMP_DIR/skills" ]; then
    # Copy skills (preserve directory structure)
    cp -r "$TEMP_DIR/skills/"* ~/.claude/skills/
fi

# Check for agents directory
if [ -d "$TEMP_DIR/agents" ]; then
    # Copy agents
    cp -r "$TEMP_DIR/agents/"* ~/.claude/agents/
fi

# Cleanup
rm -rf "$TEMP_DIR"
```

### Safety Checks

Before installing:
1. **Validate repository exists** - Use GitHub API or git ls-remote
2. **Check for skills structure** - Must have `skills/` or `agents/` directory
3. **Warn on overwrites** - Alert if existing skills will be replaced
4. **Backup existing** - Optionally backup before overwriting

### Error Handling

- **Invalid URL**: Provide format examples
- **Repo not found**: Suggest checking URL
- **No skills found**: Explain expected structure
- **Permission denied**: Suggest checking git credentials
- **Network error**: Retry with exponential backoff

## Commands

| Command | Description |
|---------|-------------|
| `/load-skills <url>` | Load skills from GitHub URL |
| `/add-source <url>` | Add URL as persistent source |
| `/update-skills` | Update from all sources |
| `/list-sources` | List configured sources |
| `/remove-source <name>` | Remove a source |

## Examples

### Load from URL
```
User: Load skills from https://github.com/escotilha/skills

Claude: [skill-loader activates]
- Cloning repository...
- Found 6 skills: autonomous-dev, claude-setup-optimizer, cpo-ai-skill, cto, fulltest-skill, worktree-scaffold
- Found 6 agents: frontend-agent, api-agent, database-agent, devops-agent, fulltesting-agent, orchestrator-fullstack
- Installing to ~/.claude/skills/ and ~/.claude/agents/
- Done! Skills are now available.
- Would you like to save this as a skill source? (y/n)
```

### Add Persistent Source
```
User: Always load skills from https://github.com/escotilha/skills

Claude: [skill-loader activates]
- Adding source to ~/.claude/skill-sources.json
- Source "escotilha-skills" added successfully
- Installing skills now...
- 6 skills and 6 agents installed
```

### Update All Sources
```
User: Update my skills

Claude: [skill-loader activates]
- Reading skill sources...
- Found 2 sources: escotilha-skills, my-custom-skills
- Updating escotilha-skills... 2 skills updated
- Updating my-custom-skills... no changes
- Update complete!
```

## Memory Integration

When the user says "always load skills from X", this skill:
1. Adds the source to `~/.claude/skill-sources.json`
2. Installs the skills immediately
3. Remembers the preference for future sessions

## Output Format

After successful installation, report:
```
Installed Skills:
- skill-name-1 (v1.0.0) - Description
- skill-name-2 (v2.1.0) - Description

Installed Agents:
- agent-name-1 - Description
- agent-name-2 - Description

Source saved: escotilha-skills
Location: ~/.claude/skills/
```

## Troubleshooting

### "Repository not found"
- Check the URL is correct
- Ensure the repository is public or you have access

### "No skills found in repository"
- Repository must have a `skills/` directory with SKILL.md files
- Or an `agents/` directory with .md agent files

### "Permission denied"
- For private repos, ensure git credentials are configured
- Use SSH URLs if HTTPS fails