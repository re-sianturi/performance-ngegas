# LP Integrity Rules — Performance NgeGAS

Aturan integritas untuk landing page yang di-generate Step 08. Red Team akan mengaudit ini di Step 09.

## Fake Scarcity — DILARANG

❌ **JANGAN:**
- `Math.random()` counter decrement ("Stok tinggal 3... 2... 1...")
- Countdown timer yang reset setiap reload
- "Hanya tersisa X botol!" tanpa basis data inventory real
- "Diskon berakhir dalam 00:05:00" yang tidak benar-benar berakhir

✅ **BOLEH:**
- Batch terbatas berbasis real ("Batch #3 hanya 500 botol — produksi terbatas propolis Trigona musiman")
- Harga early bird dengan deadline jelas ("Harga early bird sampai 30 Juni 2026")
- Bonus periode ("Gratis ongkir untuk 100 order pertama bulan ini")
- Social proof urgency ("1,247+ ibu sudah join Alpha Moms Community")

**Rasionale:** Trust adalah CORE positioning Alpha Propolis (BPOM, transparansi, garansi 30 hari). Fake scarcity = trust contradiction = conversion killer jangka panjang.

## Statistik — WAJIB SUMBER

❌ **JANGAN:**
- Angka presisi tanpa sumber ("87% ibu melaporkan anak lebih jarang sakit dalam 30 hari")
- Propagate angka dari Step 05 ke LP tanpa verifikasi
- "Terbukti secara klinis" tanpa menyebut studi

✅ **BOLEH:**
- Bahasa kualitatif: "Banyak ibu melaporkan anak lebih jarang sakit setelah rutin konsumsi"
- Placeholder: `[BUTUH DATA: Studi klinis propolis — cek PubMed]`
- Statistik bersumber: "Studi dari Journal of Ethnopharmacology (2019) menunjukkan propolis meningkatkan..." dengan link/citation
- Angka umum: "Mengandung 67% Propolis Apis + 33% Propolis Trigona" (fakta produk, bukan klaim hasil)

**Rasionale:** Risiko BPOM. Suplemen di Indonesia tidak boleh klaim "menyembuhkan" atau menggunakan statistik hasil tanpa evidence. Brief sendiri menyebut: "Gunakan kalimat 'membantu' atau 'mendukung', bukan 'menyembuhkan'."

## Trust Signals — WAJIB REAL

✅ **HARUS ADA:**
- BPOM registration number: POM TR 213656281 (link ke cek BPOM)
- Garansi: 30 hari uang kembali
- Komposisi transparan: Apis 67%, Trigona 33%
- Testimoni dengan identitas (nama + kota, bukan "Ibu R***")

❌ **JANGAN:**
- Testimoni fiktif tanpa identitas
- "Rekomendasi dokter" tanpa nama dokter spesifik
- Sertifikasi palsu ("Halal MUI" kalau belum ada)

## Urgency — Berbasis Real

✅ **BOLEH:**
- Harga early bird dengan deadline
- Bonus periode terbatas
- Bundle savings (1 botol vs 2 vs 4 — "Hemat 25% untuk Family Bundle")
- Social proof ("Baru saja dibeli oleh Ibu Dewi dari Bandung")

❌ **JANGAN:**
- Fake countdown
- Stok palsu
- "Harga akan naik besok" yang tidak benar
