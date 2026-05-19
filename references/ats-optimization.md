# ATS Keyword Optimization

Applicant Tracking Systems (ATS) — Greenhouse, Lever, Workday, Taleo, 104 Pro Match, CakeResume's internal matcher, etc. — parse resume text and rank candidates based on keyword overlap with the job description. A resume that's brilliant for human readers can still get filtered out by a poor keyword match. This file explains how to optimize without resorting to keyword stuffing.

## Mental model: how ATS actually scores

Most ATS implementations work roughly like this:

1. **Parse** — extract raw text from the PDF/DOCX, attempt to identify sections (experience, skills, education).
2. **Tokenize** — break into terms, normalize plurals and capitalizations.
3. **Match** — compare resume terms against the JD's requirement terms. Weight contextual matches (inside experience bullets) higher than skills-list matches.
4. **Score** — produce a percentage match. Common thresholds: <50% auto-rejected, 50–70% reviewed if pipeline is slow, 70%+ surfaced to recruiter.
5. **Format penalties** — multi-column layouts, text-in-images, decorative tables, and headers/footers in critical sections often get parsed incorrectly, dropping the score.

The two biggest wins are: (a) make sure target keywords appear in the *experience bullets* in natural context (not just a skills section), and (b) use a clean single-column PDF that text-extracts cleanly.

## JD decomposition checklist

When the user provides a JD, extract keywords in tiers:

**Tier 1 — Hard requirements (must match)**
- Programming languages (Go, Python, Java, TypeScript, …)
- Frameworks (React, Spring Boot, Django, FastAPI, …)
- Cloud / infra (AWS, GCP, Azure, Kubernetes, Terraform, …)
- Specific tools/products mentioned by name (Kafka, Snowflake, dbt, Datadog, …)
- Years of experience requirements (5+ years, senior, staff)
- Education requirements (degree fields, certifications)

**Tier 2 — Domain & methodology**
- Architecture patterns (microservices, event-driven, serverless, monolith decomposition)
- Practices (CI/CD, TDD, code review, on-call, SRE, DevOps)
- Data structures / scale signals (high-throughput, low-latency, distributed, real-time)

**Tier 3 — Soft signals & culture**
- Ownership, autonomy, ambiguity, 0→1, scale, platform, customer-facing
- Cross-functional, mentorship, leadership
- Industry (fintech, healthtech, gaming, e-commerce, …)

Tier 1 terms must appear verbatim (or with the standard variant — "Postgres" ↔ "PostgreSQL", "K8s" ↔ "Kubernetes" — include both if space allows). Tier 2 and Tier 3 should be reflected through bullet content and headline phrasing.

## Coverage analysis

Build a coverage table during Customize mode. Example for a "Senior Backend Engineer (Go, Kubernetes)" JD:

| JD term            | Tier | Resume mention?              | Action                                                |
|--------------------|------|------------------------------|-------------------------------------------------------|
| Go                 | 1    | Yes — 2 bullets at FooCorp   | Keep. Move FooCorp role up if not first.              |
| Kubernetes         | 1    | "managed prod cluster"       | Strengthen: add scale (nodes, pods, clusters).        |
| gRPC               | 1    | No                           | Ask user; if has experience, add bullet.              |
| microservices      | 2    | Implied not stated           | Add to one bullet's prose.                            |
| on-call / SRE      | 2    | No                           | If user has on-call rotation experience, add it.      |
| ownership          | 3    | Implied via "led migration"  | Keep as-is; phrasing already signals this.            |
| 5+ years           | 1    | Yes — total tenure ≈ 6 years | Make sure dates are visible in summary.               |

## Natural placement, not keyword stuffing

Bad — looks like keyword salad, ATS systems often detect and downrank:

> Skills: Go, Python, Java, Kubernetes, Docker, AWS, GCP, Azure, Kafka, Redis, PostgreSQL, MySQL, MongoDB, Elasticsearch, Terraform, Ansible, Jenkins, GitLab CI, GitHub Actions, Prometheus, Grafana, Datadog, New Relic, Sentry, gRPC, REST, GraphQL, microservices, serverless, event-driven, CI/CD, TDD, BDD, agile, scrum, kanban, …

Good — keyword appears *in context* inside a bullet, with the impact:

> Migrated payments service from monolith to **Go microservices** on **Kubernetes** (12 services, 80 pods, 3 regions), reducing p99 latency from 850ms to 210ms and on-call pages by 60%.

Still keep a skills section, but make it shorter and grouped:

```
Languages:   Go, Python, TypeScript
Infra:       Kubernetes, Terraform, AWS (EKS, RDS, S3)
Data:        PostgreSQL, Redis, Kafka
Observability: Datadog, Prometheus, Grafana
```

Grouped skills lists parse cleanly and don't trip the keyword-stuffing detection that some ATS use.

## Section labels ATS expects

Use conventional section labels — ATS parsers look for these strings to segment the resume:

- "Experience" / "Work Experience" / "Professional Experience" — *not* "My Journey", "Adventures", "Where I've Been"
- "Education" — *not* "Schooling", "Academic Life"
- "Skills" / "Technical Skills" — *not* "What I Know"
- "Projects" — fine as-is

For 中文 履歷: 「工作經歷」、「學歷」、「技能」、「專案經歷」are all standard and parse fine through Taiwan-localized ATS (104, 1111, CakeResume).

## Common ATS-breaking patterns to avoid

- **Multi-column layouts** — sidebar with skills/contact often loses its association with the main content; the parser may emit skills as a separate block with no role attached.
- **Text rendered as images** — invisible to ATS. Common offender: name/title rendered as a logo-style graphic.
- **Tables for layout** — modern parsers handle simple tables OK but get confused by nested or merged cells. Use them for actual tabular data only.
- **Headers/footers with critical info** — some parsers skip page headers/footers entirely. Don't put your phone number only in the footer.
- **Non-standard bullet glyphs** — •, ‣, ▪ are fine; ASCII art (>>, →→) sometimes confuses parsers. Stick with the standard bullet.
- **Fancy fonts / font embedded as outlines** — text becomes vector shapes, ATS can't extract. Use system fonts that embed as text.

The `scripts/render_pdf.py` template avoids all of these by default.

## A note on truthful keyword inclusion

Only add keywords for experience the user actually has. If they don't have Kubernetes experience, don't write "Kubernetes" into a bullet to game the ATS — recruiters will spot the mismatch in screening calls, and even if they don't, the user will fail the interview loop. Honest gap-acknowledgment + adjacent-strength positioning beats keyword fraud every time.
