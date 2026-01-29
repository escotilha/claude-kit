#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SKILL_NAME="autonomous-agent"
SKILLS_DIR="$HOME/.claude/skills"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo ""
echo "=================================="
echo "  Autonomous Agent Skill Installer"
echo "=================================="
echo ""

# Check for required dependencies
echo "Checking dependencies..."
MISSING_DEPS=""
for cmd in jq git; do
    if ! command -v $cmd &> /dev/null; then
        MISSING_DEPS="$MISSING_DEPS $cmd"
    fi
done

if [ -n "$MISSING_DEPS" ]; then
    echo -e "${RED}Error: Required dependencies not found:${NC}$MISSING_DEPS"
    echo ""
    echo "Please install the missing dependencies:"
    echo "  - jq: JSON processor (brew install jq / apt install jq)"
    echo "  - git: Version control (brew install git / apt install git)"
    echo ""
    exit 1
fi
echo -e "${GREEN}All dependencies found.${NC}"
echo ""

# Check if Claude Code config directory exists
if [ ! -d "$HOME/.claude" ]; then
    echo -e "${YELLOW}Warning: ~/.claude directory not found.${NC}"
    echo "Creating it now..."
    mkdir -p "$HOME/.claude"
fi

# Create skills directory if it doesn't exist
if [ ! -d "$SKILLS_DIR" ]; then
    echo "Creating skills directory..."
    mkdir -p "$SKILLS_DIR"
fi

# Check if skill already exists
if [ -d "$SKILLS_DIR/$SKILL_NAME" ]; then
    echo -e "${YELLOW}Skill already installed at $SKILLS_DIR/$SKILL_NAME${NC}"
    read -p "Do you want to overwrite it? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled."
        exit 0
    fi
    rm -rf "$SKILLS_DIR/$SKILL_NAME"
fi

# Copy skill files (SKILL.md and references/)
echo "Installing skill..."
mkdir -p "$SKILLS_DIR/$SKILL_NAME"
cp "$SCRIPT_DIR/SKILL.md" "$SKILLS_DIR/$SKILL_NAME/"
cp -r "$SCRIPT_DIR/references" "$SKILLS_DIR/$SKILL_NAME/"

# Verify installation
if [ -f "$SKILLS_DIR/$SKILL_NAME/SKILL.md" ]; then
    echo ""
    echo -e "${GREEN}Installation successful!${NC}"
    echo ""
    echo "Installed to: $SKILLS_DIR/$SKILL_NAME"
    echo ""
    echo "To use the skill, start Claude Code and type:"
    echo "  /autonomous-agent"
    echo ""
    echo "Or just describe a feature to build and say:"
    echo "  \"build this autonomously\""
    echo ""
else
    echo -e "${RED}Installation failed. Please check permissions and try again.${NC}"
    exit 1
fi
