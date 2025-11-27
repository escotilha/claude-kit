#!/bin/bash
set -euo pipefail

echo "🚀 Installing Claude Code Setup..."
echo ""

# Color codes
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Determine script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if Claude Code is installed
if ! command -v claude &> /dev/null; then
    echo -e "${YELLOW}⚠️  Claude Code not found. Please install it first:${NC}"
    echo "   npm install -g @anthropic-ai/claude-code"
    echo "   or visit: https://docs.claude.com"
    exit 1
fi

echo -e "${BLUE}📋 Installation Plan:${NC}"
echo "   - Settings    → ~/.claude/"
echo "   - Agents      → ~/.claude/agents/"
echo "   - Commands    → ~/.claude/commands/"
echo "   - Skills      → ~/.config/claude/skills/"
echo "   - Scripts     → ~/bin/"
echo "   - Guides      → ~/.claude/"
echo ""

read -p "Continue with installation? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Installation cancelled."
    exit 0
fi

echo ""
echo -e "${BLUE}📁 Creating directories...${NC}"

# Create necessary directories
mkdir -p ~/.claude
mkdir -p ~/.claude/agents
mkdir -p ~/.claude/commands
mkdir -p ~/.config/claude/skills
mkdir -p ~/bin

echo -e "${GREEN}✓${NC} Directories created"

# Backup existing files
echo ""
echo -e "${BLUE}💾 Backing up existing configuration...${NC}"

if [ -f ~/.claude/settings.json ]; then
    BACKUP_TIME=$(date +%Y%m%d_%H%M%S)
    cp ~/.claude/settings.json ~/.claude/settings.json.backup_${BACKUP_TIME}
    echo -e "${GREEN}✓${NC} Backed up settings.json to settings.json.backup_${BACKUP_TIME}"
fi

# Install settings
echo ""
echo -e "${BLUE}⚙️  Installing settings...${NC}"

if [ -f "$SCRIPT_DIR/settings.json" ]; then
    # Merge settings if existing settings file is present
    if [ -f ~/.claude/settings.json ]; then
        echo -e "${YELLOW}  Existing settings found. Manual merge may be required.${NC}"
        cp "$SCRIPT_DIR/settings.json" ~/.claude/settings.json.new
        echo -e "${YELLOW}  New settings saved to: ~/.claude/settings.json.new${NC}"
        echo -e "${YELLOW}  Please review and merge manually.${NC}"
    else
        cp "$SCRIPT_DIR/settings.json" ~/.claude/settings.json
        echo -e "${GREEN}✓${NC} Settings installed"
    fi
fi

# Install agents
echo ""
echo -e "${BLUE}🤖 Installing agents...${NC}"

if [ -d "$SCRIPT_DIR/agents" ]; then
    cp -r "$SCRIPT_DIR/agents/"* ~/.claude/agents/
    echo -e "${GREEN}✓${NC} Agents installed ($(ls -1 "$SCRIPT_DIR/agents" | wc -l | tr -d ' ') files)"
fi

# Install commands
echo ""
echo -e "${BLUE}⚡ Installing custom commands...${NC}"

if [ -d "$SCRIPT_DIR/commands" ]; then
    cp -r "$SCRIPT_DIR/commands/"* ~/.claude/commands/
    echo -e "${GREEN}✓${NC} Commands installed ($(ls -1 "$SCRIPT_DIR/commands" | wc -l | tr -d ' ') files)"
fi

# Install skills
echo ""
echo -e "${BLUE}🎓 Installing skills...${NC}"

if [ -d "$SCRIPT_DIR/skills" ]; then
    cp -r "$SCRIPT_DIR/skills/"* ~/.config/claude/skills/
    echo -e "${GREEN}✓${NC} Skills installed"
fi

# Install scripts
echo ""
echo -e "${BLUE}📜 Installing utility scripts...${NC}"

if [ -d "$SCRIPT_DIR/bin" ]; then
    cp "$SCRIPT_DIR/bin/"* ~/bin/
    chmod +x ~/bin/claude-*
    echo -e "${GREEN}✓${NC} Scripts installed and made executable"
    
    # Check if ~/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/bin:"* ]]; then
        echo -e "${YELLOW}⚠️  ~/bin is not in your PATH${NC}"
        echo "   Add this to your ~/.zshrc or ~/.bashrc:"
        echo "   export PATH=\"\$HOME/bin:\$PATH\""
    fi
fi

# Install guides
echo ""
echo -e "${BLUE}📚 Installing guides...${NC}"

if [ -d "$SCRIPT_DIR/guides" ]; then
    cp -r "$SCRIPT_DIR/guides/"* ~/.claude/
    echo -e "${GREEN}✓${NC} Guides installed"
fi

# Check for required tools
echo ""
echo -e "${BLUE}🔍 Checking dependencies...${NC}"

if ! command -v tmux &> /dev/null; then
    echo -e "${YELLOW}⚠️  tmux not found (required for claude-agents)${NC}"
    echo "   Install with: brew install tmux"
else
    echo -e "${GREEN}✓${NC} tmux found"
fi

if ! command -v npx &> /dev/null; then
    echo -e "${YELLOW}⚠️  npx not found (required for MCP servers)${NC}"
    echo "   Install Node.js from: https://nodejs.org"
else
    echo -e "${GREEN}✓${NC} npx found"
fi

# Environment variables reminder
echo ""
echo -e "${BLUE}🔐 Environment Variables${NC}"
echo ""
echo "Don't forget to set up your environment variables:"
echo ""
echo "  export GITHUB_PERSONAL_ACCESS_TOKEN=\"your_token\""
echo "  export SLACK_BOT_TOKEN=\"your_token\""
echo "  export NOTION_API_KEY=\"your_key\""
echo ""
echo "See the README for the complete list."

# Success message
echo ""
echo -e "${GREEN}✅ Installation complete!${NC}"
echo ""
echo "Next steps:"
echo "  1. Set up environment variables (see above)"
echo "  2. Review settings: ~/.claude/settings.json"
echo "  3. Test installation: claude code"
echo "  4. Launch agents: claude-agents . --full-stack"
echo ""
echo "Documentation: ~/.claude/AGENT_COORDINATION_GUIDE.md"
echo ""
