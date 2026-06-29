# Jskope Demo Portal — Demo → Action → Policy Map

> Full inventory of every demo, what the user does, the use case, the outcome
> currently built into the site, and the **Netskope policy** that would produce
> that outcome. Built to support mapping/building real policy to match the portal.
>
> **Important:** the "Built-in expected outcome" column reflects what the site
> currently *states*. Actual results depend on your tenant policy — these are
> typical/representative, not guarantees (see "Tenant variance" at the end).

## Policy action legend

| Action | Meaning |
|---|---|
| **Block** | Transaction denied, Netskope block page shown |
| **Coach (User Alert)** | User warned, can proceed — optionally with justification capture |
| **Justification** | User must enter a business reason before proceeding (logged) |
| **Alert / Log** | Allowed, but an incident/log event is raised |
| **Allow + Inspect** | Allowed but passed to a deeper engine (SWG/DLP) for inspection |
| **Allow** | Permitted, normal logging |

## Netskope engine ↔ demo mapping (platform stack)

| Layer | Engine | Demos that exercise it |
|---|---|---|
| L3/L4 | Cloud Firewall (FWaaS) | Cloud Firewall |
| L7 DNS | DNS Security | DNS Security, (Cloud Firewall redirect) |
| L7 HTTP/S | SWG (Real-time Protection) | Web Blocking, User Coaching |
| L7 Content | DLP (inline) | Data Protection, (Series 01/03), AI demos |
| L7 App | CASB (inline + discovery) | Shadow IT, Shadow AI |
| L7 AI | AI Guardrails | AI Security, Shadow AI |
| Threat | Threat Protection | Threat Protection, DNS Security |
| Access | NPA (ZTNA) | Zero Trust Access |
| Browser | Enterprise Browser / RBI | Enterprise Browser |

---

## 1. Web Blocking — `demos/web-blocking/` · SWG (Real-time Protection)

**User action:** clicks a real site link; SWG evaluates URL category inline.

| Category (trigger) | Sites | Use case | Built-in expected | Recommended policy (engine · match · action) |
|---|---|---|---|---|
| Unsanctioned File Sharing | WeTransfer, Pastebin, SendGB, Filebin | Block exfil-prone file drops | **TYPICAL: BLOCK** | RTP · URL category = *File Storage/Sharing* (unsanctioned) · **Block** |
| Personal Cloud Storage | Dropbox, OneDrive, iCloud, MEGA (personal) | Stop personal sync of corp data | **TYPICAL: COACHING** | RTP · category = *Cloud Storage (consumer)* · **Coach** |
| Social Media | TikTok, Reddit, Discord, Twitch | Productivity / acceptable use | **TYPICAL: COACHING / BLOCK** | RTP · category = *Social Networking* · **Coach or Block (tenant choice)** |
| Streaming & Entertainment | Netflix, Spotify, Disney+, Prime | Bandwidth / acceptable use | **TYPICAL: LOG / COACH** | RTP · category = *Streaming Media* · **Alert/Log or Coach** |

> ⚠ **Reddit note:** Social Media is currently tagged "COACHING / BLOCK". For your
> tenant Reddit is a **Coach** — this category is the main place to soften/parameterise.

## 2. User Coaching — `demos/coaching/` · SWG with User Notification

**User action:** clicks a personal-use site; coaching notification (and optional justification) fires instead of a hard block.

| Category | Sites | Use case | Built-in expected | Recommended policy |
|---|---|---|---|---|
| Personal Cloud Storage | Dropbox, OneDrive, Google Drive, Box (personal) | Educate before data leaves | **COACHING + JUSTIFICATION** | RTP · category = consumer Cloud Storage · **User Alert + Justification** |
| Personal Email | Gmail, Outlook.com, ProtonMail, Yahoo | Prevent webmail exfil | **COACHING** | RTP · category = *Webmail (consumer)* · **Coach** |
| Social & Professional | LinkedIn, X, Facebook, Instagram | Acceptable-use nudge | **COACH / LOG** | RTP · category = *Social/Professional Networking* · **Coach or Log** |

## 3. Data Protection (DLP) — `demos/dlp/` · DLP inline (Real-time Protection)

**User action:** downloads a synthetic file, or copies a snippet and pastes/uploads into a target (Pastebin, Dropbox, Drive, GitHub, Outlook, WeTransfer).

| Trigger | Data type | Use case | Built-in expected | Recommended policy |
|---|---|---|---|---|
| `employee-records-synthetic.txt` | SSN / PII / financial | PII exfil on download | Block (PII match) | RTP · DLP profile *PII* · activity Download/Upload · **Block** |
| `payment-data-synthetic.csv` | PCI / card PANs | Cardholder data leak | Block (PCI match) | RTP · DLP profile *PCI-DSS* · **Block** |
| `billing-service-synthetic.py` | Source code + hardcoded secrets + internal hostnames | Secrets in code leaving | Block (source/creds match) | RTP · DLP profile *Source Code + Credentials* · **Block** |
| Paste: SSN / PII | PII | Inline paste into web form | Trigger inline | RTP · DLP *PII* · activity Upload/Post · **Block/Alert** |
| Paste: PCI / CARD | Card PAN | Card data into cloud app | Trigger inline | RTP · DLP *PCI-DSS* · **Block/Alert** |
| Paste: CREDENTIALS | API keys / tokens | Secrets into paste sites | Trigger inline | RTP · DLP *Credentials* · **Block** |
| Paste: PHI / HIPAA | NHS/PHI | Health data exfil | Trigger inline | RTP · DLP *PHI/HIPAA* · **Block** |
| Industry-specific files | Law/Finance/Insurance/Health/Defence variants | Vertical-tailored DLP | Block per profile | RTP · DLP industry profile · **Block** |

## 4. AI Security — `demos/ai-security/` · AI Guardrails (inline prompt inspection)

**Tools monitored:** ChatGPT (High), Copilot (High), Gemini (Med), Claude (Monitored).
**User action:** copies a scenario prompt, pastes into the AI tool; guardrails inspect the prompt content.

| Scenario (general) | Tool | Use case | Built-in expected | Recommended policy |
|---|---|---|---|---|
| PII Exfiltration via Prompt | ChatGPT | Staff records into AI | Block — SSN + PII | RTP/AI · GenAI app + DLP *PII* on prompt · **Block** |
| Source Code & Credentials | Copilot | Code w/ secrets into AI to debug | Block — code + creds + internal hostname | RTP/AI · GenAI app + DLP *Source Code/Credentials* · **Block** |
| Financial Data Disclosure | Gemini | Card data analysis in AI | Block — PCI PAN | RTP/AI · GenAI app + DLP *PCI* · **Block** |
| *Industry variants* (e.g. lawfirm: privileged memo, KYC pack) | various | Vertical AI risk | Block / Coach | RTP/AI · GenAI app + industry DLP profile · **Block/Coach** |

## 5. Shadow AI / AI Shadow IT — `demos/ai-shadow-it/` · CASB instance + AI Guardrails

**User action:** simulates running out of corporate AI tokens and switching to a **personal** AI account, pasting sensitive context.

| Scenario | Switch | Use case | Built-in expected | Recommended policy |
|---|---|---|---|---|
| Corporate Claude → personal claude.ai | token limit | Personal AI exfil | Block — PII/financial; personal instance flagged | CASB *app instance* (personal vs corp) + DLP on prompt · **Block** |
| Copilot → personal Gemini | budget cap | M&A confidential into AI | Block — multi-profile DLP | CASB instance + DLP *Confidential/Financial* · **Block (high sev)** |
| Unsanctioned Poe.com | no approved tool | Source code w/ creds into unapproved AI | Intercept — source/creds DLP | CASB *unsanctioned app* + DLP *Source/Credentials* · **Block/Alert** |

## 6. Threat Protection — `demos/threat/` · Threat Protection (inline AV/sandbox + URL)

**User action:** downloads industry-standard test artefacts / visits safe test URLs.

| Trigger | Type | Use case | Built-in expected | Recommended policy |
|---|---|---|---|---|
| EICAR (txt / zip / double-zip) | Benign AV test string | Malware download block | Block (signature) | Threat Protection · malware scan · **Block** |
| Phishing & Malicious URL (AMTSO, Wicar) | Safe test pages | Phishing/exploit block | Block | Threat Protection / SWG · threat category · **Block** |
| C2 / Botnet (testmyids) | Threat-intel test | C2 callback detection | Block | Threat Protection · threat intel · **Block** |

## 7. Shadow IT Discovery — `demos/shadow-it/` · CASB (discovery + CCI)

**User action:** visits unsanctioned apps; CASB classifies + risk-scores via Cloud Confidence Index.
**CCI bands:** 76–100 Trusted · 51–75 General · 26–50 Low · 0–25 Poor. (Typical auto-policy: block <60, coach 60–75, allow >75.)

| App | CCI | Category | Recommended policy |
|---|---|---|---|
| WeTransfer | 42 | File sharing | CASB · CCI<60 · **Block** |
| MEGA | 22 | Cloud storage | CASB · CCI<25 (Poor) · **Block** |
| Filebin | 33 | Temp file storage | CASB · CCI<60 · **Block** |
| Pastebin | 38 | Text/exfil | CASB · CCI<60 · **Block** |
| AnonFiles | 18 | Anonymous hosting | CASB · CCI<25 · **Block** |
| Dropbox (personal) | 69 | Cloud storage | CASB · CCI 60–75 · **Coach** |
| OneDrive personal | 65 | Cloud storage | CASB · CCI 60–75 · **Coach** |
| SharePoint/OneDrive Corp | 89 | Enterprise storage | CASB · CCI>75 · **Allow** |

## 8. Zero Trust Access — `demos/ztna/` · NPA (ZTNA)

**User action:** attempts to reach a private app (`[YOUR-PRIVATE-APP-URL]`) — unreachable until an NPA policy grants identity-aware access.

| Trigger | Use case | Built-in expected | Recommended policy |
|---|---|---|---|
| Live access test | VPN-less least-privilege access | Unreachable by design until policy grants | NPA · private app def + access policy (user/group, device posture) · **Allow to authorised identities only** |

> ⚠ Needs `[YOUR-PRIVATE-APP-URL]` + tenant config before this is live.

## 9. DNS Security — `demos/dns-security/` · DNS Security

**User action:** resolves/visits malicious test domains; blocked at DNS layer before TCP.

| Trigger | Use case | Built-in expected | Recommended policy |
|---|---|---|---|
| AMTSO malware, testmyids, Wicar | Pre-connection threat block | Block (sinkhole) | DNS Security · malicious/C2 categories · **Block/Sinkhole** |
| AMTSO phishing | Layered DNS+SWG | DNS blocks lookup; SWG backs up | DNS Security · phishing category · **Block** |

## 10. Cloud Firewall — `demos/cloud-firewall/` · FWaaS (L3/L4)

**User action:** (network-level) non-web protocols evaluated by FWaaS rules.

| Service | Port | Built-in action | Recommended policy |
|---|---|---|---|
| Telnet | TCP 23 | BLOCK | FW · port/proto · **Block** (cleartext legacy) |
| IRC / Chat C2 | TCP 6667/6697 | BLOCK | FW · **Block** (C2 channel) |
| Tor entry nodes | TCP 9001/9030 | BLOCK | FW · **Block** (anonymiser/exfil) |
| SSH (external) | TCP 22 | BLOCK | FW · **Block** (unless justified) |
| RDP (external) | TCP 3389 | BLOCK | FW · **Block** (lateral movement) |
| HTTPS | TCP 443 | ALLOW + INSPECT | FW · **Allow → SWG inspection** |
| SMTP (external) | TCP 25 | BLOCK | FW · **Block** (bypasses email GW) |
| DNS | UDP 53 | LOG + REDIRECT | FW · **Redirect → DNS Security** |

## 11. Enterprise Browser — `demos/enterprise-browser/` · Enterprise Browser / RBI

**User action:** demonstrates browser-level controls (needs `[YOUR-SHAREPOINT]`).

| Control | Use case | Recommended policy |
|---|---|---|
| Contractor clipboard restriction | Block copy/paste out of app | EB · clipboard policy · **Block copy/paste** |
| Sensitive file download block | Prevent local download | EB · download policy · **Block download** |
| Screen watermarking | Deter screenshots/leaks | EB · watermark policy · **On** |
| Remote Browser Isolation (RBI) | Render risky sites remotely | RBI policy · risky categories · **Isolate** |

## 12. Demo Series (composite journeys)

| Series | Steps → outcome | Policies exercised |
|---|---|---|
| **01 Insider Threat** | Personal cloud (coach/block) → upload PII (DLP block) → email external (DLP block) → audit log | SWG category + DLP PII + audit |
| **02 AI Risk** | PII into ChatGPT (block) → source code to Copilot (block) → console review | AI Guardrails + DLP PII/Source |
| **03 Shadow IT Audit** | Visit unsanctioned (CASB) → download sensitive (DLP) → re-upload personal Dropbox (DLP block) | CASB CCI + DLP |

---

## Consolidated Policy Build Inventory

The unique set of policies that, if built, make the whole portal behave as documented:

**Real-time Protection (inline SWG/DLP/AI):**
1. Web — Unsanctioned File Sharing category → **Block**
2. Web — Personal Cloud Storage (consumer) → **Coach + Justification**
3. Web — Social / Streaming → **Coach / Log** *(tenant-specific; Reddit = Coach for you)*
4. Webmail (consumer) → **Coach**
5. DLP — PII/SSN profile → **Block**
6. DLP — PCI-DSS profile → **Block**
7. DLP — PHI/HIPAA profile → **Block**
8. DLP — Source Code + Credentials profile → **Block**
9. GenAI apps + DLP on prompt content → **Block/Coach** (AI Guardrails)

**CASB:**
10. CCI auto-policy: block <60 · coach 60–75 · allow >75
11. App instance: personal vs corporate AI/cloud instance → **Block sensitive on personal**
12. Unsanctioned app access → **Alert/Block**

**Threat Protection:** 13. Malware (AV/sandbox) → **Block** · 14. C2/threat-intel → **Block**

**DNS Security:** 15. Malicious/phishing/C2 domains → **Block/Sinkhole**

**Cloud Firewall:** 16. Protocol ruleset (Telnet/IRC/Tor/SSH/RDP/SMTP **Block**; 443 **Allow+Inspect**; 53 **Redirect**)

**NPA (ZTNA):** 17. Private app + identity-aware access policy

**Enterprise Browser:** 18. Clipboard / download / watermark / RBI controls

---

## Tenant variance (why outcomes shouldn't be hard-asserted)

The same trigger can legitimately resolve to Block, Coach, or Log depending on a
tenant's risk appetite, user group, device posture, and data sensitivity. Examples:
- **Reddit** — Block for one org, **Coach** for you, Allow for another.
- **Personal Dropbox** — Coach (CCI 69) by default, but Block if a stricter
  data-classification policy applies.
- **GenAI** — Block on sensitive prompts, but Allow+Log for sanctioned corporate instances.

**Recommendation:** treat the "Built-in expected outcome" as *representative*, and
either (a) soften the on-page language to "typical", or (b) make outcomes
configurable per tenant (see `NEXT-STEPS.md` item 2). This map is structured so a
real policy set can be built 1:1 against the "Recommended policy" column.
