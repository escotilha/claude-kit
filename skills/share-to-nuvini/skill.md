---
name: share-to-nuvini
description: Share skills or agents to the nuvini-claude repository. Use when the user wants to share, export, or sync a skill or agent to their nuvini-claude repo. Triggers on "share skill", "share agent", "export to nuvini", "sync to nuvini", or "/share".
user-invocable: true
allowed-tools:
  - Bash
  - Read
  - Glob
  - AskUserQuestion
---

# Share to Nuvini-Claude

This skill copies selected skills or agents from the active Claude Code configuration to the nuvini-claude repository for version control and sharing.

## Paths

- **Source Skills**: `/Users/ps/code/claude/skills/`
- **Source Agents**: `/Users/ps/code/claude/agents/`
- **Destination Skills**: `/Users/ps/code/nuvini-claude/skills/`
- **Destination Agents**: `/Users/ps/code/nuvini-claude/agents/`

## Workflow

### Step 1: Determine What to Share

If the user specifies what to share (e.g., `/share website-design`), use that directly.

Otherwise, ask the user:

```
What would you like to share to nuvini-claude?

1. A skill
2. An agent
3. Multiple items
```

### Step 2: List Available Items

**For skills:**

```bash
ls -1 /Users/ps/code/claude/skills/ | grep -v README
```

**For agents:**

```bash
ls -1 /Users/ps/code/claude/agents/
```

Present the list and let the user choose, or accept their input if already provided.

### Step 3: Check for Existing Files

Before copying, check if the item already exists in the destination:

```bash
# For a skill
ls -la /Users/ps/code/nuvini-claude/skills/<skill-name> 2>/dev/null

# For an agent
ls -la /Users/ps/code/nuvini-claude/agents/<agent-name> 2>/dev/null
```

If it exists, inform the user it will be overwritten and ask for confirmation.

### Step 4: Copy the Item

**For a skill (can be a directory or single .md file):**

```bash
# Check if it's a directory
if [ -d "/Users/ps/code/claude/skills/<skill-name>" ]; then
  cp -r "/Users/ps/code/claude/skills/<skill-name>" "/Users/ps/code/nuvini-claude/skills/"
else
  cp "/Users/ps/code/claude/skills/<skill-name>.md" "/Users/ps/code/nuvini-claude/skills/"
fi
```

**For an agent:**

```bash
cp -r "/Users/ps/code/claude/agents/<agent-name>" "/Users/ps/code/nuvini-claude/agents/"
```

### Step 5: Show Git Status

After copying, show what changed:

```bash
cd /Users/ps/code/nuvini-claude && git status --short
```

### Step 6: Offer to Commit

Ask the user if they want to commit the changes:

```
Successfully shared <item-name> to nuvini-claude!

Would you like me to commit this change?
- Yes, commit now
- No, I'll commit later
```

If yes, create a commit:

```bash
cd /Users/ps/code/nuvini-claude && \
git add . && \
git commit -m "feat(skills): add <skill-name>"
# or "feat(agents): add <agent-name>"
```

## Quick Mode

If the user provides the item name directly (e.g., `/share website-design`), skip the prompts and:

1. Detect if it's a skill or agent by checking both locations
2. Copy it
3. Show git status
4. Offer to commit

## Examples

**User:** `/share`
**Response:** List both skills and agents, ask what to share

**User:** `/share website-design`
**Response:** Copy website-design skill, show status, offer to commit

**User:** `share the autonomous-agent skill to nuvini`
**Response:** Copy autonomous-agent, show status, offer to commit

## Error Handling

- If the item doesn't exist, show available items
- If the destination repo doesn't exist, inform the user
- If copy fails, show the error and suggest fixes
