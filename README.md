# Performance NgeGAS — Autonomous Landing Page & CRO Pipeline

> **Turn product briefs into live, conversion-ready landing pages in hours instead of weeks.**
> 9-step research-to-execution pipeline built for Hermes Agent, driven by structured AI agents, JSON artifacts, and zero hand-waving.

---

## 1. Philosophy (Why This Exists)

**Problem:** Agencies charge retainers and still take 4–6 weeks to deliver a single landing page. Solo founders burn cash on ads that send traffic to a page that "feels right" but was never validated against real buyer psychology.

**Solution:** A fully autonomous, agent-driven pipeline that compresses research, positioning, CRO strategy, and landing page build into a single coherent workflow. Every step is artifact-first (JSON schema), every output is traceable, and every decision is grounded in the same customer data.

**Core principles:**
- **Outcome over output** — we don't deliver "a landing page." We deliver *conversion probability*.
- **Artifact-first** — every step produces a machine-readable JSON artifact with strict schema. The next step reads it, not the human.
- **Role-based** — we don't target "segments." We target *decision-making humans in specific life roles*.
- **No hand-waving** — every insight must be traceable to prior steps. If it's not in the artifact, it doesn't exist.

---

## 2. Who Is This For (And Who Should Skip)

**This is for you if:**
- You are a solo founder, indie hacker, or small team with no budget for a $5k+/month agency retainer.
- You run paid ads and need a landing page that actually matches the buyer psychology behind the click.
- You have a product brief but no idea how to turn it into messaging, positioning, and a live page.
- You want multiple CRO plans and A/B variants, not just one "good enough" page.
- You care about traceability — every headline must be justified by research, not vibes.

**This is NOT for you if:**
- You want a bespoke 3D animated site with custom WebGL shaders. This pipeline outputs clean, fast, conversion-focused static HTML.
- You need a full e-commerce checkout with payment gateway integration. The output is a landing page (lead capture / sales page), not a store.
- You expect "set it and forget it" without reviewing the output. The pipeline auto-runs, but you still need to read the CRO plan and QA report before shipping.
- You are looking for a no-code drag-and-drop builder. This is an agent-driven pipeline for people who want to deploy raw HTML.

---

## 3. Technical Stack

| Layer | Technology | Why |
|-------|------------|-----|
| Orchestration | Hermes Agent + `pipeline.yaml` | Native agent dispatch, retry logic, and artifact routing |
| Agent definitions | YAML with `system_prompt`, `input_artifacts`, `output_artifact` | Explicit contracts, no prompt drift |
| Data format | JSON artifacts + JSON Schema Draft-07 | Machine-readable, validated, versioned |
| Styling | Tailwind CSS via CDN | Zero build step, fast, mobile-first |
| Typography | Google Fonts (Inter default) | Clean, readable, web-optimized |
| Output | Static HTML5 (no JS) | Fastest possible load, no framework bloat, no security surface |
| QA | Red-team audit + schema validation | Automated safety before human review |
| Version control | Git + `metadata.brief_hash` | Every artifact is traceable to its input brief |

---

## 4. Pipeline Overview (The 9 Steps)

| Step | Agent | What It Does | Output Artifact |
|------|-------|--------------|-----------------|
| 01 | `agent-01` | Target Market Analysis | `01-market/target-market-analysis.json` |
| 02 | `agent-02` | JTBD Deep Analysis (Christensen-Moesta) | `02-jtbd/jtbd-analysis.json` |
| 03 | `agent-03` | JTBD Deep Analysis v2 (Deep Job Map) | `03-jtbd-v2/jtbd-v2-analysis.json` |
| 04 | `agent-04` | Life Role Profile | `04-role/role-profile.json` |
| 05 | `agent-05` | Customer Motivation Database | `05-motivation/customer-motivation-database.json` |
| 06 | `agent-06a/b/c` | Strategic Opportunity & Positioning | `06-opportunity/strategic-analysis.json` |
| 07 | `agent-07` | CRO Plan Generator | `07-cro/cro-plan.json` + `07-cro/plans/plan-*.json` |
| 08 | `agent-08` | Landing Page Builder | `08-lp/primary/` + `08-lp/challenger/` |
| 09 | `agent-09` | QA & Red Team Audit | `09-qa/qa-report.json` |

**Orchestrator:** `pipeline.yaml` (YAML definition) + `scripts/run.py` (execution entry point).

---

## 3. Step-by-Step Technical Detail & Scope

### Step 01 — Target Market Analysis
**Scope:** Given a product brief (text/markdown), produce a rigorous market map with at least 5 segments, 1 Ideal Customer Profile (ICP), 20 pain points, 20 desires, 20 fears, 20 objections, 20 daily-language phrases, and an awareness-level breakdown.

**Technical detail:**
- Input: raw product brief (any text up to ~10k chars).
- Output: strict `schema-01.json` (JSON Schema Draft-07). Minimum arrays enforced (`minItems: 20`).
- Scoring: each segment gets a `score` (1–10), priority ranking computed.

**Promised outcome:** You will know *exactly* who to sell to, what they call their pain, and why they haven't bought yet. No persona guessing.

---

### Step 02 — JTBD Deep Analysis (Christensen-Moesta)
**Scope:** Consume Step 01 artifact and map the Jobs To Be Done using the Christensen-Moesta framework. Identify functional, emotional, and social jobs. Build job stories, progress maps, hiring criteria, and switching forces.

**Technical detail:**
- Input: `01-market/target-market-analysis.json`.
- Output: `schema-02.json` with `job_list`, `job_stories`, `progress_map`, `job_drivers`, `job_blockers`, `hiring_criteria`.
- Confidence scoring per field.

**Promised outcome:** You will understand *why* the ICP hires a product — not what they *say* they want, but what progress they are actually trying to make.

---

### Step 03 — JTBD Deep Analysis v2 (Deep Job Map)
**Scope:** Cross-reference Step 02 output and produce a deeper job map: actual vs. aspirational job, job-map stages, emotional journey, situational triggers, alternative solutions, and switching barriers.

**Technical detail:**
- Input: `01-market` + `02-jtbd` artifacts.
- Output: `schema-03.json` with `deep_job_maps`, `cross_reference_v1` (consistencies/inconsistencies/reconciliations), `trigger_words`, `switching_barriers`.
- If inconsistencies found, the agent must reconcile them and flag assumptions.

**Promised outcome:** A clean, validated job map with no contradictions — and a list of trigger words you can use in ads and headlines.

---

### Step 04 — Life Role Profile
**Scope:** Shift from demographics to *life roles*. Map the buyer's roles (e.g., "stressed parent," "ambitious founder," "skeptical spouse") and identify which role dominates the purchase decision.

**Technical detail:**
- Input: `01-market`, `03-jtbd-v2` artifacts.
- Output: `schema-04.json` with `life_roles`, `actual_vs_aspirational`, `dominant_role`, `persona_variants`.
- Minimum 5 life roles, minimum 3 actual-vs-aspirational gaps.

**Promised outcome:** You will know *which role* is the real buyer — so your messaging speaks to the person writing the check, not a generic demographic.

---

### Step 05 — Customer Motivation Database
**Scope:** Extract every root pain, surface pain, fear, desire, frustration, objection, and behavioral trigger into a structured, scored database. Every item must be traceable to prior steps (not invented).

**Technical detail:**
- Input: all prior artifacts (`01`–`04`).
- Output: `schema-05.json` with `pain_points`, `desires`, `fears`, `frustrations`, `behavioral_triggers`, each scored with `severity`, `frequency`, `surface_or_deep`, `confidence_score`, `evidence_type`.
- If evidence is weak, marked as `Assumption`.

**Promised outcome:** A reusable database you can plug into landing pages, ads, sales scripts, and product strategy — without starting from scratch every time.

---

### Step 06 — Strategic Opportunity & Positioning
**Scope:** Synthesize everything into competitive positioning, opportunity sizing, and strategic recommendations. Don't repeat prior data — produce *new* insights from synthesis.

**Technical detail:**
- Input: `01`–`05` artifacts.
- Output: `schema-06.json` with `competitive_analysis`, `opportunity_sizing`, `strategic_positioning`, `priority_recommendations`.
- Opportunity scoring formula: `(Importance × Urgency × Frequency × Market Gap)` on 1–10 scale.
- Competitive SWOT per competitor (minimum 5).

**Promised outcome:** A clear, defensible positioning and a ranked list of which opportunities to attack first — based on market gaps, not gut feeling.

---

### Step 07 — CRO Plan Generator
**Scope:** Convert customer research into a concrete Conversion Rate Optimization plan with multiple variants (Primary / Challenger / Archive). Each plan includes section order, messaging hierarchy, conversion psychology, and A/B test hypotheses.

**Technical detail:**
- Input: `01`–`06` artifacts.
- Output: `schema-07.json` with `plans` (array, each scored), `sections`, `ab_tests`.
- Variant types: `primary` (execute now), `challenger` (test against), `archive` (keep permanently, manual activation).
- Each plan scored on `conversion_probability`, `implementation_ease`, `strategic_fit`.
- Plan acts as the **single source of truth** for Step 08.

**Promised outcome:** A validated CRO plan that tells the builder exactly what sections to build, in what order, and why — so no one is guessing in the build phase.

---

### Step 08 — Landing Page Builder
**Scope:** Build the actual landing page. No invention. No extra sections. The builder reads the CRO plan and executes it faithfully into HTML, CSS, and assets.

**Technical detail:**
- Input: `07-cro/cro-plan.json` + selected plan (`plan-01.json`).
- Output: `schema-08.json` with `variants` (max 2: Primary + Challenger). Each variant is a folder:
  - `index.html` (shell, loads sections in exact order)
  - `section/` (one `.html` per section from `recommended_section_order`)
  - `img/` (image assets)
  - `style.css` (shared styles, optional)
- Constraints: **No JavaScript.** No `js/` folder. No frameworks. Tailwind CSS via CDN. Mobile-responsive (min 320px). Google Fonts (Inter default).
- Progressive disclosure enforced: Hook → Desire → Trust → Objection → CTA.
- Scroll retention: sticky CTA after hero, visual rhythm, open loops.
- Persuasion completeness mapping: every CRO plan field has a visual execution rule.

**Promised outcome:** Two live, responsive, persuasion-engineered landing page variants ready to deploy. Not a template. Not a wireframe. A finished page.

---

### Step 09 — QA & Red Team Audit
**Scope:** Validate every step against its schema, its upstream data, and a red-team checklist (fake scarcity detection, missing BPOM/disclaimer, schema compliance, confidence thresholds).

**Technical detail:**
- Input: all artifacts `00`–`08`.
- Output: `schema-09.json` with `step_audits` (min 8 steps), `overall_status`, `fix_recommendations`, `red_team_findings`.
- Each step audited: `schema_compliant`, `confidence_pass`, `completeness`, `issues`, `red_team_findings`.
- Overall status: `PASS`, `NEEDS_FIX`, or `FAIL`.
- Lite mode (`agent-09-lite`): reads pre-compressed `audit-input.json` (~5 KB) instead of full 118 KB artifacts, for batch runs.
- If `FAIL`, pipeline halts. If `NEEDS_FIX`, fixes are applied and re-audited (max 2 loops).

**Promised outcome:** You ship with confidence. No fake scarcity. No missing disclaimers. No broken schema. No hand-waving.

---

## 6. Architecture & Orchestration

```
┌─────────────────────────────────────────────────────┐
│  Brief (Text/Markdown)                              │
└────────────┬────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────┐
│  Pipeline Orchestrator (pipeline.yaml)              │
│  - Max 2 retry loops per step                        │
│  - Auto-jalan checkpoint (auto-proceed)             │
│  - Artifact validation after every step             │
└────────────┬────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────┐
│  Step 01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09 │
│  Each step: Agent reads prior JSON, writes new JSON │
│  No human-in-the-loop between steps (auto mode)     │
└────────────┬────────────────────────────────────────┘
             │
┌────────────▼────────────────────────────────────────┐
│  Final deliverables:                                │
│  - 09-qa/qa-report.json (PASS / FAIL)               │
│  - 08-lp/primary/ (live HTML)                       │
│  - 08-lp/challenger/ (live HTML)                    │
│  - 07-cro/plans/ (archive plans for future use)     │
└─────────────────────────────────────────────────────┘
```

---

## 7. JSON Artifact-First Design

Every step produces a JSON artifact validated against a strict JSON Schema (Draft-07). This is not documentation — it is the *contract* between agents.

- `schemas/schema-01.json` through `schema-09.json` define the exact shape, required fields, and min/max constraints.
- `schemas/schema-09-lite.json` defines the lightweight QA contract for batch mode.
- If an agent output fails schema validation, the orchestrator retries the step (max 2 times).
- If it still fails, the pipeline halts and logs the error.

**Why this matters:** Agents don't read paragraphs. They read structured data. The pipeline is deterministic because every step's input is the previous step's output.

---

## 8. Folder Structure

```
performance-ngegas/
├── agents/                # Agent definitions (YAML: name, role, system_prompt, inputs, outputs)
│   ├── agent-01.yml       # Target Market Analyst
│   ├── agent-02.yml       # JTBD Researcher
│   ├── agent-03.yml       # JTBD Deep Map v2
│   ├── agent-04.yml       # Role Profiler
│   ├── agent-05.yml       # Motivation Database Builder
│   ├── agent-06a.yml      # Opportunity Analyst (Variant A)
│   ├── agent-06b.yml      # Opportunity Analyst (Variant B)
│   ├── agent-06c.yml      # Opportunity Analyst (Variant C — Principal)
│   ├── agent-07.yml       # CRO Strategist
│   ├── agent-08.yml       # LP Builder
│   ├── agent-09.yml       # QA & Red Team Auditor
│   └── agent-09-lite.yml  # QA Lite (Batch Mode)
├── prompts/               # Full prompts for each step (Markdown)
│   ├── 01-target-market-analysis.md
│   ├── 02-jtbd-deep-analysis.md
│   ├── 03-jtbd-deep-analysis-v2.md
│   ├── 04-role-profile.md
│   ├── 05-customer-motivation-database.md
│   ├── 06-strategic-opportunity.md
│   ├── 07-cro-plan.md
│   └── 08-landing-page-builder.md
├── schemas/               # JSON Schema contracts (Draft-07)
│   ├── schema-01.json     # Target Market Analysis
│   ├── schema-02.json     # JTBD Analysis
│   ├── schema-03.json     # JTBD v2
│   ├── schema-04.json     # Role Profile
│   ├── schema-05.json     # Customer Motivation Database
│   ├── schema-06.json     # Strategic Opportunity
│   ├── schema-07.json     # CRO Plan
│   ├── schema-08.json     # Landing Page Implementation
│   ├── schema-08-qa.json  # QA metadata for LP
│   ├── schema-09.json     # QA Final Report
│   └── schema-09-lite.json# QA Lite Report
├── references/            # Methodology docs, run patterns, troubleshooting
│   ├── methodology.md
│   ├── pipeline-orchestration.md
│   ├── run-patterns.md
│   ├── brief-validator.md
│   ├── landing-page-constraints.md
│   ├── qa-step-09-optimization.md
│   └── ...
├── scripts/               # Execution helpers
│   ├── run.py             # Main entry point
│   ├── cro-plan-health-check.py
│   ├── generate-audit-input.py
│   └── qa-script.py
├── .planning/             # Project planning & requirements
│   ├── PROJECT.md
│   ├── REQUIREMENTS.md
│   └── ROADMAP.md
├── pipeline.yaml          # Pipeline orchestration config
└── SKILL.md               # Hermes Agent skill manifest
```

---

## 9. Quick Start Example

**Typical run from a founder's brief:**

```
User: "I sell a cold-pressed juice subscription for busy professionals in Jakarta.
Target: 25-40, health-conscious, time-poor, skeptical of 'detox' claims.
Constraint: Must comply with BPOM labeling. No fake scarcity."

Hermes: skill: performance-ngegas

Pipeline:
01 → 02 → 03 → 04 → 05 → 06 → 07 → 08 → 09

Deliverables:
- 08-lp/primary/index.html      (Hero: "Capek Terus? Bukan Kurang Tidur")
- 08-lp/challenger/index.html   (Hero: "3 Hari Tanpa Kafein = Lebih Fokus")
- 07-cro/plans/plan-archive.json (for future Ramadan campaign)
- 09-qa/qa-report.json          (PASS, 0 red-team findings)
```

**Step-by-step:**

1. **Load the skill:**
   ```
   skill: performance-ngegas
   ```

2. **Provide a brief:**
   Paste your product/service brief as text. Include:
   - Product description
   - Target audience hint (even if rough)
   - Any constraints (regulatory, brand, technical)

3. **Run:**
   The orchestrator (`pipeline.yaml`) dispatches agents sequentially. Each agent reads the prior JSON artifact and writes the next one.

4. **Review the CRO plan:**
   Before the build starts, read `07-cro/plans/plan-01.json`. If the messaging feels off, you can adjust the brief and re-run. The pipeline is fast enough to iterate.

5. **Receive deliverables:**
   - `08-lp/primary/index.html` — your live landing page
   - `08-lp/challenger/index.html` — A/B challenger variant
   - `07-cro/plans/` — archived CRO plans for future campaigns
   - `09-qa/qa-report.json` — audit report with confidence scores

6. **Deploy:**
   The HTML is static, framework-free, and CDN-ready. Upload to any hosting (Caddy, Vercel, Netlify, S3, or your VPS).

---

## 10. QA & Safety

- **Schema validation:** Every artifact is validated against its JSON Schema before the next step begins.
- **Confidence scoring:** Every agent assigns confidence scores. If any step drops below threshold, the orchestrator flags it.
- **Red team audit:** Step 09 checks for fake scarcity (Math.random, countdown scripts, fake stock), missing regulatory disclaimers (BPOM, etc.), and schema compliance.
- **Max retries:** 2 loops per step. If still failing, pipeline halts — no broken output ships.
- **No JS bloat:** Step 08 produces static HTML. No frameworks, no tracking scripts, no unnecessary JS.
- **Audit trail:** Every artifact includes `metadata` with `timestamp`, `agent`, `brief_hash`, and `pipeline_version`.

---

## 11. Outcomes You Get (Not Features)

| Instead of... | You get... |
|---------------|------------|
| A "nice-looking" landing page | A persuasion-engineered page with proven section order and messaging hierarchy |
| Copy based on guesswork | Copy derived from real buyer pain, fear, desire, and daily language |
| One-size-fits-all strategy | Multiple scored CRO plans (Primary + Challenger + Archive) |
| Weeks of back-and-forth | A complete pipeline from brief to live page in hours |
| Unvalidated assumptions | Every insight scored, sourced, and traceable to prior research |
| Fake scarcity / compliance risk | Red-team audit catches it before you ship |

---

## 12. Anti-Patterns & What This Pipeline Won't Do

To set honest expectations, here is what the pipeline explicitly does **not** do:

| Anti-Pattern | Why It's Excluded |
|--------------|-------------------|
| **Inventing data** | Every insight must be traceable to a prior artifact. If the research is thin, the output is flagged as `Assumption` — not fact. |
| **One-size-fits-all copy** | The pipeline builds variants based on the CRO plan. If the plan says two audiences need different hooks, you get two pages. |
| **Fake urgency / dark patterns** | Red-team audit (Step 09) scans for `Math.random`, fake countdowns, and fabricated stock numbers. If found, the pipeline fails. |
| **Custom backend logic** | The output is static HTML. No payment processing, no user auth, no database. Integrate with your own backend or use a form handler. |
| **SEO blog content** | This is a landing page pipeline, not a content marketing engine. The focus is conversion, not organic search volume. |
| **Infinite revision loops** | Max 2 retries per step. If it still fails, the pipeline halts. We ship when it's good, not when it's perfect. |

---

## 13. Roadmap & Context

- Full project planning, requirements, and roadmap live in `.planning/`.
- See `.planning/PROJECT.md` for the origin story and design decisions.
- See `.planning/REQUIREMENTS.md` for functional and non-functional requirements.
- See `.planning/ROADMAP.md` for future phases and milestones.

---

## 14. License & Disclaimer

- **No proprietary credentials, API keys, or tokens are included in this repository.** This is a methodology and agent-definition repo. You run it with your own LLM API keys and hosting infrastructure.
- **No medical, financial, or legal claims.** The pipeline produces marketing assets. You are responsible for ensuring compliance with local regulations (BPOM, FDA, advertising standards, etc.) before publishing.
- **Performance is not guaranteed.** "Conversion-ready" means "built on validated research principles." Actual conversion rates depend on traffic quality, offer strength, market fit, and external factors beyond the pipeline's scope.

---

**Built for solo founders and small teams who want agency-grade results without the agency timeline.**
