# Landing Page Constraints

## Rule: Max 2 Variants

**Default:** 2 varian LP.
- `primary.html` — desain utama, yang dipublish pertama
- `challenger.html` — varian A/B test, yang dipublish kedua untuk testing

**Kalau minta lebih dari 2:** Wajib ada justifikasi di brief. Kalau nggak ada, default ke 2.

**Alasan:** Lebih dari 2 varian = user bingung. Cognitive load tinggi. Decision paralysis. Fokus: primary vs challenger. Itu saja.

## Folder Structure (Step 07)

```
07-lp/
├── primary.html           # Yang dipublish
├── challenger.html         # Yang di-A/B test
├── components/             # Potongan reusable
│   ├── hero-primary.html
│   ├── hero-challenger.html
│   ├── cta-primary.html
│   ├── cta-challenger.html
│   ├── header.html
│   ├── footer.html
│   ├── trust-badges.html
│   ├── social-proof.html
│   └── form.html
└── images/
    └── prompts.md           # Prompts untuk generate gambar per slide
```

## Component Splitting

**Kenapa dipecah:**
- Kalau 1 file HTML gede, susah edit.
- Component bisa di-reuse antara primary dan challenger.
- Component bisa di-test individual (A/B test per component).

**Wajib ada component:**
- Header (logo, nav)
- Hero (headline, subhead, CTA, hero image)
- CTA (button, form, urgency)
- Trust badges (guarantee, secure, certification)
- Social proof (testimonial, case study, numbers)
- Footer (links, copyright, contact)

**Bedanya primary vs challenger:**
- Biasanya: hero headline, CTA color, social proof format, urgency mechanism
- Component non-hero (header, footer) biasanya sama

## Image Prompts

Semua gambar yang perlu di-generate (hero image, testimonial photo, social proof graphic) ada di `images/prompts.md`.

Format:
```markdown
## Image 01: Hero Image
**Prompt:** "Professional photo, [product] in modern setting, warm lighting, clean background"
**Style:** Photorealistic, 16:9
**Negative:** "Cartoon, illustration, low quality"

## Image 02: Testimonial Photo
**Prompt:** "Professional headshot, Indonesian businessman, confident smile, neutral background"
**Style:** Portrait, 1:1
```

## Aesthetic Reference

**Default:** Stripe, Linear, Vercel — clean, modern, lots of whitespace, subtle gradients, bold typography.

**Kalau brief minta style lain:** Mention di component. "Style: Dark mode, neon accent, cyberpunk."

## Tech Stack

- HTML5
- Tailwind CSS via CDN
- Vanilla JavaScript (no framework)
- Mobile-responsive (min 320px)
- Google Fonts (Inter default)

## Performance Budget

- First Contentful Paint: < 1.5s
- Total page size: < 500KB (excluding images)
- Image: lazy loading, WebP format

## Persuasion Completeness QA Gate

This QA gate runs automatically after Step 08 (Landing Page Builder). It verifies that the LP faithfully executes the CRO Plan from Step 07.

### Checklist

1. **Section Order Integrity**
   - Every section name in `recommended_section_order` from the CRO Plan exists as a `.html` file in `section/`
   - The order of inclusion in `index.html` matches `recommended_section_order` exactly
   - No extra sections exist that are not in `recommended_section_order`
   - No sections from `recommended_section_order` are missing

2. **Conversion Psychology Visual Execution**
   - `dominant_fear` is visually expressed (urgency, scarcity, deadline, consequence visualization)
   - `dominant_desire` is visually expressed (benefit visualization, outcome preview, transformation)
   - `dominant_pain` is visually expressed (empathy, relatability, problem agitation)
   - `dominant_objection` is visually expressed (counter-proof, guarantee, risk reversal, FAQ)
   - `trust_requirement` is visually expressed (credibility, authority, social proof, testimonials)

3. **Messaging Hierarchy Presence**
   - `primary_message` appears in the hero headline and subheadline
   - `secondary_messages` appear in section headlines and body copy
   - `emotional_messages` appear in emotional hooks, subheads, and empathy statements
   - `proof_messages` appear in testimonials, data, studies, and numbers
   - `conversion_messages` appear in CTAs, urgency, and offer detail

4. **CRO Plan Strategy Fidelity**
   - `hero_strategy` is implemented in the hero section
   - `mechanism_strategy` is implemented in the mechanism/science section
   - `objection_strategy` is implemented in the objection/FAQ section
   - `proof_placement_strategy` is implemented in the proof/testimonial section
   - `cta_placement_strategy` is implemented in the CTA section

5. **Progressive Disclosure**
   - The page unfolds like a story (hook → desire → trust → objection → CTA)
   - No section explains the product before the user wants it
   - Proof appears only after desire is activated
   - CTA appears only after objection is neutralized
   - Micro-commitments exist between sections

6. **No JS Folder**
   - No `js/` folder exists in either variant
   - No JavaScript files exist
   - No inline `<script>` tags exist
   - CSS folder/file is allowed

7. **Max 2 Variants**
   - Only `primary` and `challenger` exist
   - No third variant unless explicitly briefed

### Scoring

- Each check scores 0.0–1.0
- Any check scoring < 0.8 triggers the fixer loop (max 2 retries)
- `js/` folder existing = automatic 0.0 for that check, immediate fail
- Missing section from `recommended_section_order` = automatic 0.0 for Section Order Integrity, immediate fail
