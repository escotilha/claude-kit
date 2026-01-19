---
name: fulltest-skill
description: Unified full-spectrum testing for websites and applications. Maps sites, spawns parallel testers, analyzes failures, auto-fixes issues, generates comprehensive reports.
version: 2.0.0
tools: Task
model: sonnet
color: green
triggers:
  - "test the website"
  - "run e2e tests"
  - "comprehensive testing"
  - "test and fix"
  - "fulltest"
dependencies:
  mcp:
    - chrome-devtools
---

# Full-Spectrum Testing Skill

This skill provides comprehensive website testing by invoking the `fulltesting-agent`.

## What It Does

When you run `/fulltest`, it will:
1. Map your entire site structure
2. Test all pages in parallel
3. Analyze failures and auto-fix issues
4. Re-test until all tests pass (max 3 iterations)
5. Generate a comprehensive report

## Usage

The skill forwards your request to the specialized `fulltesting-agent` which handles all testing logic.

**Your task**: Invoke the fulltesting-agent with the user's request.

## Example

```
User: "Test http://localhost:3000 and fix any issues"

You: [Use Task tool with subagent_type="fulltesting-agent" and pass the URL and user's requirements]
```

The agent will handle:
- Chrome DevTools MCP configuration
- Site mapping and discovery
- Parallel testing with page-tester subagents
- Failure analysis and auto-fixing
- Re-test loops (max 3 iterations)
- Comprehensive report generation
