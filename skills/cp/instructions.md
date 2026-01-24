# Instructions for /cp Skill

When the user invokes `/cp`, follow these steps:

## 1. Check Git Status

```bash
git status --porcelain
```

If no changes, inform user and exit:
```
No changes to commit.
```

## 2. Stage Changes

If there are unstaged changes:
```bash
git add -A
```

Show what was staged:
```bash
git status --short
```

## 3. Generate Commit Message

If user provided a message (e.g., `/cp fix typo`), use that message.

Otherwise, analyze the diff to generate a concise message:
```bash
git diff --cached --stat
```

Generate a commit message following conventional commits:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `refactor:` for code changes that don't add features or fix bugs
- `chore:` for maintenance tasks

Keep the message under 50 characters for the subject line.

## 4. Commit

```bash
git commit -m "$(cat <<'EOF'
<generated or provided message>

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

## 5. Push

```bash
git push
```

If no upstream is set:
```bash
git push -u origin $(git branch --show-current)
```

## 6. Output Summary

```
✓ Committed: <message>
✓ Pushed to origin/<branch>
```

## Error Handling

- **No changes**: Inform user, exit cleanly
- **Push rejected**: Suggest `git pull --rebase` first
- **No remote**: Inform user to add a remote
