# Claude Code Skills & Agents

Open source collection of powerful skills and agents for Claude Code CLI.

## 🚀 Skills Included

### 1. **Autonomous Dev** (`autonomous-dev`)

Autonomous coding agent that breaks features into small user stories and implements them iteratively with fresh context per iteration.

**Features:**
- PRD generation from feature ideas
- JSON conversion for machine-readable task lists
- Autonomous implementation loop
- Cross-codebase learning with Memory MCP
- Worktree integration for parallel development
- Smart delegation to specialized agents (optional)

**Usage:**
```
"Build a user authentication system"
"Create a PRD for dashboard feature"
"Continue autonomous implementation"
```

**Dependencies:**
- frontend-agent, api-agent, database-agent, devops-agent, orchestrator-fullstack (optional for delegation)
- worktree-scaffold skill (optional for parallel development)

---

### 2. **Claude Setup Optimizer** (`claude-setup-optimizer`)

Analyzes Claude Code changelog, reviews your current agents/skills setup, and recommends improvements based on new features.

**Features:**
- Fetches latest Claude Code changelog
- Analyzes your current skill/agent setup
- Identifies optimization opportunities
- Provides prioritized recommendations
- Auto-implements approved changes

**Usage:**
```
"Optimize my claude setup"
"Check for claude updates"
"/optimize-setup"
```

---

### 3. **Full-Spectrum Testing** (`fulltest-skill`)

Unified full-spectrum testing for websites and applications. Maps sites, spawns parallel testers, analyzes failures, auto-fixes issues.

**Features:**
- Site structure mapping
- Parallel page testing
- Console error detection
- Network failure analysis
- Broken link checking (404s)
- Auto-fix capabilities
- Re-test loops (max 3 iterations)
- Comprehensive reports

**Usage:**
```
"Test http://localhost:3000 and fix issues"
"/fulltest"
```

**Dependencies:**
- fulltesting-agent
- Chrome DevTools MCP

---

### 4. **Worktree Scaffold** (`worktree-scaffold`)

Parallel feature development automation using git worktrees with project scaffolding.

**Features:**
- Feature workspace creation
- Project scaffolding
- Parallel development support
- Workspace cleanup

**Usage:**
```
"Create worktree for feature-name"
"List active workspaces"
"Remove workspace feature-name"
```

---

## 🤖 Agents Included

### Core Agents

- **fulltesting-agent** - Full E2E testing with Chrome DevTools
- **frontend-agent** - React, Vue, Angular, Next.js, Svelte development
- **api-agent** - REST/GraphQL API design and implementation
- **database-agent** - Schema design, migrations, query optimization
- **devops-agent** - CI/CD, Docker, cloud deployments
- **orchestrator-fullstack** - Multi-layer feature coordination

---

## 📦 Installation

### Quick Install (Recommended)

Copy skills and agents to your Claude Code directory:

```bash
# Clone repository
git clone https://github.com/yourusername/claude-code-skills.git
cd claude-code-skills

# Install skills
cp -r skills/* ~/.claude/skills/

# Install agents
cp -r agents/* ~/.claude/agents/

# Verify installation
ls ~/.claude/skills/
ls ~/.claude/agents/
```

### Manual Install

Install individual skills/agents:

```bash
# Install specific skill
cp -r skills/autonomous-dev ~/.claude/skills/

# Install specific agent
cp agents/fulltesting-agent.md ~/.claude/agents/
```

---

## 🔧 Configuration

### Autonomous Dev Setup

1. **Enable Memory MCP** (for cross-codebase learning):
   ```json
   // Add to ~/.claude/settings.json
   {
     "mcp": {
       "servers": {
         "memory": {
           "command": "npx",
           "args": ["-y", "@anthropic-ai/memory-server"]
         }
       }
     }
   }
   ```

2. **Enable Smart Delegation** (optional):
   ```json
   // In your project's prd.json
   {
     "delegation": {
       "enabled": true,
       "fallbackToDirect": true
     }
   }
   ```

3. **Configure Worktrees** (optional):
   ```bash
   # Initialize worktree config in your project
   # Run autonomous-dev, it will prompt to create .worktree-scaffold.json
   ```

### Full-Spectrum Testing Setup

1. **Install Chrome DevTools MCP**:
   ```json
   // Add to ~/.claude/settings.json
   {
     "mcp": {
       "servers": {
         "chrome-devtools": {
           "command": "npx",
           "args": ["-y", "chrome-devtools-mcp"]
         }
       }
     }
   }
   ```

---

## 📖 Usage Examples

### Example 1: Build Feature Autonomously

```
User: "Build a dark mode toggle feature"

Claude: [autonomous-dev activates]
- Asks clarifying questions
- Generates PRD with user stories
- Creates prd.json
- Implements each story iteratively
- Runs verification after each story
- Commits changes
- Creates PR when done
```

### Example 2: Test Website

```
User: "Test http://localhost:3000 and fix any issues"

Claude: [fulltest-skill activates]
- Maps site structure
- Tests all pages in parallel
- Finds console errors and broken links
- Auto-fixes issues
- Re-tests until all pass
- Generates report
```

### Example 3: Optimize Setup

```
User: "Check for claude updates"

Claude: [claude-setup-optimizer activates]
- Fetches latest changelog
- Analyzes your skills/agents
- Recommends HIGH priority: "Add parallel tool calls"
- Implements approved changes
- Creates backup and commits
```

---

## 🎯 Skill Triggers

Each skill activates automatically when you mention relevant keywords:

**Autonomous Dev:**
- "autonomous agent", "build autonomously", "create prd", "user stories"

**Claude Setup Optimizer:**
- "optimize claude setup", "check claude updates", "improve my agents"

**Full-Spectrum Testing:**
- "test the website", "run e2e tests", "test and fix"

**Worktree Scaffold:**
- "create worktree", "checkout feature", "parallel features"

---

## 🔗 Dependencies

### Required MCP Servers

- **Memory MCP** (for autonomous-dev cross-codebase learning)
  ```bash
  npx -y @anthropic-ai/memory-server
  ```

- **Chrome DevTools MCP** (for fulltest-skill)
  ```bash
  npx -y chrome-devtools-mcp
  ```

### Optional but Recommended

- Git (for all features)
- Node.js/npm (for verification commands)
- jq (for JSON manipulation in autonomous-dev)

---

## 📂 Repository Structure

```
claude-code-skills/
├── README.md                           # This file
├── skills/                             # Skills directory
│   ├── autonomous-dev/                 # Autonomous coding agent
│   │   ├── SKILL.md                    # Skill definition
│   │   └── references/                 # Examples and docs
│   ├── claude-setup-optimizer/         # Setup optimizer
│   │   └── SKILL.md
│   ├── fulltest-skill/                 # Full-spectrum testing
│   │   └── SKILL.md
│   └── worktree-scaffold/              # Worktree management
│       └── SKILL.md
├── agents/                             # Agents directory
│   ├── fulltesting-agent.md            # E2E testing agent
│   ├── frontend-agent.md               # Frontend specialist
│   ├── api-agent.md                    # API specialist
│   ├── database-agent.md               # Database specialist
│   ├── devops-agent.md                 # DevOps specialist
│   └── orchestrator-fullstack.md       # Fullstack orchestrator
└── LICENSE                             # Open source license
```

---

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🙏 Acknowledgments

Built for the Claude Code community. Special thanks to Anthropic for the amazing Claude Code CLI.

---

## 📞 Support

- Issues: [GitHub Issues](https://github.com/yourusername/claude-code-skills/issues)
- Discussions: [GitHub Discussions](https://github.com/yourusername/claude-code-skills/discussions)

---

## 🔄 Updates

Check the [CHANGELOG.md](CHANGELOG.md) for version history and updates.

**Current Version:** 1.0.0

**Last Updated:** January 2026
