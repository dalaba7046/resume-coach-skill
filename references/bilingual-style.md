# Bilingual Resume Style Guide (zh-Hant + English)

When producing both a 中文版 and an English 版, treat them as two parallel resumes for two different audiences — not as translations of each other. The content overlaps but the conventions, expected sections, and phrasing differ.

## Audience model

- **中文版** is for: Taiwan-based companies (本土軟體公司、外商台灣分公司), 104 / 1111 / CakeResume listings, internal HR review. Reviewer is often a Taiwan-trained HR generalist plus a hiring engineer.
- **English version** is for: international tech companies (US, EU, SG, Japan English-speaking pipelines), remote roles, LinkedIn presence. Reviewer is often a US-style recruiter + hiring engineer.

The differences below come from these audience expectations.

## Sections — what's expected vs optional

| Section            | 中文版              | English | Notes                                                            |
|--------------------|--------------------|---------|------------------------------------------------------------------|
| 照片 / Photo        | Optional, common    | Never   | English resumes with photos are penalized in US/UK (bias laws).  |
| 個人資料 / Header    | Name + contact      | Same    | 中文 may include LinkedIn/GitHub URL.                            |
| 出生年月 / DOB       | Optional, common    | Never   | Omit in 中文 for senior roles to avoid age inference.            |
| 婚姻 / Marital state | Optional, declining | Never   | Modern 中文 履歷 usually omits.                                  |
| 兵役 / Military      | Common (TW)         | Never   | If已退役/免役, fine to mention briefly. Skip entirely in English.|
| 個人簡介 / Summary   | 3–4 lines           | 2–3 lines | Lead with seniority, domain, and 1 differentiator.             |
| 技能 / Skills        | Yes                 | Yes     | Same grouped format works in both.                               |
| 工作經歷 / Experience| Yes                 | Yes     | Reverse chronological, most recent first.                        |
| 學歷 / Education     | Yes                 | Yes     | More senior → place below Experience.                            |
| 專案 / Projects      | Optional            | Optional| Worth including for early-career or career-changer.              |
| 證照 / Certifications| Optional            | Optional| Only if relevant (AWS, GCP, K8s CKA, Security certs).            |
| 自我評價 / Soft pitch| Optional            | Never   | English doesn't have a "personal traits" section; soft signals show through bullets. |

## Date format

- 中文版: `2022/03 – 2024/05` or `2022.03 – 至今`
- English: `Mar 2022 – May 2024` or `Mar 2022 – Present`

Consistent format throughout — pick one and stick with it.

## Headline / title

中文版:
> 資深後端工程師 ｜ Go、Kubernetes、分散式系統 ｜ 6 年經驗

English:
> Senior Backend Engineer · Go, Kubernetes, Distributed Systems · 6 yrs

Both should signal: seniority + 2-3 core technologies + (optional) years.

## Tone & verb choice

- **中文** tolerates slightly more compact, noun-heavy phrasing. Bullets often start with a verb but the prose can be terse.
- **English** strongly prefers verb-led bullets. Past-tense for prior roles, present-tense for current role.

## Taiwan terminology QA — avoid 中國用語

When producing 中文版, automatically check for and replace 中國用語 with 台灣常用語. The most common offenders in tech-context resumes:

| 中國用語 | 台灣用語        | Notes                                                          |
|----------|----------------|---------------------------------------------------------------|
| 項目      | 專案            | "Project". This is the most common one.                       |
| 質量      | 品質            | "Quality".                                                    |
| 視頻      | 影片            | "Video".                                                      |
| 信息      | 資訊            | "Information".                                                |
| 數據      | 資料            | Context-dependent — 「資料」 in most cases, but 「數據」 is also accepted in TW for ML/statistical contexts ("數據科學家", "大數據"). Don't blindly replace; check context. |
| 程序      | 程式 / 程序     | "Program / process". `程序` in TW = `process` (流程); `程式` = `program (code)`. In CN, `程序` is also `program`. Check meaning. |
| 軟件      | 軟體            | "Software".                                                   |
| 硬件      | 硬體            | "Hardware".                                                   |
| 服務器    | 伺服器          | "Server".                                                     |
| 用戶      | 使用者          | "User".                                                       |
| 默認      | 預設            | "Default".                                                    |
| 文檔      | 文件 / 文檔     | "Document". TW prefers 「文件」; 「文檔」 is also OK in tech.   |
| 緩存      | 快取            | "Cache".                                                      |
| 隊列      | 佇列            | "Queue".                                                      |
| 接口      | 介面            | "Interface" (API or UI).                                      |
| 平臺      | 平台            | "Platform". TW prefers 平台 (without 臺).                      |
| 集群      | 叢集            | "Cluster".                                                    |
| 開發者    | 開發人員 / 工程師| "Developer". TW more often uses 「工程師」 in resume context. |

Pass the 中文 output through this filter before delivering. When in doubt about a context-sensitive term like 數據/資料 or 程序/程式, leave it as-is and flag it for the user.

## Technical terms — keep in English even in 中文版

For Taiwan tech roles, keep technology names, frameworks, and architecture terms in English. ATS systems (104, CakeResume) and Taiwan engineering hiring managers expect this. Don't translate:

- Kubernetes → 不要寫成「k8s 容器編排系統」 — just write Kubernetes
- microservices → 微服務 is OK, but Kubernetes/Docker/CI-CD stay in English
- gRPC, REST, GraphQL → English
- Programming languages → English (Go, Python, Java, not 戈、蟒、爪哇)

It's normal and expected to mix English technical terms into 中文 prose:

> 主導 payments 服務從單體拆解為 12 個 Go 微服務，部署在 Kubernetes (EKS) 上，將 p99 latency 從 850ms 降至 210ms。

## Bilingual bullet examples

**Backend bullet, English:**
> Migrated payments service from monolith to 12 Go microservices on Kubernetes (EKS, 80 pods, 3 regions), cutting p99 latency 75% (850ms→210ms) and on-call pages by 60%.

**Same bullet, 中文版:**
> 主導 payments 服務從單體架構拆解為 12 個 Go 微服務，部署於 Kubernetes (EKS，80 pods、3 個 region)，將 p99 latency 從 850ms 降至 210ms（-75%），on-call 警報量降低 60%。

Notice:
- Same numbers, same structure
- Technical terms stay in English
- 中文 uses 「主導」 instead of "Led" — sounds natural
- 中文 uses 「降至」 / 「降低」 instead of "cutting" / "reducing"

## File naming when delivering both

- `<name>_resume_zh.pdf`
- `<name>_resume_en.pdf`

Or if just one:
- `<name>_resume.pdf`

## Quick checklist

中文版:
- [ ] 用繁體中文（不是簡體）
- [ ] 日期格式統一 (YYYY/MM)
- [ ] 技術名詞保留英文
- [ ] 沒有放照片時要徵詢使用者意願
- [ ] 沒有出生年月/婚姻狀態（除非使用者要求）

English:
- [ ] No photo, no DOB, no marital status
- [ ] All bullets verb-led
- [ ] Past tense for prior roles, present for current
- [ ] Date format: `Mon YYYY – Mon YYYY` or `Mon YYYY – Present`
- [ ] American spelling unless user is targeting UK/AU (then UK English)
