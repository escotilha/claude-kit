---
description: Build project user manual (MkDocs) with optional Word export
argument-hint: [format: html|word]
allowed-tools: Bash, Read, Glob
---

Build the user manual for the current project.

## Arguments

- `$1` (optional): Output format
  - `html` or empty: Build MkDocs site
  - `word`: Build and convert to Word document

## Instructions

### Step 1: Detect Manual Configuration

Look for manual configuration in the current directory:

1. Check for `mkdocs-manual.yml` (preferred)
2. Check for `mkdocs.yml` with `docs_dir: manual`
3. Check for a `manual/` directory with markdown files
4. Check for a `Makefile` with a `manual` target

```bash
# Check what's available
ls -la mkdocs*.yml 2>/dev/null
ls -la Makefile 2>/dev/null
ls -la manual/ 2>/dev/null | head -10
```

### Step 2: Build HTML Documentation

If a Makefile with `manual` target exists:

```bash
make manual
```

Otherwise, build directly with mkdocs:

```bash
python3 -m mkdocs build -f mkdocs-manual.yml --strict
```

Or if only `mkdocs.yml` exists:

```bash
python3 -m mkdocs build --strict
```

### Step 3: Word Export (if requested)

If the user requested `word` format:

a. Ensure pandoc is installed:

```bash
which pandoc || brew install pandoc
```

b. Read the MkDocs config to extract navigation and metadata:

```bash
# Read the mkdocs config file
cat mkdocs-manual.yml 2>/dev/null || cat mkdocs.yml
```

c. Extract key info from the config:

- `docs_dir`: Source directory for markdown files (default: `docs` or `manual`)
- `site_name`: Used as document title
- `site_author`: Used as document author
- `nav`: Navigation structure defines file order

d. Build the list of markdown files in navigation order from the `nav:` section.

- Parse each entry under `nav:`
- For entries like `- Section: file.md`, extract `file.md`
- For nested entries, extract all `.md` files recursively
- Prefix each file with the `docs_dir` path

e. Combine and convert:

```bash
# Example (adapt based on actual nav structure):
cd <docs_dir> && cat \
  file1.md \
  section/file2.md \
  ... \
  > /tmp/manual_combined.md && \
pandoc /tmp/manual_combined.md \
  -o "/Users/ps/Library/Mobile Documents/com~apple~CloudDocs/Downloads/manual/Manual_<ProjectName>.docx" \
  --toc \
  --toc-depth=3 \
  -f markdown \
  -t docx \
  --metadata title="<site_name>" \
  --metadata author="<site_author>"
```

### Step 4: Report Results

For HTML:

- Report the output directory (from `site_dir` in config, default: `./site/` or `./site-manual/`)
- Mention preview command: `make serve-manual` or `mkdocs serve -f <config>`

For Word:

- Report the Word document path: `/Users/ps/Library/Mobile Documents/com~apple~CloudDocs/Downloads/manual/Manual_<ProjectName>.docx`
- Ensure the output directory exists before writing

## Configuration Detection

The command auto-detects project configuration:

| Config File         | docs_dir | site_dir    | Notes                      |
| ------------------- | -------- | ----------- | -------------------------- |
| `mkdocs-manual.yml` | manual   | site-manual | Preferred for user manuals |
| `mkdocs.yml`        | docs     | site        | Standard MkDocs            |
| `manual/` dir only  | manual   | site-manual | Fallback                   |

## Examples

**Project with Makefile:**

```
/manual → make manual
/manual word → make manual + pandoc export
```

**Project without Makefile:**

```
/manual → mkdocs build -f mkdocs-manual.yml
/manual word → mkdocs build + pandoc export
```
