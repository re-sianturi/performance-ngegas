# Alpha Propolis Run — June 10, 2026

Case study: full 9-step pipeline execution on real sales brief.

## Brief

Alpha Propolis — suplemen kesehatan alami dari propolis lebah. Kombinasi Propolis Apis (67%) + Propolis Trigona (33%). 4 manfaat utama: imun, gula darah/kolesterol, antioksidan, kesehatan otak. BPOM POM TR 213656281. Target: Ibu Muda Urban prioritas.

## Execution Stats

| Step | Agent | Duration | Output Size | Confidence | QA |
|------|-------|----------|-------------|------------|----|
| 01 Target Market | agent-01 | 9m 11s | 53 KB | 0.85 | PASS |
| 02 JTBD v1 | agent-02 | 8m 09s | 67 KB | 0.82 | PASS |
| 03 JTBD v2 | agent-03 | 7m 50s | 84 KB | 0.80 | PASS |
| 04 Role Profile | agent-04 | 7m 51s | 61 KB | 0.88 | PASS |
| 05 Motivation | agent-05 | 5m 20s | 48 KB | 0.87 | PASS |
| 06 Strategy | agent-06c | 5m 11s | 49 KB | 0.81 | PASS |
| 07 CRO Plan | agent-07 | 10m (+retry) | 15 files | 0.83 | PASS |
| 08 LP | agent-08 | 7m 13s | 3 files (50+50+6 KB) | — | NEEDS_FIX |
| 09 QA Final | agent-09 | 4m 45s | 24 KB | — | — |

**Total:** ~71 min wall time, 32 files, 740 KB artifacts.

## Confidence Score Range

All research steps (01-07): 0.80–0.88. Consistent, no outliers. Suggests pipeline produces stable quality when input brief is comprehensive (5/5 validation).

## Timeout Pattern

- 06a (Competitive Analysis): timeout 600s — file already written (35 KB), no retry needed
- 07 (CRO Plan): timeout 600s — most files written (10/15), retry for 5 remaining sections + A/B test
- 07 retry: timeout 600s — all 15 files completed during timeout

**Pattern:** Timeouts on heavy steps (many output files) are NORMAL. Always check filesystem before retry. Retry FOCUSED (only missing files), not full rerun.

## QA Critical Findings (Step 09)

Three issues found in Step 08 output — now documented as pitfalls 16-18:

1. **Statistik "87% Ibu..."** — propagated from Step 05 → Step 07 → LP HTML. No source. Risk: BPOM regulatory.
2. **Math.random() fake counter** — tracked element `early-bird-counter` decremented randomly every 15s. Contradicts CRO plan directive: "DIHINDARI: fake countdown reset, stok palsu."
3. **Missing schema-08 metadata** — `08-lp/landing-page.json` tidak di-generate. Hanya HTML + assets.json.

## Additional QA Findings (Not Yet Fixed)

4. **"4.9 ⭐ dari 1.247+ Review" — unverifiable.** Tidak ada sumber, bukan aggregate real dari marketplace. Kalau live → BPOM bisa flag klaim performa tanpa bukti.
5. **Dose economics inkonsisten.** Subheadline "Rp 125rb/bulan untuk keluarga" vs kalkulasi dosis brief: 10ml ≈ 200 tetes, 6 tetes × 3x/hari = 18 tetes/hari/orang. Keluarga 4 orang = 72 tetes/hari → 1 botol habis ~2.8 hari, bukan 1 bulan.
6. **Identity monoculture (Step 04).** Semua 5+ persona_variants female "Ibu." Male buyer dan anak dewasa yang beli untuk orang tua lansia under-represented. Risiko: messaging alienasi 30-40% potential buyers.
7. **Revenue projection overclaim (Step 06).** Year 1 SOM IDR 15-25B tanpa sensitivity analysis, tanpa asumsi marketing budget/CAC/distribusi. Best/base/worst case tidak dimodelin.
8. **Only 1 A/B test (Step 07).** CRO ideal butuh 3-5 hypotheses. Satu test (Plan 01 vs Plan 02) kurang untuk iterasi komprehensif.

## Fix Applied

- `primary.html` line 112: `87% Ibu Melaporkan` → `Banyak Ibu Melaporkan`
- `primary.html` lines 779-790: removed `Math.random()` interval, replaced with static display
- Generated `08-lp/landing-page.json` metadata

## ⚠️ Post-Fix Re-QA Gap

Setelah 3 fix applied, **re-QA tidak pernah dijalankan.** Akibatnya:
- `state.json` masih `"status": "NEEDS_FIX"`
- `manifest.json` masih `"overall_status": "NEEDS_FIX"`
- Run stuck di NEEDS_FIX meski 3 critical issue sudah resolved
- Butuh: re-run QA untuk Step 08 → update state → run jadi PASS

Fix yang masih outstanding: #4 (review stat) dan #5 (dose math). #6-#8 adalah medium/low priority untuk run selanjutnya.

## Stitch SDK Attempt

Attempted 4x to generate LP via Stitch SDK (`creative/stitch-sdk-hermes`). Failed consistently:
- Project `15019923529038010734` exists in `list_projects` but `generate_screen_from_text` returns "not found"
- `create_project` also fails: "invalid argument" (wrong param name — should be `title`, not `displayName`)
- SDK auto-prepends `projects/` prefix — don't double-prefix
- Likely root cause: Stitch API billing/quota not enabled on GCP project `gen-lang-client-0543790092`
- **Fallback:** Use existing agent-08 Tailwind HTML (50KB, proper), fix issues, add metadata

## Key Positioning Outcome

**"SATU tameng alami untuk SELURUH keluarga Indonesia — propolis kombinasi Apis+Trigona, perlindungan 4-in-1, kualitas premium tanpa harga premium."**

Top 3 recommendations: Alpha Moms Community (10/3) → Cost Calculator (9/3) → 30-day guarantee (9/4)
