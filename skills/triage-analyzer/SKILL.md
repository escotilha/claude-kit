---
name: triage-analyzer
description: Analyze M&A opportunities and score them 0-10 against investment criteria. Use when evaluating acquisition targets, identifying red flags, or generating triage reports.
user-invocable: true
model: sonnet
context: fork
version: 1.0.0
color: "#f59e0b"
allowed-tools:
  - Read
  - Write
  - Bash
  - WebFetch
  - WebSearch
  - Glob
  - Grep
  - TaskCreate
  - TaskUpdate
  - TaskList
  - AskUserQuestion
---

# M&A Triage Analyzer

## Session Tracking

Use `${CLAUDE_SESSION_ID}` to track analysis across sessions for comprehensive deal tracking.

### Organizing Multiple Document Extractions

When triaging a deal involves multiple data sources (CIMs, financial statements, pitch decks), organize extractions by session:

```bash
# Create session-specific directories for triage inputs
DEAL_DIR="deals/${COMPANY_NAME}/sessions/${CLAUDE_SESSION_ID}"
mkdir -p "$DEAL_DIR/sources"

# Store all source documents and extractions
cp CIM.pdf "$DEAL_DIR/sources/"
cp financials.xlsx "$DEAL_DIR/sources/"

# Tag triage output with session ID
TRIAGE_OUTPUT="$DEAL_DIR/triage_${CLAUDE_SESSION_ID}.json"
```

### Cross-Referencing with Proposals and Analyses

Link triage sessions with downstream proposal and investment analysis workflows:

```bash
# Include session reference in triage output for traceability
cat > "$TRIAGE_OUTPUT" << EOF
{
  "session_id": "${CLAUDE_SESSION_ID}",
  "timestamp": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "company": "${COMPANY_NAME}",
  "score": 8.2,
  "recommendation": "PROCEED",
  "next_session_type": "proposal",
  "related_sessions": {
    "cim_extraction": "<extraction_session_id>",
    "financial_review": "<review_session_id>"
  }
}
EOF

# Reference triage session when generating proposal
/mna proposal --triage-session ${CLAUDE_SESSION_ID}
```

### Audit Trail for Due Diligence

Maintain complete audit trails for investment committee review and compliance:

```bash
# Create audit log for all triage activities
AUDIT_LOG="deals/${COMPANY_NAME}/audit_trail.log"

# Log triage decision with full context
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] SESSION=${CLAUDE_SESSION_ID} ACTION=triage_initiated COMPANY=${COMPANY_NAME}" >> "$AUDIT_LOG"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] SESSION=${CLAUDE_SESSION_ID} ACTION=data_sources SOURCES=[CIM.pdf,financials.xlsx]" >> "$AUDIT_LOG"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] SESSION=${CLAUDE_SESSION_ID} ACTION=triage_complete SCORE=8.2 RECOMMENDATION=PROCEED" >> "$AUDIT_LOG"
echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] SESSION=${CLAUDE_SESSION_ID} ACTION=handoff NEXT_PHASE=proposal NEXT_SESSION=<proposal_session_id>" >> "$AUDIT_LOG"
```

### Benefits

- **Reproducibility**: Recreate any triage analysis from session artifacts
- **Compliance**: Full audit trail for investment committee due diligence
- **Team collaboration**: Share session IDs across team members
- **Multi-source tracking**: Link all document extractions to their triage context

---

## Name
M&A Triage Analyzer

## Description
Analyzes M&A opportunities and scores them 0-10 against Nuvini's investment criteria. This skill evaluates potential acquisitions across four key dimensions: financial health, business model quality, market position, and strategic fit with the existing portfolio.

## When to Use This Skill
Invoke this skill when you need to:
- Evaluate a potential acquisition target for initial screening
- Score a deal against investment criteria
- Identify red flags and strengths in an M&A opportunity
- Determine if a deal should proceed to financial modeling
- Compare multiple acquisition opportunities
- Generate a triage report for investment committee

## Required Inputs
At minimum, you need:
- **Company name**
- **Revenue** (annual, in millions BRL)
- **EBITDA** (in millions BRL)

## Optional Inputs
For more accurate analysis, provide:
- Revenue growth rate (%)
- EBITDA margin (%)
- Recurring revenue percentage
- Annual churn rate (%)
- Customer count
- Geographic location
- Business model (SaaS, Software, B2B)
- Market vertical (tax_tech, optical, government, etc.)
- Team size
- Founding year

## Output
The skill provides:
- **Overall Score** (0-10 scale)
- **Recommendation** (PROCEED/REVIEW/REJECT)
- **Scoring Breakdown** by category:
  - Financial Health (0-35 points)
  - Business Model (0-25 points)
  - Market Position (0-20 points)
  - Strategic Fit (0-20 points)
- **Strengths** - Key positive factors
- **Weaknesses** - Areas of concern
- **Red Flags** - Disqualifying issues
- **Strategic Fit** - Portfolio synergies assessment
- **Next Steps** - Recommended actions

## Scoring Criteria

### Financial Health (35 points)
- **EBITDA Margin** (15 points)
  - ≥40%: 15 points
  - ≥30%: 10 points
  - ≥20%: 5 points
- **Revenue Growth** (10 points)
  - ≥30%: 10 points
  - ≥20%: 7 points
  - ≥10%: 3 points
- **Cash Conversion** (10 points)
  - ≥80%: 10 points
  - ≥60%: 7 points

### Business Model (25 points)
- **Recurring Revenue** (10 points)
  - ≥95%: 10 points
  - ≥80%: 7 points
  - <80%: 3 points
- **Churn Rate** (10 points)
  - <5%: 10 points
  - ≤8%: 7 points
- **Customer Base** (5 points)
  - >500: 5 points
  - >100: 3 points

### Market Position (20 points)
- Identified vertical focus (8 points)
- Market leadership indicators (7 points)
- Large customer base (5 points)

### Strategic Fit (20 points)
- Portfolio synergies (10 points)
- Integration complexity (5 points)
- Scale potential (5 points)

## Red Flags (Auto-Disqualifiers)
- Not a SaaS/Software business
- Not Brazil-focused
- EBITDA below R$5M or above R$100M
- Churn rate > 15%
- Cash conversion < 60%

## Implementation
**Python Module:** `/Volumes/AI/Code/MNA/nuvini-ma-system-complete/triage-analyzer/scripts/triage_analyzer.py`

Invoke through:
1. **MCP Server** (Recommended): Use `mcp__nuvini-mna__triage_deal` tool
2. **Direct Python**: Import and call `TriageAnalyzer` class
3. **CLI**: Run as command-line tool

## Claude Code Integration
When this skill is invoked in Claude Code, use the Read, Grep, and Bash tools to:
1. Locate or gather company financial data
2. Call the MCP tool `mcp__nuvini-mna__triage_deal` with the parameters
3. Save results with session tracking: `triage_${CLAUDE_SESSION_ID}.json`
4. Present the results to the user with clear recommendations

### Session Tracking Integration

Always use `${CLAUDE_SESSION_ID}` for output files. See the [Session Tracking](#session-tracking) section above for complete documentation on:
- Organizing multiple document extractions per deal
- Cross-referencing extraction sessions with triage/proposals
- Audit trail for due diligence work

## Examples

### Example 1: Complete Triage
```
User: Analyze TechBrasil for acquisition:
- Revenue: R$50M
- EBITDA: R$15M
- Growth: 25% YoY
- SaaS model, tax tech vertical