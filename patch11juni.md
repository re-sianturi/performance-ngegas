# Patch 11 Juni 2026 — Multi-File LP + CRO Plan as Source of Truth

## Problem yang Di-fix

1. **Schema vs Prompt kontradiksi** — Prompt minta multi-file, schema cuma support `file_path: string` (1 file). Jadinya agent terpaksa bikin single-file HTML.
2. **Prompt nggak reference CRO Plan** — Prompt 08 nggak pernah mention `cro-plan.json`, `recommended_section_order`, atau `conversion_psychology`. Agent improvisasi sendiri, jadinya section dikit dan nggak membius.
3. **"Jangan maksa jumlah section" disalah-artikan** — Agent mikir "jangan maksa" = bebas bikin dikit. Padahal maksudnya: struktur folder jangan hardcode (header/body/footer), tapi jumlah section HARUS ngikut CRO Plan.
4. **Role prompt cuma UI/UX + Engineer** — Nggak ada Direct Response Copywriter, Behavioral Economist, atau Persuasion Engineer. Jadinya copy generic.
5. **Pipeline enforce single-file** — `variants.files: [primary.html, challenger.html]` jadi aturan bawaan.

---

## File yang Diubah

### 1. `schemas/schema-08.json` (rewrite)
- Dari: `file_path: string` (1 file per variant)
- Ke: `files: array` dengan multi-file support
- Field baru:
  - `root_directory` — path root per variant
  - `files[].file_path` — relative path (index.html, section/hero.html, img/hero-bg.webp, style.css)
  - `files[].file_type` — enum: html, css, image, asset
  - `files[].section_name` — untuk file HTML di folder section/
  - `files[].description` — apa isi file ini
  - `section_order: array` — exact copy dari `recommended_section_order`
  - `metadata.cro_plan_reference` — path ke CRO Plan yang dipakai (wajib)
- `assets[].asset_type` — enum diupdate: image, video, copy, icon, form, css (script dihapus)

### 2. `prompts/08-landing-page-builder.md` (rewrite total)
- Role baru:
  - Direct Response Copywriter
  - Behavioral Economist
  - Persuasion Engineer
  - Conversion-Focused Web Designer
  - Front-End Engineer
- Section baru: **Single Source of Truth Principle**
  - Agent wajib baca `07-cro/cro-plan.json` dan `07-cro/plans/plan-01.json` sebelum nulis kode
  - Extract exact: `recommended_section_order`, `conversion_psychology`, `messaging_hierarchy`, `conversion_strategy`, `landing_page_recommendation`
  - Rule: CRO Plan bilang 15 section = build 15. Bilang 6 = build 6.
- Section baru: **Output Structure**
  - `index.html` = shell, include section sesuai `recommended_section_order`
  - `section/` = 1 file HTML per section, nama file match section name dari CRO Plan
  - `img/` = image assets
  - `style.css` = allowed
  - **NO `js/` folder. No JS files. No scripts.**
- Section baru: **Progressive Disclosure** (5 rules)
  1. Hook before explanation
  2. Desire before proof
  3. Trust before complexity
  4. Objection before CTA
  5. Micro-commitments
- Section baru: **Scroll Retention Mechanics**
  - Typography rhythm, visual breaks, sticky CTA (muncul setelah objection section), progress indicators, open loops
- Section baru: **Persuasion Completeness Mapping**
  - Tabel map tiap field CRO Plan ke visual execution (fear→urgency, desire→benefit viz, pain→empathy, dll)
- Section baru: **Copywriting Rules** (5 rules)
  - "So what?" test, answer user's question at that moment, use user's language, benefits > features, specific CTAs
- HTML requirements: HTML5, Tailwind CSS CDN, mobile-responsive, lazy loading, no JS, CSS allowed

### 3. `pipeline.yaml` (patch)
- Step 08 output diubah:
  - Dari: `files: [primary.html, challenger.html]`
  - Ke: `root_directories: [08-lp/primary/, 08-lp/challenger/]` + `expected_files: [index.html, section/*.html, img/*, style.css]`
- Step 09 input diubah:
  - Dari: `08-lp/primary.html`
  - Ke: `08-lp/primary/`, `08-lp/qa-report.json`
- Step 08-qa baru ditambah:
  - Name: "Persuasion Completeness QA Gate"
  - Agent: `agent-08-qa`
  - Input: `08-lp/`, `07-cro/cro-plan.json`
  - Output: `08-lp/qa-report.json`
  - Schema: `schema-08-qa.json`
  - 7 checks otomatis:
    1. Section Order Integrity
    2. Conversion Psychology Visual Execution
    3. Messaging Hierarchy Presence
    4. CRO Plan Strategy Fidelity
    5. Progressive Disclosure
    6. No JS Folder
    7. Max 2 Variants

### 4. `references/landing-page-constraints.md` (patch)
- Section baru: **Persuasion Completeness QA Gate**
  - 7 checklist detail (sama kayak pipeline.yaml)
  - Scoring rules: tiap check 0.0–1.0, < 0.8 trigger fixer loop (max 2 retries)
  - Auto-fail: `js/` folder exists, missing section dari `recommended_section_order`

---

## Apa yang Berubah di Output LP

### Sebelum (broken)
```
08-lp/
├── primary.html      # 1 file self-contained, 6 section generic
└── challenger.html   # 1 file self-contained, 6 section generic
```

### Sesudah (fixed)
```
08-lp/
├── primary/
│   ├── index.html
│   ├── section/
│   │   ├── hero.html
│   │   ├── problem.html
│   │   ├── mechanism.html
│   │   ├── proof.html
│   │   ├── faq.html
│   │   ├── cta.html
│   │   └── footer.html
│   ├── img/
│   │   └── hero-bg.webp
│   └── style.css
└── challenger/
    ├── index.html
    ├── section/
    │   ├── hero.html
    │   ├── problem.html
    │   ├── mechanism.html
    │   ├── proof.html
    │   ├── faq.html
    │   ├── cta.html
    │   └── footer.html
    ├── img/
    └── style.css
```

Note: Section names di `section/` fleksibel per offer — nggak hardcode. Ngikut `recommended_section_order` dari CRO Plan.

---

## Yang Belum Diubah / Butuh Decision

| Item | Status | Action |
|------|--------|--------|
| `schema-08-qa.json` | Belum dibuat | Direference di pipeline.yaml, perlu dibikin |
| `SKILL.md` | Belum diupdate | Mungkin perlu mention step 08-qa |
| GitHub repo | Belum ada | Skill ini belum di-init sebagai git repo |

---

## Author
Patch dikerjakan 11 Juni 2026 oleh Ucok (Sapi).
