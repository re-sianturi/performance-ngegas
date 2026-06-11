#!/usr/bin/env python3
"""
qa-script.py — LP HTML Quality Assurance Scanner.

Scans landing page HTML files for 8 common issues found across
multiple pipeline runs. Outputs JSON summary consumable by
agent-09-lite or as standalone pre-deploy gate.

Usage:
  # Scan single run (all variants)
  python3 qa-script.py <run_dir>

  # Scan single variant directory
  python3 qa-script.py <lp_variant_dir>

  # Output JSON only (for pipeline consumption)
  python3 qa-script.py <run_dir> --json

Modes:
  1. Pre-deploy gate  — run before publishing LP
  2. Post-fix verify  — run after fixing NEEDS_FIX issues
  3. Batch QA         — parallel, feed output to agent-09-lite

8 Check Patterns:
  1. Unverified statistics (87%, 1247+, 4.9⭐)
  2. Dose economics mismatch (per bulan vs per botol)
  3. Fake scarcity (Math.random, setInterval, countdown)
  4. Missing medical disclaimer
  5. Contradictory claims (hero vs FAQ)
  6. WhatsApp placeholder (wa.me/ without number)
  7. "Teruji klinis" without source
  8. Stat cascade (unverified stats from research → LP)
"""

import json
import os
import re
import sys
from datetime import datetime


# ============================================================
# 8 CHECK PATTERNS
# ============================================================

CHECKS = {
    "unverified_stats": {
        "severity": "high",
        "patterns": [
            (r"\d+\+?\s*(?:Review|review|ulasan)", "Unverified review count"),
            (r"⭐\s*\d+\.\d+\s*(?:dari|from)", "Unverified star rating"),
            (r"\d+%\s*(?:ibu|pria|pelanggan|customer|user)", "Unverified percentage claim"),
            (r"\d+[,.]?\d*\+?\s*(?:Review|Pelanggan|Customer)", "Unverified customer count"),
        ],
        "fix": "Ganti bahasa kualitatif: 'Review positif dari pelanggan' atau 'Banyak ibu melaporkan...'",
    },
    "dose_economics": {
        "severity": "medium",
        "patterns": [
            (r"Rp\s*\d+[,.]?\d*\s*/\s*bulan\s*(?:untuk\s*)?(?:keluarga|family)", "Dose claim per month for family"),
            (r"Rp\s*\d+[,.]?\d*\s*jadi\s*Rp\s*\d+[,.]?\d*\s*/\s*bulan", "Savings claim per month"),
        ],
        "fix": "Validasi: 10ml ≈ 200 tetes ÷ (6 tetes × 3x/hari × N orang) = realistis? Gunakan 'per botol' atau 'per orang'.",
    },
    "fake_scarcity": {
        "severity": "critical",
        "patterns": [
            (r"Math\.random\s*\(", "Math.random() counter"),
            (r"setInterval\s*\(", "setInterval timer"),
            (r"setTimeout\s*\(", "setTimeout timer"),
            (r"countdown|countDown|count-down", "Countdown timer"),
            (r"(?:stok|stock)\s*(?:tinggal|sisa|terbatas).*?\d+(?:\s*pcs|\s*unit)?", "Stock limit claim"),
        ],
        "fix": "Hapus fake counter. Ganti static urgency: 'Batch terbatas' atau urgency berbasis kalender.",
    },
    "missing_disclaimer": {
        "severity": "critical",
        "patterns": [],  # Special check: absence of disclaimer
        "required_text": [
            r"tidak\s+dimaksudkan",
            r"mendiagnosis|mengobati|menyembuhkan|mencegah",
            r"konsultasikan.*dokter",
        ],
        "fix": "Tambah disclaimer: 'Produk ini tidak dimaksudkan untuk mendiagnosis, mengobati, menyembuhkan, atau mencegah penyakit. Konsultasikan dokter.'",
    },
    "contradictory_claims": {
        "severity": "high",
        "patterns": [
            (r"tanpa\s+efek\s+samping", "Absolute 'no side effects' claim"),
            (r"terbukti\s+(?:menyembuhkan|menyehatkan|ampuh)", "Proven health claim"),
            (r"100%\s*(?:aman|safe|alami|natural)", "Absolute safety claim"),
        ],
        "cross_check": {
            "tanpa efek samping": [r"efek\s+samping", r"sensasi\s+hangat", r"konsultasi"],
        },
        "fix": "Soften: 'formula alami tanpa resep dokter' atau 'umumnya ditoleransi dengan baik'. Konsistenkan hero dan FAQ.",
    },
    "wa_placeholder": {
        "severity": "critical",
        "patterns": [
            (r'href="https://wa\.me/"', "Empty wa.me/ link"),
            (r"wa\.me/\s*$", "wa.me/ at end of line"),
            (r"wa\.me/[^0-9+]", "wa.me/ without phone number"),
        ],
        "fix": "Ganti semua wa.me/ placeholder → wa.me/NOMOR_BISNIS (global replace).",
    },
    "unverified_clinical": {
        "severity": "medium",
        "patterns": [
            (r"teruji\s+klinis", "Clinically tested claim"),
            (r"terbukti\s+secara\s+ilmiah", "Scientifically proven claim"),
            (r"(?:uji|riset)\s+(?:klinis|klinik|clinical)", "Clinical trial reference"),
            (r"(?:penelitian|study|research)\s+(?:menunjukkan|membuktikan)", "Research claim"),
        ],
        "fix": "Softened: 'berbasis penelitian' atau tambah link studi spesifik.",
    },
    "stat_cascade": {
        "severity": "medium",
        "patterns": [
            (r"\d+%\s*(?:ibu|pria|pelanggan|anak|mama|ayah)", "Demographic percentage"),
            (r"\d+[,.]?\d*\s*(?:juta|million|ribu|thousand)", "Large number claim"),
        ],
        "fix": "Trace origin: kalau stat dari Step 05 tanpa sumber, hapus dari LP. Gunakan bahasa kualitatif.",
    },
}


def check_disclaimer(content):
    """Special check: disclaimer must be PRESENT, not absent."""
    issues = []
    found_patterns = 0
    for pattern in CHECKS["missing_disclaimer"]["required_text"]:
        if re.search(pattern, content, re.IGNORECASE):
            found_patterns += 1

    if found_patterns == 0:
        issues.append("Medical disclaimer MISSING entirely")
    elif found_patterns < 2:
        issues.append(f"Disclaimer partial ({found_patterns}/3 required phrases found)")

    return issues


def scan_file(filepath, variant_dir):
    """Scan single HTML file for all 8 checks."""
    with open(filepath) as f:
        content = f.read()

    rel = os.path.relpath(filepath, variant_dir)
    file_issues = []

    for check_name, check_def in CHECKS.items():
        if check_name == "missing_disclaimer":
            # Special handling
            issues = check_disclaimer(content)
            for issue in issues:
                file_issues.append({
                    "check": check_name,
                    "severity": check_def["severity"],
                    "file": rel,
                    "issue": issue,
                    "fix": check_def["fix"],
                })
            continue

        if check_name == "contradictory_claims":
            # Check for the claim
            for pattern, desc in check_def["patterns"]:
                if re.search(pattern, content, re.IGNORECASE):
                    # Cross-check: does FAQ/safety section contradict?
                    cross = check_def.get("cross_check", {})
                    for claim_pat, contradict_pats in cross.items():
                        if re.search(claim_pat, content, re.IGNORECASE):
                            for cp in contradict_pats:
                                if re.search(cp, content, re.IGNORECASE):
                                    file_issues.append({
                                        "check": check_name,
                                        "severity": check_def["severity"],
                                        "file": rel,
                                        "issue": f"{desc} — contradicted by FAQ/safety section",
                                        "fix": check_def["fix"],
                                    })
            continue

        # Standard pattern matching
        for pattern, desc in check_def.get("patterns", []):
            matches = list(re.finditer(pattern, content, re.IGNORECASE))
            if matches:
                for m in matches[:2]:  # Max 2 matches per pattern
                    ctx_start = max(0, m.start() - 30)
                    ctx_end = min(len(content), m.end() + 30)
                    context = content[ctx_start:ctx_end].replace("\n", " ").strip()
                    file_issues.append({
                        "check": check_name,
                        "severity": check_def["severity"],
                        "file": rel,
                        "issue": desc,
                        "context": f"...{context}...",
                        "fix": check_def["fix"],
                    })

    return file_issues


def scan_variant(variant_dir):
    """Scan all HTML files in a variant directory."""
    all_issues = []
    file_count = 0
    word_count = 0

    if not os.path.isdir(variant_dir):
        return {"error": f"Directory not found: {variant_dir}"}

    for root, dirs, files in os.walk(variant_dir):
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            fp = os.path.join(root, f)
            file_count += 1
            with open(fp) as fh:
                word_count += len(fh.read().split())
            issues = scan_file(fp, variant_dir)
            all_issues.extend(issues)

    # Deduplicate same issue in same file
    seen = set()
    unique_issues = []
    for issue in all_issues:
        key = (issue["check"], issue["file"], issue["issue"])
        if key not in seen:
            seen.add(key)
            unique_issues.append(issue)

    # Determine status
    critical = [i for i in unique_issues if i["severity"] == "critical"]
    high = [i for i in unique_issues if i["severity"] == "high"]

    if critical:
        status = "FAIL"
        confidence = 0.3
    elif high:
        status = "NEEDS_FIX"
        confidence = 0.6
    elif unique_issues:
        status = "NEEDS_FIX"
        confidence = 0.75
    else:
        status = "PASS"
        confidence = 0.95

    return {
        "variant": os.path.basename(variant_dir),
        "status": status,
        "confidence": confidence,
        "files_scanned": file_count,
        "word_count": word_count,
        "issues": unique_issues,
        "issue_count": len(unique_issues),
        "critical_count": len(critical),
        "high_count": len(high),
    }


def scan_run(run_dir):
    """Scan full run (primary + challenger)."""
    run_id = os.path.basename(run_dir)
    lp_dir = os.path.join(run_dir, "08-lp")

    if not os.path.isdir(lp_dir):
        return {"error": f"08-lp/ not found in {run_dir}"}

    results = {
        "metadata": {
            "tool": "qa-script.py",
            "version": "2.0",
            "timestamp": datetime.now().isoformat(),
            "run_id": run_id,
        },
        "variants": {},
        "overall_status": "PASS",
        "summary": {
            "total_issues": 0,
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        },
    }

    for variant in ["primary", "challenger"]:
        variant_dir = os.path.join(lp_dir, variant)
        if os.path.isdir(variant_dir):
            result = scan_variant(variant_dir)
            results["variants"][variant] = result

            if result.get("status") == "FAIL":
                results["overall_status"] = "FAIL"
            elif result.get("status") == "NEEDS_FIX" and results["overall_status"] != "FAIL":
                results["overall_status"] = "NEEDS_FIX"

            results["summary"]["total_issues"] += result.get("issue_count", 0)
            results["summary"]["critical"] += result.get("critical_count", 0)
            results["summary"]["high"] += result.get("high_count", 0)

    return results


def print_report(results):
    """Print human-readable report."""
    print("=" * 60)
    print(f"QA SCAN: {results['metadata']['run_id']}")
    print(f"Status: {results['overall_status']}")
    print("=" * 60)

    for variant_name, variant_data in results["variants"].items():
        print(f"\n  [{variant_name.upper()}] {variant_data['status']} (conf={variant_data.get('confidence', '?')})")
        print(f"  Files: {variant_data.get('files_scanned', 0)}, Words: {variant_data.get('word_count', 0)}")

        if not variant_data.get("issues"):
            print("  ✅ No issues found")
            continue

        for issue in variant_data["issues"]:
            sev = issue["severity"].upper()
            print(f"  ⚠ [{sev}] {issue['file']}: {issue['issue']}")
            if issue.get("context"):
                print(f"    Context: {issue['context']}")
            print(f"    Fix: {issue['fix']}")

    print(f"\n{'=' * 60}")
    print(f"TOTAL: {results['summary']['total_issues']} issues "
          f"({results['summary']['critical']} critical, {results['summary']['high']} high)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <run_dir_or_variant_dir> [--json]")
        print(f"Example: {sys.argv[0]} ~/.hermes/runs/performance-ngegas/2026-06-11_010541_segment-01-muslim-taqwa")
        sys.exit(1)

    target = os.path.expanduser(sys.argv[1])
    json_mode = "--json" in sys.argv

    if os.path.basename(target) in ("primary", "challenger"):
        # Single variant
        result = scan_variant(target)
        if json_mode:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"Variant: {result.get('variant')} — {result.get('status')}")
            for issue in result.get("issues", []):
                print(f"  [{issue['severity'].upper()}] {issue['file']}: {issue['issue']}")
    else:
        # Full run
        results = scan_run(target)
        if json_mode:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print_report(results)
