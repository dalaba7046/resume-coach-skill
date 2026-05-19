# Quantified Achievements

The single highest-leverage rewrite on most engineering resumes is turning responsibility bullets into outcome-quantified achievements. This file is the playbook.

## The three bullet types

When reading a resume, classify each bullet:

**Type A — Quantified outcome (good):**
> Reduced API p99 latency from 1.2s to 280ms by introducing read-through Redis cache, saving ~$18k/yr in EC2 costs.

**Type B — Outcome stated, no metric (medium):**
> Improved API performance by introducing a caching layer.

**Type C — Responsibility only (weak):**
> Worked on API performance improvements.

Goal: convert B and C to A. If the user genuinely doesn't have a number (early-career projects, NDA-bound metrics), keep the bullet at type B but at least make the outcome concrete.

## The 「待確認」 rule — never fabricate numbers

If a rewrite needs a metric the user hasn't provided, **mark it inline** and surface it as a question at the end of the response:

```
Cut document processing time from [待確認: 約多少小時] hours to 2 hours (95%+ accuracy).
```

Then list `[待確認]` items at the bottom of the response:

> **待補資訊 / Information to confirm**
> - 文書處理在自動化前的耗時（約幾小時/月）
> - Khmer OCR 翻譯的 BLEU 或人工複核準確率（若有）
> - Fedwire pacs.008 月處理量（若有）

**Never silently guess.** Inventing a number is worse than leaving the placeholder — recruiters and engineers will catch fabricated metrics in screening calls, and the cost is much higher than the bullet looking slightly unfinished.

The only metrics you can use without `[待確認]` are those already in:
1. The canonical YAML (`Yu_Kun_Liu_CV.yaml`)
2. `references/user-context.md`
3. Explicitly provided by the user in the current conversation

## The rewrite formula

You can use either of two patterns. Both work; pick whichever fits the bullet's natural flow.

**STAR-derived:**
```
[Situation context (optional)] + [Action verb + Task] + [Result with metric]
```

**Action → Tech → Problem → Outcome (recommended for tech bullets):**
```
[Action verb] + [What you did + tech stack] + [Problem it addressed] + [Measurable outcome]
```

Or the simple compact form:
```
[Action verb] + [What you did] + [Measurable outcome] + [Why it mattered]
```

Examples:

- Migrated → checkout service from Rails to Go → cutting median latency 60% (320ms→128ms) → enabling a 2x throughput at the same infrastructure cost
- Built → idempotency layer for payments API → eliminating duplicate-charge incidents (was 3/month, now 0 in 14 months) → preventing ~$40k/quarter in chargebacks
- Led → 4-engineer team migrating 30 services from EC2 to EKS → reducing infra costs 35% and deploy time from 25min to 4min

You don't always need all four parts — sometimes the outcome is the "why". But aim for at least three.

## Metric libraries by engineering domain

When the user has the experience but no number, suggest credible metrics from their domain. They'll usually know the rough value and can fill in.

### Backend / API engineering
- Latency: p50 / p95 / p99 in ms, before vs after
- Throughput: requests/sec, queries/sec
- Error rate: % errors, 5xx count
- Availability / uptime: 99.9% → 99.99%
- Scale: # users, # requests/day, # transactions
- Cost: $ saved on infra/quarter

### Frontend / web
- Page load: LCP, FCP, TTI in seconds or ms
- Lighthouse score: before → after
- Bundle size: KB / MB reduction
- Conversion lift: % increase in signup / checkout / engagement
- A/B test wins: lift %, statistical significance

### Mobile
- App size: MB reduction
- Crash-free rate: % before → after
- ANR rate (Android)
- Startup time: cold/warm start in ms
- Adoption: DAU, MAU, retention curves

### Data / ML
- Model metrics: AUC, F1, accuracy (and the lift vs prior baseline)
- Pipeline scale: GB or TB processed/day
- Pipeline reliability: SLA hit rate, # incidents
- Latency: inference time, batch job duration
- Cost: $/inference, $/training run

### Infrastructure / SRE / DevOps
- Deploy frequency: per day/week
- Lead time for changes: hours
- MTTR: minutes/hours
- Change failure rate: %
- Toil reduction: hours/week saved
- Cluster scale: # nodes, # pods, # services, # regions
- Cost: $ infra savings, % cost reduction

### RPA / Banking automation (the user's primary domain)
- Process time reduction: hours → minutes/hours, before vs after (e.g., `8 hours → 15 minutes`)
- Person-hours saved: hours/month or hours/week reclaimed (e.g., `80 person-hours/month`)
- Volume: # documents/transactions processed per period (e.g., `200+ documents/month`, `500+ transactions/day`)
- Coverage: # systems integrated, # branches deployed, # agencies monitored
- Accuracy: OCR / parse accuracy %, error rate before/after
- Compliance: # regulatory checks automated, audit trail completeness
- Cost: $ saved by avoiding manual work or vendor licenses (only if user has the number)
- Reliability: % SLA, # incidents prevented

### Document AI / OCR / LLM pipelines
- Throughput: pages/docs/month
- Accuracy: OCR character/word accuracy, translation BLEU or human-eval % (only if measured)
- Latency: per-doc processing time
- Language coverage: # languages supported (e.g., Khmer + English + Mandarin)
- Quality control: % of docs requiring manual review, before/after

### NLP / ML research
- Model metrics: F1, AUC, accuracy on benchmark (with comparison baseline)
- Dataset scale: # samples annotated, # categories
- Methods: explicit named techniques (BIO tagging, sequence labeling, fine-tuning chinese-bert-wwm-ext)
- Publication / presentation venues (if any)

### Security
- Vulnerabilities closed: # critical/high
- Mean time to remediate: days
- Audit findings: passed/closed
- Coverage: % services with SAST/DAST, % infra IaC-managed

### Leadership / cross-functional (any role)
- Team size: # engineers led/mentored
- Cross-team coordination: # teams, # stakeholders
- Hiring: # roles closed, # interviews conducted
- Process: % review cycle reduction, # incidents avoided post-process-change

## Before / after rewrites

**Backend (vague → quantified):**

Before: *"Improved system performance and reliability."*

After: *"Cut payment-API p99 latency 65% (940ms→330ms) and eliminated weekly cascading-failure incidents by introducing per-tenant rate limiting and circuit breakers across 12 downstream services."*

---

**Frontend (responsibility → outcome):**

Before: *"Worked on the checkout flow redesign."*

After: *"Led frontend rewrite of checkout flow (React → Next.js), raising mobile conversion 14% and cutting LCP from 4.1s to 1.6s. Shipped to 100% of 2M MAU over a 6-week rollout."*

---

**Infra (verb-noun → impact):**

Before: *"Managed Kubernetes clusters in production."*

After: *"Operated 4 production Kubernetes clusters (80 nodes, 350 services, 3 AWS regions), cutting deploy time from 22min to 5min via ArgoCD adoption and holding 99.97% availability across the year."*

---

**Junior engineer with limited metrics:**

Before: *"Built features for the internal admin tool."*

After: *"Shipped 8 features for the internal admin tool (used by 25-person ops team), including a bulk-edit flow that cut a recurring 4hr/week manual task to under 10 minutes."*

Notice: even a junior dev who "just built features" can quantify scope (8 features), audience (25 people), and time saved (4hr/wk → 10min). Numbers don't have to be cosmic.

## Asking the user for numbers

If a bullet describes a real outcome but the user didn't include a number, ask — but ask concretely, not vaguely.

Bad: "Can you quantify this?"

Good: "For 'improved API performance' — do you remember roughly what the latency was before and after? Even a rough number (like '~1s to ~300ms') is much stronger than 'improved'."

Offer 2-3 plausible numbers from the metric library so they can pick or correct.

## Action verbs

Lead with strong, specific verbs. Avoid weak/vague ones. (Use these as a substitution list, not a worship list — the verb is less important than the outcome.)

**Strong, specific:**
Built, Designed, Architected, Migrated, Decomposed, Refactored, Optimized, Profiled, Instrumented, Shipped, Launched, Owned, Led, Mentored, Cut, Reduced, Eliminated, Doubled, Tripled, Scaled, Automated, Eliminated, Resolved, Introduced, Pioneered.

**Weak, avoid:**
Worked on, Helped with, Assisted, Was involved in, Participated, Took part in, Familiar with, Exposed to, Responsible for (use sparingly).

For 中文 履歷 the equivalent strong verbs are: 重構、遷移、設計、主導、推動、優化、上線、導入、量化、自動化、降低、縮減、提升、擴展、整合、解決。
