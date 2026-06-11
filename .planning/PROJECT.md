# Performance NgeGAS

## What This Is

Performance NgeGAS adalah Hermes skill pack yang menjalankan pipeline riset & eksekusi performance marketing 8-step. Skill pack ini menerima brief produk/jasa, lalu menghasilkan deliverable lengkap: target market analysis, JTBD analysis, customer persona, motivation database, strategic positioning, CRO plan, dan landing page (HTML + Tailwind CDN).

## Core Value

**Pipeline dari brief → landing page dalam 1 run, dengan output terstruktur yang bisa di-trace, di-audit, dan di-resume.**

## Requirements

### Validated

- (None yet — project baru)

### Active

- [ ] 8-step pipeline (01 Target Market → 02 JTBD v1 → 03 JTBD v2 → 04 Role Profile → 05 Motivation → 06 Strategy → 07 CRO → 08 LP) + 09 QA Final
- [ ] Multi-agent orchestration dengan orchestrator lean (~15% context) + sub-agent specialist
- [ ] Artifact-first: tiap step menghasilkan file terstruktur (json + md)
- [ ] File-to-file pipeline: step N baca output step N-1
- [ ] QA gate + fixer loop di setiap step (max 2 retry, lalu escalate)
- [ ] Confidence scoring (0-1) per section, transparan ke user
- [ ] 1 folder per run di `~/.hermes/runs/performance-ngegas/YYYYMMDD_HHMMSS_nama-brief/`
- [ ] Resume capability: crash di step 5 bisa lanjut dari situ
- [ ] Brief validation gate (pre-flight) sebelum pipeline start
- [ ] Human checkpoint setelah Step 05 (strategic bottleneck) — auto-jalan, report ringkasan ke chat
- [ ] Max 2 CRO plan dieksekusi (primary + challenger), sisanya archive (keep, bisa di-activate)
- [ ] Max 2 landing page (primary + challenger)
- [ ] Schema JSON validation untuk tiap artifact
- [ ] Manifest audit trail per run
- [ ] All prompts in Indonesian (English brief supported)
- [ ] Hat System default, Expert Team untuk Step 05 (parallel + merge)
- [ ] Resume capability
### Out of Scope

- [ ] Persistent database / CRM integration — hanya file-based artifact
- [ ] Real-time A/B testing execution — hanya rencana (brief untuk tim marketing)
- [ ] Multi-brief paralel dalam 1 run — 1 brief = 1 run
- [ ] Image generation / media asset creation — hanya prompt untuk image generation
- [ ] Auto-deployment landing page ke hosting — hanya file HTML, user deploy manual
- [ ] Integration dengan Zalo/WhatsApp API — hanya flow diagram
- [ ] Support brief non-Indonesian = out of scope — English brief **supported** untuk v1
- [ ] Step 02 JTBD v1 dan v2 terpisah — **Ya, 8 step terpisah, nggak di-merge**
- [ ] >2 LP variant tanpa justifikasi eksplisit — default 2, max 2

## Context

- Target audience: User sendiri (solo builder, marketing team kecil)
- Domain: Performance marketing, JTBD (Christensen + Moesta), Behavioral Economics
- Environment: Hermes Agent (cmd v0.28.0), tool delegate_task, file-based I/O
- Prior art: 8 prompt files sudah ada di `prompts/`, perlu refactor jadi pipeline
- Constraint: Nggak ada API key, nggak ada external DB. Pure file + sub-agent.
- Quality standard: Confidence >= 0.6 per section, red team review present

## Constraints

- **[Tech Stack]**: Hermes Agent skill pack (SKILL.md + prompt templates + agent personas)
- **[I/O]**: File-based (JSON/YAML/MD), nggak ada network I/O kecuali sub-agent internal
- **[Context]**: Orchestrator lean ~15%, sub-agent 100% fresh
- **[Language]**: Indonesian (Bahasa Indonesia) untuk semua prompt dan output
- **[Output Location]**: `~/.hermes/runs/performance-ngegas/YYYYMMDD_HHMMSS_nama-brief/`
- **[Step Count]**: 7 step aktif + 1 QA final. Bukan 8 prompt terpisah.
- **[Retry]**: Max 2x QA fail per step, lalu escalate ke user

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Step 2 & 3 terpisah (8+1 step) | User requirement: nggak usah kepinteran. 8 step terpisah + 1 QA. | — Pending |
| Hat System default, Expert Team Step 05 | Step 05 = strategic bottleneck. Parallel competitive analysis + opportunity sizing. | — Pending |
| Max 2 LP (primary + challenger) | User requirement: >2 bingung. Default 2, lebih butuh justifikasi. | — Pending |
| Folder per run | User requirement: nggak kecampur. Tiap run = folder baru. | — Pending |
| A/B Testing Expert = for-human | Output A/B test plan untuk tim marketing, bukan serving pipeline. | — Pending |
| Brief validation gate | Anti-sampah. Save token. Validate sebelum burn. | — Pending |
| Resume capability | Anti-waste. Crash di step 5 = lanjut, nggak dari 0. | — Pending |
| Step 05 checkpoint = auto-jalan | User requirement: nggak mau stop. Report ke chat tapi lanjut otomatis. | — Pending |
| Archive plan ke-3+ | Keep archive, bisa di-activate kalau primary/challenger gagal. | — Pending |
| English brief supported | Bilingual. Prompt tetap Indonesian, brief bisa English. | — Pending |

---
*Last updated: 2026-06-10 after architecture design*
