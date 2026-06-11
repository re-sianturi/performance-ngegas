# LP Step 08 Fix — Multi-File Structure + Persuasion Framework (Revised)

## Issue Summary

User complaint: LP output cuma 1 file HTML self-contained, section cuma 6 (hero, problem, value, why, FAQ, CTA), nggak persuasif, nggak ada img/ folder, nggak ada scroll retention / psychology.

Root cause (3 masalah konflik di skill):
1. **Schema cuma define `file_path: string`** — agent terpaksa output 1 file per variant
2. **Prompt 08 tidak reference CRO Plan sama sekali** — agent tidak tahu `recommended_section_order` dari step 07 harus jadi blueprint
3. **Prompt bilang "Jangan memaksa jumlah section"** — agent jadi minimalis, cuma 6 section

## User Requirements (Session Corrections)

1. **No `js/` folder.** Vanilla JS inside HTML files only. No separate JS files.
2. **CSS allowed.** Tailwind CDN default, optional `css/style.css` if needed.
3. **No rigid 12+ section table.** Sections are dynamic per offer — `recommended_section_order` from CRO Plan is the blueprint.
4. **CRO Plan is single source of truth for copywriting.** Prompt 08 does NOT need a Copywriter role. Prompt 08 just orchestrates the CRO Plan output.
5. **Prompt 08 must reference CRO Plan explicitly.** Input = `07-cro/plans/plan-01.json` + `recommended_section_order`.
6. **Progressive disclosure + persuasion completeness QA gate = agreed.**
7. **QA gate must be detailed per role and offer from chosen plan hook.**
8. **Auto-jalan checkpoint (Option B).** Orchestrator logs summary to chat, pipeline continues.

## Fix: Schema-08.json (Revised)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Landing Page Implementation",
  "description": "Output schema for Step 08: Landing Page Builder — multi-file variant, CRO Plan driven",
  "type": "object",
  "required": ["metadata", "variants", "assets", "confidence_scores"],
  "properties": {
    "metadata": {
      "type": "object",
      "required": ["step", "agent", "timestamp", "brief_hash", "cro_plan_ref"],
      "properties": {
        "step": { "type": "string", "enum": ["08"] },
        "agent": { "type": "string", "enum": ["agent-08"] },
        "timestamp": { "type": "string", "format": "date-time" },
        "brief_hash": { "type": "string" },
        "cro_plan_ref": { "type": "string", "description": "Path to CRO plan used as blueprint" }
      }
    },
    "variants": {
      "type": "array",
      "maxItems": 2,
      "items": {
        "type": "object",
        "required": ["variant_name", "type", "components_included", "html_summary", "files", "section_order_source"],
        "properties": {
          "variant_name": { "type": "string" },
          "type": { "type": "string", "enum": ["primary", "challenger"] },
          "components_included": { "type": "array", "items": { "type": "string" } },
          "html_summary": { "type": "string" },
          "section_order_source": { "type": "string", "description": "Must reference 07-cro/plans/plan-XX.json recommended_section_order" },
          "files": {
            "type": "array",
            "description": "All files that make up this variant. index.html must be first. Each section is its own file. Dynamic count based on recommended_section_order.",
            "items": {
              "type": "object",
              "required": ["file_type", "file_path"],
              "properties": {
                "file_type": { "type": "string", "enum": ["index", "section", "asset", "style"] },
                "file_path": { "type": "string" },
                "section_name": { "type": "string", "description": "Human-readable section name from CRO Plan" }
              }
            }
          }
        }
      }
    },
    "assets": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["asset_type", "description", "required"],
        "properties": {
          "asset_type": { "type": "string", "enum": ["image", "video", "copy", "icon", "form"] },
          "description": { "type": "string" },
          "required": { "type": "boolean" }
        }
      }
    },
    "confidence_scores": {
      "type": "object",
      "required": ["overall", "primary", "challenger"],
      "properties": {
        "overall": { "type": "number", "minimum": 0, "maximum": 1 },
        "primary": { "type": "number", "minimum": 0, "maximum": 1 },
        "challenger": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    }
  }
}
```

## Fix: Prompt 08-landing-page-builder.md (Revised Sections)

### INPUT (Replace)

```
# INPUT

Agent WAJIB membaca file-file berikut sebelum generate LP:

1. `07-cro/plans/plan-01.json` (primary plan) — ambil:
   - `recommended_section_order` → ini adalah urutan section yang HARUS diimplementasi
   - `conversion_psychology` (dominant_desire, dominant_fear, dominant_pain, dominant_objection, trust_requirement)
   - `conversion_strategy` (core_promise, unique_mechanism, trust_strategy, proof_strategy, risk_reduction_strategy, offer_strategy, cta_strategy)
   - `messaging_hierarchy` (primary_message, secondary_messages, emotional_messages, proof_messages, conversion_messages)
   - `landing_page_recommendation` (hero_strategy, mechanism_strategy, objection_strategy, proof_placement_strategy, cta_placement_strategy)

2. `06-strategy/strategic-positioning.json` — positioning context
3. `05-motivation/customer-motivation.json` — behavioral triggers

**Rule:** Jangan invent section yang tidak ada di `recommended_section_order`. Jangan skip section yang ada di `recommended_section_order`.
```

### ROLE (Revised — No Copywriter)

```
# ROLE: Landing Page Implementation Engineer

Kamu adalah agen eksekusi yang mengubah CRO Plan (Step 07) jadi HTML/CSS.

**Role stack:**
* UI/UX Designer — layout, visual hierarchy, interaction, mobile
* Conversion-Focused Web Designer — persuasion layout, CTA placement, trust signals
* Front-End Engineer — clean HTML, Tailwind CSS, semantic markup
* Visual Designer — typography, color, spacing, imagery

**Tidak perlu:** Direct Response Copywriter atau Behavioral Economist. CRO Plan sudah define semua copywriting strategy dan psychology. Kamu cukup ORCHESTRASI output CRO Plan menjadi visual + code.

**Fokus tambahan:**
* Progressive disclosure (scroll triggers, curiosity gaps, retention hooks)
* Visual execution of `conversion_psychology` (fear → urgency, desire → benefit viz, pain → empathy, objection → counter-proof, trust → credibility signals)
* Scroll retention mechanics (sticky CTAs, micro-commitments, visual momentum)
* Multi-file structure: `index.html` + `section/*.html` + `img/`
```

### SECTION ARCHITECTURE (Dynamic — CRO Plan Driven)

```
# SECTION ARCHITECTURE (FLEKSIBEL PER OFFER)

**Blueprints:** `recommended_section_order` dari `07-cro/plans/plan-01.json`

Contoh CRO Plan A: ["hero", "problem", "mechanism", "proof", "faq", "cta", "footer"]
Contoh CRO Plan B: ["hero", "story", "ingredients", "science", "testimonial", "guarantee", "urgency", "cta", "footer"]

**Setiap item di `recommended_section_order` = 1 file di `section/<name>.html`.**

**Rules:**
- Jangan tambah section yang tidak ada di `recommended_section_order`
- Jangan skip section yang ada di `recommended_section_order`
- Setiap section harus punya "scroll hook" — elemen visual/copy yang membuat visitor scroll ke bawah
- Emotional arc harus coherent: problem → agitation → solution → proof → CTA (di-level page, tidak harus per section)
- Kalau `recommended_section_order` hanya 6 section, itu valid. Kalau 15, itu juga valid.
```

### FILE STRUCTURE (Revised — No js/)

```
# FILE STRUCTURE (WAJIB MULTI-FILE, NO JS FOLDER)

```
08-lp/
  index.html                    ← shell yang include semua section
  section/
    <name>.html                 ← 1 file per item di recommended_section_order
  img/
    prompts.md                  ← prompt untuk generate gambar per section
  css/
    style.css                   ← optional, kalau butuh custom CSS di luar Tailwind
  landing-page.json             ← metadata schema
```

**Constraints:**
- **NO `js/` folder.** Vanilla JS allowed inside HTML files only (<script> tag inline).
- CSS allowed: Tailwind CDN default, optional `css/style.css`.
- **JANGAN output 1 file HTML self-contained.**

**Alasan:**
- 1 file gede = susah edit, susah A/B test per section
- Component splitting = bisa reuse antara primary dan challenger
- `img/prompts.md` = designer bisa generate asset yang sesuai
- `index.html` sebagai shell = gampang rearrange section
```

### OUTPUT FORMAT (Add Part 5 — Persuasion Completeness)

```
## PART 5 — PERSUASION COMPLETENESS CHECK

Sebelum final, cek:
- [ ] Semua section dari `recommended_section_order` ada di `section/`
- [ ] `conversion_psychology` visually executed (fear → urgency, desire → benefit, pain → empathy, objection → counter-proof, trust → credibility)
- [ ] `messaging_hierarchy` present in copy (primary → hero, secondary → body, emotional → headlines, proof → testimonials, conversion → CTAs)
- [ ] `hero_strategy`, `mechanism_strategy`, `objection_strategy`, `proof_placement_strategy`, `cta_placement_strategy` from CRO Plan faithfully implemented
- [ ] Progressive disclosure: page unfolds like a story, complexity hidden until trust built, proof after desire activated, CTA after objection neutralized
- [ ] Social proof: minimal 1 testimonial + 1 stat (atau kualitatif jika ga ada data)
- [ ] Risk reversal: guarantee/refund/return policy visible
- [ ] Urgency: genuine (batch terbatas real, early bird, bonus period) — NO fake scarcity
- [ ] Multi-file: index.html + section/ + img/ exist
- [ ] Image prompts: img/prompts.md ada
- [ ] Tracking placeholder: Meta Pixel, GA4, CAPI inline di HTML (not separate JS file)
```

## QA Gate Update (Step 09)

```
- [ ] Persuasion completeness: semua section dari recommended_section_order ada
- [ ] Emotional arc: pain → agitation → solution → proof → CTA
- [ ] CRO Plan strategy execution: hero, mechanism, objection, proof, CTA placement
- [ ] Conversion psychology visually executed: fear, desire, pain, objection, trust
- [ ] Messaging hierarchy present in copy
- [ ] Objection handling: minimal 3 objections addressed
- [ ] Social proof: testimonial + stat/kualitatif
- [ ] Risk reversal: guarantee visible
- [ ] Urgency: genuine (no fake scarcity)
- [ ] Multi-file structure: index.html + section/ exist
- [ ] No js/ folder (vanilla JS inline only)
- [ ] Image prompts: img/prompts.md ada
- [ ] Tracking placeholder: inline in HTML
```

## Pitfall Baru

`Prompt 08 tidak reference CRO Plan → agent tidak tahu `recommended_section_order` harus dipakai. Result: agent improvisasi section, cuma 6 section, nggak sesuai CRO Plan. Prompt HARUS wajibkan baca `07-cro/plans/plan-01.json` dan gunakan `recommended_section_order` sebagai section blueprint exact.`

`Schema lama `file_path: string` memaksa single file. Schema HARUS jadi `files: array` dengan dynamic count. Count = length(recommended_section_order) + 1 (index.html).`

`User reject js/ folder. Output LP hanya boleh HTML, CSS, dan inline vanilla JS. Tracking script harus inline di index.html, bukan file terpisah.`

`User reject mandatory 12+ section. Jumlah section = length(recommended_section_order). Fleksibel per offer. 6 section valid, 15 section valid. Yang penting: jangan skip, jangan nambah.`

`User reject Copywriter role di prompt 08. CRO Plan (step 07) sudah define semua copywriting strategy. Prompt 08 cukup ORCHESTRASI jadi HTML. Role: UI/UX + Frontend + Visual Designer. Copywriting done upstream.`

## Skill Manifest Update (Expected Output)

```
08-lp/
  ├── index.html
  ├── section/
  │   ├── <name>.html   ← 1 per item di recommended_section_order
  ├── img/
  │   ├── prompts.md
  │   └── placeholder.md
  ├── css/
  │   └── style.css (optional)
  ├── primary.html (optional self-contained fallback)
  ├── challenger.html (optional self-contained fallback)
  └── landing-page.json
```
