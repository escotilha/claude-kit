# Unified Memory Strategy

Cross-skill memory conventions for consistent knowledge graph usage.

## Memory Entity Naming Conventions

All memory entities follow the pattern: `{type}:{identifier}`

### Standard Entity Types

| Prefix | Purpose | Used By |
|--------|---------|---------|
| `pattern:` | Reusable code/design patterns | cto, autonomous-dev |
| `mistake:` | Errors to avoid | cto, autonomous-dev |
| `tech-insight:` | Technology-specific learnings | cto, cpo-ai-skill |
| `preference:` | User/project preferences | all skills |
| `research-cache:` | Cached research findings | cpo-ai-skill |
| `design-decision:` | Design choices made | website-design |
| `component-pattern:` | Reusable UI components | website-design |
| `test-pattern:` | Reusable test sequences | testing-agent, fulltest-skill |
| `common-bug:` | Frequently found issues | testing-agent, fulltest-skill |
| `test-selector:` | Reliable CSS/element refs | testing-agent |
| `failure-pattern:` | Categorized test failures | fulltest-skill |
| `architecture:` | Architecture decisions | cto |
| `security:` | Security insights | cto |
| `epic-pattern:` | Epic/stage structures | cpo-ai-skill |
| `product-decision:` | Product choices | cpo-ai-skill |

### Identifier Conventions

- Use lowercase with hyphens: `pattern:early-returns`
- Include project name when project-specific: `design-decision:contably-colors`
- Include date for time-sensitive data: `research-cache:saas-2026-01`
- Use descriptive names: `component-pattern:dashboard-stats-card`

---

## Standard Observations Format

Every entity should include these metadata observations:

```javascript
observations: [
  // Required
  "Discovered: {YYYY-MM-DD}",  // When created

  // Recommended
  "Source: {how learned}",     // implementation, user-feedback, research, mistake
  "Project: {project-name}",   // If project-specific
  "Applies to: {contexts}",    // Technologies, situations

  // For tracking
  "Applied in: {project} - {HELPFUL|NOT HELPFUL}",  // Usage tracking
  "Last used: {YYYY-MM-DD}",   // For decay calculation
]
```

---

## When to Save vs Skip

### Save to Memory When:

1. **High Generality** - Applies to multiple projects/frameworks
2. **Learned from Failure** - Mistakes are valuable
3. **User Explicitly Shared** - Explicit preferences/feedback
4. **Expensive to Regenerate** - Research, competitor analysis
5. **High Severity** - Critical bugs, security issues

### Skip Memory When:

1. **Duplicate Exists** - Similarity > 85% with existing
2. **Project-Specific Detail** - Only applies to one codebase
3. **Trivial/Obvious** - Common knowledge
4. **Low Relevance Score** - Score < 5 (see relevance calculation)

---

## Relevance Score Calculation

Before saving, calculate relevance (threshold: 5):

```javascript
let score = 0;

// Novelty (-∞ if duplicate, -2 if similar)
if (similarity > 0.85) return 0;  // Don't save
if (similarity > 0.6) score -= 2;

// Generality (+2-3)
if (appliesTo.length > 2) score += 3;
else if (appliesTo.length > 1) score += 2;

// Severity (+1-5)
const severityScores = { critical: 5, high: 3, medium: 2, low: 1 };
score += severityScores[severity] || 1;

// Source (+2-3)
if (source === 'mistake') score += 2;
if (source === 'user_feedback') score += 3;

// Frequency (+2)
if (frequencyHint === 'common') score += 2;

return score >= 5;  // Save if true
```

---

## Cross-Skill Memory Queries

### At Session Start

```javascript
// Load user preferences
mcp__memory__search_nodes({ query: "preference:" })

// Load relevant patterns for current work
mcp__memory__search_nodes({ query: "pattern:" })
mcp__memory__search_nodes({ query: "mistake:" })
```

### Before Major Operations

```javascript
// Before design work
mcp__memory__search_nodes({ query: "design-decision:{project}" })
mcp__memory__search_nodes({ query: "component-pattern:" })

// Before testing
mcp__memory__search_nodes({ query: "test-pattern:{app}" })
mcp__memory__search_nodes({ query: "common-bug:" })

// Before architecture decisions
mcp__memory__search_nodes({ query: "architecture:" })
mcp__memory__search_nodes({ query: "tech-insight:{technology}" })

// Before product research
mcp__memory__search_nodes({ query: "research-cache:{vertical}" })
```

---

## Memory Lifecycle

```
Session Learning
      │
      ▼
┌─────────────────┐
│ Relevance Check │ ─── Score < 5 ──► Discard
└────────┬────────┘
         │
    Score >= 5
         │
         ▼
┌─────────────────┐
│  Long-term MCP  │
│    (Memory)     │
└────────┬────────┘
         │
         ├── Use tracking (Applied in: X)
         │
         ▼
┌─────────────────┐
│  Consolidation  │ ─── Stale/Ineffective ──► Archive & Delete
│  (/consolidate) │
└────────┬────────┘
         │
    High usage + effectiveness
         │
         ▼
┌─────────────────┐
│  Core Memory    │
│  (Stable)       │
└─────────────────┘
```

---

## Skills Memory Integration Status

| Skill | Memory Tools | Entity Types Used |
|-------|--------------|-------------------|
| cto | ✅ `mcp__memory__*` | pattern, mistake, architecture, security, tech-insight |
| testing-agent | ✅ `mcp__memory__*` | test-pattern, common-bug, test-selector, test-insight |
| fulltest-skill | ✅ `mcp__memory__*` | failure-pattern, fix-solution |
| website-design | ✅ `mcp__memory__*` | design-decision, component-pattern, client-preference, design-insight |
| cpo-ai-skill | ✅ `mcp__memory__*` | research-cache, product-decision, epic-pattern, tech-stack-decision |
| memory-consolidation | ✅ `mcp__memory__*` | All types (maintenance) |

---

## Maintenance Schedule

- **Weekly**: Run `/consolidate` to merge duplicates, prune stale
- **Post-Project**: Save key learnings, archive project-specific details
- **Monthly**: Review core memory for promotions
- **Quarterly**: Deep review of memory health and patterns

---

## Best Practices

1. **Be Specific** - "pattern:react-useEffect-cleanup" not "pattern:react-tip"
2. **Track Usage** - Add "Applied in:" observations when using memories
3. **Include Context** - Why this matters, when it applies
4. **Link Related** - Use `create_relations` for connected concepts
5. **Prune Regularly** - Run consolidation to keep memory healthy
