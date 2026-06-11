# Agent Patterns: Hat System vs Expert Team

## Hat System (1 Agent, Multi-Role)

**Pakai kalau SEMUA kondisi terpenuhi:**

| # | Kriteria | Alasan |
|---|----------|--------|
| 1 | Output wajib **1 artifact kohesif**. Nggak bisa dipecah jadi partial. | Kalau pecah, merge-nya harus re-align semua section. Overhead > benefit. |
| 2 | Role-role di **domain adjacent** (sama atau mirip). | 1 agent bisa hold context. Nggak perlu "onboarding" domain baru. |
| 3 | Tiap bagian output **butuh konteks bagian lain**. | Section A harus align dengan Section B. Kalau agent beda, nanti contradict. |
| 4 | Nggak ada **konflik fundamental** antar role. | Nggak perlu mediasi. |
| 5 | Speed lebih penting dari **depth spesifik**. | Hat System lebih cepat. Kalau step bukan strategic bottleneck, nggak usah parallel. |

**Langkah eksekusi:**
1. Agent mulai dengan Primary Role
2. Sebelum ganti topi, baca ulang output yang sudah ditulis
3. Tulis section baru dengan tag role: `### [Icon] Role Name Perspective`
4. Cross-reference: cek apakah section baru align dengan section sebelumnya
5. Kalau konflik, tulis konflik dan resolusi dalam artifact
6. Primary Role review keseluruhan di akhir

## Expert Team (Parallel + Merge)

**Pakai kalau SALAH SATU kondisi terpenuhi:**

| # | Kriteria | Alasan |
|---|----------|--------|
| 1 | Output bisa dipecah jadi **2+ partial independen**. | Partial A dan B bisa jalan bareng tanpa saling tunggu. |
| 2 | Role di **domain yang benar-benar beda**. | Beda framework. |
| 3 | Butuh **depth spesifik** yang 1 agent nggak bisa hold. | 1 agent nggak bisa jadi expert A + expert B dalam 1 turn. |
| 4 | Hasil partial bisa di-**cross-validate** sebelum merge. | 2 expert ngasih angle beda. Merge agent bisa spot bias. |
| 5 | Step ini adalah **strategic bottleneck** atau **pivot point**. | Salah di sini = downstream semua salah. |

**Langkah eksekusi:**
1. Spawn Agent A dan Agent B secara parallel (tiap agent dapat brief + input file)
2. Agent A menghasilkan `partial-a.json`
3. Agent B menghasilkan `partial-b.json`
4. Spawn Agent C (Merge Agent) dengan input: `partial-a.json` + `partial-b.json`
5. Agent C menghasilkan `artifact.json` final
6. QA Gate di `artifact.json` final

## Step Mapping (Performance NgeGAS)

| Step | Pattern | Role | Why |
|------|---------|------|-----|
| 01 | Hat System | Senior Market Researcher + Consumer Psychologist | 1 artifact: target market profile |
| 02 | Hat System | JTBD Analyst (Christensen-Moesta) | 1 artifact: JTBD analysis |
| 03 | Hat System | JTBD Analyst v2 (Deep Job Map) | 1 artifact: cross-reference + deep map |
| 04 | Hat System | Anthropologist / Role Profiler | 1 artifact: life role database |
| 05 | Hat System | Behavioral Economist | 1 artifact: motivation database |
| 06 | **Expert Team** | Competitive Analyst + Opportunity Sizer → Strategic Planner | 2 domain beda + strategic bottleneck |
| 07 | Hat System | CRO Specialist + UX Designer + A/B Testing Expert | 1 plan kohesif, domain adjacent, section-tagged |
| 08 | Hat System | Landing Page Engineer | 1 artifact: HTML halaman |
| 09 | Hat System | QA Lead + Red Team Adversarial | 1 artifact: verdict + audit |

## Role Tagging in Hat System (Section-Level)

Walaupun 1 agent, output di-tag per role di setiap section. Ini penting untuk **Step 07** di mana 3 role punya output audience berbeda:

| Tag | Audience | Role | Dikonsumsi Step Berikutnya |
|-----|----------|------|---------------------------|
| `[FOR-PIPELINE]` | Step 08 LP | CRO Specialist + UX Designer | Ya |
| `[FOR-HUMAN]` | User referensi | A/B Testing Expert | Tidak |

**Langkah eksekusi section-tagging:**
1. Agent mulai dengan Primary Role
2. Sebelum ganti topi, baca ulang output yang sudah ditulis
3. Tulis section baru dengan tag role: `### [Icon] Role Name Perspective [FOR-PIPELINE|FOR-HUMAN]`
4. Cross-reference: cek apakah section baru align dengan section sebelumnya
5. Kalau konflik, tulis konflik dan resolusi dalam artifact
6. Primary Role review keseluruhan di akhir

## Anti-Patterns

- **Jangan parallel semua step.** Overhead merge lebih mahal dari benefit.
- **Jangan hat system kalau role benar-benar beda domain.** Contoh: Data Scientist + Creative Director = 2 otak.
- **Jangan expert team kalau output harus kohesif.** Merge agent akan kehilangan nuansa.
- **Jangan lupa tag `[FOR-PIPELINE]` vs `[FOR-HUMAN]`.** Kalau A/B Testing Expert output masuk ke Step 08, pipeline akan error (non-structured output di HTML builder).
