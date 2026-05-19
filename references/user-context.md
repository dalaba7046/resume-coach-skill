# User Context

**Fill this file in before using the resume-coach skill.**
This is the single source of truth for your background. The skill will not invent or assume any information beyond what you write here.

Canonical resume YAML (if using RenderCV): `path/to/your_cv.yaml`

---

## Snapshot

- **Name**: [Your full name]
- **Location**: [City, Country]
- **Seniority**: [e.g., Senior, Mid-level, New grad]
- **Current role**: [Title] @ [Company], [YYYY-MM] → present
- **Primary archetype**: [e.g., Backend Engineer, Data Engineer, ML Engineer]
- **Secondary archetypes**: [optional]
- **Headline (for resume)**: [e.g., Senior Backend Engineer | Payments & Platform Infrastructure]

---

## Career Timeline

| Period | Company / Role | Stack & focus |
|--------|----------------|---------------|
| YYYY-MM – present | [Company] — [Title] | [Key tech, domain] |
| YYYY-MM – YYYY-MM | [Company] — [Title] | [Key tech, domain] |
| YYYY-MM – YYYY-MM | [Company] — [Title] | [Key tech, domain] |

---

## Key Projects

List your most impactful projects. Use real numbers — if a number is uncertain, write `[待確認]` next to it.

### [Project Name] — [Context or company]
- [What it did, the problem it solved]
- [Confirmed impact metric, e.g., "Reduced processing time from X to Y"]

### [Project Name] — [Context or company]
- [What it did]
- [Impact]

---

## Skills

List under the same groupings you use in your resume YAML. Example format:

- **Programming Languages**: [e.g., Python, Go, TypeScript]
- **Frameworks / Libraries**: [e.g., FastAPI, React, pandas]
- **Databases**: [e.g., PostgreSQL, MySQL, Redis]
- **Infra / DevOps**: [e.g., Docker, Kubernetes, AWS, Terraform]
- **Domain-specific**: [e.g., Kafka, Snowflake, dbt, T24, ISO 20022]

---

## Extended Technical Context

List any skills or experience areas that are real but may not be on the canonical resume yet. Confirm with the user before pulling these into resume content.

- [e.g., Side project using X]
- [e.g., Prior exposure to Y in academic context]

---

## Education

- **[University Name]** — [Degree], [Field], [YYYY-MM]
- **[University Name]** — [Degree], [Field], [YYYY-MM]

---

## Certifications

- **[Certification Name]** — issued by [Issuer], [YYYY-MM-DD]

---

## Positioning Angles

When customizing for a JD, pick the angle that best fits. Define 2–3 angles:

### As **[Primary Archetype]** (default)
- Lead with: [your strongest signal for this angle]
- Key stack: [technologies to front-load]
- Differentiator: [what makes you stand out in this angle]

### As **[Secondary Archetype]**
- Lead with: [...]
- Key stack: [...]
- Differentiator: [...]

---

## Style Preferences

- **bold_keywords** (RenderCV): [terms to auto-bold, e.g., Python, Docker, AWS]
- **Tone**: [e.g., action verb → technology → outcome]
- **Number formatting**: [e.g., bold headline metrics]
- **Section order**: [e.g., summary, experience, key_projects, skills, education]

---

## Hard Rules — Do Not Violate

- Never list a technology the user has not confirmed they used.
- Never invent project names, company names, or scale numbers.
- The confirmed metrics above are the only numbers permitted without explicit user confirmation.
- Mark any uncertain number as `[待確認]` / `[To confirm]`.
