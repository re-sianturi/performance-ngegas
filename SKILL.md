---
name: performance-ngegas
description: |
  9-total pipeline riset & eksekusi performance marketing: 8 step aktif + 1 QA
  final. Target Market → JTBD v1 → JTBD v2 → Role Profile → Customer Motivation
  Database → Strategic Opportunity → CRO Plan → Landing Page Builder → Final QA.
  Multi-agent orchestration dengan artifact-first output (JSON/YAML), file-to-file
  pipeline, QA gates, fixer loops, archive/activate capability, dan auto-jalan
  checkpoint. Output: structured research artifacts + ready-to-publish landing page HTML.
version: 1.0.5
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [marketing, research, jtbd, cro, landing-page, multi-agent]
    related_skills: [skill-builder, subagent-driven-development, hermes-agent-skill-authoring]
---

# Performance NgeGAS — 9-Total Marketing Research Pipeline

## Overview

Performance NgeGAS adalah pipeline riset & eksekusi performance marketing yang
menerima sebuah brief produk/jasa dan menghasilkan 9 deliverable:

1. **01 Target Market Analysis** — ICP, 5+ segmen, awareness, psychographic
2. **02 JTBD v1** — Deep JTBD (Christensen + Moesta method)
3. **03 JTBD v2** — Deep Job Map, cross-reference v1, switching barriers
4. **04 Role Profile** — Life role database, 5+ persona variants, dominant role
5. **05 Customer Motivation** — 20 pain/fear/desire/frustration + 15 behavioral triggers
6. **06 Strategic Opportunity** — Expert team: Competitive Analysis + Opportunity Sizing → Strategic Positioning
7. **07 CRO Plan** — 9 sections blueprint + A/B tests. Max 2 dieksekusi, archive ke-3+
8. **08 Landing Page** — Primary + challenger HTML, multi-file structure (max 2 variants)
9. **08-qa Persuasion Completeness QA Gate** — 7-point persuasion check before final QA
10. **09 QA Final** — QA gate + Red Team adversarial audit

**Architecture:** Multi-agent orchestration dengan artifact-first design. Setiap
step menghasilkan file terstruktur (JSON) yang dibaca oleh step berikutnya.
Orchestrator koordinasi, sub-agent melakukan heavy work.

**User requirement:** Pipeline ini didesain untuk **solo builder / marketing team kecil**.
Semua prompt dalam Bahasa Indonesia. Brief bisa English atau Indonesian (bilingual).

## Pipeline DAG

```
BRIEF ──→ 01 Target Market ──→ 02 JTBD v1 ──→ 03 JTBD v2
                                         │
                                         └──→ 04 Role Profile ──→ 05 Motivation
                                         │                                          │
                                         └──→ 05 Motivation (parallel via 04) ──────┘
                                                                                   │
                                                                              06 Strategy
                                                                                   │
                                                                             [AUTO CHECKPOINT]
                                                                                   │
                                                                                   ↓
                                                                         07 CRO ──→ 08 LP ──→ 08-qa QA Gate ──→ 09 QA Final
```

**Step 04 & 05 berjalan paralel** setelah Step 03 selesai.
**Step 06a & 06b berjalan paralel**, hasil di-merge oleh 06c.

## Agent Pattern: Hat System vs Expert Team

Pipeline ini menggunakan **dua pola multi-role** yang berbeda per step.

### 🎩 Hat System (Default)

1 agent, multiple hats. Ganti topi per section, output 1 artifact kohesif.

**Pakai kalau:**
- Output wajib 1 artifact kohesif (tidak bisa dipecah)
- Role-role domain adjacent (sama framework)
- Tiap bagian butuh konteks bagian lain
- Tidak ada konflik fundamental antar role
- Speed lebih penting dari depth spesifik

**Step yang pakai:** 01, 02, 03, 04, 05, 07, 08, 09

### 👥 Expert Team (Step 06)

2-3 agent parallel, hasil di-merge oleh agent ketiga.

**Pakai kalau salah satu terpenuhi:**
- Output bisa dipecah jadi 2+ partial independen
- Role di domain yang benar-benar beda (beda framework)
- Butuh depth spesifik yang 1 agent tidak bisa hold
- Hasil partial bisa di-cross-validate
- Step ini adalah strategic bottleneck / pivot point

**Step yang pakai:** 06 (Competitive Analyst + Opportunity Sizer → Strategic Planner)

### Section-Tagging (Hat System)

Walaupun 1 agent, output di-tag per role di setiap section. Agent wajib:

1. **Context Carry:** Baca ulang section sebelumnya sebelum ganti topi
2. **Cross-Reference Check:** Cek apakah metric, layout, dan test variants align
3. **Konflik Resolution:** Tulis konflik dan resolusi kalau ada

Contoh tag (Step 07 CRO Plan):
```
### 🎯 CRO Specialist Perspective [FOR-PIPELINE]
- Goal, headline strategy, conversion metric

### 🎨 UX Designer Perspective [FOR-PIPELINE]
- Layout, visual hierarchy, interaction, mobile

### 🧪 A/B Testing Expert Perspective [FOR-HUMAN]
- Hypothesis, primary metric, sample size, duration
```

## Artifact-First Design

**Rule:** Tiap step wajib menghasilkan file. Tidak boleh output chat-only.

| Step | Output File | Schema | Format |
|------|-------------|--------|--------|
| 01 | `01-analysis/target-market.json` | schema-01.json | JSON |
| 02 | `02-jtbd-v1/jtbd-analysis.json` | schema-02.json | JSON |
| 03 | `03-jtbd-v2/jtbd-v2-analysis.json` | schema-03.json | JSON |
| 04 | `04-role-profile/life-role-profile.json` | schema-04.json | JSON |
| 05 | `05-motivation/customer-motivation.json` | schema-05.json | JSON |
| 06 | `06-strategy/strategic-positioning.json` | schema-06.json | JSON |
| 07 | `07-cro/cro-plan.json` + `SCORING.md` + `plans/` + `archive/` + `sections/` + `ab-tests/` | schema-07.json | JSON + MD |
| 08 | `08-lp/landing-page.json` + `08-lp/primary/` (index.html + section/*.html + img/ + style.css) + `08-lp/challenger/` (index.html + section/*.html + img/ + style.css) | schema-08.json | JSON + HTML |
| 09 | `09-qa/qa-report.json` | schema-09.json | JSON |

## QA Gate & Fixer Loop

**Setiap step selesai → QA Reviewer di-dispatch.**

**QA Checklist:**
1. Artifact file exists (json)
2. JSON valid parse, schema compliance (cek schema-0X.json)
3. Required fields present
4. Confidence score ≥ 0.6 (jika ada)
5. Red team review section present
6. Tidak ada hallucination (semua claim punya basis brief)
7. Koherensi dengan step sebelumnya (jika ada)
8. Tidak ada copywriting / offer di step riset (02-05)
9. Format sesuai spec
10. Section-tagging lengkap (untuk hat system steps)

**Retry Policy:**

| Kondisi | Aksi |
|---------|------|
| QA PASS | Mark done. Lanjut step berikutnya. |
| QA FAIL (1x) | Dispatch Fixer. Re-QA. |
| QA FAIL (2x) | **STOP.** Report ke user: gap apa, minta arahan. |
| Sub-agent error | Retry 1x. Masih error → escalate. |

## Folder Structure (Per Run)

**Rule:** Tiap run = folder baru. Format: `YYYY-MM-DD_HHMMSS_<slug>`
Tidak boleh shared / cumulative. Symlink `latest/` selalu ke run terbaru.

```
~/.hermes/runs/performance-ngegas/
├── 2026-06-10_150305_wardah-baby/
│   ├── 00-input/
│   │   ├── brief.json
│   │   └── brief.md
│   ├── 01-analysis/
│   │   └── target-market.json
│   ├── 02-jtbd-v1/
│   │   └── jtbd-analysis.json
│   ├── 03-jtbd-v2/
│   │   └── jtbd-v2-analysis.json
│   ├── 04-role-profile/
│   │   └── life-role-profile.json
│   ├── 05-motivation/
│   │   └── customer-motivation.json
│   ├── 06-strategy/
│   │   ├── competitive-analysis.json
│   │   ├── opportunity-size.json
│   │   └── strategic-positioning.json
│   ├── 07-cro/
│   │   ├── cro-plan.json
│   │   ├── SCORING.md
│   │   ├── plans/
│   │   │   ├── plan-01.json
│   │   │   └── plan-02.json
│   │   ├── sections/
│   │   │   ├── hero.md
│   │   │   ├── social-proof.md
│   │   │   ├── cta.md
│   │   │   ├── lp-structure.md
│   │   │   ├── urgency.md
│   │   │   ├── trust.md
│   │   │   ├── retention.md
│   │   │   ├── retargeting.md
│   │   │   └── reporting.md
│   │   ├── ab-tests/
│   │   │   └── test-01.md
│   │   └── archive/
│   │       └── plan-03.json
│   ├── 08-lp/
│   │   ├── primary/
│   │   │   ├── index.html
│   │   │   ├── section/
│   │   │   │   ├── hero.html
│   │   │   │   ├── problem.html
│   │   │   │   ├── mechanism.html
│   │   │   │   ├── proof.html
│   │   │   │   ├── faq.html
│   │   │   │   ├── cta.html
│   │   │   │   └── footer.html
│   │   │   ├── img/
│   │   │   │   ├── prompts.md
│   │   │   │   └── placeholder.md
│   │   │   └── style.css
│   │   ├── challenger/
│   │   │   ├── index.html
│   │   │   ├── section/
│   │   │   │   ├── hero.html
│   │   │   │   ├── problem.html
│   │   │   │   ├── mechanism.html
│   │   │   │   ├── proof.html
│   │   │   │   ├── faq.html
│   │   │   │   ├── cta.html
│   │   │   │   └── footer.html
│   │   │   ├── img/
│   │   │   │   ├── prompts.md
│   │   │   │   └── placeholder.md
│   │   │   └── style.css
│   │   ├── qa-report.json
│   │   └── landing-page.json
│   ├── 09-qa/
│   │   └── qa-report.json
│   ├── qa/
│   │   └── qa-01.md
│   ├── manifest.json
│   ├── state.json
│   └── checkpoint.md
└── latest -> 2026-06-10_150305_wardah-baby/
```

## Step-by-Step Input/Output Chain

```
01 ← 00-input/brief.json
02 ← 00-input/brief.json + 01-analysis/target-market.json
03 ← 00-input/brief.json + 01-analysis/target-market.json + 02-jtbd-v1/jtbd-analysis.json
04 ← 00-input/brief.json + 01-analysis/target-market.json + 02-jtbd-v1/jtbd-analysis.json + 03-jtbd-v2/jtbd-v2-analysis.json
05 ← 00-input/brief.json + 01-analysis/target-market.json + 02-jtbd-v1/jtbd-analysis.json + 03-jtbd-v2/jtbd-v2-analysis.json + 04-role-profile/life-role-profile.json
06a ← 00-input/brief.json + 01-analysis/target-market.json + 05-motivation/customer-motivation.json
06b ← 00-input/brief.json + 01-analysis/target-market.json + 05-motivation/customer-motivation.json
06c ← 06-strategy/competitive-analysis.json + 06-strategy/opportunity-size.json
07 ← 00-input/brief.json + 06-strategy/strategic-positioning.json + 05-motivation/customer-motivation.json
08 ← 07-cro/cro-plan.json + 07-cro/plans/ + 06-strategy/strategic-positioning.json + 05-motivation/customer-motivation.json
08-qa ← 08-lp/ + 07-cro/cro-plan.json
09 ← semua artifact 01-08 + 08-lp/qa-report.json
```

## Pre-Flight Gate (Brief Validation)

Sebelum pipeline start, brief wajib lolos validasi:

**Brief harus punya ≥ 3 dari 5 elemen:**
1. Product description (produk/jasa apa)
2. Target audience hint (target market)
3. Value proposition (nilai yang ditawarkan)
4. Pricing model (harga/business model)
5. Competitive context (kompetitor/lanskap pasar)

**Kalau brief kurang:** STOP. Report ke user: "Brief kurang X, Y, Z. Perbaiki dulu."

## Human Checkpoint (Auto-Jalan)

Setelah Step 06 (Strategic Opportunity) selesai + QA PASS:
- Orchestrator **tidak pause** (auto-jalan)
- Orchestrator log ringkasan positioning ke chat
- Pipeline lanjut ke Step 07 otomatis
- User bisa intervensi kapanpun dengan `/stop` atau revisi manual

**Override:** User bisa pilih manual checkpoint dengan flag `--checkpoint`.

## Landing Page Constraint

**Max 2 varian:** `primary.html` (publish) + `challenger.html` (A/B test).

Kalau brief minta lebih dari 2, wajib ada justifikasi di brief. Default = 2.
Plan ke-3+ masuk `07-cro/archive/` dan bisa di-activate manual.

## Context Hygiene Rules

1. **Orchestrator:** Cuma baca `pipeline.yaml`, `state.json`, dan file path. Tidak boleh baca isi artifact.
2. **Orchestrator context budget:** Maksimal 15%. 85% didelegasi ke sub-agent.
3. **Sub-agent:** Spawn dengan fresh context. Tiap task = 1 agent invocation.
4. **Agent tidak baca plan file:** Orchestrator inject full task text + context langsung.

## Resume Capability

- `state.json` catat step dan status (`pending` / `in_progress` / `qa_passed` / `done` / `failed`)
- `checkpoint.md` catat: "Step 1-4 selesai, lanjut dari Step 5"
- Orchestrator baca state.json kalau ada. Resume dari step terakhir, tidak dari 0.

## Manifest (Audit Trail)

```json
{
  "run_id": "2026-06-10_150305",
  "brief_hash": "sha256:abc123...",
  "brief_file": "brief.json",
  "pipeline_version": "1.0.2",
  "steps": {
    "01": {"status": "done", "agent": "agent-01", "qa": "PASS", "artifact": "01-analysis/target-market.json"}
  },
  "completed_at": "2026-06-10T15:45:00Z"
}
```

## Retention Policy

- Run > 30 hari: dipindah ke `archive/` (zip)
- Run > 60 hari: dihapus kecuali flagged `--keep`
- `latest/` symlink selalu ke run terbaru

## Landing Page Revision Entry Points

**Pertanyaan yang sering:** "Kalo mau perbaiki LP yang udah ada, start dari step mana?"

Pipeline NgeGAS desain untuk **run baru dari brief**, tapi bukan berarti harus dari 0 tiap kali. Ada 3 entry point untuk LP revision:

### 1. LP dari run pipeline sebelumnya, artifact riset (01-07) lengkap
**→ Mulai dari Step 08 (Landing Page Builder) + Step 08-qa (Persuasion Completeness QA).**

Agent-08 baca `07-cro/cro-plan.json` + `07-cro/plans/` + `06-strategy/` + `05-motivation/` terus rebuild LP-nya. Step 08-qa cek apakah section, psychology, dan progressive disclosure faithful ke CRO Plan.

### 2. LP dari run sebelumnya, status `NEEDS_FIX`
**→ Fix masalahnya manual, terus jalankan re-QA (Step 08-qa atau Step 09).**

Jangan ulang dari 0. Kalau `state.json` masih `NEEDS_FIX` setelah fix, wajib re-QA supaya `state.json` dan `manifest.json` update ke `PASS`. Tanpa re-QA, run stuck di `NEEDS_FIX` meskipun issue sudah resolved.

### 3. LP dari luar pipeline / tidak ada artifact riset (01-07)
**→ Mesti turun lebih dalam.** Tabel keputusan:

| Masalah yang mau diperbaiki | Mulai dari step |
|---|---|
| Visual, layout, struktur section, persuasion execution | **08** (rebuild dari CRO Plan yang ada) |
| Copywriting tidak meyakinkan, messaging salah, CTA lemah | **07** (revisi CRO Plan) atau **06** (revisi strategi) |
| Audience tidak nyambung, value prop salah, offer mismatch | **05** atau lebih rendah (riset ulang) |
| Brief sendiri tidak jelas atau salah | **00** (mulai dari brief baru) |

### Critical Dependency Check

**Step 08 butuh file-file ini — cek sebelum dispatch:**
- `07-cro/cro-plan.json` ← **WAJIB**, single source of truth untuk section blueprint
- `06-strategy/strategic-positioning.json` ← positioning context
- `05-motivation/customer-motivation.json` ← behavioral triggers

Kalau salah satu missing, agent-08 tidak bisa jalan. Musti turun ke step yang menghasilkan file missing itu.

---

## Pitfalls

1. **Jangan parallel semua step.** Overhead merge > benefit. Hat System cukup untuk domain adjacent.
2. **Jangan hat system kalau role benar-benar beda domain.** Misal: Data Scientist + Creative Director = spawn Expert Team.
3. **Orchestrator jangan baca isi artifact.** Context pollution. Cukup baca file path.
4. **Step 02 (JTBD) jangan lompat ke pain point / copywriting.** JTBD murni = pemahaman progress, bukan solusi.
5. **QA gate wajib lolos sebelum lanjut.** Skip QA = compound error downstream.
6. **Jangan output chat-only.** Wajib artifact file. Kalau agent output chat, dispatch ulang dengan reminder.
7. **Max 2 LP varian.** Lebih dari 2 = user bingung. Default primary + challenger.
8. **Folder per run.** Jangan pakai folder shared. Format: `YYYY-MM-DD_HHMMSS_<slug>`.
9. **Step 2 & 3 (JTBD v1 & v2) pisah.** Jangan digabung. V1 = Christensen/Moesta. V2 = Deep Job Map + cross-reference.
10. **A/B Testing Expert output [FOR-HUMAN].** Jangan dikonsumsi Step 08. CRO Specialist + UX Designer = [FOR-PIPELINE].
11. **Cek existing file CONTENTS sebelum overwrite.** Jangan asal tulis tanpa cek `ls` atau `read_file` dulu. User bisa punya file lama yang penting. Backup kalau perlu. User scold: *"Cek dulu ada isinya ga? Jangan asal. Pinteran dikit, kaya bocil lu."* → verify contents, not just file existence.
12. **GSD questioning sebelum eksekusi.** Jangan langsung coding. Jalankan GSD questioning dulu untuk surface gaps. User mungkin punya masukan yang mengubah arsitektur.
13. **Jangan over-engineer kalau user bilang simple.** "Pisah aja ga usah kepinteran" = jangan gabung, jangan nambah abstraction, jangan "optimasi" tanpa diminta.
14. **Define istilah baru sebelum pakai.** Jangan drop jargon, acronym, atau tool name tanpa inisialisasi. User: *"Jangan pake istilah baru. Kalau mau pake istilah baru inisialisasi dulu."* → Setiap term baru harus dijelaskan di awal penggunaan.
15. **Verify availability BEFORE trying, explain method upfront.** Jangan trial-and-error tanpa transparansi. User: *"Verify installation/availability BEFORE trying, then explain method upfront."* → Cek dulu, jelaskan approach, baru eksekusi.
16. **Rigid structure defined and approved before execution.** User: *"Bikin rigid dulu sebelum good to go."* → Plan + structure + approval, baru coding. No trial-and-error without structure.

## LP Builder Pitfalls (Step 08)

14. **JANGAN fake scarcity.** Jangan pakai `Math.random()`, `setInterval` counter decrement, fake countdown reset, atau "stok palsu." Ini kontradiksi langsung dengan Step 07 CRO Plan yang eksplisit bilang "DIHINDARI: fake countdown reset, stok palsu." Urgency harus genuine (musim, batch terbatas real, early bird real).
15. **JANGAN statistik fiktif.** "87% ibu melaporkan..." tanpa sumber = risiko BPOM dan trust collapse. Kalau ga ada data primer, pakai bahasa kualitatif: "Banyak ibu melaporkan..." atau "Pelanggan kami melaporkan..."
16. **HARUS ada metadata JSON.** Step 08 wajib output `08-lp/landing-page.json` sesuai schema-08. HTML dan assets.json tidak cukup. Schema-08 butuh: metadata, variants array dengan html_summary, confidence_scores.
17. **Stitch integration: pakai curl, bukan SDK.** SDK `@google/stitch-sdk` v0.3.5 ada bug double `projects/` prefix. Gunakan direct curl ke `stitch.googleapis.com/mcp` dengan numeric project ID. Lihat `stitch-sdk-hermes` skill untuk script wrapper.
14. **Subagent timeout ≠ gagal.** delegate_task sering write file sebelum timeout (600s). Selalu cek filesystem dulu (`find` / `ls`) sebelum dispatch retry. Kalau file sudah ada dan valid, anggap selesai. Retry cuma kalau file kosong atau corrupted. Retry FOCUSED: cuma kerjakan bagian yang kurang, jangan ulang dari nol.
15. **delegate_task task string length limit.** Task descriptions > ~8 KB sering fail dengan "Error invoking agent" (no stack trace). Keep task strings concise; reference file paths instead of inlining full content. Split into shorter, focused tasks. First observed June 2026 during 7-run batch rebuild.
16. **Parallel dispatch pakai `tasks` array di delegate_task.** Untuk Expert Team (Step 06), gunakan `delegate_task(tasks=[{...}, {...}])` bukan dua `delegate_task` terpisah.
16. **Step 08 output wajib `08-lp/landing-page.json` metadata.** QA gate FAIL kalau cuma HTML + assets tanpa JSON. Generate sesuai schema-08.
17. **Statistik di LP harus punya sumber.** Jangan propagate angka tanpa sumber ke landing page. QA Red Team akan flag. Gunakan bahasa kualitatif ("Banyak ibu...") atau tandai `[BUTUH DATA]`.
18. **Fake scarcity dilarang di LP.** `Math.random()` counter, countdown reset, "stok tinggal X" palsu = kontradiksi dengan trust positioning. Urgency berbasis real: batch terbatas, harga early bird, bonus periode.
19. **Stitch SDK preferred untuk LP.** User expects proper UI; tawarkan Stitch dulu (`creative/stitch-sdk-hermes`). Fallback ke Tailwind HTML manual kalau Stitch gagal.
20. **Step 07 CRO file yang di-output.** Pastikan 15 file lengkap: `cro-plan.json`, `SCORING.md`, `plans/plan-01.json`, `plans/plan-02.json`, `archive/plan-03.json`, 9 sections (01-09), `ab-tests/test-01.md`. Timeout sering terjadi; retry focused untuk sisa yang kurang.
21. **Post-fix re-QA wajib.** Kalau QA report flag `NEEDS_FIX` lalu fix diapply secara manual (di luar fixer loop otomatis), wajib re-run QA untuk step tersebut + update `state.json` dan `manifest.json`. Tanpa re-QA, run stuck di status `NEEDS_FIX` meskipun semua issue udah resolved. Pattern dari Alpha Propolis: 3 critical issue difix, tapi `state.json` masih `NEEDS_FIX` karena re-QA gak pernah jalan. **Verification tool:** `scripts/qa-script.py <run_dir> --json` bisa dipake sebagai quick check sebelum re-QA formal. Kalau script bilang PASS, tinggal update state.json.
22. **Stat cascade detection.** Stat tanpa sumber di step awal (05) bisa propagasi ke step downstream (07, 08) tanpa terdeteksi. QA Step 09 harus trace balik origin setiap stat. Cara cegah: kalau stat gak punya sumber di Step 05, tandai `[BUTUH DATA]` dan jangan dipake di LP.
23. **Dose economics validation.** Klaim penghematan biaya di LP (misal "Rp X/bulan untuk keluarga") harus dicek dengan perhitungan dosis dari brief. 1 botol 10ml ≈ 200 tetes ÷ (6 tetes × 3x/hari × N orang) = realistis? Kalau gak match, klaim bisa misleading.
24. **Multi-segment runs wajib isolated.** Kalau user minta beberapa target/segmen, treat `1 segment = 1 run folder + 1 claim/value prop set + 1 LP package`. Jangan campur claim, CTA, role review, atau positioning antar segmen. Kalau user bilang “jangan campur-campur” / “masing-masing claim target”, ini adalah hard constraint.
25. **Designer/Stitch handoff is a first-class artifact.** Kalau user minta prompt LP dilempar ke Stitch/designer, final package wajib punya `08-lp/stitch-design-brief.md`, `stitch-prompt-primary.md`, dan `stitch-prompt-challenger.md` per segmen. Jangan cuma sebut prompt di chat.
26. **LP HTML wajib lolos 8-point check sebelum deploy.** Jalankan `scripts/qa-script.py` untuk scan 8 pola bermasalah: unverified stats, dose economics, fake scarcity, missing disclaimer, contradictory claims, WhatsApp placeholder, unverified clinical claims, stat cascade. Script output JSON yang bisa dikonsumsi agent-09-lite atau dipake sebagai standalone pre-deploy gate.
27. **Redundancy check sebelum execute.** Kalau bikin list todo/plan untuk user, CEK DULU apakah ada item yang overlap atau redundant. User koreksi: "cek ulang ada yang redundant atau overlap ga?" — jangan langsung execute tanpa review. Pattern: tulis list → scan untuk overlap → merge → baru execute. Contoh: 7 items bisa jadi 4 kalau di-merge dengan benar.
28. **Target-role review loop per LP sebelum lanjut segmen berikutnya.** Setelah Step 08, simulate reviewer roles khusus segmen, score, buat `change-list.md`, implement revisi ke LP + Stitch prompt, tulis `implemented-changes.md`, baru lanjut.
27. **Post-QA batch fix pattern.** Kalau QA report bilang NEEDS_FIX, jangan fix satu-satu manual. Pakai pattern Scan → Fix → Verify dari `references/post-qa-batch-fix.md`. Scan dulu dengan regex untuk dapat exact file:line, batch fix dengan execute_code (re.sub / str.replace), final verify untuk pastikan zero issues remain. Contoh: 23 files, 30+ issues, <5 menit execution.
27. **Relative `.hermes/...` path can nest outputs in the wrong run.** Subagents harus diberi absolute output path (`/home/ubuntu/.hermes/runs/...`) dan Final QA harus verify filesystem, bukan percaya summary. Jika cwd/session sudah menunjuk folder yang terhapus, file/terminal tools bisa error `FileNotFoundError`; recover dengan absolute-path sandbox or restart context.
29. **Scan-then-fix pattern untuk post-QA repair.** Kalau user bilang "find the problem and fix it" atau "apa yang salah?", JANGAN langsung propose fix. Scan dulu SEMUA file HTML di `08-lp/` dengan regex patterns (Math.random, wa.me/[^0-9], unverified %, tanpa efek samping, teruji klinis, missing disclaimer). Present findings sebagai exact file:line + context snippet. Group ke batch (blocking/high/post-launch). Baru eksekusi fix setelah user approve. Lihat `references/post-qa-repair-pattern.md` untuk full pattern.
30. **JANGAN output LP cuma 1 file HTML self-contained.** Schema-08 lama cuma define `file_path: string` (1 file per variant). Ini memaksa agent jadi single-file. Output HARUS multi-file: `index.html` + `section/*.html` + `img/` + `style.css`. **NO `js/` folder. No JS files.** Lihat `references/lp-step-08-fix.md` untuk schema revised dan prompt patch.
- Kalau salah satu missing, agent-08 tidak bisa jalan. Musti turun ke step yang menghasilkan file missing itu.

---

## File References

| File | Path | Purpose |
|------|------|---------|
| Pipeline config | `pipeline.yaml` | DAG, step definitions, QA gates |
| Agent personas | `agents/agent-01.yml` … `agent-09.yml` | 11 agent definitions (09 includes 06a/b/c) |
| JSON schemas | `schemas/schema-01.json` … `schema-09.json` | Output validation per step |
| Prompt templates | `prompts/01-target-market-analysis.md` … `08-landing-page-builder.md` | Raw prompt templates |
| Run patterns | `references/run-patterns.md` | Orchestration patterns: timeout handling, parallel dispatch, retry logic |
| LP integrity | `references/lp-integrity.md` | Landing page integrity rules: no fake scarcity, verified stats, trust signals |
| Alpha Propolis run | `references/alpha-propolis-run.md` | Case study: full 9-step run on real brief (June 2026) |
| Hidden gem targets | `references/hidden-gem-targets.md` | Non-obvious market angles: cancer, sunnah, anti-aging, fertility, dental, kidney, brain, COVID, wound, athletic |
| Multi-segment isolation | `references/multi-segment-isolation-and-recovery.md` | Lessons from 6-segment LP run: absolute paths, no claim mixing, Stitch handoff files, role-review loop, recovery from nested relative-path outputs |
| Delivering artifacts | `references/delivering-artifacts.md` | Workflow: gather LP files, package into ZIP, send to Telegram via `send_message` with `MEDIA:` prefix. Python `zipfile` fallback, file naming conventions, and HTML delivery notes. |
| LP Step 08 Fix | `references/lp-step-08-fix.md` | Patch notes: multi-file schema, persuasion framework, mandatory 12+ section table, prompt role additions, QA completeness checklist. Apply when fixing Step 08 output. |
| LP Revision Entry Points | `references/lp-revision-entry-points.md` | Decision matrix: where to start when fixing an existing LP. Covers 3 entry points (Step 08 rebuild, NEEDS_FIX re-QA, and external LP deep-dive) with artifact dependency checklist. |
| Batch Rebuild Workflow | `references/rebuild-batch-workflow.md` | Mass-rebuild Step 07 + Step 08 across multiple existing runs. Pre-flight checklist, batch dispatch strategy, constraint compliance verification, post-rebuild validation script. |
| Web Deployment | `devops/ngegas-web-ops` skill | Deploy finished LP variants to ngegas.biz.id. Covers replace-existing pattern, backup-before-deploy, Caddyfile config, post-deploy curl verification. Use when user says "deploy to ngegas" or "upload to ngegas". |
| **QA Step 09 Optimization** | `references/qa-step-09-optimization.md` | Chunked audit pattern untuk batch QA. Root cause analysis timeout, pre-compress phase, schema-09-lite, token savings 94%. Includes dispatch strategy (max 3 concurrent, timeout handling, fallback). |
| **Post-QA Batch Fix** | `references/post-qa-batch-fix.md` | Scan → Fix → Verify workflow untuk memperbaiki NEEDS_FIX issues secara batch. Common patterns: unverified stats, dose economics, disclaimer injection, WhatsApp placeholder. |
| **Post-QA Repair Pattern** | `references/post-qa-repair-pattern.md` | Scan-then-fix workflow: grep LP files for known issues (fake scarcity, placeholders, unverified claims), present exact file:line findings, group by severity batch, execute fixes, re-QA. |
| Skill maintenance | `references/skill-maintenance.md` | Checklist: 6 SKILL.md locations to sync when pipeline.yaml changes. Impact assessment framework, patch doc format, pending items policy. |

## Usage

```bash
# Load skill
hermes skill load performance-ngegas

# Run dengan brief
hermes skill run performance-ngegas --brief path/to/brief.md

# Run dengan auto-jalan (default)
hermes skill run performance-ngegas --brief brief.md

# Run dengan manual checkpoint
hermes skill run performance-ngegas --brief brief.md --checkpoint

# Resume run yang terhenti
hermes skill run performance-ngegas --resume

# Lihat run terbaru
ls -la ~/.hermes/runs/performance-ngegas/latest/
```

## Landing Page: Stitch SDK (Preferred)

Setelah pipeline selesai dan CRO Plan (Step 07) ready, user biasanya minta LP yang proper UI — bukan HTML mentah Tailwind. **Selalu tawarkan Stitch SDK dulu.**

Stitch SDK (`creative/stitch-sdk-hermes`) generate LP dari text prompt via Google AI. Hasil: HTML self-contained + screenshot.

**Workflow:**
1. Baca `07-cro/plans/plan-01.json` + `plan-02.json` (CRO specs: headline, color, layout)
2. Baca `06-strategy/strategic-positioning.json` (positioning, key messages)
3. Baca `05-motivation/customer-motivation.json` (behavioral triggers)
4. Construct prompt dari semua data di atas
5. Generate via Stitch: primary + challenger, `deviceType: 'DESKTOP'`
6. Download HTML URL → save ke `08-lp/primary.html` + `08-lp/challenger.html`

Kalau Stitch gagal (project expired, auth error), fallback ke agent-08 Tailwind HTML.
