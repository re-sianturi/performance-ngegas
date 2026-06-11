# Batch Rebuild Workflow — Step 07 + Step 08

Use this when you need to rebuild CRO Plans and Landing Pages across **multiple existing runs** (e.g., after a schema/prompt update that affects all historical runs).

## Pre-Flight Checklist

1. **Verify actual run directories** — `ls ~/.hermes/runs/performance-ngegas/`
   - Do NOT trust run names from memory. Timestamps vary.
   - Example: `segment-06-pasca-operasi` had both `2026-06-11_013148` and `2026-06-11_020600`.

2. **Check 07-cro depth** — `stat` cro-plan.json size. < 5 KB = shallow, needs rebuild.
3. **Check for recommended_section_order** — grep this field. If missing, step 08 will output single-file LPs.
4. **Check 08-lp exists** — if yes, backup to `08-lp-legacy/` before overwrite: `mv 08-lp 08-lp-legacy`

## Batch Dispatch Strategy

For 7 runs: **3 + 3 + 1 batches** (prevent context overflow).

Each `delegate_task` call handles ONE run per task. Use 3 tasks per batch.

## Step 07 Rebuild — Per Run Agent Task

Agent reads:
- `00-input/brief.json`
- `05-motivation/customer-motivation.json`
- `06-strategy/strategic-positioning.json`
- Existing `07-cro/cro-plan.json` (if any)
- `prompts/07-cro-plan.md` + `schemas/schema-07.json`

Agent writes:
- `07-cro/cro-plan.json` — enriched with ALL fields: `recommended_section_order`, `messaging_hierarchy`, `conversion_psychology`, `conversion_strategy`, `landing_page_recommendation`, `creative_direction`, `red_team_review`, `confidence_scores`
- `07-cro/plans/plan-01.json` — primary variant, with `cro_specialist` and `ux_designer` sections
- `07-cro/plans/plan-02.json` — challenger variant, same structure
- `07-cro/SCORING.md`
- `07-cro/sections/*.md` — 9 section blueprints

> **Note:** If `01-analysis/` is missing (e.g., segment-03), agent synthesizes from segment name + prompt. Mark confidence < 0.75 in `confidence_scores` to reflect data gap.

## Step 08 Rebuild — Per Run Agent Task

Agent reads:
- `07-cro/cro-plan.json`, `plans/plan-01.json`, `plans/plan-02.json`
- `06-strategy/strategic-positioning.json`, `05-motivation/customer-motivation.json`
- `prompts/08-landing-page-builder.md` + `schemas/schema-08.json` + `references/landing-page-constraints.md`

Agent writes (per variant):
- `08-lp/<variant>/index.html` — shell with SSI or inline includes
- `08-lp/<variant>/style.css` — design system
- `08-lp/<variant>/section/*.html` — one file per section in `recommended_section_order`
- `08-lp/landing-page.json` — schema-08 metadata

### Constraint Compliance (verify before declaring done)

| Constraint | Check method |
|---|---|
| No JS folder / no inline scripts | `find 08-lp -name "*.js"` → empty; `grep -r "<script>" 08-lp/` → only Tailwind CDN |
| No fake scarcity | `grep -ri "countdown\|timer\|stok tinggal\|sisa.*unit\|math.random" 08-lp/` → empty |
| Progressive disclosure | Section order matches: hook → desire → benefit → proof → scarcity → close |
| Medical disclaimers | `grep -ri "bukan obat\|pendamping\|konsultasi dokter" 08-lp/` → present |
| Verifiable stats | No "87%" without source; use qualitative or mark `[BUTUH DATA]` |
| Max 2 variants | Only `primary/` and `challenger/` exist |

## Post-Rebuild Verification

```python
from pathlib import Path
base = Path.home() / ".hermes/runs/performance-ngegas"
for run in sorted(base.iterdir()):
    lp = run / "08-lp"
    if not lp.exists(): continue
    for variant in ["primary", "challenger"]:
        v = lp / variant
        idx = v / "index.html"
        css = v / "style.css"
        sec = v / "section"
        sections = [f.name for f in sec.iterdir()] if sec.exists() else []
        print(f"{run.name} {variant}: idx={idx.exists()} css={css.exists()} sec={len(sections)}")
```

## Pitfalls

1. **delegate_task task string length** — Keep descriptions under ~8 KB. First batch with 14 KB task strings failed with "Error invoking agent". Split into shorter, focused tasks.
2. **Path mismatch** — Always verify actual directory names via `ls` before constructing paths.
3. **Backup before rebuild** — Legacy `08-lp/` single-file outputs must be moved to `08-lp-legacy/` before multi-file rebuild. User scolds if overwritten without check.
4. **Segment-03 anomaly** — Missing `01-analysis/` directory. Step 07 agent must synthesize from available artifacts + segment name, not fail.
5. **Tailwind CDN `<script>` is allowed** — Only JS allowed in LP. No custom JS, no countdowns, no Math.random().
6. **Re-QA after manual fix** — If `state.json` shows `NEEDS_FIX`, re-run QA after rebuild to update status. Otherwise run stays stuck.
