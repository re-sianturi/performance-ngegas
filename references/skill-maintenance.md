# Skill Maintenance Reference

## Problem
Ketika `pipeline.yaml` diubah (misal: step baru, struktur output baru, schema baru), SKILL.md jadi out of sync. Skill manifest adalah user-facing docs yang pertama kali dibaca. Kalau nggak sync, user bingung: pipeline-nya udah v1.0.4 tapi manifest masih bilang single-file LP.

## Impact Analysis Framework

Before patching, run this assessment:

| Question | Kalau "ya", harus di-patch |
|----------|-------------|
| Step baru ditambah? | Overview list, DAG diagram, artifact table, step chain |
| Output struktur berubah? | Folder structure, artifact table, step chain |
| Constraint baru (no js/, max 2)? | Pitfalls, LP Builder Pitfalls |
| Input/output chain berubah? | Step-by-step chain |
| Schema file baru direference? | File References table, pending items tracker |

## SKILL.md Sync Checklist (6 Lokasi)

Wajib cek semua lokasi ini setiap kali `pipeline.yaml` diubah:

1. **Overview list** (line 26-35) — Step count harus match. Step baru wajib disebut.
2. **DAG diagram** (line 47-58) — Flow harus include step baru. Format: `07 CRO ──→ 08 LP ──→ 08-qa QA Gate ──→ 09 QA Final`
3. **Artifact-First table** (line 118-128) — Output file format harus match pipeline. No `js/` kalau step-qa cek "no js folder". No `primary.html` fallback kalau output sekarang directory.
4. **Folder structure** (line 159-232) — Tree harus match. Hapus duplikasi atau outdated entry. Tambah file baru yang dihasilkan step (misal `qa-report.json`).
5. **Step-by-step chain** (line 237-248) — Input/output chain harus include step baru. Format step baru: `08-qa ← 08-lp/ + 07-cro/cro-plan.json`
6. **Pitfalls / LP Builder Pitfalls** (line 341-364) — Kalau constraint baru muncul (no-js, multi-file), update pitfall yang relevan. Jangan biarkan pitfall lama kontradiksi dengan pipeline baru.

## Patch Documentation Format

Setiap patch wajib didokumentasi di `patch{DD}{bulan}.md` (misal: `patch11juni.md`). Struktur:

```markdown
# Patch {DD} {Bulan} {YYYY} — {One-line summary}

## Problem yang Di-fix
1. {Problem 1}
2. {Problem 2}
...

## File yang Diubah
### 1. `filename` (jenis perubahan: rewrite/patch/add)
- Dari: {old state}
- Ke: {new state}
- Field baru / Section baru / Lokasi patch

## Apa yang Berubah di Output
### Sebelum
```tree
```
### Sesudah
```tree
```

## Yang Belum Diubah / Butuh Decision
| Item | Status | Action |
|------|--------|--------|
| `{filename}` | Belum dibuat | {reason} |

## Author
Patch dikerjakan {DD} {Bulan} {YYYY} oleh Ucok (Sapi).
```

## Pending Items Policy

- **Schema file yang direference tapi belum dibuat** (e.g., `schema-08-qa.json`) = LOW impact. Pipeline bisa jalan tanpa. Agent generate manual. Boleh di-skip dulu.
- **SKILL.md out of sync** = MEDIUM impact. Bikin user bingung. Wajib di-patch segera.
- **GitHub repo sync** = LOW impact. Skill tetap jalan lokal. Tapi version control wajib untuk rollback.

## Verdict Hierarchy

Kalau user minta: "patch X biar sesuai dan ga perlu revisit"

1. **SKILL.md** harus di-patch dulu (user-facing docs).
2. **patch{DD}{bulan}.md** harus di-update (audit trail).
3. **Schema file pending** boleh di-skip (bukan critical path).
4. **GitHub push** jalanin background: `git add -A && git commit && git push`.
