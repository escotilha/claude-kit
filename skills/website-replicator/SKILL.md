---
name: website-replicator
description: Clone websites locally for study and analysis. Use when users ask to replicate, clone, mirror, download, or save a website for studying its structure, design, CSS, JavaScript, or overall architecture. Also use when asked to analyze a website's code structure or create an offline copy of a site.
---

# Website Replicator

Clone websites locally to study their structure, styling, and implementation. Supports both public websites and login-protected sites.

## Available Scripts

| Script | Use Case |
|--------|----------|
| `replicate_website.py` | Public websites (no login required) |
| `authenticated_website_replicator.py` | Sites requiring authentication (login, MFA, SSO) |

---

## Basic Replicator (Public Sites)

For websites that don't require login.

### Quick Start

```bash
python3 ~/.claude/skills/website-replicator/scripts/replicate_website.py https://example.com -o ./output
```

### Options

| Argument | Default | Description |
|----------|---------|-------------|
| `url` | required | Target website URL |
| `-o, --output` | `./replicated-site` | Output directory |
| `-d, --depth` | 2 | Max crawl depth (0 = single page) |
| `-p, --pages` | 50 | Max pages to download |

### Examples

```bash
# Single page only
python3 ~/.claude/skills/website-replicator/scripts/replicate_website.py https://example.com -d 0

# Deep crawl
python3 ~/.claude/skills/website-replicator/scripts/replicate_website.py https://example.com -d 5 -p 200
```

---

## Authenticated Replicator (Login-Protected Sites)

For websites requiring login, MFA, SSO, or other authentication.

### Quick Start

**Interactive mode (recommended for first use):**
```bash
python3 ~/.claude/skills/website-replicator/scripts/authenticated_website_replicator.py \
    https://app.example.com/login \
    https://app.example.com/dashboard \
    --interactive
```

**Automated login with credentials:**
```bash
python3 ~/.claude/skills/website-replicator/scripts/authenticated_website_replicator.py \
    https://app.example.com/login \
    https://app.example.com/dashboard \
    --username user@email.com \
    --password "mypassword"
```

### Options

| Option | Default | Description |
|--------|---------|-------------|
| `login_url` | required | URL of the login page |
| `target_url` | required | URL to start replicating from after login |
| `-o, --output` | `./replicated-site` | Output directory |
| `-d, --depth` | 2 | Max crawl depth |
| `-p, --pages` | 50 | Max pages to download |
| `-u, --username` | - | Username/email for login |
| `--password` | - | Password for login |
| `-i, --interactive` | false | Interactive mode - manually complete login |
| `--visible` | false | Show browser window during automated login |
| `--use-playwright` | false | Use Playwright for all pages (slower, handles JS) |
| `--wait` | 3 | Seconds to wait after login |

### Custom Selectors

For non-standard login forms:

| Option | Description |
|--------|-------------|
| `--username-selector` | CSS selector for username field |
| `--password-selector` | CSS selector for password field |
| `--submit-selector` | CSS selector for submit button |

### Examples

**Login with MFA (Interactive):**
```bash
python3 ~/.claude/skills/website-replicator/scripts/authenticated_website_replicator.py \
    https://secure-app.com/signin \
    https://secure-app.com/home \
    --interactive
```
A browser window opens. Complete login including MFA, then press Enter.

**Custom login form selectors:**
```bash
python3 ~/.claude/skills/website-replicator/scripts/authenticated_website_replicator.py \
    https://custom-app.com/auth \
    https://custom-app.com/main \
    -u admin --password admin123 \
    --username-selector "#login-field" \
    --password-selector "#pass-field" \
    --submit-selector ".submit-btn"
```

**JavaScript-heavy SPA:**
```bash
python3 ~/.claude/skills/website-replicator/scripts/authenticated_website_replicator.py \
    https://spa-app.com/login \
    https://spa-app.com/app \
    --interactive --use-playwright -d 3 -p 100
```

---

## What Gets Downloaded

- **HTML pages** - With rewritten links to local files
- **CSS** - Stylesheets and their referenced assets (fonts, images)
- **JavaScript** - External script files
- **Images** - Including srcset variants
- **Media** - Video/audio sources
- **Favicons** - All icon variants

## Output Structure

```
output-dir/
├── index.html           # Entry point
├── css/                 # Stylesheets
├── js/                  # Scripts
├── images/              # Image assets
├── _manifest.txt        # Download summary
└── _cookies.json        # Session cookies (authenticated only)
```

## Workflow

1. Run the appropriate script with target URL(s)
2. For authenticated sites, complete login (auto or manual)
3. Open `output-dir/index.html` in browser to view
4. Examine source files to study implementation
5. Check `_manifest.txt` for download summary

## Troubleshooting

- **Login fails?** Use `--interactive` and `--visible` to debug
- **Missing content?** Try `--use-playwright` for JS-rendered pages
- **Timeouts?** Increase `--wait` for slow-loading apps
- **Wrong selectors?** Inspect the login page and use custom `--*-selector` options

## Limitations

- Same-domain only (won't follow external links)
- Some dynamic/SPA content may require `--use-playwright`
- Does not handle CAPTCHA automatically (use interactive mode)
- File downloads/binary attachments may not work
