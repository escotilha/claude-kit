---
description: Smart diff-based deployment to DigitalOcean
argument-hint: [--dry-run|--force|--services api,admin|status|logs|info|diagnose|rollback]
allowed-tools: Bash, Read, Task
---

# DigitalOcean Smart Update

Smart, diff-based deployment to DigitalOcean App Platform. Detects what changed and only rebuilds affected services.

## Usage

```
/do-update [options]
/do-update [command]
```

### Commands

- `status` - Check current deployment status
- `logs [service]` - View application logs (api, admin, client-portal)
- `info` - Show app info and URLs
- `diagnose` - **[Uses devops-agent]** Diagnose deployment issues and failures
- `rollback` - **[Uses devops-agent]** Roll back to a previous deployment
- `optimize` - **[Uses devops-agent]** Analyze and suggest deployment optimizations

### Options

- `--dry-run` - Preview what would deploy without making changes
- `--force` - Rebuild all services regardless of changes
- `--services api,admin` - Explicitly specify services to deploy
- `--skip-push` - Build locally only, don't push or deploy
- `--no-wait` - Don't wait for deployment to complete

## Examples

```
/do-update                    # Smart update (detect and deploy changes)
/do-update --dry-run          # Preview what would deploy
/do-update --force            # Force rebuild all services
/do-update --services api     # Deploy only the API
/do-update status             # Check deployment status
/do-update logs api           # View API logs
/do-update info               # Show app URLs
/do-update diagnose           # Diagnose deployment failures (uses devops-agent)
/do-update rollback           # Roll back to previous deployment (uses devops-agent)
/do-update optimize           # Get deployment optimization suggestions (uses devops-agent)
```

## How It Works

1. **Pull from GitHub** - Always fetches and pulls latest changes from origin
2. **Detect Changes** - Compares current commit to last deployment tag
3. **Map Services** - Determines which services need rebuild:
   - `apps/api/` changes → rebuild api
   - `apps/admin/` changes → rebuild admin
   - `apps/client-portal/` changes → rebuild client-portal
   - `packages/` changes → rebuild all services
4. **Trigger Deploy** - DigitalOcean App Platform builds from GitHub directly (no local Docker builds)
5. **Run Migrations** - Alembic migrations via PRE_DEPLOY job
6. **Wait for Completion** - Monitors deployment until active or failed
7. **Tag & Cleanup** - Creates deployment tag, removes old tags (keeps 10)
8. **Notify** - Sends Slack notification with status

**Important**: No local Docker builds are required. DigitalOcean builds directly from GitHub.

## DevOps Agent Integration

This skill uses the **devops-agent** for complex infrastructure tasks. The devops-agent is automatically spawned for:

### When devops-agent is used:

| Command | Description | When Agent is Spawned |
|---------|-------------|----------------------|
| `diagnose` | Analyze deployment failures | Always |
| `rollback` | Roll back to previous deployment | Always |
| `optimize` | Suggest deployment optimizations | Always |
| Regular deploy | Normal deployment | Only if deployment fails |

### Automatic Failure Handling

When a deployment fails, the assistant will:
1. Automatically spawn the devops-agent to diagnose the issue
2. The devops-agent will analyze:
   - Recent deployment logs
   - Build logs for failed services
   - App spec configuration
   - Recent git changes that may have caused the issue
3. Provide a diagnosis with recommended fixes
4. Offer to attempt automated remediation if safe

### Example: diagnose command

When you run `/do-update diagnose`, the devops-agent will:
1. Fetch recent deployment history
2. Check for ERROR or CANCELED deployments
3. Analyze build and runtime logs
4. Review the app.yaml configuration
5. Check for common issues (resource limits, env vars, dependencies)
6. Provide a detailed report with recommendations

### Example: rollback command

When you run `/do-update rollback`, the devops-agent will:
1. List recent successful deployments with their tags
2. Show what changed between current and target deployment
3. Confirm the rollback target with the user
4. Execute the rollback safely
5. Verify the rollback was successful
6. Send Slack notification about the rollback

## Process

When invoked, the assistant will:

1. **Check prerequisites** - Verify doctl and docker are available
2. **Pre-flight check** - Check for uncommitted changes and unpushed commits:
   - Run `git status --porcelain` to detect uncommitted changes
   - Run `git log @{u}.. --oneline` to detect unpushed commits
   - If either exists, show the user what's pending and ask if they want to commit and push now
   - If user agrees, commit all changes with a descriptive message and push to origin
   - If user declines, abort the deployment (since DO builds from GitHub, local changes won't deploy)
3. **Pull from GitHub** - Fetch and pull latest changes from origin (always)
4. **Detect changes** - Compare git HEAD to last deploy/do/* tag
5. **Confirm services** - Show which services will be deployed
6. **Execute deployment** via the do-update.sh script
7. **Report results** - Show deployment status, URLs, and any errors
8. **On failure** - Automatically spawn devops-agent to diagnose and suggest fixes

### Handling Special Commands

For `diagnose`, `rollback`, or `optimize` commands:

```
Use the Task tool with subagent_type="devops-agent" to handle these commands.
```

**diagnose** prompt:
```
Diagnose deployment issues for the Contably DigitalOcean App Platform deployment.

1. Check recent deployment status: doctl apps list-deployments <app-id>
2. Get deployment logs for any failed deployments
3. Review the app.yaml configuration at .do/app.yaml
4. Check for common issues:
   - Build failures (missing dependencies, Dockerfile issues)
   - Runtime errors (env vars, database connections)
   - Resource limits (memory, CPU)
   - Network/ingress issues
5. Provide a detailed diagnosis with specific recommendations
```

**rollback** prompt:
```
Roll back the Contably deployment to a previous version.

1. List deployment tags: git tag -l "deploy/do/*" --sort=-creatordate | head -10
2. Show the user the available rollback targets with their commit messages
3. Ask which deployment to roll back to
4. Execute: git checkout <tag> -- . && commit && push
5. Trigger new deployment
6. Verify rollback success
7. Send Slack notification
```

**optimize** prompt:
```
Analyze the Contably DigitalOcean deployment for optimization opportunities.

Review:
1. .do/app.yaml - resource sizing, scaling, caching
2. Dockerfile configurations - multi-stage builds, layer caching
3. Build times and patterns
4. Cost analysis based on current resource allocation
5. Security best practices

Provide recommendations with estimated impact.
```

### Pre-flight Check Details

Before deploying, ALWAYS run these checks:

```bash
# Check for uncommitted changes (staged or unstaged)
git status --porcelain

# Check for commits not pushed to origin
git log @{u}.. --oneline 2>/dev/null || git log origin/$(git branch --show-current)..HEAD --oneline
```

If changes are found:
- Show the list of uncommitted files and/or unpushed commits
- Use AskUserQuestion to ask: "You have local changes not pushed to GitHub. DigitalOcean builds from GitHub, so these won't be deployed. Would you like me to commit and push now?"
- Options: "Yes, commit and push" / "No, abort deployment"
- If yes: stage all changes, create commit with message describing the changes, push to origin
- If no: stop the deployment process

## Script Location

```
infrastructure/scripts/do-update.sh
infrastructure/scripts/setup-do.sh   # First-time setup for new machines
```

## First-Time Setup (New Machines)

Run the setup script to install prerequisites:
```bash
./infrastructure/scripts/setup-do.sh
```

This will:
- Install doctl (DigitalOcean CLI)
- Check Docker installation
- Authenticate with DigitalOcean
- Login to the container registry
- Verify the app exists

## Deployment Tags

Deployments are tracked with git tags in the format:
```
deploy/do/YYYYMMDD-HHMMSS
```

Only the last 10 deployment tags are kept; older ones are automatically cleaned up.

## Output

- App URL: https://contably-5q4oj.ondigitalocean.app
- API: https://contably-5q4oj.ondigitalocean.app/api
- Health: https://contably-5q4oj.ondigitalocean.app/health
- API Docs: https://contably-5q4oj.ondigitalocean.app/docs

## Estimated Costs

- API (basic-xs): $12/month
- Admin (basic-xxs): $5/month
- Client Portal (basic-xxs): $5/month
- PostgreSQL (db-s-1vcpu-1gb): $15/month
- Registry (Basic): $5/month
- **Total**: ~$42/month
