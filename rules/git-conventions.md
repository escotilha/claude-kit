# Git Conventions

Standards for version control across all projects.

## Commit Messages

Format: `type(scope): description`

Types:

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code restructuring without behavior change
- `test`: Adding or updating tests
- `chore`: Build process, dependencies, tooling

Examples:

- `feat(auth): add OAuth2 login flow`
- `fix(api): handle null response from external service`
- `docs(readme): update installation instructions`

## Commit Best Practices

- Write commits in imperative mood ("add feature" not "added feature")
- Keep subject line under 50 characters
- Separate subject from body with blank line
- Reference issue numbers when applicable
- Make atomic commits (one logical change per commit)

## Branch Naming

- `feature/description` - New features
- `fix/description` - Bug fixes
- `hotfix/description` - Urgent production fixes
- `refactor/description` - Code improvements
- `docs/description` - Documentation updates

## Pull Requests

- Keep PRs focused and reviewable (under 400 lines when possible)
- Write clear PR descriptions explaining the change
- Include testing instructions
- Request reviews from relevant team members
- Address review feedback before merging

## Protected Branches

- Never force push to main/master
- Require PR reviews before merging to main
- Ensure CI passes before merging
- Squash commits when merging feature branches

## Git Hygiene

- Rebase feature branches on main before PR
- Delete branches after merging
- Use `.gitignore` to exclude build artifacts, secrets, IDE files
- Never commit secrets, credentials, or API keys
