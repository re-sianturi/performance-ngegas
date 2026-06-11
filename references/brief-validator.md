# Brief Validator: Pre-Flight Gate

## Purpose

Sebelum pipeline start, brief wajib lolos validasi. Brief yang kopas dari chat client (formatting aneh, putus-putus, terlalu pendek) akan menghasilkan output sampah dan membuang token.

## Checklist (5 Element Brief)

Brief harus punya ≥ 3 dari 5 elemen ini:

1. **Produk / Jasa** — Apa yang dijual? Digital product? Physical? Service?
2. **Target Market** — Siapa yang beli? Implisit atau eksplisit. Kalau nggak ada, infer dari produk.
3. **Masalah yang Dipecahkan** — Apa pain point customer? Apa yang mereka cari solusi?
4. **Value Proposition** — Kenapa produk ini worth it? Benefit utama apa?
5. **Call to Action / Tujuan** — Mau apa? Jual? Lead? Brand awareness? Educate?

## Validation Rules

| Elemen | Detect | Fail Action |
|--------|--------|-------------|
| Produk | Mention product name atau kategori | "Brief tidak menyebutkan produk/jasa. Tambahkan deskripsi produk." |
| Target Market | Mention audience, segment, atau bisa diinfer | "Target market tidak jelas. Tambahkan siapa yang mau beli." |
| Masalah | Mention problem, pain, atau challenge | "Tidak ada masalah yang diselesaikan. Tambahkan apa yang bikin customer frustrasi." |
| Value Prop | Mention benefit, advantage, atau differentiator | "Value proposition tidak jelas. Kenapa customer harus pilih produk ini?" |
| CTA / Tujuan | Mention goal, objective, atau desired outcome | "Tujuan tidak jelas. Mau convert? Lead? Awareness?" |

## Kalau Brief Kurang

**STOP.** Jangan lanjut pipeline. Report ke user:

> "Brief belum lolos pre-flight gate. Kurang X elemen dari 5. Detail: [list]. Perbaiki brief dulu, lalu paste ulang."

## Kalau Brief Valid

**Proceed.** Simpan ke:
- `00-input/BRIEF.md` (raw text dari user)
- `00-input/BRIEF.json` (parsed: extract 5 elemen + meta)

## Parsed JSON Structure

```json
{
  "brief_id": "2026-06-10_150305",
  "raw_text": "...",
  "elements": {
    "product": {"detected": true, "text": "..."},
    "target_market": {"detected": true, "text": "..."},
    "problem": {"detected": false, "text": "..."},
    "value_proposition": {"detected": true, "text": "..."},
    "cta_goal": {"detected": false, "text": "..."}
  },
  "score": "3/5",
  "valid": true,
  "assumptions": ["Target market diinfer dari produk"]
}
```

## Edge Cases

- **Brief sangat pendek (< 100 kata):** FAIL. "Brief terlalu pendek. Minimal 100 kata untuk validasi."
- **Brief formatting aneh (copy-paste dari chat):** Parse. Kalau nggak bisa parse, FAIL.
- **Brief dalam bahasa selain Indonesia:** Translate dulu ke Indonesia. Tag: "Translated from [language]."
- **Brief ada tapi kurang 2 elemen:** Ask user. "Brief kurang [list]. Bisa asumsikan atau perlu diperjelas?"
