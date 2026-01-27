---
name: fulltest-skill
description: "Swarm-enabled full-spectrum testing for websites and applications. Uses TeammateTool for true parallel page testers that share failure patterns in real-time. Maps sites, spawns concurrent testers, detects cross-page patterns, auto-fixes with parallel fixers, generates comprehensive reports."
version: 4.0.0
tools:
  - Task
  - TeammateTool
model: sonnet
color: green
triggers:
  - "test the website"
  - "run e2e tests"
  - "comprehensive testing"
  - "test and fix"
  - "fulltest"
  - "swarm test"
dependencies:
  mcp:
    - chrome-devtools
    - memory
---

# Full-Spectrum Testing Skill (v4.0 - Swarm Mode)

Comprehensive website testing with **true parallel execution** via TeammateTool, real-time failure sharing, and cross-page pattern detection.

## What It Does

When you run `/fulltest`, it will:
1. Map your entire site structure
2. **Spawn concurrent page testers** via TeammateTool (not sequential Task calls)
3. **Share failures in real-time** - when one tester finds CSS issue, others check immediately
4. **Detect cross-page patterns** - same error on multiple pages = systemic issue
5. **Learn from failures** and store patterns in MCP memory
6. **Spawn parallel fixers** by category (CSS, JS, assets, etc.)
7. Re-test until all tests pass (max 3 iterations)
8. Generate comprehensive report with live progress

## Execution Modes

| Mode | Description | When to Use |
|------|-------------|-------------|
| **Sequential** | Task-based parallel (standard) | Small sites, debugging |
| **Swarm** | TeammateTool true concurrency | Large sites, speed priority |

## Swarm Mode Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    FULLTEST SWARM ORCHESTRATOR                       │
│                                                                      │
│   Phase 1: Site Mapping                                             │
│          │                                                          │
│          ▼                                                          │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │              PHASE 2: SWARM PAGE TESTING                     │   │
│   │                                                              │   │
│   │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐            │   │
│   │  │Tester 1│  │Tester 2│  │Tester 3│  │Tester N│            │   │
│   │  │ /home  │◀─▶│ /about │◀─▶│ /blog  │◀─▶│ /...   │            │   │
│   │  └───┬────┘  └───┬────┘  └───┬────┘  └───┬────┘            │   │
│   │      │           │           │           │                  │   │
│   │      └───────────┴───────────┴───────────┘                  │   │
│   │                      │                                       │   │
│   │         ┌────────────┴────────────┐                         │   │
│   │         │   REAL-TIME MESSAGING    │                         │   │
│   │         │ • Failure broadcasts     │                         │   │
│   │         │ • CSS issue alerts       │                         │   │
│   │         │ • Pattern sharing        │                         │   │
│   │         └─────────────────────────┘                         │   │
│   └─────────────────────────────────────────────────────────────┘   │
│          │                                                          │
│          ▼                                                          │
│   ┌─────────────────────────────────────────────────────────────┐   │
│   │              PHASE 3: SWARM PARALLEL FIXING                  │   │
│   │                                                              │   │
│   │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │   │
│   │  │CSS Fixer │  │ JS Fixer │  │Asset Fix │  │Layout Fix│    │   │
│   │  └──────────┘  └──────────┘  └──────────┘  └──────────┘    │   │
│   └─────────────────────────────────────────────────────────────┘   │
│          │                                                          │
│          ▼                                                          │
│   Phase 4: Report Generation                                        │
└─────────────────────────────────────────────────────────────────────┘
```

## New in v3.0: Visual Verification + Learning

### Visual Verification (Always On)
Every page test now includes:
- **CSS Load Check**: Verify all CSS files return 200 and styles apply
- **Computed Style Check**: Sample key elements for expected styles (dark background, proper fonts)
- **Asset Check**: Verify images and fonts load correctly
- **Screenshot Capture**: On failure only, for debugging

### Pattern Learning
After each test:
- Extract patterns from failures (visual and functional)
- Store patterns in MCP memory for future reference
- Get fix recommendations based on past successful fixes
- Share patterns across similar projects

## Usage

The skill forwards your request to the specialized `fulltesting-agent` which handles all testing logic.

**Your task**: Invoke the fulltesting-agent with the user's request.

## Example

```
User: "Test http://localhost:3000 and fix any issues"

You: [Use Task tool with subagent_type="fulltesting-agent" and pass the URL and user's requirements]
```

## Enhanced Testing Flow

The fulltesting-agent should now follow this enhanced flow:

### Phase 1: Discovery
- Navigate to the site
- Extract all internal links
- Build page map

### Phase 2: Parallel Testing (Per Page)
For each page, run these checks:

#### 2a. Basic Checks (existing)
- Console errors
- Network failures (4xx/5xx)
- Broken links

#### 2b. Visual Verification (NEW)
Execute this JavaScript via `mcp__chrome-devtools__evaluate_script`:

```javascript
() => {
  const body = document.body;
  const computedStyle = window.getComputedStyle(body);
  const bgColor = computedStyle.backgroundColor;
  const fontFamily = computedStyle.fontFamily;

  // Check for unstyled page (CSS not loaded)
  const defaultBgs = ['rgba(0, 0, 0, 0)', 'rgb(255, 255, 255)', 'transparent'];
  const defaultFonts = ['times new roman', 'times', 'serif'];

  const bgIsDefault = defaultBgs.some(d => bgColor.toLowerCase().includes(d.toLowerCase()));
  const fontIsDefault = defaultFonts.some(d => fontFamily.toLowerCase().includes(d.toLowerCase()));

  // Count loaded CSS files
  const cssLinks = document.querySelectorAll('link[rel="stylesheet"]');
  const cssCount = cssLinks.length;

  // Check for visible styled content
  const hasStyledContent = !bgIsDefault || !fontIsDefault || cssCount > 0;

  return {
    cssLoaded: hasStyledContent,
    backgroundColor: bgColor,
    fontFamily: fontFamily,
    cssFileCount: cssCount,
    isUnstyled: bgIsDefault && fontIsDefault,
    issue: (bgIsDefault && fontIsDefault) ? 'CSS appears not loaded - page has default unstyled appearance' : null
  };
}
```

If `isUnstyled` is true, this is a **CRITICAL** visual issue that should fail the test.

### Phase 3: Pattern Learning (NEW)
After testing each page, if there are failures:

1. **For console errors**, check if they're visual issues:
   - CSS load failures: `/failed to load resource.*\.css/i`
   - Font issues: `/failed to decode font/i`
   - Image broken: `/failed to load resource.*\.(png|jpg|svg)/i`

2. **Store patterns** in MCP memory using `mcp__memory__create_entities`:
   ```
   Entity name: failure-pattern:visual:{fingerprint}
   Entity type: failure-pattern
   Observations:
   - "visual_type: css-not-loaded"
   - "affected_url: {url}"
   - "message_pattern: {normalized message}"
   - "category: css-load-error"
   - "severity: critical"
   - "occurrence_count: 1"
   - "first_seen: {ISO date}"
   ```

3. **Search for existing patterns** using `mcp__memory__search_nodes`:
   - Query: "css-load-error" or the normalized error message
   - If found, check for associated fixes

4. **Get fix recommendations**:
   - Search memory for `fix-solution` entities linked to the pattern
   - Include recommendations in the report

### Phase 4: Screenshot on Failure (NEW)
When visual issues are detected:
```
mcp__chrome-devtools__take_screenshot with filePath to save for debugging
```

### Phase 5: Analysis & Auto-Fix
- Aggregate all issues
- Prioritize by severity (visual issues = critical)
- Apply fixes for known patterns
- Re-test affected pages

### Phase 6: Report Generation
Include in the report:
- All pages tested
- Visual verification results
- Pattern matches found
- Fix recommendations with confidence scores
- Screenshots of failures

## Pattern Categories

The system recognizes these visual pattern categories:
- `css-load-error`: CSS file failed to load
- `style-missing`: Element missing expected styles
- `layout-error`: Layout/responsive issues
- `visual-regression`: Visual difference detected
- `asset-missing`: Image/font/icon not loaded

## Fix Categories

When storing fixes, use these categories:
- `css-fix`: CSS/style changes
- `layout-fix`: Layout/flexbox/grid fixes
- `asset-fix`: Image/font path corrections
- `responsive-fix`: Media query additions

## Integration with smart-testing

The testing-learning library at `src/lib/testing-learning/` provides:
- `processBrowserTestResult()`: Main hook for recording results
- `verifyCSSLoaded()`: Check CSS is properly loaded
- `hasVisualIssues()`: Quick check for visual problems
- `getVisualIssuesSummary()`: Summary for reporting

These functions can be called by reading the TypeScript source and understanding the interface, then using MCP memory tools to store/retrieve the same entity structures.

---

## Swarm Mode Summary

### When Swarm Mode Activates
- Site has >10 pages
- User requests "swarm test" or "fast test"
- Explicit `mode: swarm` in config

### Swarm Capabilities

| Feature | Description |
|---------|-------------|
| **Parallel Testers** | One tester per page via TeammateTool |
| **Failure Broadcast** | CSS issue found → all testers notified |
| **Pattern Detection** | Same error on 3+ pages = systemic issue |
| **Parallel Fixers** | CSS, JS, assets, config fixers run concurrently |
| **Live Dashboard** | Real-time progress during testing |

### Example Swarm Output

```
## Test Progress (Live)

[0:02] Spawned 15 page testers
[0:08] tester-0 (/): ✅ Pass
[0:10] tester-3 (/blog): 🚨 CSS 404 - broadcasting to all
[0:11] tester-* received known_issue: skip CSS check
[0:15] tester-5 (/products): ❌ JS error (new)
[0:18] Pattern detected: JS error on 3 pages (systemic)
[0:25] All testers complete: 12 pass, 3 fail

[0:26] Spawned 2 parallel fixers: css-fixer, js-fixer
[0:35] css-fixer: Fixed /styles/main.css path
[0:42] js-fixer: Fixed null reference in bundle.js
[0:45] All fixers complete

[0:46] Re-testing 3 failed pages...
[0:52] All tests pass!

Total: 52 seconds (vs ~3 minutes sequential)
```

---

## Version

**Current Version:** 4.0.0 (Swarm-enabled)
**Last Updated:** January 2026

### Changelog
- **4.0.0**: Added swarm mode
  - True parallel testers via TeammateTool
  - Real-time failure sharing between testers
  - Cross-page pattern detection
  - Parallel category-based fixers
  - Live progress dashboard
- **3.0.0**: Added visual verification + pattern learning
- **2.0.0**: Added parallel testing via Task batches
- **1.0.0**: Initial release

### Requirements
- **Both Modes**: Chrome DevTools MCP, Memory MCP
- **Sequential Mode**: Standard Claude Code
- **Swarm Mode**: Requires `claude-sneakpeek` or official TeammateTool support
