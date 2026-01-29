# prd.json Schema Reference

Complete schema for the prd.json file.

## Full Schema

```json
{
  "project": "string - Project name",
  "branchName": "string - Git branch name",
  "description": "string - Feature description",
  "createdAt": "string - ISO 8601 timestamp",

  "verification": {
    "typecheck": "string - Command (e.g., npm run typecheck)",
    "test": "string - Command (e.g., npm run test)",
    "lint": "string - Command (optional)",
    "build": "string - Command (optional)"
  },

  "parallelConfig": {
    "enabled": "boolean - Enable parallel execution (default: false)",
    "maxConcurrent": "number - Max concurrent agents (default: 3)"
  },

  "userStories": [
    {
      "id": "string - e.g., US-001",
      "title": "string - Short title",
      "description": "string - As a [user], I want...",
      "acceptanceCriteria": ["string - Verifiable criteria"],
      "priority": "number - Lower = higher priority",
      "complexity": "number - 1-10 score",
      "complexityFactors": ["string - What makes it complex"],
      "dependsOn": ["string - IDs of prerequisite stories"],
      "status": "string - pending|blocked|in_progress|completed|skipped|expanded",
      "passes": "boolean - Has verification passed",
      "attempts": "number - Implementation attempts",
      "notes": "string - Implementation notes",
      "completedAt": "string - ISO 8601 timestamp",
      "expandedInto": ["string - Child story IDs if expanded"],
      "expandedFrom": "string - Parent story ID if from expansion"
    }
  ]
}
```

## Minimal Example

```json
{
  "project": "My App",
  "branchName": "feature/user-auth",
  "createdAt": "2024-01-15T10:00:00Z",
  "verification": {
    "typecheck": "npm run typecheck",
    "test": "npm run test"
  },
  "userStories": [
    {
      "id": "US-001",
      "title": "Add login form",
      "description": "As a user, I want to log in",
      "acceptanceCriteria": ["Form renders", "Typecheck passes"],
      "priority": 1,
      "complexity": 3,
      "dependsOn": [],
      "status": "pending",
      "passes": false,
      "attempts": 0
    }
  ]
}
```

## Status Values

| Status | Meaning |
|--------|---------|
| `pending` | Ready to start |
| `blocked` | Waiting on dependencies |
| `in_progress` | Currently being implemented |
| `completed` | Passed verification |
| `skipped` | Manually skipped |
| `expanded` | Split into sub-stories |
