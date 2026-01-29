#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

SKILL_NAME="autonomous-agent"
SKILLS_DIR="$HOME/.claude/skills"

echo ""
echo "=================================="
echo "  Autonomous Agent Skill Uninstaller"
echo "=================================="
echo ""

# Check if skill exists
if [ ! -d "$SKILLS_DIR/$SKILL_NAME" ]; then
    echo -e "${YELLOW}Skill not found at $SKILLS_DIR/$SKILL_NAME${NC}"
    echo "Nothing to uninstall."
    exit 0
fi

# Confirm uninstall
echo "This will remove: $SKILLS_DIR/$SKILL_NAME"
read -p "Are you sure? (y/N) " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

# Remove skill
rm -rf "$SKILLS_DIR/$SKILL_NAME"

# Verify removal
if [ ! -d "$SKILLS_DIR/$SKILL_NAME" ]; then
    echo ""
    echo -e "${GREEN}Uninstall successful!${NC}"
    echo ""
else
    echo -e "${RED}Uninstall failed. Please manually remove: $SKILLS_DIR/$SKILL_NAME${NC}"
    exit 1
fi
