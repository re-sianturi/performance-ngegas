# CRO Plan Health Check — Pre-Flight & Post-Run Verification

## Why this exists

During the 11 Juni 2026 patch session (multi-file LP schema v1.0.4), a comprehensive health check of all 7 production runs revealed that **zero runs** had `recommended_section_order` in their `07-cro/cro-plan.json` — the field that schema-08 and prompt-08 treat as mandatory for LP section blueprint. This was a schema-07 gap: prompt-07 mentions the field but schema-07 does not enforce it, and the agent consistently omits it.

This reference documents the verification script, the expected artifact structure, and the pre-flight checklist that must pass before dispatching Step 08.

---

## Quick Health Check Script

Run this Python script against any run folder to verify artifact completeness:

```python
import os, json

base = "/home/ubuntu/.hermes/runs/performance-ngegas"
run = "2026-06-10_163245_alpha-propolis"  # change me

required = {
    "01": "01-analysis/target-market.json",
    "02": "02-jtbd-v1/jtbd-analysis.json",
    "03": "03-jtbd-v2/jtbd-v2-analysis.json",
    "04": "04-role-profile/life-role-profile.json",
    "05": "05-motivation/customer-motivation.json",
    "06": "06-strategy/strategic-positioning.json",
    "07": "07-cro/cro-plan.json",
}

run_dir = os.path.join(base, run)
step_ok = 0
for step, rel in required.items():
    path = os.path.join(run_dir, rel)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        try:
            with open(path) as f: json.load(f)
            print(f"  {step}: OK")
            step_ok += 1
        except:
            print(f"  {step}: INVALID JSON")
    else:
        print(f"  {step}: MISSING")

# CRO Plan specific check
cro_path = os.path.join(run_dir, "07-cro/cro-plan.json")
with open(cro_path) as f:
    cro = json.load(f)
has_rso = "recommended_section_order" in cro
has_layout = "layout" in cro
has_messaging = "messaging_hierarchy" in cro
print(f"  CRO Plan has rso={has_rso} layout={has_layout} messaging={has_messaging}")

# LP structure check
lp_dir = os.path.join(run_dir, "08-lp")
files = os.listdir(lp_dir) if os.path.exists(lp_dir) else []
has_index = any("index.html" in f for f in files)
has_section = any(os.path.isdir(os.path.join(lp_dir, f)) and f == "section" for f in files)
print(f"  LP structure: index={has_index} section_dir={has_section}")
print(f"  RISART: {'PASS' if step_ok == 7 else 'FAIL'} ({step_ok}/7)")
```

---

## Expected Artifact Structure Per Step

| Step | File | Min Size | Key Fields |
|------|------|----------|------------|
| 01 | `01-analysis/target-market.json` | 2 KB | segments, icp, psychographic |
| 02 | `02-jtbd-v1/jtbd-analysis.json` | 2 KB | core_job, forces_of_progress, desired_outcomes |
| 03 | `03-jtbd-v2/jtbd-v2-analysis.json` | 2 KB | job_map, switching_barriers, cross_reference_v1 |
| 04 | `04-role-profile/life-role-profile.json` | 2 KB | dominant_role, role_variants, life_context |
| 05 | `05-motivation/customer-motivation.json` | 2 KB | pain_points, fears, desires, frustrations, behavioral_triggers |
| 06 | `06-strategy/strategic-positioning.json` | 2 KB | positioning, competitive_gaps, opportunity_size |
| 07 | `07-cro/cro-plan.json` | 5 KB | **recommended_section_order**, messaging_hierarchy, conversion_strategy, landing_page_recommendation |

---

## CRO Plan Depth Inconsistency

**Finding from 7-run audit:**

- **Main run** (Alpha Propolis): ~28 KB cro-plan.json, 7-8 KB per plan file, rich `cro_specialist`, `ux_designer`, `funnel_optimization`
- **Segment runs** (01-06): ~0.4-1.4 KB cro-plan.json, 630-900 bytes per plan file, shallow structure (headline, subheadline, CTA, layout string only)

**Impact:** Segment run CRO Plans are too shallow to drive a persuasive multi-file LP. Step 08 agent will have no `conversion_psychology`, `messaging_hierarchy`, or `funnel_optimization` to implement. The result will be a generic LP regardless of how good schema-08 is.

**Recommendation:** For segment runs, either (a) run Step 07 with the same depth as main runs, or (b) accept that segment LP quality will be lower unless enriched.

---

## Pre-Flight Checklist Before Dispatching Step 08

**MUST pass before agent-08 is dispatched:**

1. `07-cro/cro-plan.json` exists and is valid JSON
2. `07-cro/cro-plan.json` contains `recommended_section_order` (array of section name strings)
3. `07-cro/cro-plan.json` contains `messaging_hierarchy` (object with primary_message, secondary_messages, emotional_messages, proof_messages, conversion_messages)
4. `07-cro/cro-plan.json` contains `conversion_strategy` (object with core_promise, unique_mechanism, trust_strategy, proof_strategy, risk_reduction_strategy, offer_strategy, cta_strategy)
5. `07-cro/cro-plan.json` contains `landing_page_recommendation` (object with hero_strategy, mechanism_strategy, objection_strategy, proof_placement_strategy, cta_placement_strategy)
6. `07-cro/plans/plan-01.json` exists and has `headline`, `subheadline`, `cta`
7. `07-cro/plans/plan-02.json` exists (for challenger variant)
8. `06-strategy/strategic-positioning.json` exists and valid
9. `05-motivation/customer-motivation.json` exists and valid

**If any check fails:** Do NOT dispatch Step 08. The agent will improvise and produce a generic single-file LP. Go back to Step 07 and fix the CRO Plan first.

---

## Schema-07 Gap

**Root cause:** schema-07.json does not list `recommended_section_order` in its `required` array. The prompt-07 mentions it under `landing_page_recommendation.recommended_section_order`, but without schema enforcement, the agent omits it. schema-08 and prompt-08 then fail because they expect the field.

**Fix needed:** Update schema-07.json to add `recommended_section_order` as a required top-level field (or under `landing_page_recommendation`). Until fixed, use the pre-flight checklist above as a manual gate.
