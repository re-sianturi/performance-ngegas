# Run Patterns — Performance NgeGAS Orchestration

## Timeout Handling

**Rule:** `delegate_task` timeout (600s) ≠ subagent gagal. Subagent sering menulis file sebelum timeout terjadi — API call terakhir mungkin lambat tapi write_file sudah selesai.

**Prosedur:**
1. Timeout terjadi → JANGAN langsung retry
2. Jalankan `find <run_dir>/<step_dir>/ -type f -exec ls -la {} \;` untuk cek file
3. Kalau file ada dan `wc -c` > 0 → file valid, anggap step selesai
4. Kalau file kosong atau tidak ada → retry sekali
5. Kalau retry juga timeout → cek lagi. Double-timeout dengan file parsial → dispatch task kecil untuk complete missing parts

**Contoh dari run Alpha Propolis:**
- Step 06a timeout di API call 8/8 → file `competitive-analysis.json` 35KB sudah tertulis → SKIP retry
- Step 07 timeout pertama → 10/15 file tertulis → task kedua (continuation) untuk 5 remaining sections
- Step 07 timeout kedua → semua 15 file complete → SKIP retry

## Parallel Dispatch (Expert Team)

**Pattern:** Gunakan `delegate_task(tasks=[...])` dengan array of task objects, BUKAN dua `delegate_task` terpisah.

```python
# ✅ BENAR — parallel dalam satu dispatch
delegate_task(tasks=[
    {"context": "...", "goal": "STEP 06a — Competitive Analysis", "toolsets": ["file","terminal"]},
    {"context": "...", "goal": "STEP 06b — Opportunity Sizing", "toolsets": ["file","terminal"]}
])

# ❌ SALAH — dua dispatch terpisah tidak terkoordinasi
delegate_task(...)  # 06a
delegate_task(...)  # 06b (tidak parallel, blocking)
```

**Step yang pakai:** 06a + 06b (paralel) → hasil dibaca 06c (merge)

## Retry Logic

| Kondisi | Aksi |
|---------|------|
| Timeout, file lengkap | SKIP — anggap selesai |
| Timeout, file tidak ada | Retry 1x full task |
| Timeout, file parsial (beberapa missing) | Dispatch task kecil untuk complete missing parts |
| QA FAIL | Dispatch fixer, re-QA |
| QA FAIL 2x | STOP, escalate ke user |

## Post-Fix Re-QA Pattern

**Situasi:** QA report flag `NEEDS_FIX` → fix diterapkan manual (di luar fixer loop otomatis: edit file, generate missing artifact, hapus fake content).

**Masalah:** `state.json` dan `manifest.json` tidak auto-update setelah manual fix. Run stuck di `NEEDS_FIX` meski issue resolved.

**Prosedur:**
1. Setelah manual fix diterapkan, **jangan skip re-QA.**
2. Re-run QA agent (agent-09) untuk step yang di-fix saja — baca artifact hasil fix, validasi ulang.
3. Kalau re-QA PASS → update `state.json`: status step jadi `qa_passed`, `run.status` jadi `done` (kalau semua step udah complete).
4. Update `manifest.json`: step status jadi `PASS`, `overall_status` jadi `PASS`.
5. Kalau re-QA masih FAIL → tandai outstanding issues, jangan skip.

**Contoh dari Alpha Propolis:**
- QA flag 3 critical issues di Step 08 → fix diterapkan (hapus fake counter, ganti stat, generate JSON metadata)
- Re-QA **tidak** dijalankan → `state.json` stuck `NEEDS_FIX`, `manifest.json` stuck `NEEDS_FIX`
- Run terlihat complete (31 file, 753KB) tapi status tetap merah
- **Lesson:** Manual fix tanpa re-QA = pipeline gak pernah "lulus." Re-QA adalah mandatory gate — bukan optional setelah fix.

## Stat Cascade Detection

**Pattern:** Stat tanpa sumber di step riset (05) propagasi ke downstream (07 CRO, 08 LP) tanpa terdeteksi sampai QA final (09).

**Contoh:** "87% ibu melaporkan..." muncul pertama di Step 05 `behavioral_triggers`, lalu dikutip Step 07 `social_proof` section, lalu muncul di LP HTML. Tidak ada sumber di semua 3 step.

**Cara cegah:**
1. Di Step 05: kalau stat estimasi/proyeksi, tandai `[BUTUH DATA]` atau `[ESTIMASI]` eksplisit
2. Di Step 07: jangan kutip stat yang di-tandai `[BUTUH DATA]` — ganti dengan bahasa kualitatif
3. Di Step 08: cek setiap angka di LP punya trail ke sumber. Kalau gak ada → pakai "Banyak...", "Mayoritas...", "Pelanggan kami..."
4. QA Step 09: trace balik origin setiap stat numerik — kalau gak ketemu sumbernya di step manapun, flag sebagai `UNVERIFIED STATISTIC`

## Context Budget per Step

| Step | Pattern | Token Estimate | Notes |
|------|---------|---------------|-------|
| 01 | Hat System | 130K in / 23K out | Brief + persona ringan |
| 02 | Hat System | 155K in / 21K out | + Step 01 context |
| 03 | Hat System | 200K in / 28K out | + Step 01+02, paling berat di research |
| 04 | Hat System | 330K in / 20K out | 4 input files dibaca |
| 05 | Hat System | 225K in / 15K out | 5 input files, output ringkas |
| 06a+b | Expert Team | 180K in / 6K out | Parallel, masing-masing lebih kecil |
| 06c | Hat System | 260K in / 18K out | Merge 2 partial + 3 full |
| 07 | Hat System | 470K in / 31K out | Paling berat — 9 sections + 3 plans |
| 08 | Hat System | 470K in / 31K out | Baca semua sections + plans → HTML |
| 09 | QA | 760K in / 14K out | Baca semua 8 artifact + 7 schema |
