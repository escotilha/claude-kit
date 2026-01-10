# Claude Code Setup

My personal Claude Code configuration and tools for quick setup on new machines.

## 🚀 Quick Install

```bash
git clone https://github.com/YOUR_USERNAME/claude-setup.git ~/.claude-setup
cd ~/.claude-setup
./install.sh
```

## 📦 What's Included

- **Settings**: Core Claude Code configuration with 14 MCP servers
- **Agents**: 9 specialized agents for development and M&A workflows
- **Commands**: 4 custom slash commands for M&A analysis
- **Skills**: 3 production M&A skills (triage, proposal, presentation)
- **MCP Servers**: Custom nuvini-mna MCP server with 3 tools
- **Scripts**: Multi-agent launcher, snapshot, and rollback tools
- **Guides**: Agent coordination and setup documentation

## 🛠️ Components

### MCP Servers (14 Total)

**Official Servers:**

- **filesystem**: Local file access (`/Users/psm2`)
- **github**: GitHub repository integration
- **postgres**: PostgreSQL database access
- **sequential-thinking**: Enhanced problem-solving
- **memory**: Persistent knowledge graph
- **puppeteer**: Browser automation
- **fetch**: Web content fetching
- **resend**: Email sending via Resend API
- **slack**: Slack integration (legacy)
- **slack-app**: Slack app integration
- **notion**: Notion workspace access
- **gmail**: Gmail integration
- **google-calendar**: Google Calendar access

**Custom Servers:**

- **nuvini-mna**: Custom M&A analysis tools
  - `triage_deal` - Score M&A opportunities (0-10)
  - `generate_proposal` - Create financial proposals with IRR/MOIC
  - `create_presentation` - Generate board approval decks

See [mcp-servers/README.md](mcp-servers/README.md) for detailed documentation.

### Agents (9 Specialized)

- **frontend-agent**: React, Vue, Next.js, TypeScript
- **backend-agent**: Node.js, Python, Go, APIs
- **fulltesting-agent**: Unit, integration, E2E tests
- **security-agent**: Security reviews and audits
- **devops-agent**: CI/CD, Docker, infrastructure
- **database-agent**: Schema design and optimization
- **documentation-agent**: README, API docs
- **codereview-agent**: PR reviews and quality checks
- **flight-price-optimizer**: Flight price optimization

### Skills (3 M&A Skills)

- **triage-analyzer**: Score M&A opportunities 0-10 against investment criteria
- **mna-proposal-generator**: Generate financial proposals with IRR/MOIC calculations
- **committee-presenter**: Create board approval presentations (5-slide or 20+ slide)

See [skills/README.md](skills/README.md) for detailed documentation.

### Commands (4 M&A Workflows)

- **/triage**: Quick deal triage workflow
- **/analyze-deal**: Comprehensive deal analysis
- **/financial-model**: Financial modeling workflow
- **/generate-deck**: Presentation generation

### Utility Scripts

- **claude-agents**: Launch multiple specialized agents in tmux
- **claude-snapshot**: Create git snapshots for rollback
- **claude-rollback**: Interactive rollback to previous snapshots

## 📝 Manual Installation

If you prefer manual setup:

### 1. Settings

```bash
cp settings.json ~/.claude/settings.json
```

### 2. Agents

```bash
cp -r agents ~/.claude/
```

### 3. Commands

```bash
cp -r commands ~/.claude/
```

### 4. Skills

```bash
cp -r skills ~/.config/claude/
```

### 5. Scripts

```bash
cp bin/* ~/bin/
chmod +x ~/bin/claude-*
```

### 6. Documentation

```bash
cp guides/AGENT_COORDINATION_GUIDE.md ~/.claude/
```

## ⚙️ Environment Variables

Create a `.env` file or add to your shell profile:

```bash
# GitHub
export GITHUB_PERSONAL_ACCESS_TOKEN="your_token"

# Slack
export SLACK_BOT_TOKEN="your_token"
export SLACK_TEAM_ID="your_team_id"
export SLACK_APP_TOKEN="your_app_token"

# Notion
export NOTION_API_KEY="your_key"

# Resend
export RESEND_API_KEY="your_key"

# Gmail (if using)
export GMAIL_CLIENT_ID="your_client_id"
export GMAIL_CLIENT_SECRET="your_secret"
export GMAIL_REFRESH_TOKEN="your_token"

# Google Calendar (if using)
export GOOGLE_CALENDAR_API_KEY="your_key"
```

## 🎯 Usage

### Launch Single Agent

```bash
claude code
```

### Launch Multiple Agents

```bash
# Full-stack development (frontend, backend, testing, security)
claude-agents . --full-stack

# Custom combination
claude-agents . --agents frontend,backend,documentation

# Using presets
claude-agents . --preset core      # frontend, backend, testing
claude-agents . --preset infra     # devops, database, backend
claude-agents . --preset review    # codereview, security, testing
```

### Create Snapshots

```bash
# Before major changes
claude-snapshot frontend "pre-refactor"

# At checkpoints
claude-snapshot backend "api-complete"
```

### Rollback Changes

```bash
# Interactive rollback menu
claude-rollback
```

### Custom Commands

```bash
# M&A Analysis
/triage
/analyze-deal
/financial-model
/generate-deck
```

## 🔧 Customization

### Add Your Own Agent

1. Create `~/.claude/agents/your-agent.md`
2. Follow the frontmatter format:

```markdown
---
name: Your Agent
description: Agent description
tools: Bash, Read, Write, Edit
color: #FF5733
---

# Your Agent

[Your agent instructions here]
```

### Add Custom Commands

1. Create `~/.claude/commands/your-command.md`
2. Add instructions for the command

### Modify Settings

Edit `~/.claude/settings.json` to:

- Add/remove MCP servers
- Change default arguments
- Configure thinking mode

## 📚 Resources

- [Claude Code Documentation](https://docs.claude.com)
- [MCP Servers](https://github.com/modelcontextprotocol)
- [Agent Coordination Guide](guides/AGENT_COORDINATION_GUIDE.md)

## 🤝 Contributing

Feel free to fork and customize for your own use!

## 📄 License

MIT
