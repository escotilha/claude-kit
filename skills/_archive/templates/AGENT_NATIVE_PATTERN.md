# Agent-Native Design Pattern for Skills

Guidelines for creating skills that follow the "atomic tools, not workflows" principle.

## Core Principle

**"Tools should be atomic primitives. Features are outcomes achieved by an agent operating in a loop."**

## The Problem: Workflow-Shaped Skills

### Anti-Pattern Example

```python
# DON'T: Hardcoded workflow tool
@mcp_tool
def analyze_and_organize_files(files: list[str]) -> dict:
    """Analyze files and organize them by type."""
    analysis = {}
    for file in files:
        # Hardcoded decision logic
        file_type = detect_type(file)
        category = categorize(file_type)
        action = decide_action(category)
        analysis[file] = action
    return analysis
```

**Problems with this approach:**

1. **Decision logic is frozen** - To change categorization, you must edit tool code
2. **No agent involvement** - Agent just calls the tool and gets results
3. **Inflexible** - Can't adapt to new file types or categories without code changes
4. **Not inspectable** - User can't see intermediate decisions
5. **Workflow-shaped** - The tool embeds a multi-step workflow

### Correct Pattern

```markdown
## Skills Instructions (prompts, not code)

When organizing files:
1. Use Read to analyze file contents
2. Use Glob to discover related files
3. Consider project context and conventions
4. Use Write/Edit to reorganize as appropriate
5. Explain decisions to the user as you work

### Categorization Guidelines

**Source code** → `/src/` directory
**Tests** → `/tests/` or `__tests__/` directories
**Documentation** → `/docs/` directory
**Configuration** → Root directory
**Build artifacts** → `.gitignore` and remove
```

**Benefits:**

1. **Agent makes decisions** - Applies guidelines contextually
2. **Easily modified** - Edit prompts to change behavior
3. **Transparent** - User sees agent's reasoning
4. **Adaptive** - Agent can handle unexpected situations
5. **Atomic tools** - Read, Write, Glob, Edit are primitives

## Identifying Workflow Logic in Skills

### Red Flags (Workflow-Shaped)

Look for these patterns in your skill definitions:

- **Sequential steps with hardcoded order** - "Step 1: Do X, Step 2: Do Y, Step 3: Do Z"
- **Conditional branching in instructions** - "If X then do A, else do B"
- **Tools that do multiple things** - `analyze_plan_execute()`
- **Fixed templates** - "Always generate this exact structure"
- **Explicit loops** - "For each item in list, do X"

### Green Flags (Agent-Native)

Look for these patterns instead:

- **Outcome descriptions** - "Achieve X by doing whatever is needed"
- **Guideline-based instructions** - "Consider these factors when deciding"
- **Atomic tool usage** - "Use Read/Write/Bash to accomplish the goal"
- **Adaptive behavior** - "Adjust approach based on context"
- **Memory integration** - "Learn from past decisions"

## Refactoring Workflow Logic to Outcomes

### Example 1: File Organization

**Before (Workflow-Shaped):**
```markdown
1. Scan all files in directory
2. For each file:
   - If .js or .ts → move to /src
   - If .test.js → move to /tests
   - If .md → move to /docs
3. Create .gitignore with build artifacts
4. Generate directory structure report
```

**After (Outcome-Oriented):**
```markdown
Organize the project files following modern conventions:
- Source code should be in appropriate directories
- Tests near the code they test or in dedicated test directory
- Documentation in a docs folder
- Configuration files at root
- Build artifacts should be ignored

Use Read to understand file contents, Glob to find patterns,
Write/Edit to reorganize. Explain your organizational decisions.

Consider project type (e.g., Node.js, Python, monorepo) when deciding structure.
```

### Example 2: Code Generation

**Before (Workflow-Shaped):**
```markdown
1. Parse API specification
2. Generate TypeScript interfaces from schema
3. Generate React hooks for each endpoint
4. Generate test files with mock data
5. Update index.ts with exports
```

**After (Outcome-Oriented):**
```markdown
Generate type-safe API client code from the specification:
- Types should match the API schema exactly
- Provide convenient hooks/functions for common operations
- Include tests with realistic mock data
- Follow the project's existing patterns

Use Read to analyze existing code patterns, Write to create new files,
Edit to integrate with existing code. Test that generated code compiles.

Reference memory for project-specific preferences on API client patterns.
```

### Example 3: Testing Workflow

**Before (Workflow-Shaped):**
```markdown
Testing sequence:
1. Start dev server on port 3000
2. Wait 5 seconds for server ready
3. Test homepage: check title, hero section, footer
4. Test login: fill email/password, submit, verify redirect
5. Test dashboard: check stats cards, charts render
6. Generate pass/fail report
```

**After (Outcome-Oriented):**
```markdown
Comprehensively test the application:
- Verify critical user journeys work end-to-end
- Test both happy paths and error scenarios
- Check UI elements render correctly
- Validate API responses and error handling
- Report findings with reproduction steps for issues

Use Bash to start services, browser tools to interact with UI,
Read to check logs for errors. Adapt testing based on what you discover.

If tests fail, investigate root cause before proceeding.
```

## Documenting "Atomic Tools vs Outcomes"

Every skill should include this section in its SKILL.md:

```markdown
## Atomic Tools vs Outcomes

### Agent-Native Design Principle

This skill follows the **Agent-native principle**: "Tools should be atomic primitives. Features are outcomes achieved by an agent operating in a loop."

### Atomic Tools Used

List the primitive tools this skill uses:
- Read/Write/Edit - File operations
- Bash - Command execution
- Glob/Grep - Code search
- WebFetch/WebSearch - Internet access
- mcp__memory__* - Long-term learning
- [any other atomic tools]

### Outcomes Achieved via Prompts

Describe what outcomes the skill achieves and how they're accomplished through agent decision-making (not hardcoded workflows).

### How to Modify Behavior via Prompts

Provide concrete examples of how users/developers can change skill behavior by editing prompts rather than code.

### Contrast: Workflow-Shaped Anti-Pattern

Show what the skill does NOT do (hardcoded workflows) vs what it DOES do (outcome-oriented prompts + atomic tools).
```

## Examples from Real Skills

### cpo-ai-skill

**Atomic tools**: Read, Write, Bash, TaskList, TeammateTool, mcp__memory__*

**Outcomes** (not workflows):
- "Transform product idea into qualified definition" (via questions and synthesis)
- "Create staged implementation plan" (via subagent consultation and planning prompts)
- "Implement each stage with testing" (via delegation to autonomous-dev and fulltest-skill)

**Modification via prompts**:
- Change discovery questions → edit prompts in references/phase-details.md
- Change planning strategy → modify Phase 2 prompts
- Adjust swarm behavior → edit TeammateTool message templates

### mna-toolkit

**Atomic tools**: Read, Write, Bash, WebFetch, WebSearch, TaskList

**Outcomes** (not workflows):
- "Score deal against investment criteria" (triage scoring via prompts)
- "Extract financial data from documents" (flexible extraction via prompts)
- "Generate financial model" (calculation via Bash + prompts for structure)

**Modification via prompts**:
- Change scoring criteria → edit scoring framework table
- Adjust deal structure → modify default assumptions
- Add industry-specific logic → add conditional prompts

### website-design

**Atomic tools**: Read, Write, Edit, WebFetch, WebSearch, mcp__memory__*

**Outcomes** (not workflows):
- "Create conversion-optimized landing page" (design via best practice prompts)
- "Design production-ready dashboard" (layout via UX principle prompts)
- "Build accessible component library" (coding via accessibility prompts)

**Modification via prompts**:
- Add design aesthetics → extend color palette section
- Change component patterns → modify example components
- Industry-specific guidelines → add vertical-specific prompts

## Decision Tree: Tool vs Prompt

When designing a skill, ask:

```
Does this need to be a tool (code)?
├─ YES if:
│  ├─ Requires non-LLM computation (complex math, image processing)
│  ├─ Needs guaranteed precise behavior (cryptography, financial calculations)
│  ├─ External system integration (API calls, database queries)
│  └─ Performance-critical operation (can't afford agent loop iterations)
│
└─ NO if:
   ├─ Involves decision-making based on context
   ├─ Requires adaptation to varying inputs
   ├─ Benefits from transparency (user should see reasoning)
   ├─ Needs to evolve with new patterns/trends
   └─ Can be accomplished with atomic tools + prompts
```

## Testing Agent-Native Designs

Validate that your skill is agent-native:

### Test 1: Prompt Modification Test
**Can you change behavior by only editing prompts?**
- ✅ Good: Edit guidelines and agent adapts
- ❌ Bad: Must modify tool code to change behavior

### Test 2: Transparency Test
**Can the user see the agent's decision-making?**
- ✅ Good: Agent explains reasoning as it works
- ❌ Bad: Tool returns opaque results

### Test 3: Adaptability Test
**Does the skill handle unexpected situations?**
- ✅ Good: Agent adapts using atomic tools
- ❌ Bad: Fails if inputs don't match expected format

### Test 4: Learning Test
**Can the skill improve from experience?**
- ✅ Good: Uses Memory MCP to learn patterns
- ❌ Bad: Behavior is fixed in code

### Test 5: Atomic Tool Test
**Does the skill use only atomic primitives?**
- ✅ Good: Read, Write, Bash, Glob, Grep, etc.
- ❌ Bad: Custom tools that embed workflows

## Migration Path for Existing Skills

If you have a workflow-shaped skill:

1. **Identify the workflows** - Find hardcoded step-by-step logic
2. **Extract decision criteria** - What rules govern the workflow?
3. **Convert to prompts** - Rewrite as outcome descriptions with guidelines
4. **Replace custom tools with atomic tools** - Use Read/Write/Bash instead
5. **Add Memory integration** - Let the skill learn from experience
6. **Document in "Atomic Tools vs Outcomes"** - Explain the pattern
7. **Test with prompt modifications** - Verify behavior changes via prompts

## Key Takeaways

1. **Skills are prompts, not code** - Behavior should be in instructions, not tools
2. **Agents make decisions, not tools** - Tools are primitives, agents compose them
3. **Outcomes, not workflows** - Describe what to achieve, not how to achieve it
4. **Adapt via prompts, not code** - Editing prompts should change behavior
5. **Learn from experience** - Use Memory MCP to evolve without code changes
6. **Transparent reasoning** - Users should see agent decision-making
7. **Atomic tools only** - Use Read, Write, Bash, Glob, Grep, Web*, Memory

## Further Reading

- [cpo-ai-skill SKILL.md](../cpo-ai-skill/SKILL.md) - Comprehensive orchestration example
- [mna-toolkit SKILL.md](../mna-toolkit/SKILL.md) - Multi-command interface example
- [website-design SKILL.md](../website-design/SKILL.md) - Creative task example
- [memory-strategy.md](../../rules/memory-strategy.md) - Memory-driven behavior evolution
