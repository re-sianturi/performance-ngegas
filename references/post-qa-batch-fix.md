# Post-QA Batch Fix Workflow

## When to Use

Step 09 QA menghasilkan `qa-report.json` dengan status `NEEDS_FIX`. Workflow ini
memperbaiki semua blocking issues secara batch, bukan satu-satu.

## Pattern: Scan → Fix → Verify (3 Phase)

### Phase 1: Scan (execute_code + regex)

Cari exact issues di HTML files dengan regex patterns. Output: daftar file:line
untuk setiap issue.

```python
import os, re

base = os.path.expanduser("~/.hermes/runs/performance-ngegas")
run = "RUN_DIR_NAME"
lp_dir = os.path.join(base, run, "08-lp")

patterns = {
    "issue_label": r"regex_pattern",
    "wa.me placeholder": r"wa\.me/[^0-9]",
    "fake scarcity": r"Math\.random|setInterval",
    "unverified stats": r"\d+%\s*(pria|ibu|pelanggan)",
}

for root, dirs, files in os.walk(lp_dir):
    for f in sorted(files):
        if not f.endswith('.html'):
            continue
        fp = os.path.join(root, f)
        with open(fp) as fh:
            content = fh.read()
        rel = os.path.relpath(fp, lp_dir)
        for label, pat in patterns.items():
            matches = list(re.finditer(pat, content, re.IGNORECASE))
            if matches:
                for m in matches[:2]:
                    line_num = content[:m.start()].count('\n') + 1
                    ctx = content[max(0,m.start()-40):m.end()+40].replace('\n',' ')
                    print(f"  [{label}] {rel}:{line_num} → ...{ctx}...")
```

### Phase 2: Fix (execute_code + re.sub / str.replace)

Batch fix semua issues dalam satu execute_code block. Per issue:

```python
# Simple replacement
content = content.replace('old_text', 'new_text')

# Regex replacement
content = re.sub(r'pattern', 'replacement', content)

# Conditional (only if not already present)
if "required_text" not in content.lower():
    content = content.replace('insert_point', 'insert_point\n' + NEW_CONTENT)
```

**Tips:**
- Gunakan `str.replace()` untuk exact match (lebih aman)
- Gunakan `re.sub()` untuk pattern match (lebih fleksibel)
- Combine related fixes (misal "teruji klinis — tanpa efek samping" jadi satu pattern)
- Selalu verify `content != original` sebelum write

### Phase 3: Verify (execute_code + regex scan)

Final scan untuk pastikan zero issues remain:

```python
issues = {
    "label": r"pattern",
    # ... semua patterns yang di-fix
}

all_clean = True
for root, dirs, files in os.walk(lp_dir):
    for f in sorted(files):
        if not f.endswith('.html'):
            continue
        fp = os.path.join(root, f)
        with open(fp) as fh:
            content = fh.read()
        rel = os.path.relpath(fp, lp_dir)
        for label, pat in issues.items():
            if re.search(pat, content, re.IGNORECASE):
                print(f"  ⚠ {rel}: {label}")
                all_clean = False

if all_clean:
    print("✅ ALL CLEAN")
```

## Common Fix Patterns

### Unverified Statistics
```python
# Before: "1.247+ Review ⭐4.9"
# After:  "Review Positif dari Pelanggan Marketplace"
content = re.sub(r'✅ 1\.247\+ Review ⭐4\.9', '✅ Review Positif dari Pelanggan', content)
```

### Dose Economics
```python
# Before: "Rp 350rb/bulan jadi Rp 125rb/bulan" (misleading)
# After:  "Rp 125rb/botol — lebih hemat dari suplemen terpisah"
content = re.sub(r'Rp 350rb.*?Rp 125rb/bulan', 'Suplemen terpisah jadi Rp 125rb/botol', content)
```

### Medical Disclaimer Injection
```python
DISCLAIMER = '<p class="text-xs text-gray-500 mt-2">Disclaimer: Produk ini tidak dimaksudkan untuk mendiagnosis, mengobati, menyembuhkan, atau mencegah penyakit. Konsultasikan dokter sebelum menggunakan suplemen.</p>'

# Insert after first CTA button
content = content.replace('</a>', '</a>\n' + DISCLAIMER, 1)
```

### WhatsApp Placeholder (Global Replace)
```python
# Replace across ALL html files in directory
for root, dirs, files in os.walk(lp_dir):
    for f in files:
        if f.endswith('.html'):
            fp = os.path.join(root, f)
            with open(fp) as fh:
                content = fh.read()
            new = content.replace('href="https://wa.me/"', 'href="https://wa.me/NOMOR"')
            if new != content:
                with open(fp, 'w') as fh:
                    fh.write(new)
```

### Claim Softening
```python
# Absolute → qualified
content = content.replace('tanpa efek samping', 'formula alami tanpa resep dokter')
content = content.replace('teruji klinis', 'berbasis penelitian')
content = re.sub(r'87% pria merasa', 'Banyak pria melaporkan merasa', content)
```

## Pitfalls

1. **Jangan asal replace tanpa cek context.** "125" bisa muncul di harga, nomor telepon, atau angka lain. Selalu cek surrounding text.

2. **Challenger dan primary punya pola beda.** Jangan assume pattern yang sama. Scan dulu, baru fix.

3. **Fallback insertion point.** Kalau regex insert gagal (pattern gak match), coba simpler approach: `content.replace('</a>', '</a>\n' + DISCLAIMER, 1)`.

4. **Verify lintas semua file.** Pattern yang "sudah di-fix" di satu file mungkin masih ada di file lain. Final scan harus cover SEMUA .html files.

5. **WhatsApp placeholder sering lebih banyak dari yang dilaporkan QA.** QA bilang "16 lokasi", actual fix = 24. Selalu pakai global replace, bukan manual per-file.

6. **Combine related fixes.** "teruji klinis — tanpa efek samping" = 1 pattern, bukan 2. Kurangi jumlah replacement, kurangi risiko error.

## Example: Full Session Fix (June 2026)

3 runs × 2 variants = 6 LP variants, 23 files patched, 30+ issues resolved:

| Run | Issues | Files | Time |
|-----|--------|-------|------|
| Alpha Propolis | 10 | 6 | ~2 min |
| Seg-03 Pria 35+ | 5 | 5 | ~1 min |
| Seg-04 Lansia | 5 | 12 | ~30 sec |

Total execution time: <5 menit (vs manual editing 2-3 jam)
