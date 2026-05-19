# RenderCV YAML Schema & Patterns

RenderCV is the canonical output format. All other outputs (Markdown, PDF preview, plain text, LinkedIn/CakeResume bios, cover letters) are *derived* from the YAML.

Canonical file: `path/to/your_cv.yaml` (set in references/user-context.md)

## Top-level structure

```yaml
cv:
  name: "[Your Name]"
  headline: "[Your headline]"
  location: "Taiwan"
  social_networks: []
  sections:
    summary: [...]
    experience: [...]
    key_projects: [...]
    skills: [...]
    education: [...]
    certifications: [...]

design:
  theme: classic
  colors:
    name: rgb(0, 79, 144)
    section_titles: rgb(0, 79, 144)
    links: rgb(0, 79, 144)
    connections: rgb(0, 79, 144)
  typography:
    font_size:
      body: 10pt
      name: 28pt
    alignment: justified
  header:
    alignment: left
  page:
    size: a4
    top_margin: 0.7in
    bottom_margin: 0.7in
    left_margin: 0.7in
    right_margin: 0.7in

locale:
  language: english   # or: chinese — produces 中文版

settings:
  render_command:
    output_folder: rendercv_output
    pdf_path: rendercv_output/Your_CV.pdf
  bold_keywords:
    - Python
    - RPA
    - T24
    - ISO 20022
    - SWIFT
    - Docker
    - AWS
    - Selenium
```

## Section conventions

### `cv.sections.summary`

A list of strings (typically one or two). Markdown bold is allowed and renders.

```yaml
summary:
  - "**5+ years** of Python development experience specializing in **RPA automation**
    and **financial systems integration**. Delivered **21 RPA projects** for E.SUN
    Bank overseas branches..."
```

### `cv.sections.experience`

Each entry is a role:

```yaml
- company: Acme Corp (示範公司)
  position: Senior Software Engineer
  start_date: 2024-01
  end_date: present          # or 2024-01, etc.
  location: Taiwan
  highlights:
    - "Verb-led bullet with **bold key terms** and clear outcome"
```

- Dates: `YYYY-MM` format. Use `present` for current role.
- `highlights` is the bullet list. Each entry is one bullet — keep to one or two sentences max.
- Use **bold** for headline metrics or key technologies inside a bullet.

### `cv.sections.key_projects`

```yaml
- name: Automated Document Processing System
  date: "Acme Corp — Singapore Office"   # repurposed as a sub-heading, not a date
  highlights:
    - "Integrated **5 third-party APIs** for automated data extraction and validation"
    - "Reduced manual review time by **80 hours/month**"
```

Note: the `date` field is used here as a sub-heading line (branch/context), not an actual date — preserve it across edits.

### `cv.sections.skills`

Each entry is a category group:

```yaml
- label: Programming Languages
  details: Python 3.x, Kotlin, SQL, HTML/CSS
```

Don't switch to comma-separated mega-lists or to single-skill entries. Keep grouped.

### `cv.sections.education`

```yaml
- institution: Soochow University (東吳大學 巨資學院)
  area: Big Data & AI — Part-time Master's Program
  degree: M.S.
  end_date: 2024-06
  location: Taipei, Taiwan
```

### `cv.sections.certifications`

```yaml
- name: Bank Internal Control and Internal Audit Examination (General Finance)
  date: "Issued: 2010-08-11"
  highlights:
    - "Issued by the **Financial Supervisory Commission (FSC)**, Taiwan"
```

## `bold_keywords` — what to put there

RenderCV auto-bolds every occurrence of these terms across the resume. Current list reflects the user's signature stack:

```
Python, RPA, T24, ISO 20022, SWIFT, Docker, AWS, Selenium
```

When customizing for a JD, you may **add** keywords that:
- Are central to the JD
- Actually appear in the user's bullets (no point auto-bolding a word that doesn't exist in the resume)
- Are unambiguous (avoid generic words like "data" or "system" — they'll bold half the resume)

Reasonable additions for specific JDs:
- LLM-heavy JD: `LLM`, `OCR`, `Hugging Face`
- NLP JD: `BERT`, `NLP`, `Transformers`
- Pure backend JD: `Oracle`, `MySQL`, `pandas`
- FinTech JD: `Fedwire`, `pacs.008`, `KYC`

Don't go above ~12 entries — too many and the resume becomes visually noisy.

## Patterns to maintain

These are conventions visible in the canonical YAML — preserve them across edits:

- **Bilingual company / institution names**: `Acme Corp (示範公司)`, `National Taiwan University (國立台灣大學)`. English first for international parsing, Chinese in parens.
- **Bold-emphasis on metrics**: `**4 hours → 30 minutes**` not `4 hours to 30 minutes`. The bold makes the impact pop in PDF.
- **Project sub-heading pattern**: `date: "Acme Corp — Singapore Office"` — using the `date` field as a deployment-context line.
- **Skills grouping**: 6 groups, each with a `label` + `details`. Don't collapse into one flat list.
- **Tense**: current role uses present-continuous-ish action verbs; prior roles use simple past.

## Generating a 中文版

Two approaches, depending on user preference:

### Option A: separate YAML file
- Copy `Yu_Kun_Liu_CV.yaml` to `Yu_Kun_Liu_CV_zh.yaml`
- Translate the prose fields (summary, highlights, position titles where 中文 is conventional) — keep tech names in English
- Change `locale.language` to `chinese` (verify RenderCV accepts this in the user's version — if not, may need a different value)
- Update `settings.render_command.pdf_path` so PDFs don't collide

### Option B: in-place language switch
- Maintain two `summary` lists in the same file but commented out — but RenderCV doesn't support comments-as-content. Less clean. Prefer Option A.

## Validation

Before saving, run `scripts/yaml_helpers.py validate <file>` to check:
- Required fields are present
- Date formats are valid
- No accidental fabricated fields
- Skills section uses the canonical grouped structure

If the user's installed RenderCV version differs from the schema this skill knows about, that's expected — just point them at `rendercv render <file>` for the actual validation, and if errors come back, address them by adjusting the YAML.

## Rendering

The user has RenderCV set up locally. To produce the final PDF:

```bash
cd ~/Desktop/project/workspace/rendercv-demo
rendercv render Yu_Kun_Liu_CV.yaml
```

Output goes to `rendercv_output/Yu_Kun_Liu_CV.pdf` (per the `settings.render_command` block).

If RenderCV isn't installed, fall back to `scripts/render_pdf.py` for a Markdown → PDF preview — note that this won't apply the RenderCV theme, but it's useful for quick review while iterating.
