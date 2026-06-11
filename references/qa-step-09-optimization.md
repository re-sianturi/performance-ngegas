# Step 09 QA Optimization — Chunked Audit Pattern

## Problem Statement

Step 09 QA (Final QA & Red Team Audit) mengalami **systematic timeout dan max_iterations failure** saat dijalankan dalam batch untuk multiple runs.

**Evidence dari log (June 2026):**
- Task 0 (Alpha Propolis): Timeout 600s, 22 API calls — stuck di file reads
- Task 1 (Muslim Taqwa): Completed tapi 581s, 496K input tokens — barely made it  
- Task 2 (Diabetes Ginjal): Failed max_iterations — kehabisan iterasi karena baca file terus

## Root Cause Analysis

| Issue | Evidence | Impact |
|-------|----------|--------|
| **Artifact bloat** | 52 KB steps 00-07 + 66 KB LP files = **118 KB per run** | Context window overload |
| **Redundant file reads** | Subagent baca SEMUA file 00-07 untuk tiap run | 500K+ tokens per task |
| **Schema-09 over-spec** | Requires `minItems: 8` step_audits + detailed red_team_findings | Forced verbose output |
| **No streaming/chunking** | Single write_file untuk report 8K+ bytes | Memory spike |

**Pattern dari log:**
- Subagent timeout bukan karena "thinking" lama, tapi karena **baca file terus-menerus**
- Tiap file read = 1 tool call, tiap tool call = context accumulation
- 8 steps × 3-4 files per step = 24-32 file reads sebelum generate output

## Solution: Chunked QA Pattern

### Phase 1: Pre-Compress (Orchestrator)

Generate `09-qa/audit-input.json` yang isinya **extracted key data only**:

```json
{
  "run_metadata": {
    "run_id": "2026-06-11_010541_segment-01-muslim-taqwa",
    "brief_hash": "sha256:abc123...",
    "segment": "Muslim Taqwa",
    "timestamp": "2026-06-11T01:05:41Z"
  },
  "cro_highlights": {
    "selected_plans": ["plan-01", "plan-02"],
    "section_order": ["hero", "social-proof", "mechanism", "offer", "faq", "cta"],
    "key_messaging": "Family immune support with Sunnah alignment",
    "trust_elements": ["BPOM", "MUI Halal", "Adab Klaim"],
    "urgency_type": "early-bird-real"
  },
  "lp_structure": {
    "primary": {
      "sections": 9,
      "total_words": 1247,
      "has_js": false,
      "has_fake_scarcity": false,
      "bpom_present": true,
      "disclaimer_present": true
    },
    "challenger": {
      "sections": 9,
      "total_words": 1189,
      "has_js": false,
      "has_fake_scarcity": false,
      "bpom_present": true,
      "disclaimer_present": true
    }
  },
  "critical_flags": []
}
```

**Size:** ~5 KB (dari 118 KB = **96% reduction**)

**Script untuk generate:**
```python
# scripts/generate-audit-input.py
import json, os, re

def extract_lp_structure(lp_dir):
    structure = {"sections": 0, "total_words": 0, "has_js": False}
    for root, dirs, files in os.walk(lp_dir):
        for f in files:
            if f.endswith('.html'):
                with open(os.path.join(root, f)) as file:
                    content = file.read()
                    structure["total_words"] += len(content.split())
                    if '<script' in content or 'Math.random()' in content:
                        structure["has_js"] = True
    structure["sections"] = len([f for f in os.listdir(lp_dir) if f.endswith('.html')])
    return structure

def generate_audit_input(run_dir):
    # Read cro-plan.json
    with open(os.path.join(run_dir, "07-cro", "cro-plan.json")) as f:
        cro = json.load(f)
    
    # Extract highlights
    audit_input = {
        "run_metadata": {...},
        "cro_highlights": {
            "selected_plans": [p["plan_id"] for p in cro["plans"] if p.get("selected_for_execution")],
            "section_order": cro.get("sections", []),
            "trust_elements": extract_trust_elements(cro)
        },
        "lp_structure": {
            "primary": extract_lp_structure(os.path.join(run_dir, "08-lp", "primary")),
            "challenger": extract_lp_structure(os.path.join(run_dir, "08-lp", "challenger"))
        }
    }
    
    with open(os.path.join(run_dir, "09-qa", "audit-input.json"), "w") as f:
        json.dump(audit_input, f, indent=2)
```

### Phase 2: Lightweight QA (Subagent)

Subagent baca `audit-input.json` + `schema-09-lite.json`:

**Schema-09-lite (minimal):**
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["metadata", "variant_audits", "overall_status"],
  "properties": {
    "metadata": {
      "type": "object",
      "properties": {
        "step": {"enum": ["09"]},
        "agent": {"enum": ["agent-09-lite"]},
        "timestamp": {"type": "string"},
        "brief_hash": {"type": "string"}
      }
    },
    "variant_audits": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["variant", "status", "confidence", "blocking"],
        "properties": {
          "variant": {"enum": ["primary", "challenger"]},
          "status": {"enum": ["PASS", "NEEDS_FIX", "FAIL"]},
          "confidence": {"type": "number", "minimum": 0, "maximum": 1},
          "critical_issues": {"type": "array", "items": {"type": "string"}},
          "blocking": {"type": "boolean"}
        }
      }
    },
    "overall_status": {"enum": ["PASS", "NEEDS_FIX", "FAIL"]},
    "fix_recommendations": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "variant": {"type": "string"},
          "issue": {"type": "string"},
          "severity": {"enum": ["critical", "high", "medium", "low"]},
          "recommendation": {"type": "string"}
        }
      }
    }
  }
}
```

**Task description untuk subagent:**
```
Goal: Run lightweight QA for {run_id}

Input files:
- 09-qa/audit-input.json (pre-compressed, ~5KB)
- schemas/schema-09-lite.json

Do NOT read:
- 00-input/brief.json
- 01-06 artifacts
- 07-cro/cro-plan.json (sudah di-audit-input)
- 08-lp/*.html (sudah di-lp_structure summary)

Output:
- 09-qa/qa-report-lite.json

Checks:
1. CRO plan alignment (dari audit-input.cro_highlights)
2. LP structure compliance (dari audit-input.lp_structure)
3. Critical blockers: fake scarcity, missing BPOM, missing disclaimer
4. Confidence score 0.0-1.0

Skip: deep red_team_findings, per-step audits, full schema compliance
```

### Phase 3: Deep Audit (Optional)

Kalau user minta **full Red Team audit**, jalanin terpisah dengan scope reduced:

**Constraints:**
- 1 run at a time (bukan batch 3-4)
- 1 variant at a time (primary dulu, challenger terpisah)
- Pre-filter: cuma baca step yang ada red flags di Phase 1

**Task description:**
```
Goal: Deep Red Team Audit for {run_id} / {variant}

Pre-condition: Phase 1 audit-input.json shows critical_flags non-empty

Scope:
- Cuma baca artifact untuk step yang flagged
- Generate red_team_findings lengkap untuk step tersebut
- Output: 09-qa/red-team-{variant}.json
```

## Token Savings

| Mode | Input Tokens | Output Tokens | Per Run | Batch 4 Runs |
|------|--------------|---------------|---------|--------------|
| Full schema-09 | ~760K | ~14K | 774K | **3.1M** |
| Lite schema-09 | ~45K | ~3K | 48K | **192K** |
| **Savings** | **94%** | **79%** | **94%** | **94%** |

## When to Use What

| Situasi | Schema | Notes |
|---------|--------|-------|
| Batch QA banyak run (4+) | **Lite** | Speed, no timeout |
| Single run, user minta deep audit | Full | Complete red_team_findings |
| QA gate sebelum deploy | **Lite** | Blocking issues only |
| Post-mortem / compliance audit | Full | Complete traceability |
| CI/CD pipeline | **Lite** | Fast feedback |
| Regulatory submission | Full | Full documentation |

## Migration Path

**Existing runs dengan qa-report.json (full):**
- Biarkan — valid, cuma lambat
- Kalau perlu re-QA, generate audit-input.json dulu, terus lite audit

**New runs:**
- Default ke lite untuk batch
- Full audit on-demand dengan flag `--deep-qa`

**Schema files:**
- `schemas/schema-09.json` — full (existing)
- `schemas/schema-09-lite.json` — lite (new)

**Agent definitions:**
- `agents/agent-09.yml` — full QA (existing)
- `agents/agent-09-lite.yml` — lite QA (new)

## Dispatch Strategy (Batch QA)

Ketika menjalankan QA untuk multiple runs (batch), ikuti strategi ini:

### Concurrency
- **Max 3 concurrent** (delegate_task limit default)
- 4+ runs: split jadi batch 3-3-... 
- Jangan lebih dari 3 parallel — timeout risk naik eksponensial

### Priority Order
1. Runs yang sudah PASS (quick verify, <60s each)
2. Runs yang NEEDS_FIX (lebih lama, butuh deeper scan)
3. Runs yang belum punya QA report (full audit)

### Timeout Handling
Kalau subagent timeout (>600s):
1. **CEK FILESYSTEM DULU** — `ls 09-qa/qa-report*.json`
2. File mungkin udah ke-write sebelum timeout (common pattern)
3. Kalau file ada dan valid JSON → anggap selesai
4. Kalau file kosong/corrupted → retry focused (cuma bagian yang kurang)
5. Kalau file tidak ada → retry dengan scope lebih kecil (lite mode)

### Fallback Strategy
Kalau batch 3 gagal semua:
1. Switch ke 1-by-1 mode (sequential, bukan parallel)
2. Gunakan lite mode (agent-09-lite) bukan full (agent-09)
3. Pre-compress dulu dengan generate-audit-input.py
4. Task description yang lebih ringan: cuma baca audit-input.json

### QA Script Usage
Gunakan `scripts/qa-script.py` sebagai pre-check sebelum dispatch agent:
```bash
# Quick scan (tanpa agent, <5 detik per run)
python3 scripts/qa-script.py <run_dir> --json

# Kalau clean → skip agent-09, langsung PASS
# Kalau ada issues → dispatch agent-09-lite dengan context issues
```

## Pitfalls

1. **Jangan skip Phase 1.** Lite audit tanpa pre-compress = masih baca 118KB, cuma output yang dipendek.
2. **Critical flags harus lengkap.** Kalau audit-input.json gak capture fake scarcity, lite audit akan PASS padahal ada issue.
3. **Lite ≠ shallow.** Lite tetap rigorous, cuma scope-nya reduced (variant-level, bukan step-level).
4. **Re-QA setelah fix.** Kalau lite audit flag NEEDS_FIX lalu fix diterapkan, re-run lite audit untuk update status.
5. **qa-script.py disclaimer check: per-file, bukan per-variant.** Script check disclaimer di SETIAP file HTML. Kalau cuma index.html yang punya disclaimer tapi section/*.html tidak, script flag semua section sebagai MISSING. Ini false positive — yang penting minimal SATU file per variant punya disclaimer lengkap. Workaround: ignore `missing_disclaimer` issues untuk file yang bukan index.html atau hero.html, atau patch script jadi per-variant check.
6. **Timeout ≠ gagal.** Subagent sering write file sebelum timeout. SELALU cek filesystem (`ls 09-qa/`) sebelum retry. Kalau file ada dan valid JSON, anggap selesai.

## References

- `run-patterns.md` — Timeout handling, retry logic
- `lp-integrity.md` — Fake scarcity detection, trust elements
- `alpha-propolis-run.md` — Case study: stat cascade, fake scarcity
