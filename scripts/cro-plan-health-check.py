#!/usr/bin/env python3
"""
CRO Plan Health Check — Pre-flight & post-run verification for Performance NgeGAS pipeline.

Usage:
    python3 cro-plan-health-check.py [run_folder]

If run_folder is omitted, checks all runs in ~/.hermes/runs/performance-ngegas/.
"""
import os, sys, json

BASE = os.path.expanduser("~/.hermes/runs/performance-ngegas")

REQUIRED_FILES = {
    "01": "01-analysis/target-market.json",
    "02": "02-jtbd-v1/jtbd-analysis.json",
    "03": "03-jtbd-v2/jtbd-v2-analysis.json",
    "04": "04-role-profile/life-role-profile.json",
    "05": "05-motivation/customer-motivation.json",
    "06": "06-strategy/strategic-positioning.json",
    "07": "07-cro/cro-plan.json",
}

CRO_REQUIRED_FIELDS = [
    "recommended_section_order",
    "messaging_hierarchy",
    "conversion_strategy",
    "landing_page_recommendation",
]

def check_run(run_dir: str) -> dict:
    result = {"run": os.path.basename(run_dir), "steps_ok": 0, "steps_total": 0, "json_valid": 0, "cro_depth": "unknown", "lp_structure": "unknown", "issues": []}
    for step, rel in REQUIRED_FILES.items():
        result["steps_total"] += 1
        path = os.path.join(run_dir, rel)
        if os.path.exists(path) and os.path.getsize(path) > 0:
            try:
                with open(path) as f:
                    json.load(f)
                result["steps_ok"] += 1
                result["json_valid"] += 1
            except Exception as e:
                result["issues"].append(f"{step}: invalid JSON ({e})")
        else:
            result["issues"].append(f"{step}: missing or empty")

    # CRO Plan depth
    cro_path = os.path.join(run_dir, "07-cro/cro-plan.json")
    if os.path.exists(cro_path):
        with open(cro_path) as f:
            cro = json.load(f)
        size_kb = os.path.getsize(cro_path) / 1024
        missing_fields = [f for f in CRO_REQUIRED_FIELDS if f not in cro]
        if missing_fields:
            result["issues"].append(f"CRO Plan missing fields: {missing_fields}")
            result["cro_depth"] = "shallow"
        else:
            result["cro_depth"] = "rich"
        if size_kb < 2:
            result["issues"].append(f"CRO Plan suspiciously small ({size_kb:.1f} KB)")
            result["cro_depth"] = "shallow"

    # LP structure
    lp_dir = os.path.join(run_dir, "08-lp")
    if os.path.exists(lp_dir):
        files = os.listdir(lp_dir)
        has_index = any("index.html" in f for f in files)
        has_section = any(os.path.isdir(os.path.join(lp_dir, f)) and f == "section" for f in files)
        if has_index and has_section:
            result["lp_structure"] = "multi-file"
        elif any("primary.html" in f or "challenger.html" in f for f in files):
            result["lp_structure"] = "single-file"
        else:
            result["lp_structure"] = "incomplete"
    else:
        result["lp_structure"] = "missing"

    return result

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    if target:
        run_dirs = [os.path.join(BASE, target)]
    else:
        if not os.path.exists(BASE):
            print(f"Base directory not found: {BASE}")
            sys.exit(1)
        run_dirs = [os.path.join(BASE, d) for d in os.listdir(BASE) if os.path.isdir(os.path.join(BASE, d))]

    all_proper = True
    for run_dir in run_dirs:
        if not os.path.exists(run_dir):
            continue
        r = check_run(run_dir)
        status = "PASS" if r["steps_ok"] == r["steps_total"] and r["cro_depth"] == "rich" and r["lp_structure"] == "multi-file" else "FAIL"
        if status == "FAIL":
            all_proper = False
        print(f"\n=== {r['run']} ===")
        print(f"  Steps: {r['steps_ok']}/{r['steps_total']}  JSON valid: {r['json_valid']}")
        print(f"  CRO depth: {r['cro_depth']}  LP structure: {r['lp_structure']}")
        for issue in r["issues"]:
            print(f"  ❌ {issue}")
        if not r["issues"]:
            print(f"  ✅ No issues")
        print(f"  STATUS: {status}")

    print(f"\n{'='*60}")
    print(f"OVERALL: {'ALL PROPER' if all_proper else 'SOME RUNS INCOMPLETE'}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
