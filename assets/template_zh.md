# 王小明

資深後端工程師 ｜ Go、Kubernetes、分散式系統 ｜ 6 年經驗

[email@example.com](mailto:email@example.com) ｜ +886 9xx-xxx-xxx ｜ [linkedin.com/in/username](https://linkedin.com/in/username) ｜ [github.com/username](https://github.com/username)

## 個人簡介

專注於 payments 與平台基礎建設的後端工程師。6 年經驗在 Kubernetes 上建構 Go 微服務，特別關注系統可靠度與基礎建設成本。曾主導 4 人團隊完成 monolith → microservices 遷移，將 p99 latency 降低 75%，年度節省 18 萬美金基礎建設費用。

## 工作經歷

### 資深後端工程師 ｜ FooCorp ｜ *2022/03 – 至今*

- 主導 payments 服務從 Rails 單體拆解為 12 個 Go 微服務，部署於 Kubernetes (EKS，80 pods、3 個 region)，將 p99 latency 從 850ms 降至 210ms，on-call 警報量降低 60%。
- 設計 payments API 的 idempotency 層，將重複扣款事故從每月 3 件降至 14 個月 0 件，預估避免每季 4 萬美金的 chargeback 損失。
- 帶領 3 位 mid-level 工程師，1 年內全數升職。

### 後端工程師 ｜ BarCorp ｜ *2019/08 – 2022/02*

- 建構 event-driven 訂單處理管線（Kafka、Go、PostgreSQL），每日處理 500 萬筆訂單，SLA 達 99.97%。
- 將每日批次任務從 4 小時縮減至 35 分鐘，透過 reducer 階段平行化與 Kafka partition 調校。

## 技能

- **程式語言**：Go、Python、TypeScript
- **基礎建設**：Kubernetes、Terraform、AWS（EKS、RDS、S3、SQS）
- **資料**：PostgreSQL、Redis、Kafka
- **可觀測性**：Datadog、Prometheus、Grafana

## 學歷

### 國立台灣大學 ｜ 資訊工程學系 學士 ｜ *2015 – 2019*
