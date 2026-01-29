# Claude Code Resources

Shared Claude Code skills and configurations for the Nuvini team.

## Skills

| Skill                                          | Description                                                              |
| ---------------------------------------------- | ------------------------------------------------------------------------ |
| [autonomous-agent](./skills/autonomous-agent/) | Breaks features into small user stories and implements them autonomously |

## Quick Install

```bash
# Clone the repo
git clone git@github.com:Nuvinigroup/claude.git
cd claude

# Install a skill
cd skills/autonomous-agent
./install.sh
```

## Adding New Skills

1. Create a new directory under `/skills/your-skill-name/`
2. Add a `SKILL.md` with frontmatter and instructions
3. Add `install.sh` and `uninstall.sh` scripts
4. Add a `README.md` with usage docs
5. Open a PR
