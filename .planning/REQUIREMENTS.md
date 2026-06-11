# REQUIREMENTS.md — Performance NgeGAS

## Scope

Hermes skill pack: Performance NgeGAS — Pipeline riset & eksekusi performance marketing: 8 step aktif + 1 QA final.

## Functional Requirements

### FR-01: Orchestrator
- Orchestrator menerima brief dari user (plain text)
- Orchestrator memvalidasi brief (pre-flight gate) sebelum pipeline start
- Orchestrator membaca pipeline.yaml untuk tahu DAG step 1-8 + QA
- Orchestrator dispatch sub-agent per step dengan input: brief + artifact step N-1 + prompt + persona
- Orchestrator maintain state.json (step status, artifact path, qa result)
- Orchestrator checkpoint: setelah Step 05, report ringkasan ke chat tapi lanjut otomatis (auto-jalan)
- Orchestrator compile final deliverable: semua artifact + manifest.json
- Orchestrator nggak boleh membaca isi artifact (context hygiene)

### FR-02: Sub-Agent Dispatch
- Tiap sub-agent spawned via delegate_task dengan toolsets=['file', 'web']
- Tiap sub-agent baca persona dari agents/agent-0X.md
- Tiap sub-agent baca input artifact dari folder step sebelumnya
- Tiap sub-agent tulis output artifact ke folder step sendiri
- Sub-agent wajib tulis 2 file: artifact.md (human) + artifact.json (structured)

### FR-03: Artifact Format
- JSON = structured data, machine readable, dengan schema validation
- MD = human readable, elaborated, dengan heading yang jelas
- Tiap artifact punya confidence_score per section (0.0 - 1.0)
- Tiap artifact punya red_team_review section
- Schema validation: wajib lolos sebelum QA gate

### FR-04: QA Gate
- QA Reviewer sub-agent di-dispatch setelah tiap step selesai
- QA Checklist: 10 item (completeness, accuracy, format, logic, no hallucination, schema valid, confidence >= 0.6, evidence-based, no contradiction, red team present)
- QA output: PASS / FAIL + daftar gap
- QA report disimpan di qa/ folder

### FR-05: Fixer Loop
- Kalau QA FAIL: dispatch Fixer sub-agent (1x)
- Fixer input: artifact + QA report
- Fixer output: corrected artifact
- Re-QA setelah fix
- Kalau masih FAIL: STOP, report ke user
- Max 1 retry (total 2x QA: original + fixed)

### FR-06: Pipeline DAG
```
Step 01 (Target Market) → Step 02 (JTBD v1)
Step 02 → Step 03 (JTBD v2)
Step 03 → Step 04 (Role Profile)
Step 04 → Step 05 (Motivation)
Step 04 → Step 05 (Motivation) [parallel via 04]
Step 05 → Step 06 (Strategy)
Step 06 → [AUTO CHECKPOINT] → Step 07 (CRO)
Step 07 → Step 08 (LP)
Step 08 → Step 09 (QA Final)
```
Step 04 (JTBD v2) → Step 05 (Motivation) → Step 06 (Strategy). Step 04 (Role Profile) → Step 05 (Motivation).

### FR-07: Output Folder
- Lokasi: `~/.hermes/runs/performance-ngegas/YYYYMMDD_HHMMSS_slug/`
- Struktur: 01-analysis/ → 02-jtbd/ → 03-persona/ → 04-motivation/ → 05-strategy/ → 06-cro/ → 07-lp/ → 08-review/
- Tiap folder: artifact.md + artifact.json
- 06-cro/ punya subfolder: sections/ + ab-tests/
- 07-lp/ punya subfolder: components/ + images/
- Symlink `latest/` ke run terakhir

### FR-08: CRO Plan Multiplicity
- Step 06 boleh generate N CRO plan (sebanyak kombinasi Role+JTBD yang valid)
- Orchestrator filter: cuma 2 terbaik yang dieksekusi ke Step 08 (LP)
- Archive: plan ke-3 dst disimpan di `06-cro/archive/`, bisa di-activate manual
- Selection logic: scoring transparan di SCORING.md

### FR-09: Landing Page
- Max 2 file HTML: primary.html + challenger.html
- Default: 1 (primary) kalau CRO plan cuma 1
- HTML pakai Tailwind CDN (bukan build step)
- Image prompts disimpan di images/prompts.md

### FR-10: Resume
- state.json disimpan per run folder
- Orchestrator baca state.json kalau ada saat start
- Kalau status = "in_progress", resume dari step terakhir
- Kalau status = "qa_failed", resume dari fixer loop

## Non-Functional Requirements

### NFR-01: Performance
- Pipeline complete dalam < 30 menit untuk brief standar
- Tiap step agent timeout 10 menit

### NFR-02: Reliability
- Crash di step tengah = bisa resume, nggak dari 0
- Artifact corrupt = bisa re-generate dari state.json

### NFR-03: Maintainability
- Skill pack = file-based, nggak butuh external DB
- Prompt templates terpisah dari agent personas
- Pipeline.yaml = DAG config, bisa di-extend tanpa ubah orchestrator

### NFR-04: Observability
- Manifest.json per run: audit trail lengkap
- Checkpoint.md: human-readable resume point
- Orchestrator log.md: log semua dispatch

## Quality Attributes

- **QA**: Confidence >= 0.6 per section
- **QA**: Schema validation 100% pass
- **QA**: Red team review present di tiap artifact
- **QA**: Evidence-based, assumption labeled

---
*Last updated: 2026-06-10*
