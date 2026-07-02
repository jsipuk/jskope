# Jskope Demo Portal — Next Steps / Actions

> Working backlog for the next review pass. Nothing here is implemented yet —
> it captures the items raised for review so we can pick them up cleanly.
> Branch: `claude/jskope-netskope-demos-hb8btb`

**Status legend:** `[ ]` to do · `[~]` partially done · `[?]` needs your decision first

---

## 1. Categorise demos to match policy (not just capability)

Right now demos are grouped by Netskope **capability** (SWG, CASB, DLP, AI
Guardrails, NPA…). You want them to line up with how **policy** is actually
structured, so a viewer maps each demo to a policy they'd recognise.

- [?] **Decide the lens.** Two options (could do both):
  - **By policy action** — Block / Coach / Alert / Allow + Log / Justify / Quarantine.
  - **By policy type/engine** — Real-time Protection (inline), API Data Protection, Threat Protection, Web/SWG, Private Access (ZTNA).
- [ ] Add a secondary "policy" tag to each demo card on the hub (`temp/index.html`)
      and to each trigger inside the demo pages, alongside the existing capability badge.
- [ ] (Optional) Add a hub filter so you can show "all demos that exercise a
      **Block** policy" or "everything under **Real-time Protection**".

**Files:** `temp/index.html` (cards), every `temp/demos/*/index.html` (per-trigger tags).

---

## 2. Remove / soften fixed "expected outcome" language

Demos currently assert a single result (e.g. *"Expected: Block — SSN pattern
match"*). That's wrong for anyone whose policy differs — see the Reddit example
in item 3. Outcomes are **tenant-specific** and shouldn't be hard-asserted.

- [?] **Pick the approach:**
  - **(A) Soften everywhere (quick, safe).** Replace "Expected: Block" with
    neutral phrasing like *"Typical policy response: Block / Coach / Alert —
    depends on your tenant configuration."* The `web-blocking` page already does
    this in places (`TYPICAL: LOG / COACH`) — make it the consistent model.
  - **(B) Make it configurable (richer).** A small settings panel (like the
    industry picker) where you set your tenant's action per category, saved to
    `localStorage`, and the pages reflect it. Then "Social Networking → Coach"
    makes Reddit show *Coach*.
  - **Recommended:** ship (A) now as the baseline, add (B) later if you want
    per-tenant accuracy during POCs.
- [ ] Add a one-line disclaimer banner on demo pages: *"Outcomes shown are
      typical — your tenant's policy determines the actual result."*

**Files with hard-coded expectations to revisit** (count of assertions):
`ai-security` (18), `coaching` (4), `dns-security` (3), `web-blocking` (3),
`series/shadow-it-audit` (2), plus `series/ai-risk`, `series/insider-threat`,
`threat`, `ztna`, `cloud-firewall`.

---

## 3. Tenant-specific outcomes — the Reddit example

Concrete case: **Reddit is a _coach_ for you**, but the demo treats Social
Networking as block-leaning. This is the poster child for item 2.

- [ ] Ensure Reddit (`web-blocking/index.html:476`) and its category don't
      assert "Block".
- [ ] If we build the config panel (2B), seed it with sensible defaults and let
      you flip Social Networking → Coach so Reddit reflects your real policy.

**File:** `temp/demos/web-blocking/index.html`.

---

## 4. Update copy-prompt content (real source code, not AWS key dumps)

The AI Security "Source Code & Credentials" prompt was changed to a Python
snippet — but it **still embeds AWS keys**, and other pages have their own
source-code scenarios that may not have been converted.

- [~] `ai-security` general prompt → now Python, but contains AWS_*/GitHub/Stripe
      keys inside the code.
- [ ] **Audit every copy-prompt for the source-code scenario** and confirm each
      shows real code (Python / C++ / etc.), not a bare `KEY=value` list:
  - `temp/demos/series/ai-risk/index.html` — "Upload Synthetic Source Code to Copilot" step.
  - `temp/demos/ai-shadow-it/index.html` — prompt 3 (internal source with creds).
  - Any industry-specific variants in `ai-security` that mention code.
- [?] **Clarify what "still show AWS, not Python" means for you:**
  - (i) Other pages still show the old AWS-only list and need converting, **and/or**
  - (ii) You want the AWS keys *removed* from the Python in favour of pure code, **and/or**
  - (iii) You'd like a **C++** variant alongside the Python for variety.

**Files:** `temp/demos/ai-security/index.html`, `temp/demos/series/ai-risk/index.html`,
`temp/demos/ai-shadow-it/index.html`, `temp/assets/demo-data/billing-service-synthetic.py`.

---

## 5. Three usage modes — Presenter / Guided POC / Self-service

The portal should adapt to **who's driving**. Proposed: a "mode" selector on the
hub (sibling to the industry picker), saved to `localStorage`, that changes how
much guidance is shown.

- [?] **Confirm the three modes and what differs in each:**
  - **Presenter (you, SE-led).** Lean screen + optional talk-track / "say this,
    click that" cues. You narrate; the audience watches.
  - **Guided POC (with a customer).** Step-by-step checklist the customer follows
    alongside you, with progress tracking and success criteria. Reuse the
    existing **series progress-tracker** pattern.
  - **Self-service (prospect alone).** Maximum explanation: what each control
    does, what policy *should* fire, and **how to verify it in their own
    console** — safe to run unattended.
- [ ] Add the mode toggle to `temp/index.html` and a small `localStorage` key
      (e.g. `jskope-mode`), mirroring the industry picker.
- [ ] Define per-mode content blocks on demo pages (presenter notes, POC
      checklist, self-service explainers) shown/hidden by mode.
- [ ] For self-service: add "How to confirm this in the Netskope console" guidance
      (ties into the `[YOUR-TENANT]` console links).

**Files:** `temp/index.html` (toggle + state), all `temp/demos/*/index.html`
(per-mode content), `temp/demos/series/*` (POC checklists).

---

## Decisions I need from you (blockers for the above)

1. **Expectations (item 2):** soften everywhere, make per-tenant configurable, or both?
2. **Source-code prompts (item 4):** keep AWS-in-Python / strip AWS / add C++ — and which pages still need converting?
3. **Modes (item 5):** confirm the three modes and what content should differ per mode.
4. **Policy categorisation (item 1):** by action, by engine, or both — and do you want hub filtering?

---

## Carried-over follow-ups (from earlier passes)

- [ ] **`alert()` on two series pages** (`series/ai-risk`, `series/insider-threat`):
      the "Open Netskope Console" placeholder links still pop a native dialog.
      Convert to the inline-banner pattern used on ZTNA / Enterprise Browser for consistency.
- [ ] **`[YOUR-TENANT]` / `[YOUR-PRIVATE-APP-URL]` / `[YOUR-SHAREPOINT]` placeholders:**
      fill in before go-live, or wire them to the future config panel (2B).
- [ ] **`INDUSTRIES` object is duplicated** across the hub and several demo pages.
      Fine for a static site, but a shared `industries.js` would cut duplication if the portal grows.

---

## File map (quick reference)

| Area | Path |
|---|---|
| Hub / portal | `temp/index.html` |
| Capability demos | `temp/demos/{web-blocking,coaching,dlp,ai-security,ai-shadow-it,threat,shadow-it,ztna,dns-security,cloud-firewall,enterprise-browser}/index.html` |
| Guided series | `temp/demos/series/{insider-threat,ai-risk,shadow-it-audit}/index.html` |
| Synthetic demo data | `temp/assets/demo-data/` |
