# resume-coach-skill

A Claude Code / Codex skill for AI-assisted resume coaching, resume review,
job-description tailoring, bilingual resume writing, and RenderCV-compatible
YAML maintenance.

## What It Does

This skill helps maintain a resume as structured source material instead of
loose text. It focuses on practical resume work:

- Review an existing resume and identify the highest-impact fixes.
- Tailor resume content to a specific job description.
- Rewrite rough notes into stronger resume bullets.
- Check whether claims are supported by the user's stated background.
- Produce bilingual English / Traditional Chinese resume copy.
- Work with RenderCV-style YAML as the canonical resume format.

## Structure

```text
.
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- assets/
|   |-- template_en.md
|   `-- template_zh.md
|-- references/
|   |-- ats-optimization.md
|   |-- bilingual-style.md
|   |-- quantified-achievements.md
|   |-- rendercv-yaml.md
|   `-- user-context.md
`-- scripts/
    |-- render_pdf.py
    `-- yaml_helpers.py
```

## Setup

1. Fill in `references/user-context.md` with the user's real background.
2. Install or copy this folder into the skill directory used by your agent tool.
3. Use the skill when reviewing, rewriting, or tailoring resume material.

Do not invent companies, metrics, achievements, or project details. Unknown
numbers should stay marked as `TBD` until the user confirms them.

## Common Commands

```bash
python scripts/yaml_helpers.py validate path/to/resume.yaml
python scripts/yaml_helpers.py check path/to/resume.yaml
python scripts/yaml_helpers.py diff base.yaml tailored.yaml
python scripts/render_pdf.py path/to/resume.md
```

## License

MIT
