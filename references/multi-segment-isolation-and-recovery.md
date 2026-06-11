# Multi-Segment Isolation & Recovery Notes

Session case: Alpha Propolis hidden-gem LP generation (June 2026) across 6 segments: Muslim Taqwa, Diabetes & Ginjal, Pria 35+ Testosteron, Lansia/Anak Muda Pikun, Pejuang Kanker, Pasca Operasi.

## Key workflow lessons

1. **One segment = one isolated run folder.** Do not reuse previous segment artifacts, claims, value propositions, CTAs, or LP copy unless explicitly marked as a reusable principle.
2. **Claims/value props must be segment-owned.** Health-adjacent segments are especially sensitive: Diabetes/Ginjal, Kanker, Pasca Operasi, Testosteron, Pikun must not inherit stronger claims from another segment.
3. **Step 02–08 can be run from an existing Step 01 baseline.** If `target-market.json` already has segment-specific data, extract only that segment into `01-analysis/target-market.json` and run Step 02 onward.
4. **After LP generation, run target-role review before moving on.** Simulate 5 reviewer roles for that segment, score 1–10 across relevance, headline clarity, trust, emotional resonance, scientific believability, ethical/medical sensitivity, offer clarity, CTA clarity, objection handling, and purchase intent. Then create and implement a change list.
5. **Stitch handoff files are mandatory when the user asks designer handoff.** Each segment LP package needs `08-lp/stitch-design-brief.md`, `08-lp/stitch-prompt-primary.md`, and `08-lp/stitch-prompt-challenger.md`, not just HTML.
6. **Final QA must verify missing files, not just trust worker summaries.** Workers may report PASS while files are nested incorrectly or Stitch prompts/change logs are missing.

## Relative path failure mode

A worker wrote `.hermes/runs/...` relative to the current working directory instead of `/home/ubuntu/.hermes/runs/...`, causing Segment 04–06 outputs to be nested under a previous segment folder. Later normalization accidentally removed the shell folder containing nested outputs.

Prevention:

- Always give subagents **absolute target folders** for run output.
- In final QA, locate actual directories with absolute globbing and inspect required artifacts.
- If a tool/session cwd points at a deleted folder, delegate/file tools may fail with `FileNotFoundError` before commands run. Use a sandbox/execute-code path with absolute paths when available, or restart/reset cwd.

## Required final artifacts for multi-segment LP packages

Per segment, verify at minimum:

```txt
02-jtbd-v1/jtbd-analysis.json
03-jtbd-v2/jtbd-v2-analysis.json
04-role-profile/life-role-profile.json
05-motivation/customer-motivation.json
06-strategy/strategic-positioning.json
07-cro/cro-plan.json
08-lp/primary.html
08-lp/challenger.html
08-lp/landing-page.json
08-lp/assets.json
08-lp/stitch-design-brief.md
08-lp/stitch-prompt-primary.md
08-lp/stitch-prompt-challenger.md
09-target-role-review/target-role-review.json
09-target-role-review/REVIEW.md
09-target-role-review/change-list.md
09-target-role-review/implemented-changes.md
manifest.json
state.json
checkpoint.md
```

## Example final QA checks

- Exactly one latest/selected folder per segment number.
- All required artifacts exist.
- Manifest has target-role review score and approval.
- No missing Stitch files.
- `state.json` marks completed.
- Health claims stay within each segment’s safe claim boundary.
