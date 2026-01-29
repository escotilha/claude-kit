#!/bin/bash
# Session End Hook - Capture learnings for memory system
# Location: ~/Library/Mobile Documents/com~apple~CloudDocs/claude-setup/hooks/session-end.sh

set -euo pipefail

MEMORY_DIR="$HOME/Library/Mobile Documents/com~apple~CloudDocs/claude-setup/memory"
SESSIONS_DIR="$MEMORY_DIR/sessions"
DATE=$(date +%Y-%m-%d)
TIME=$(date +%H%M%S)

# Create directories if needed
mkdir -p "$SESSIONS_DIR"

# Parse input from Claude Code (if available)
INPUT=$(cat 2>/dev/null || echo '{}')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // "unknown"' 2>/dev/null || echo "unknown")
WORKING_DIR=$(echo "$INPUT" | jq -r '.cwd // "unknown"' 2>/dev/null || echo "unknown")

# Detect project from working directory
PROJECT="unknown"
if [[ "$WORKING_DIR" == *"contably"* ]]; then
  PROJECT="Contably"
elif [[ "$WORKING_DIR" == *"agentcreator"* ]] || [[ "$WORKING_DIR" == *"AgentCreator"* ]]; then
  PROJECT="AgentCreator"
elif [[ "$WORKING_DIR" == *"mna"* ]] || [[ "$WORKING_DIR" == *"nuvini"* ]]; then
  PROJECT="M&A Toolkit"
fi

# Create session log
SESSION_FILE="$SESSIONS_DIR/${DATE}-${TIME}-session.json"
cat > "$SESSION_FILE" << EOF
{
  "date": "$DATE",
  "time": "$(date +%H:%M:%S)",
  "sessionId": "$SESSION_ID",
  "project": "$PROJECT",
  "workingDirectory": "$WORKING_DIR",
  "learnings": [],
  "memoriesApplied": [],
  "status": "pending_review"
}
EOF

# Output reminder for memory capture
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📝 SESSION ENDED - Memory Capture Reminder"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Project: $PROJECT"
echo "Session logged: $SESSION_FILE"
echo ""
echo "To capture learnings from this session:"
echo "  • Run /consolidate --health to check memory status"
echo "  • Or manually add to Memory MCP with mcp__memory__create_entities"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

exit 0
