# resume-coach-skill

An AI skill for resume coaching — review your resume, tailor it to a job posting,
rewrite weak bullet points, and produce bilingual English / Traditional Chinese versions.

No coding knowledge required to use. Just fill in two files, install the skill, and start chatting.

---

## What It Does

- **Review** your resume and tell you the highest-impact things to fix.
- **Tailor** your resume to a specific job description.
- **Rewrite** rough notes or weak bullet points into strong resume content.
- **Produce bilingual copy** — English and Traditional Chinese.
- **Never makes things up** — uncertain numbers are flagged as `[To confirm]` for you to verify.

---

## Setup (5 minutes)

### Step 1 — Fill in your background

Open `references/user-context.md` with any text editor:
- **Mac:** right-click the file → Open With → **TextEdit**
- **Windows:** right-click the file → Open With → **Notepad**

Fill in your work history, key projects, skills, and education in plain language.

> Think of it as filling in a form, not writing code. Just replace the `[placeholder]` text with your own words.

### Step 2 — Set your preferences

Open `SKILL.md` the same way (TextEdit on Mac, Notepad on Windows),
scroll to the **User Configuration** section near the top,
and answer three short questions about your target industry and preferences.

### Step 3 — Install the skill

First, decide where to install:

| | Global install | Project install |
|---|---|---|
| **Works in** | Every project, everywhere | This project folder only |
| **Good for** | Personal resume tool you always want available | Keeping the skill tied to one specific project |

---

**Global install — Mac:**

1. Open the **Terminal** app (press `Cmd + Space`, type "Terminal", press Enter).
2. Paste the following and press Enter:

```bash
cp -r resume-coach-template ~/.claude/skills/resume-coach
```

The skill is now available in all your Claude Code sessions.

---

**Global install — Windows:**

1. Open **File Explorer**.
2. In the address bar at the top, type `%USERPROFILE%\.claude\skills` and press Enter.
   (This opens something like `C:\Users\王小明\.claude\skills\`)
3. Copy the `resume-coach-template` folder into this `skills` folder.
4. Rename the copied folder from `resume-coach-template` to `resume-coach`.

The skill is now available in all your Claude Code sessions.

---

**Project install — Mac:**

1. Open the **Terminal** app.
2. Navigate to your project folder, then paste:

```bash
cp -r resume-coach-template .claude/skills/resume-coach
```

The skill is only available inside this project.

---

**Project install — Windows:**

1. Inside your project folder, open (or create) a folder named `.claude`, then inside it create a folder named `skills`.
2. Copy the `resume-coach-template` folder into `.claude\skills\`.
3. Rename it to `resume-coach`.

The skill is only available inside this project.

---

**Using Codex:** follow the Codex plugin installation guide for your environment.

### Step 4 — Start chatting

In Claude Code, type:
```
/resume-coach init
```

In Codex, type:
```
$resume-coach init
```

Or just describe what you need in plain language — the skill will figure out the rest.

---

## Example Things You Can Say

```
Review my resume and tell me what to improve.
```
```
I found this job posting — can you tailor my resume for it?
```
```
Help me rewrite this bullet point: [paste your text]
```
```
Write a resume summary for me in both English and Chinese.
```

---

## File Overview

```text
resume-coach-template/
├── SKILL.md                        ← skill settings (fill in User Configuration)
├── references/
│   └── user-context.md             ← YOUR background (fill this in first)
├── assets/
│   ├── template_en.md              ← English resume template
│   └── template_zh.md              ← Traditional Chinese resume template
└── scripts/                        ← optional tools for advanced users
```

---

## For Advanced Users

If you use RenderCV for structured resume output, the following commands are available:

```bash
# Check your resume YAML for errors
python scripts/yaml_helpers.py validate path/to/resume.yaml

# Check for any unconfirmed claims or missing numbers
python scripts/yaml_helpers.py check path/to/resume.yaml

# Compare a base resume against a tailored version
python scripts/yaml_helpers.py diff base.yaml tailored.yaml

# Render a Markdown resume to PDF
python scripts/render_pdf.py path/to/resume.md
```

---

## License

MIT
