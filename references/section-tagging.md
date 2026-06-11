# Section-Tagging: Multi-Role Output dalam Hat System

## Problem

Hat System = 1 agent, multiple roles. Tapi user perlu tau "bagian ini ditulis dari perspektif siapa?" dan "kenapa ini jadi prioritas?"

## Solusi: Section-Tagging

Tiap section dalam artifact di-tag dengan role yang sedang aktif. Agent ganti topi → tulis section dengan tag → ganti topi lagi → ulang.

## Format Tag

```markdown
### 🎯 CRO Specialist Perspective
- **Primary Goal:** Capture attention dalam 3 detik
- **Headline Strategy:** Problem-aware hook
- **Conversion Metric:** Scroll rate > 60%

### 🎨 UX Designer Perspective
- **Layout:** Full-width, centered text
- **Visual Hierarchy:** Headline H1 (42px) → Subhead (18px) → CTA Button
- **Mobile:** Stack vertical, headline 28px

### 🧪 A/B Testing Expert Perspective
- **Hypothesis:** Headline angka spesifik vs tanpa angka
- **Primary Metric:** CTR on CTA
- **Sample Size:** 1,000 visitors per variant
```

## Icon Convention

| Role | Icon | Fokus |
|------|------|-------|
| Market Researcher | 📊 | Data, sizing, segmentasi |
| Consumer Psychologist | 🧠 | Emotion, trigger, bias |
| JTBD Researcher | 🎯 | Jobs, progress, switch |
| CRO Specialist | 🎯 | Conversion, funnel, metric |
| UX Designer | 🎨 | Layout, interaction, visual |
| A/B Testing Expert | 🧪 | Hypothesis, experiment, stats |
| LP Engineer | 💻 | HTML, CSS, JS, performance |
| Competitive Analyst | ⚔️ | Competitor, landscape, gap |
| Strategic Planner | 🗺️ | Positioning, opportunity, strategy |
| QA Reviewer | ✅ | Completeness, accuracy, logic |
| Red Team | 🔴 | Adversarial, flaw, edge case |

## Rules Agent

1. **Context Carry:** Baca ulang section sebelumnya sebelum ganti topi. Referensi eksplisit: "Sekarang gue ganti topi jadi UX Designer. Tapi inget, CRO Specialist tadi bilang..."
2. **Cross-Reference Check:** Sebelum selesai, cek: apakah metric CRO bisa diukur dengan UX yang didesain? Apakah layout support CTA strategy? Apakah test variants muat di layout?
3. **Konflik Resolution:** Kalau 2 role konflik, tulis eksplisit: "⚠️ Konflik: [role A] mau X, [role B] mau Y. Resolusi: Z."

## JSON Schema untuk Tagging

```json
{
  "sections": [
    {
      "id": "01-hero",
      "section_name": "Hero",
      "roles": ["cro_specialist", "ux_designer", "ab_testing_expert"],
      "content": {
        "cro_specialist": {
          "goal": "Capture attention 3 detik",
          "headline_strategy": "Problem-aware hook",
          "conversion_metric": "Scroll rate > 60%"
        },
        "ux_designer": {
          "layout": "Full-width centered",
          "headline_size": "42px desktop, 28px mobile",
          "cta_behavior": "Hover scale 1.05"
        },
        "ab_testing_expert": {
          "hypothesis": "Headline angka spesifik vs tanpa angka",
          "primary_metric": "CTR CTA",
          "sample_size": 1000
        }
      },
      "conflicts": [],
      "coherence_check": "PASS"
    }
  ]
}
```

## Kapan Nggak Perlu Tagging

- Kalau agent cuma 1 role (no hat system) → tag tidak perlu
- Kalau step outputnya simple (contoh: 1 file persona) → tag tidak perlu
- Kalau step pakai Expert Team → tag di partial, merge agent handle koherensi
