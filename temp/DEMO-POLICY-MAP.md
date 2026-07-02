# Jskope Demo Portal — Demo ↔ Policy Map (reconciled to imported policy)

> **Source of truth:** the two imported Netskope inline-policy exports
> (UKSE shared tenant + JSkope/JSIP tenant), **enabled rules only** (165 rules).
> Where the two tenants conflict, the resolution is noted inline and the demo
> uses the more demo-representative action.
>
> This replaces the earlier "recommended policy" draft — the actions below are
> what your **actual** enabled policy does, and the demo pages have been updated
> to match so each demo triggers a real rule.

## Action vocabulary (as it appears in your policy)

| Policy action string | Demo label |
|---|---|
| `Block: …` / `High: Block: …` | **Block** |
| `User Alert: …` | **Coach** |
| `Isolate: … RBI Template` | **Isolate (RBI)** |
| `Quarantine` | **Quarantine** |
| `Alert` | **Alert / Log** |
| `Allow` / `Default` | **Allow** |

---

## 1. Web Blocking — SWG category + CCI

| Category (kept) | Real rule(s) | Action | Note |
|---|---|---|---|
| Unsanctioned File Sharing (WeTransfer, Pastebin, SendGB, Filebin) | `[Access Control] Unsafe Cloud Storage Browse` (CCL Low/Poor/Unknown) | **Block** | Low/Poor CCI cloud storage |
| Personal Cloud Storage (Dropbox, OneDrive, iCloud, MEGA) | `UCI Score High Risk Block` (Dropbox UCI<651), `[TimmS] NonCorp Dropbox Blocked`, `Unsafe Cloud Storage` (Upload, CCL Low/Poor/Medium/Unknown), `[AC] Personal OneDrive Block` | **Block** | *Changed from Coach.* Personal instances blocked |
| Social Media (TikTok, Reddit, Discord, Twitch) | `WEB - Time Wasting` (User Alert); no category block exists | **Coach / Allow** | *Changed from Block.* **Confirms Reddit = coach** |
| Streaming & Entertainment (Netflix, Spotify, Disney+, Prime) | no block rule; `WEB - Time Wasting` may coach | **Allow / Coach** | *Changed from Log/Block* |

## 2. User Coaching — where `User Alert` actually fires

| Scenario | Real rule | Action |
|---|---|---|
| Browsing any GenAI tool | `[Demo] Coach GenAI Access` (Generative AI · Browse) | **Coach** |
| Sensitive upload to sanctioned OneDrive | `[Demo] User Alert upload sensitive data into sanctioned OneDrive` (PII/PCI) | **Coach** |
| Sensitive upload/post to Slack / Teams | `Sensitive File Upload to Slack`, `Microsoft Teams Post` (PCI) | **Coach** |
| WhatsApp file transfer | `[DLP] WhatsApp` (Download/Upload) | **Coach** |
| Time-wasting / job-search sites | `WEB - Time Wasting`, `WEB - Job Sites Alert` | **Coach** |

> Note: personal cloud storage / personal webmail now **Block** in this tenant
> (see §1, §6), so the coaching demo leads with the GenAI + sanctioned-app cases.

## 3. Data Protection (DLP)

| Trigger (app · activity) | Real rule · profile | Action |
|---|---|---|
| Download from a DLP-test site | `[Data Protection] PCI Download` (Sites for DLP test · Download · PCI) | **Block** |
| Paste/upload PII/PCI via web form | `Block sensitive data upload via web form post` (Sites for DLP test · Upload/FormPost · PII+GSC) | **Block** |
| Upload PCI/PII to **sanctioned** OneDrive | `[Demo] User Alert … sanctioned OneDrive` | **Coach** |
| Upload PCI/PII to **non-sanctioned** OneDrive | `[Demo] Block Sensitive data into non sanctioned OneDrive` | **Block** |
| Post PCI to Slack / Teams | `Sensitive File Upload to Slack`, `Teams Post` | **Coach** |
| Upload any password-protected file | `[Data Protection] Password Protected Files` | **Block** |
| Upload PCI/PII to Cloud Storage / Social / Collab | `[DLP] PCI Upload Block` | **Block** |
| Source code + secrets to GenAI | `[Demo] Block Sensitive Data Upload to Gen AI` (DLP-SourceCode) | **Block** |
| Confidential-labelled file, any app | `Test File Profile for Confidential Label` | **Block** |
| Top-Secret-labelled download | `Block Download of TS labelled data` | **Block** |

## 4. AI Security — Guardrails + DLP on GenAI

| Scenario | Real rule | Action |
|---|---|---|
| Sanctioned AI (ChatGPT, Copilot, Gemini, Claude) general use | `[Demo] Sanctioned AI Allowed`, `Approved AI` | **Allow** |
| First use / browse of GenAI | `[Demo] Coach GenAI Access`, `AI Guardrails default` (ChatGPT Post/Response) | **Coach** |
| Upload PII / PCI / **source code** to Copilot/Gemini/ChatGPT | `[Demo] Block Sensitive Data Upload to Gen AI` (DLP-PCI, DLP-PII, DLP-SourceCode) | **Block** |
| Jailbreak prompt | `AI Security Guardrails - Jail Break Attempt` | **Block** |
| Competitor-watchlist content in response | `AI Security Guardrails - Predefined Triggers` | **Block (coach)** |
| Unauthenticated / non-corp ChatGPT | `block chatgpt unauth`, `Block Access to non-approved ChatGPT` | **Block** |
| Copilot sidebar post | `Block Copilot Sidebar` | **Block** |
| Sensitive image / driver-licence to AI | `[ML DLP] Block sensitive image uploads to AI`, `AI Image Detection` | **Block / Coach** |
| Unsanctioned AI (any other GenAI app) | `[Demo] Block Unsanctioned AI` | **Block** |

> **Tool risk mapping for the demo:** ChatGPT / Copilot / Gemini / Claude =
> *Sanctioned* (Allow + guardrails). Any other GenAI = *Unsanctioned* (Block).

## 5. Shadow AI (personal-instance switch)

| Scenario | Real rule | Action |
|---|---|---|
| Switch to personal/unsanctioned AI | `[Demo] Block Unsanctioned AI` (Generative AI · Any) | **Block** |
| Sensitive prompt into any monitored AI | `[Demo] Block Sensitive Data Upload to Gen AI` | **Block** |
| Corp vs personal ChatGPT instance | `Block Access to non-approved ChatGPT` (Non-Corp Instance) | **Block** |

## 6. Email / Webmail DLP

| Trigger | Real rule | Action |
|---|---|---|
| Send sensitive data via personal webmail | `[Demo] Block Sending sensitive data via Web Mail` (Outlook.com · PII/PCI) | **Block** |
| Webmail send w/ keyword profile | `test p008`, `SaaS Webmail Internal DLP Alert` | **Block / Coach** |
| Non-corp Gmail | `[Instance] Block non-corp GMail` | **Block** |
| Outbound email PCI (Exchange/Gmail) | `[Email DLP] Outbound email PCI Policy` | **Add Headers** |

## 7. Threat Protection

| Trigger | Real rule | Action |
|---|---|---|
| Malware file (EICAR etc.) up/download | `[Threat] Malicious File Protection` (Default Malware Scan) | **Block (High)** |
| First-seen / risky-category download | `Patient Zero Threat Protection` (NOD/NRD/Uncat/Parked) | **Block (High)** |
| Potentially malicious site | `[Access Control] Potentially Malicious Sites` (UKSE) **vs** `[Threat] Potentially Malicious Sites` (JSIP) | **Block *or* Coach** ⚠ conflict |
| Risky/uncategorised site render | `[Threat] RBI`, `[RBI] …` (Uncat/NRD/Parked/Web Proxies/No Content) | **Isolate (RBI)** |

## 8. Shadow IT Discovery — CCI / UCI driven

CCL → action (from `Unsafe Cloud Storage` rules + `UCI Score Block`):

| CCI / CCL | Action | Example apps |
|---|---|---|
| Poor (0–25) | **Block** (browse + upload) | MEGA 22, AnonFiles 18 |
| Low (26–50) | **Block** (browse + upload) | WeTransfer 42, Pastebin 38, Filebin 33 |
| Medium (51–75) | **Block on upload** (browse allowed) | Dropbox 69*, OneDrive 65 |
| High/Excellent (76–100) | **Allow** | SharePoint/OneDrive Corp 89 |

*Dropbox is additionally blocked outright by `UCI Score High Risk Block` (UCI < 651) and `NonCorp Dropbox Blocked`.

## 9. Zero Trust Access (NPA)

| Trigger | Real rule | Action |
|---|---|---|
| Authorised user → private app (RDP/SSH/portal) | `[NPA] User Portal Access`, `[ZTNA] … Allow`, `NPA Applications Allow` | **Allow** |
| Unauthorised user → same app | `[ZTNA] RDP … Block`, `[NPA] RDP … Block` (e.g. bob.jones) | **Block NPA Access** |
| Access not via dedicated egress IP | `[DEIP] Block if access not via DEIP` (Genesys) | **Block** |

## 10. Cloud Firewall (FWaaS) — corrected to real rules

| Service | Real rule | Action | Note |
|---|---|---|---|
| SSH | `[Demo] Allowed SSH` | **Allow** | *Changed from Block* |
| FTP (approved server) | `[CFW] Allow DLPTest FTP` | **Allow** | specific app allowed |
| FTP (generic, by signature) | `[CFW] Block FTP By Signature` | **Block** | |
| QUIC | `[CFW] Block QUIC` | **Block** | forces TLS inspection |
| DNS-over-TLS | `[CFW] Block DoT` | **Block** | prevents DNS bypass |
| DNS-over-HTTPS | `[DOH] Block` / `Block App` | **Block (mute)** | |
| TeamViewer (outbound) | `[CFW] Block TeamViewer outbound` | **Block** | remote-access risk |
| Slack | `[CFW] Allow` | **Allow** | |
| Connections to sinkhole IP | `[Demo] Block All Connections To Sinkhole IP` | **Block (sinkhole)** | |
| Other non-web protocols | `[Demo] Blocked Protocols` | **Block** | |

## 11. DNS Security

| Trigger | Real rule | Action |
|---|---|---|
| All DNS resolution | `DNS Security Policy` (Default DNS Profile), `DNSaaS` | **Default (threat filtering)** |
| DNS-over-HTTPS / -TLS bypass | `[DOH] Block`, `[CFW] Block DoT` | **Block** |
| Sinkhole callback | `Block All Connections To Sinkhole IP` | **Block** |

## 12. Enterprise Browser / RBI

| Control | Real rule | Action |
|---|---|---|
| Webmail via Enterprise Browser | `Block Webmail on EB` | **Block** |
| Risky/uncategorised sites | `[Threat] RBI`, `[RBI] Targeted …` | **Isolate (RBI)** |
| WhatsApp | `[RBI] Whatsapp Policy 2` | **Isolate** |
| Reverse-proxy download of confidential from SP/OneDrive | `Block External Party via Reverse Proxy …` | **Block** |

---

## Conflicts resolved

1. **Potentially Malicious Sites** — UKSE **Blocks**, JSIP **Coaches**. Demo shows *Block* with a note that it can be a coach page. ⚠
2. **SSH** — Cloud Firewall demo said *Block*; real policy **Allows** SSH. Corrected to Allow; real FW blocks are QUIC/DoT/TeamViewer/FTP-sig.
3. **Social / Streaming** — demo implied *Block*; no such rule exists → **Coach/Allow** (Time Wasting). Fixes the Reddit case.
4. **Personal cloud storage** — demo said *Coach*; real policy **Blocks** (UCI + non-corp + unsafe CCI).
5. **GenAI** — sanctioned tools are *Allowed + coached*, not blocked; only **sensitive-data uploads and unsanctioned tools Block**.

## Gaps — policy exists but no demo (candidate new demos)

- **MCP Server** DLP/guardrails (`Stan - MCP DLP Block`, `DLP control for MCP`, `Allow MCP Server Access`) — no demo today.
- **AI image / driver-licence DLP** (`AI Image Detection`, `[ML DLP] … image uploads to AI`).
- **Phishing via web forms** (`[Data Protection] Phishing via MS Forms / GForms Clone`).
- **Sensitivity-label / AIP enforcement** (`Alert on lack of classification`, `Block Download of TS labelled data`, Confidential-label block).
- **Add-header email DLP** (`[Email DLP] Outbound email PCI Policy` — SMTP header injection).
