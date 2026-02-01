---
name: mna-swarm-orchestrator
description: "Orchestrates full M&A deal analysis using swarm of specialists. Spawns parallel workers for financial extraction, triage scoring, proposal generation, and deck creation. Use for end-to-end deal processing from initial screening to board approval."
user-invocable: true
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - Task
  - TaskCreate
  - TaskUpdate
  - TaskList
  - TaskGet
  - TeammateTool
disable-model-invocation: true
hooks:
  Stop:
    - hooks:
        - type: prompt
          prompt: "Review the deal analysis output. Check if: 1) All analysis phases completed 2) Financial data was extracted 3) A comprehensive report was generated. Respond with {\"ok\": true} if complete, or {\"ok\": false, \"reason\": \"what's missing\"} if not."
---

# M&A Swarm Orchestrator

End-to-end M&A deal analysis using swarm mode for maximum parallelization. Coordinates multiple specialist workers to process deals from initial screening through board approval.

## Overview

This orchestrator manages the full M&A pipeline:

```
┌─────────────────────────────────────────────────────────────────┐
│                    M&A SWARM ORCHESTRATOR                        │
│                         (Leader)                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Phase 1: Parallel Intake                                        │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Extractor  │  │   Triage    │  │  Research   │              │
│  │   Worker    │  │   Worker    │  │   Worker    │              │
│  │ (PDF/Excel) │  │  (Scoring)  │  │  (Market)   │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
│         └────────────────┼────────────────┘                      │
│                          ▼                                       │
│  Phase 2: Financial Modeling (Sequential - needs extraction)     │
│  ┌─────────────────────────────────────────┐                    │
│  │           Proposal Generator            │                    │
│  │     (IRR/MOIC, Payment Schedules)       │                    │
│  └─────────────────┬───────────────────────┘                    │
│                    ▼                                             │
│  Phase 3: Parallel Output Generation                            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Analysis   │  │    Deck     │  │    Risk     │              │
│  │  Generator  │  │  Generator  │  │  Assessor   │              │
│  │  (18-page)  │  │  (PPT)      │  │  (Report)   │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Execution Modes

| Mode | Command | Description |
|------|---------|-------------|
| **Swarm** | `/mna swarm [company]` | Full parallel execution with TeammateTool |
| **Sequential** | `/mna full [company]` | Sequential execution (fallback) |
| **Single Phase** | `/mna triage`, `/mna extract`, etc. | Individual skill execution |

## Phase 1: Parallel Intake

Three workers run simultaneously on initial deal materials:

### Extractor Worker
```javascript
{
  name: 'extractor-worker',
  subagent_type: 'general-purpose',
  specialty: 'financial-data-extractor',
  inputs: ['CIM PDF', 'Financial Excel', 'Due diligence docs'],
  outputs: {
    'financials.json': 'Structured financial data',
    'metrics.json': 'Key metrics (revenue, EBITDA, margins)',
    'extraction-notes.md': 'Extraction confidence and gaps'
  }
}
```

### Triage Worker
```javascript
{
  name: 'triage-worker',
  subagent_type: 'general-purpose',
  specialty: 'triage-analyzer',
  inputs: ['Company info', 'Deal memo', 'Initial materials'],
  outputs: {
    'triage-score.json': 'Score 0-10 with breakdown',
    'red-flags.md': 'Identified concerns',
    'recommendation.md': 'Pass/Pursue recommendation'
  }
}
```

### Research Worker
```javascript
{
  name: 'research-worker',
  subagent_type: 'Explore',
  specialty: 'market-research',
  inputs: ['Company name', 'Industry', 'Geography'],
  outputs: {
    'market-analysis.md': 'Market size, trends, competitors',
    'company-background.md': 'History, leadership, news',
    'comparable-deals.md': 'Recent M&A in sector'
  }
}
```

## Phase 2: Financial Modeling

Sequential phase - requires extraction results:

### Proposal Generator
```javascript
{
  name: 'proposal-worker',
  subagent_type: 'general-purpose',
  specialty: 'mna-proposal-generator',
  inputs: ['financials.json', 'triage-score.json'],
  outputs: {
    'proposal.xlsx': 'Financial model with scenarios',
    'irr-moic.json': 'Return calculations',
    'payment-schedule.json': 'Deal structure options',
    'sensitivity-analysis.md': 'Key assumptions and ranges'
  }
}
```

## Phase 3: Parallel Output Generation

Three workers create final deliverables:

### Analysis Generator
```javascript
{
  name: 'analysis-worker',
  subagent_type: 'general-purpose',
  specialty: 'investment-analysis-generator',
  inputs: ['All Phase 1 & 2 outputs'],
  outputs: {
    'investment-analysis.pdf': '18-page comprehensive report'
  }
}
```

### Deck Generator
```javascript
{
  name: 'deck-worker',
  subagent_type: 'general-purpose',
  specialty: 'ma-board-presentation',
  inputs: ['proposal.xlsx', 'triage-score.json', 'market-analysis.md'],
  outputs: {
    'board-deck.pptx': 'Executive presentation (10-20 slides)'
  }
}
```

### Risk Assessor
```javascript
{
  name: 'risk-worker',
  subagent_type: 'general-purpose',
  specialty: 'risk-assessment',
  inputs: ['red-flags.md', 'financials.json', 'market-analysis.md'],
  outputs: {
    'risk-matrix.md': 'Risk categorization and mitigation',
    'deal-breakers.md': 'Critical issues requiring resolution'
  }
}
```

---

## Swarm Execution

### Step 1: Initialize Deal Workspace

```bash
# Create deal directory structure
mkdir -p deals/${COMPANY_NAME}/{inputs,phase1,phase2,phase3,final}

# Copy input materials
cp *.pdf *.xlsx deals/${COMPANY_NAME}/inputs/
```

### Step 2: Spawn Team

```javascript
// Initialize swarm team
await TeammateTool({
  operation: 'spawnTeam',
  team_name: `mna-${companyName}`,
  description: `M&A analysis for ${companyName}`
});
```

### Step 3: Create Task Board

```javascript
// Phase 1 tasks (parallel)
await TaskCreate({
  subject: 'Extract financial data from CIM and Excel',
  description: generateExtractorPrompt(inputs),
  metadata: { phase: 1, type: 'extraction', parallel: true }
});

await TaskCreate({
  subject: 'Score deal against investment criteria',
  description: generateTriagePrompt(inputs),
  metadata: { phase: 1, type: 'triage', parallel: true }
});

await TaskCreate({
  subject: 'Research market and company background',
  description: generateResearchPrompt(companyName, industry),
  metadata: { phase: 1, type: 'research', parallel: true }
});

// Phase 2 task (sequential - blocked by Phase 1)
const phase2Task = await TaskCreate({
  subject: 'Generate financial proposal with IRR/MOIC',
  description: generateProposalPrompt(),
  metadata: { phase: 2, type: 'proposal' }
});
await TaskUpdate({
  taskId: phase2Task.id,
  addBlockedBy: [extractTask.id, triageTask.id]
});

// Phase 3 tasks (parallel - blocked by Phase 2)
// ... similar pattern
```

### Step 4: Spawn Workers

```javascript
// Spawn Phase 1 workers in parallel
await Promise.all([
  Task({
    team_name: `mna-${companyName}`,
    name: 'extractor-worker',
    subagent_type: 'general-purpose',
    run_in_background: true,
    prompt: extractorWorkerPrompt
  }),
  Task({
    team_name: `mna-${companyName}`,
    name: 'triage-worker',
    subagent_type: 'general-purpose',
    run_in_background: true,
    prompt: triageWorkerPrompt
  }),
  Task({
    team_name: `mna-${companyName}`,
    name: 'research-worker',
    subagent_type: 'Explore',
    run_in_background: true,
    prompt: researchWorkerPrompt
  })
]);
```

### Step 5: Monitor and Coordinate

```javascript
async function monitorDeal(teamName) {
  while (true) {
    const tasks = await TaskList();
    const completed = tasks.filter(t => t.status === 'completed');
    const pending = tasks.filter(t => t.status === 'pending' && !t.blockedBy?.length);

    console.log(`Progress: ${completed.length}/${tasks.length} tasks complete`);

    // Check for phase transitions
    const phase1Complete = tasks
      .filter(t => t.metadata?.phase === 1)
      .every(t => t.status === 'completed');

    if (phase1Complete && !phase2Started) {
      console.log('Phase 1 complete. Starting Phase 2...');
      await spawnPhase2Worker(teamName);
      phase2Started = true;
    }

    // All done?
    if (completed.length === tasks.length) {
      break;
    }

    await sleep(5000);
  }
}
```

### Step 6: Compile Final Package

```javascript
async function compileDealPackage(companyName) {
  const dealDir = `deals/${companyName}`;

  // Gather all outputs
  const package = {
    summary: await generateExecutiveSummary(dealDir),
    financials: await read(`${dealDir}/phase2/proposal.xlsx`),
    analysis: await read(`${dealDir}/phase3/investment-analysis.pdf`),
    deck: await read(`${dealDir}/phase3/board-deck.pptx`),
    risks: await read(`${dealDir}/phase3/risk-matrix.md`),
    recommendation: await generateRecommendation(dealDir)
  };

  // Create final package
  await write(`${dealDir}/final/deal-package.zip`, package);

  return package;
}
```

---

## Worker Prompts

### Extractor Worker Prompt

```markdown
# Financial Data Extractor

You are extracting financial data for M&A analysis.

## Input Files
${listInputFiles()}

## Required Outputs

### 1. financials.json
Extract and structure:
- Revenue (3-5 years historical + projections)
- EBITDA and margins
- Net income
- Cash flow metrics
- Balance sheet highlights
- Key ratios

### 2. metrics.json
Calculate:
- Revenue CAGR
- EBITDA margin trends
- Working capital metrics
- Debt/EBITDA ratio
- Customer concentration

### 3. extraction-notes.md
Document:
- Data quality issues
- Missing information
- Assumptions made
- Confidence levels

## Output Format
Save files to: deals/${companyName}/phase1/

> **Note:** TeammateTool messages support **rich Markdown rendering**. Use headers, bold, code blocks, and tables for clear communication between workers and the leader.

When complete, report to leader:
```javascript
TeammateTool.write({
  to: 'leader',
  message: `## Extraction Complete

### Worker Status
- **Worker:** extractor
- **Phase:** 1
- **Quality:** High

### Output Files
| File | Description | Status |
|------|-------------|--------|
| \`financials.json\` | Structured financial data | ✅ Created |
| \`metrics.json\` | Key calculated metrics | ✅ Created |
| \`extraction-notes.md\` | Data quality notes | ✅ Created |

### Data Quality Summary
- **Revenue Data:** 5 years historical, 3 years projected
- **EBITDA:** Complete with margins
- **Confidence Level:** 92%

### Issues Encountered
_None - extraction successful_`
})
```
```

### Triage Worker Prompt

```markdown
# Deal Triage Analyst

Score this deal against Nuvini investment criteria.

## Scoring Criteria (0-10 each)

### Financial Health (25%)
- Revenue stability and growth
- EBITDA margins
- Cash flow generation
- Balance sheet strength

### Business Model (25%)
- Recurring revenue %
- Customer concentration
- Competitive moat
- Scalability

### Market Position (20%)
- Market size and growth
- Competitive landscape
- Geographic presence
- Industry trends

### Strategic Fit (20%)
- Synergy potential
- Integration complexity
- Cultural alignment
- Management quality

### Deal Terms (10%)
- Valuation reasonableness
- Structure flexibility
- Seller motivation
- Timeline

## Required Outputs

### 1. triage-score.json
{
  "overallScore": 7.5,
  "breakdown": {
    "financialHealth": { "score": 8, "rationale": "..." },
    "businessModel": { "score": 7, "rationale": "..." },
    ...
  },
  "recommendation": "PURSUE|PASS|MORE_INFO"
}

### 2. red-flags.md
List any concerns:
- Customer concentration > 20%
- Declining revenue
- Key person dependency
- Regulatory risks
- etc.

### 3. recommendation.md
Executive summary with clear recommendation.

When complete, report to leader with Markdown formatting:
```javascript
TeammateTool.write({
  to: 'leader',
  message: `## Triage Analysis Complete

### Deal Score
| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Financial Health | 8/10 | 25% | 2.00 |
| Business Model | 7/10 | 25% | 1.75 |
| Market Position | 6/10 | 20% | 1.20 |
| Strategic Fit | 8/10 | 20% | 1.60 |
| Deal Terms | 7/10 | 10% | 0.70 |
| **Overall** | **7.25/10** | | |

### Recommendation
**PURSUE** - Deal meets investment criteria.

### Key Strengths
- Strong recurring revenue (85%)
- Healthy EBITDA margins (22%)
- Low customer concentration

### Red Flags Identified
1. **Medium Risk:** Key person dependency on CTO
2. **Low Risk:** Aging tech stack needs modernization

### Output Files
- \`triage-score.json\` ✅
- \`red-flags.md\` ✅
- \`recommendation.md\` ✅`
})
```
```

---

## Configuration

### deal-config.json

```json
{
  "company": "TargetCo",
  "industry": "Accounting Software",
  "geography": "Brazil",
  "dealSize": "$5M-$15M",
  "inputs": {
    "cim": "inputs/TargetCo_CIM.pdf",
    "financials": "inputs/TargetCo_Financials.xlsx",
    "memo": "inputs/Deal_Memo.md"
  },
  "swarm": {
    "enabled": true,
    "teamName": "mna-targetco",
    "workers": {
      "phase1": ["extractor", "triage", "research"],
      "phase2": ["proposal"],
      "phase3": ["analysis", "deck", "risk"]
    },
    "timeout": 600000
  },
  "outputs": {
    "format": ["pdf", "pptx", "xlsx"],
    "branding": "nuvini"
  }
}
```

---

## Commands

| Command | Description |
|---------|-------------|
| `/mna swarm [company]` | Run full swarm analysis |
| `/mna swarm status` | Check swarm progress |
| `/mna swarm workers` | List active workers |
| `/mna swarm phase [1\|2\|3]` | Run specific phase only |
| `/mna swarm resume` | Resume interrupted analysis |
| `/mna swarm cleanup` | Cleanup team resources |

## Task Cleanup

Use `TaskUpdate` with `status: "deleted"` to clean up completed task chains.

---

## Metrics

Track performance in `deal-metrics.json`:

```json
{
  "dealName": "TargetCo",
  "startTime": "2026-01-27T10:00:00Z",
  "endTime": "2026-01-27T10:15:00Z",
  "duration": "15m",
  "phases": {
    "phase1": { "duration": "5m", "workers": 3, "parallel": true },
    "phase2": { "duration": "4m", "workers": 1, "parallel": false },
    "phase3": { "duration": "6m", "workers": 3, "parallel": true }
  },
  "speedupVsSequential": "2.3x",
  "outputs": ["investment-analysis.pdf", "board-deck.pptx", "proposal.xlsx"]
}
```

---

## Expected Performance

| Execution Mode | Phase 1 | Phase 2 | Phase 3 | Total |
|----------------|---------|---------|---------|-------|
| **Sequential** | 15 min | 8 min | 18 min | ~41 min |
| **Swarm** | 5 min | 8 min | 6 min | **~19 min** |
| **Speedup** | 3x | 1x | 3x | **2.2x** |

---

## Error Handling

### Worker Failure
```javascript
if (workerFailed) {
  // 1. Log failure details
  await appendToLog(`Worker ${worker.name} failed: ${error}`);

  // 2. Release task back to pool
  await TaskUpdate({ taskId, status: 'pending', owner: null });

  // 3. Respawn worker
  await respawnWorker(worker.type, teamName);
}
```

### Phase Timeout
```javascript
if (phaseExceedsTimeout) {
  // 1. Notify leader
  console.log(`Phase ${phase} timeout. Partial results available.`);

  // 2. Continue with available data
  await proceedWithPartialResults(phase);
}
```

---

## Integration with Existing Skills

This orchestrator coordinates your existing M&A skills:

| Skill | Used In | Purpose |
|-------|---------|---------|
| `triage-analyzer` | Phase 1 | Deal scoring |
| `financial-data-extractor` | Phase 1 | Data extraction |
| `mna-proposal-generator` | Phase 2 | Financial modeling |
| `investment-analysis-generator` | Phase 3 | PDF report |
| `ma-board-presentation` | Phase 3 | PowerPoint deck |

---

## See Also

- [mna-toolkit](../mna-toolkit/SKILL.md) - Sequential M&A pipeline
- [autonomous-dev](../autonomous-dev/SKILL.md) - Swarm mode reference
- [triage-analyzer](../triage-analyzer/SKILL.md) - Deal scoring criteria
