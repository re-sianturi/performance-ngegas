# LP Revision Entry Points — Decision Matrix

## Pertanyaan yang sering muncul

> "Kalo mau perbaiki LP yang udah ada, start dari step mana?"

Pipeline NgeGAS desain untuk **run baru dari brief**, tapi bukan berarti harus dari 0 tiap kali. Ada 3 entry point untuk LP revision.

---

## 1. LP dari run pipeline sebelumnya, artifact riset (01-07) lengkap

**→ Mulai dari Step 08 (Landing Page Builder) + Step 08-qa (Persuasion Completeness QA).**

### Prosedur:
1. Cek run folder terakhir: `~/.hermes/runs/performance-ngegas/latest/`
2. Verifikasi artifact 01-07 ada dan valid (cek `ls`, `wc -c`, JSON parse)
3. Dispatch agent-08 dengan input: `07-cro/cro-plan.json` + `07-cro/plans/` + `06-strategy/` + `05-motivation/`
4. Setelah 08 selesai, dispatch agent-08-qa untuk Persuasion Completeness check

### Artifacts yang HARUS ada:
- `07-cro/cro-plan.json` — single source of truth untuk section blueprint
- `06-strategy/strategic-positioning.json` — positioning context
- `05-motivation/customer-motivation.json` — behavioral triggers

Kalau salah satu missing, agent-08 gagal.

---

## 2. LP dari run sebelumnya, status `NEEDS_FIX`

**→ Fix masalahnya manual, terus jalankan re-QA (Step 08-qa atau Step 09).**

### Prosedur:
1. Baca `state.json` — cek step mana yang `NEEDS_FIX`
2. Baca `08-lp/qa-report.json` (kalau ada) atau `09-qa/qa-report.json`
3. Identify critical issues: stat fiktif, fake scarcity, missing section, schema violation
4. Apply fix manual (edit file, generate missing artifact, hapus fake content)
5. **WAJIB: re-run QA agent** untuk step yang di-fix
6. Update `state.json`: status step jadi `qa_passed`
7. Update `manifest.json`: step status jadi `PASS`, overall jadi `PASS`

### Warning:
- Tanpa re-QA, run stuck di `NEEDS_FIX` meskipun issue resolved.
- Pattern dari Alpha Propolis: 3 critical issue difix, tapi `state.json` masih `NEEDS_FIX` karena re-QA tidak pernah dijalankan.

---

## 3. LP dari luar pipeline / tidak ada artifact riset (01-07)

**→ Mesti turun lebih dalam.** Tabel keputusan:

| Masalah yang mau diperbaiki | Mulai dari step | Kenapa |
|---|---|---|
| Visual, layout, struktur section, persuasion execution | **08** | CRO Plan masih valid, tinggal rebuild HTML |
| Copywriting tidak meyakinkan, messaging salah, CTA lemah | **07** | CRO Plan yang define semua copywriting strategy |
| Audience tidak nyambung, value prop salah, offer mismatch | **05** atau **06** | Motivation atau Strategic Opportunity harus di-revisi |
| Brief sendiri tidak jelas atau salah | **00** | Brief = foundation. Fix brief, run ulang dari 0 |
| Ga tau masalahnya di mana | **01** atau **00** | Mulai dari riset ulang. Jangan tebak-tebakan tanpa data. |

### Critical constraint:
Kalau tidak ada `07-cro/cro-plan.json`, **TIDAK BOLEH** mulai dari 08. CRO Plan adalah single source of truth. Agent-08 tanpa CRO Plan = improvisasi section, cuma 6 section, nggak persuasif.

---

## Quick Diagnostic Checklist

```
Cek run folder: ls -la ~/.hermes/runs/performance-ngegas/latest/

Step 01-07 ada?      → Mulai dari 08
Step 08-09 ada?      → Cek status, decide fix atau rebuild
Step 01-07 missing?  → Decide turun ke step mana (tabel di atas)
Run belum ada?       → Mulai dari 00 (brief validation)
```

---

## Context Budget Implication

| Entry Point | Token Est | Notes |
|-------------|-----------|-------|
| Step 08 rebuild | 470K in / 31K out | Baca semua sections + plans → HTML |
| Step 08-qa re-QA | 100K in / 10K out | Cek 7-point persuasion completeness |
| Step 09 full QA | 760K in / 14K out | Baca semua 8 artifact + 7 schema |
| Step 07 revisi | 470K in / 31K out | Full CRO Plan rebuild |
| Step 06 revisi | 260K in / 18K out | Merge 2 partial + 3 full |
| Step 05 revisi | 225K in / 15K out | 5 input files, output ringkas |
| Full run 01-08 | ~2.2M in / 200K out | ~71 min wall time |
