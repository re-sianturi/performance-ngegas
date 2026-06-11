# Post-QA Repair Pattern — Scan-Then-Fix Workflow

## When to Use

User says "find the problem and fix it", "apa yang salah?", "cari root cause",
or any variant of "diagnose then repair" after QA reports NEEDS_FIX.

## Pattern

### Phase 1: Scan All LP Files

Grep every HTML file in `08-lp/` for known issue patterns. Report exact
file:line with 80-char context snippet. Do NOT propose fixes yet — just
present findings.

**Regex patterns to scan (in priority order):**

```python
ISSUE_PATTERNS = {
    # CRITICAL — Fake scarcity
    "Math.random()":           r"Math\.random",
    "setInterval/timer":       r"setInterval|setTimeout",
    "countdown/counter":       r"countdown|counter.*decrement|stok.*habis",

    # CRITICAL — Placeholder links
    "wa.me placeholder":       r"wa\.me/[^0-9]",

    # HIGH — Unverified claims
    "percentage claims":       r"\d+[%].*(?:melaporkan|merasa|berhasil|switchers)",
    "star rating":             r"⭐.*\d[\.,]?\d.*(?:review|rating)",
    "review count":            r"\d[\.,]?\d+\+?\s*(?:Review|review|pelanggan)",

    # HIGH — Absolute health claims
    "tanpa efek samping":      r"tanpa\s+efek\s+samping",
    "teruji klinis":           r"teruji\s+klinis",
    "menyembuhkan":            r"menyembuhkan|mengobati",

    # MEDIUM — Missing compliance
    "disclaimer check":        r"disclaimer|tidak dimeksudkan|mendiagnosis",
    "BPOM check":              r"BPOM|POM\s+TR",
}
```

**Output format:**
```
ISSUE                          | FILE:LINE | CONTEXT
───────────────────────────────┼───────────┼─────────────────────────────
[Math.random()]               | urgency.html:42 | ...count -= 1; if(count...
[wa.me placeholder]           | hero.html:8     | ...href="https://wa.me/"...
[tanpa efek samping]          | hero.html:5     | ...tanpa efek samping dan...
```

### Phase 2: Cross-Reference with QA Report

Compare scan findings with QA report issues. Identify:
- Issues found by QA but NOT by scan (might be logic/structure issues)
- Issues found by scan but NOT by QA (QA blind spots)
- Issues where QA and scan disagree on severity

### Phase 3: Present Fix List

Group by execution batch:

```
BATCH A — BLOCKING (wajib sebelum deploy):
  1. [Severity] Issue description
     Files: exact/file.html:line, exact/file2.html:line
     Fix: exact replacement text

BATCH B — HIGH (fix hari ini):
  ...

BATCH C — POST-LAUNCH (opsional):
  ...
```

### Phase 4: Execute Fixes

Apply fixes with `patch` tool. After each fix, verify with grep that the
old pattern is gone and new pattern is present.

### Phase 5: Re-QA

After all fixes applied, re-run QA (lite or full depending on scope).

## Pitfalls

1. **Scan BEFORE proposing fixes.** Don't guess what's wrong — grep for it.
2. **Present exact file:line, not vague descriptions.** "hero.html line 7"
   not "somewhere in the hero section".
3. **Don't fix in scan phase.** Scan first, present findings, get approval,
   THEN fix. User said "find the problem" — find first, fix second.
4. **Check BOTH primary AND challenger variants.** Issues might exist in
   only one variant.
5. **Verify fix didn't break surrounding HTML.** After patch, grep for
   broken tags or missing context.
