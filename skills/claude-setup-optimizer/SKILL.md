---
name: claude-setup-optimizer
version: 1.0.0
color: "#3b82f6"
description: Analyzes Claude Code changelog, reviews your current agents/skills setup, and recommends improvements based on new features. Use when asked to "optimize claude setup", "check for claude updates", "improve my agents", "sync with claude changelog", or "/optimize-setup".
user-invocable: true
context: fork
allowed-tools:
  - WebFetch
  - WebSearch
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - TaskCreate
  - TaskUpdate
  - TaskList
---

# Claude Setup Optimizer

Automatically analyzes the Claude Code changelog and recommends improvements to your agents, skills, and configuration based on new features.

## What This Skill Does

1. **Fetches Latest Changelog** - Gets the most recent Claude Code changelog from official sources
2. **Analyzes Your Setup** - Reviews all your agents, skills, commands, and configuration
3. **Identifies Opportunities** - Finds ways your setup could benefit from new Claude features
4. **Recommends Improvements** - Provides specific, actionable recommendations
5. **Implements Changes** - Optionally applies improvements automatically

## Paths

### ALWAYS USE ICLOUD PATH DIRECTLY

**Source of Truth:**

```
/Users/ps/Library/Mobile Documents/com~apple~CloudDocs/claude-setup/
├── skills/       ← All skills
├── agents/       ← All agents
├── commands/     ← All commands
└── settings.json ← Settings
```

**IMPORTANT:** Always read from AND write to the iCloud path directly. Do NOT use symlink paths like `~/.claude/` or `/Users/ps/code/claude/` - use the full iCloud path to ensure:
- Consistent behavior regardless of symlink state
- Changes persist correctly to iCloud
- No issues with symlink resolution

### Background (FYI only)

Claude Code searches for skills/agents in multiple locations, but symlinks point everything to iCloud:

- `~/.claude/skills` → iCloud
- `~/.claude/agents` → iCloud
- `~/.claude/commands` → iCloud
- `/Users/ps/code/claude/` → iCloud

## Workflow

### Step 1: Fetch Claude Code Changelog

Fetch the latest Claude Code changelog using strategies that handle large files:

**Primary Source - GitHub CLI (Recommended):**

Use the `gh` CLI to fetch recent releases which avoids large file issues:

```bash
# Get the 5 most recent releases with full details
gh release list --repo anthropics/claude-code --limit 5

# Get detailed notes for a specific release
gh release view <tag> --repo anthropics/claude-code
```

**Secondary Source - GitHub Releases Page:**

Use WebFetch on the releases page (summarized, not full changelog):

```
https://github.com/anthropics/claude-code/releases
```

Prompt: "Extract the 3 most recent releases with their version numbers, dates, and key new features. Focus on: new tools, skill/agent updates, MCP changes, configuration options."

**Tertiary Source - Web Search:**

Search for "Claude Code changelog 2026" or "Claude Code new features" for recent announcements.

**IMPORTANT: Avoid fetching the full CHANGELOG.md file directly** - it exceeds token limits (~32K tokens). If you must read it, use the Read tool with `limit` parameter to read only the first 500 lines:

```
Read file with limit=500 to get only recent entries
```

Extract key information:

- New features and capabilities
- New tools or MCP changes
- Skill/agent system updates
- Configuration options
- Breaking changes
- Best practice updates

### Step 2: Analyze Current Setup

**IMPORTANT:** Always use the iCloud path directly for all operations (both reading and writing):

```
/Users/ps/Library/Mobile Documents/com~apple~CloudDocs/claude-setup/
```

**Inventory all skills:**

```bash
# Use iCloud path directly
find "/Users/ps/Library/Mobile Documents/com~apple~CloudDocs/claude-setup/skills" -maxdepth 2 \( -name "SKILL.md" -o -name "skill.md" \) 2>/dev/null
```

For each skill, read and extract:

- Name and description
- Allowed tools
- Triggers/activation patterns
- Dependencies

**Inventory all agents:**

```bash
# Use iCloud path directly
find "/Users/ps/Library/Mobile Documents/com~apple~CloudDocs/claude-setup/agents" -name "*.md" 2>/dev/null
```

For each agent, read and extract:

- Name and purpose
- Tools it uses
- Subagent relationships

**Inventory all commands:**

```bash
# Use iCloud path directly
ls "/Users/ps/Library/Mobile Documents/com~apple~CloudDocs/claude-setup/commands/"*.md 2>/dev/null
```

**Read configuration files:**

```bash
# Settings in iCloud
cat "/Users/ps/Library/Mobile Documents/com~apple~CloudDocs/claude-setup/settings.json"

# Global Claude config
cat ~/.claude.json
```

### Step 3: Compare and Identify Opportunities

Cross-reference changelog features against your current setup:

**Feature Categories to Check:**

1. **New Tools**: Are there new tools you're not using that could benefit your workflows?
2. **Skill System Updates**: Has the skill format changed? Are there new frontmatter options?
3. **Agent Improvements**: New agent capabilities or patterns?
4. **MCP Updates**: New MCP servers or protocol changes?
5. **Performance Optimizations**: Parallelization, caching, or efficiency improvements?
6. **Security Features**: New permission patterns or security best practices?
7. **Configuration Options**: New settings that could improve your experience?

**Analysis Checklist:**

For each skill/agent, check:

- [ ] Uses latest skill format (SKILL.md with frontmatter)
- [ ] Takes advantage of parallel tool calls where applicable
- [ ] Uses appropriate model selection (haiku for fast tasks, etc.)
- [ ] Has proper error handling patterns
- [ ] Follows current best practices for triggers/descriptions
- [ ] Uses new tools/features that weren't available before

### Step 4: Generate Recommendations

Create a structured report with:

**Priority Levels:**

- **HIGH**: Security improvements, breaking change migrations, significant efficiency gains
- **MEDIUM**: New feature adoption, best practice updates
- **LOW**: Nice-to-have improvements, style updates

**Recommendation Format:**

```markdown
## [Priority] Recommendation Title

**Affected Items:** skill-name, agent-name, etc.

**Current State:**
Description of how it works now

**Recommended Change:**
What should be changed and why

**New Feature Reference:**
Link to changelog or documentation

**Implementation:**
Specific steps or code changes needed

**Effort:** Low/Medium/High
```

### Step 5: Present and Confirm

Present findings to the user:

```
# Claude Setup Optimization Report

## Changelog Summary
- Version X.Y.Z released on DATE
- Key new features: [list]

## Your Setup Analysis
- X skills analyzed
- Y agents analyzed
- Z commands analyzed

## Recommendations Found: N

### High Priority (M items)
1. [Brief description]
2. ...

### Medium Priority (N items)
1. ...

### Low Priority (P items)
1. ...

Would you like me to:
1. Show detailed recommendations for all items
2. Show only HIGH priority recommendations
3. Auto-implement all HIGH priority changes
4. Auto-implement specific recommendations
5. Skip implementation (just review)
```

### Step 6: Implement Improvements

**IMPORTANT: iCloud is the source of truth.** All changes MUST be made directly in the iCloud path to ensure they sync across devices:

```
/Users/ps/Library/Mobile Documents/com~apple~CloudDocs/claude-setup/
```

For approved changes:

1. **Back up affected files first (in iCloud):**

```bash
ICLOUD_PATH="/Users/ps/Library/Mobile Documents/com~apple~CloudDocs/claude-setup"
mkdir -p "$ICLOUD_PATH/backups/$(date +%Y%m%d-%H%M%S)"
cp <file> "$ICLOUD_PATH/backups/$(date +%Y%m%d-%H%M%S)/"
```

2. **Apply changes using Edit or Write tools to the iCloud path directly**
   - Always use the full iCloud path: `/Users/ps/Library/Mobile Documents/com~apple~CloudDocs/claude-setup/...`
   - Do NOT edit via symlinks (`~/.claude/` or `/Users/ps/code/claude/`) to ensure changes are persisted to iCloud

3. **Validate changes:**

- Check syntax/format is valid
- Ensure no breaking changes to existing functionality

4. **Verify files exist in iCloud:**

```bash
ls -la "/Users/ps/Library/Mobile Documents/com~apple~CloudDocs/claude-setup/skills/<skill-name>/"
```

5. **Auto-commit and push to GitHub:**

After all approved changes are made, automatically commit and push to the backup repo. The iCloud folder IS a git repo linked to GitHub:

```bash
ICLOUD_PATH="/Users/ps/Library/Mobile Documents/com~apple~CloudDocs/claude-setup"
cd "$ICLOUD_PATH"

# Stage all changes
git add -A

# Commit with descriptive message
git commit -m "feat: apply claude-setup-optimizer recommendations

Changes applied:
- [list of changes made]

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"

# Push to GitHub backup repo
git push origin main
```

**GitHub Backup Repo:** https://github.com/escotilha/claude

This step runs automatically after implementing approved changes - no user confirmation needed.

## Example Recommendations

### Example 1: New Tool Usage

````markdown
## [MEDIUM] Add WebSearch to financial-data-extractor skill

**Affected Items:** financial-data-extractor

**Current State:**
Skill only uses WebFetch for external data

**Recommended Change:**
Add WebSearch to allowed-tools to enable broader research capabilities when extracting financial data from unfamiliar sources.

**New Feature Reference:**
Claude Code v2.x added native WebSearch tool

**Implementation:**
Add `WebSearch` to allowed-tools in frontmatter:

```yaml
allowed-tools:
  - Read
  - WebFetch
  - WebSearch # NEW
```
````

**Effort:** Low

````

### Example 2: Parallel Execution
```markdown
## [HIGH] Enable parallel agent execution in project-orchestrator

**Affected Items:** project-orchestrator.md

**Current State:**
Agent launches subagents sequentially

**Recommended Change:**
Update orchestrator to launch independent agents (frontend, backend, database) in parallel using multiple Task tool calls in single message.

**New Feature Reference:**
Task tool now supports parallel agent launches

**Implementation:**
Update the workflow section to specify parallel launch pattern for independent tasks.

**Effort:** Medium
````

### Example 3: Skill Format Migration

```markdown
## [HIGH] Migrate legacy .skill files to SKILL.md format

**Affected Items:** financial-data-extractor.skill

**Current State:**
Using legacy .skill format

**Recommended Change:**
Migrate to new SKILL.md format with YAML frontmatter for better Claude recognition and metadata support.

**New Feature Reference:**
SKILL.md is now the recommended format

**Implementation:**

1. Rename file to SKILL.md
2. Add YAML frontmatter with name, description, allowed-tools
3. Update content to match new format

**Effort:** Low
```

## Triggers

This skill activates on:

- "optimize my claude setup"
- "check claude code updates"
- "improve my agents"
- "sync with claude changelog"
- "what's new in claude code"
- "update my skills for new features"
- "/optimize-setup"

## Error Handling

### Large File Errors

If you encounter "File content exceeds maximum allowed tokens" when fetching changelog:

1. **Use `gh` CLI instead** - Fetch releases via `gh release list` and `gh release view`
2. **Read with limits** - Use `Read` tool with `limit=500` to get only recent entries
3. **Use WebSearch** - Search for "Claude Code new features 2026" for recent announcements
4. **Fetch releases page** - WebFetch the releases page with a focused prompt

Never attempt to fetch the full CHANGELOG.md via WebFetch - it's too large.

## Notes

- Always preserve existing functionality when making changes
- Create backups before modifying files
- Test changes before committing
- Some recommendations may require manual review
- Keep track of which changelog versions have been reviewed to avoid duplicate work
