---
name: resume-coach
description: "Use this skill whenever the user asks to review, improve, tailor, rewrite, or generate resume/CV content, RenderCV YAML, ATS feedback, JD-specific positioning, LinkedIn/CakeResume/104 copy, or cover-letter material. Fill in references/user-context.md with the user's real background before first use. Never fabricate metrics, companies, dates, tools, deployment scope, or achievements; mark uncertain details as [To confirm] or [待確認]."
metadata:
  short-description: Resume coaching — review, tailor, rewrite, RenderCV YAML
---

# Resume Coach

This skill helps maintain and improve a resume system. It is not a generic rewriter — it is designed to preserve the user's real background, keep RenderCV YAML clean, and produce ATS-friendly resume variants for specific job targets.

**Before first use:** fill in `references/user-context.md` with the user's real career history, projects, and skills. The skill will not invent or assume any background information.

## How to Invoke

This skill works across Claude Code and Codex. All of the following forms are valid entry points — slash commands and `@` mentions are optional aliases, not requirements.

**Explicit init / intake:**
- `/resume-coach init` (Claude Code) / `$resume-coach init` (Codex)
- `Use the resume-coach skill to start the resume intake flow`
- `start resume intake`

**Direct task invocation (skips intake if task is clear):**
- `/resume-coach review` (Claude Code) / `$resume-coach review` (Codex) / `Use resume-coach to review my resume`
- `/resume-coach tailor` (Claude Code) / `$resume-coach tailor` (Codex) / `Use resume-coach to tailor my resume for this JD`
- `/resume-coach rewrite` (Claude Code) / `$resume-coach rewrite` (Codex) / `Use resume-coach to rewrite this bullet`
- `review my resume` / `tailor my resume for this JD` / `help me build a resume version`

**Inferred direction from uploaded material:**
- `Use resume-coach to infer the target direction from this resume and ask me to confirm`
- Upload a JD or resume file → skill reads and infers direction, then confirms before acting

## Init / First-Use Flow

**When to run init:** Run the intake flow whenever:
- The user invokes the skill with no JD, no resume file, and no concrete task (e.g., just `/resume-coach init`, `$resume-coach init`, or `start resume intake`).
- The user's intent is ambiguous and guessing the mode would waste a full response.

**When NOT to run init:** Skip intake and proceed directly to the task when:
- The user has provided a JD, a resume file, or a specific rewrite request.
- The user's message already answers three or more of the five intake questions below.
- The user explicitly names a mode: `review`, `tailor`, `rewrite`, `build copy`.

**If material is uploaded but task is unclear:** Read the uploaded content, infer the most likely target direction, then ask for confirmation before producing output. Do not start rewriting immediately.

### Intake Questions

Ask all five questions together in a single message. Wait for answers before producing or editing any resume content.

```
I'll need a few details before we start.

1. Target direction — what kind of role or company are you aiming for?
   (If you've uploaded a resume or JD, I'll infer a likely direction and ask you to confirm.)

2. Output language — English / Traditional Chinese / both?

3. Output type — what do you need?
   - Review only (feedback, no rewrite)
   - Rewrite bullets (improve existing content)
   - Update RenderCV YAML (structured file edit)
   - Generate PDF (render after YAML is ready)

4. Input material — what are you working from?
   - Existing resume (paste or upload)
   - Job description (paste or upload)
   - Rough project notes (I'll shape them into bullets)
   - Blank start (I'll guide you through the intake)

5. Strictness — which approach fits this application?
   - Conservative ATS version (safe keywords, no stretch claims)
   - Stronger positioning version (sharper angles, bolder framing — confirm metrics first)
```

After receiving answers, proceed to the appropriate mode (Review / Customize / Rewrite / Build New Copy) without repeating the intake.

## Source of Truth

Use content in this order:

1. `references/user-context.md` inside this skill — the user's canonical career background, employers, projects, skills, and confirmed metrics.
2. The user's RenderCV YAML file(s) for current resume output.
3. User-provided JD or resume text for the current task.
4. Other `references/` files for formatting and ATS guidance.

Do not invent missing metrics, employers, dates, tools, project names, or deployment scale. If a useful metric is missing, write `[To confirm: metric needed]` in English or `[待確認: 需要確認的指標]` in Traditional Chinese.

## Target Positioning

Infer the user's positioning from `references/user-context.md`. Common archetypes include:

- Backend / Software Engineer
- Data Engineer / Analyst
- ML / AI Engineer
- DevOps / Platform Engineer
- Product Manager
- Domain-specific (FinTech, HealthTech, Gaming, etc.)

If the user's context file specifies a primary archetype, lead with that. If no context is available, ask the user during the init intake flow.

## Hard Rules

- RenderCV YAML is the primary structured output when files are requested.
- Keep YAML valid and schema-compatible.
- Do not generate PDF unless the user asks for it.
- Do not keyword-stuff. Put important keywords inside real experience or project bullets.
- Keep resumes ATS-friendly: real text, conventional section names, no decorative skill bars, no photo for English resumes, no complex layout.
- For Traditional Chinese, use zh-Hant and Taiwan usage. Keep technical terms such as Python, Playwright, Selenium, MSAL, EWS, T24, ISO 20022, Fedwire, pacs.008, pacs.009, Hugging Face, BERT, BIO tagging, and Label Studio in English.
- Do not over-emphasize NLP in RPA, banking automation, or FinTech versions.

## Modes

### Review

Use when the user asks for resume feedback or improvement.

Workflow:

1. Parse the resume content.
2. Identify likely target positioning.
3. Check ATS keyword coverage and whether keywords appear in context.
4. Find responsibility-only bullets and weak outcome bullets.
5. Rewrite the top 5 highest-leverage bullets first.
6. Mark missing metrics as `[To confirm: ...]` or `[待確認: ...]`.
7. Do not rewrite everything unless the user asks.

Output:

- Overall judgment.
- Top 5 fixes with before/after examples.
- ATS coverage notes.
- Structural notes.
- Items to confirm.

### Customize

Use when the user provides a JD, target role, company, or application goal.

Workflow:

1. Decompose the JD into hard requirements, preferred qualifications, implicit signals, keyword priorities, and business or engineering pain points.
2. Map the user's evidence to the JD with strength labels: Strong, Medium, Weak, Gap.
3. Choose one primary positioning and optional secondary positioning.
4. Rewrite summary, skills ordering, and the highest-impact experience/project bullets.
5. Trim unrelated material.
6. Preserve truth. Gaps stay gaps unless the user confirms hidden experience.

Use this table shape:

```markdown
| JD Requirement | Resume Evidence | Match Strength | Action |
|---|---|---|---|
| Python automation | Outlook / M365 RPA, T24 converter | Strong | Emphasize in summary and first experience |
| Cloud deployment | Not clearly shown | Gap | Ask whether any deployment experience exists |
```

### Rewrite

Use when the user gives a rough project or work description and wants resume-ready bullets.

Prefer:

```text
Action -> Technology -> Problem -> Result
```

or:

```text
What was built -> How it was built -> Why it mattered -> Confirmed impact or pending metric
```

Produce formal, technical, business-outcome, and English variants when useful. Keep the best version concise enough for a resume.

### Build New Copy

Use for Summary, LinkedIn, CakeResume, 104, cover letter, or profile copy.

- Resume Summary: 3-4 lines, role positioning + key technologies + differentiator.
- LinkedIn: 2-3 short first-person paragraphs.
- CakeResume / 104: concise Taiwan recruiter style.
- Cover letter: company and JD specific; avoid generic enthusiasm filler.

## RenderCV Workflow

When editing YAML:

1. Read the relevant source files first.
2. Make the smallest necessary edit.
3. Validate YAML syntax if tooling is available.
4. Check dates, spelling, unsupported claims, contact fields, target clarity, and NLP emphasis.
5. Do not render PDF unless requested.

Expected commands when PDF is explicitly requested:

```bash
rendercv render rendercv/resume_zh.yaml
rendercv render rendercv/resume_en.yaml
```

If this repository uses different file names or commands, inspect the repo and follow the existing setup.

## Final Response

Keep delivery concise:

- Files changed.
- Most important content changes.
- Remaining `[To confirm]` or `[待確認]` items.
- Whether PDF was generated.
- If a JD was used, summarize alignment and remaining gaps.
