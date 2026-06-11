#!/usr/bin/env python3
"""
generate-audit-input.py — Pre-compress run artifacts for lite QA.

Generates 09-qa/audit-input.json (~5 KB) from full artifacts (~118 KB).
Used by agent-09-lite for batch QA without reading all step artifacts.

Usage:
  python3 generate-audit-input.py <run_dir>
  python3 generate-audit-input.py ~/.hermes/runs/performance-ngegas/2026-06-11_010541_segment-01-muslim-taqwa
"""

import json
import os
import re
import sys
from datetime import datetime


def extract_cro_highlights(cro_plan_path):
    """Extract key data from cro-plan.json."""
    with open(cro_plan_path) as f:
        cro = json.load(f)

    highlights = {
        "selected_plans": [],
        "section_order": [],
        "key_messaging": "",
        "trust_elements": [],
        "urgency_type": "unknown",
    }

    # Extract selected plans
    for plan in cro.get("plans", []):
        if plan.get("selected_for_execution"):
            highlights["selected_plans"].append(plan.get("plan_id", "unknown"))

    # Extract section order from first selected plan
    for plan in cro.get("plans", []):
        if plan.get("selected_for_execution"):
            for comp in plan.get("components", []):
                if comp.get("component") == "lp_structure":
                    impl = comp.get("implementation", "")
                    # Parse section order from implementation text
                    sections = re.findall(
                        r"(?:Hero|Social Proof|Problem|Mechanism|Trust|Offer|FAQ|CTA|Proof|Pricing|How to Use)",
                        impl,
                        re.IGNORECASE,
                    )
                    highlights["section_order"] = sections
                    break
            break

    # Extract trust elements
    for plan in cro.get("plans", []):
        if plan.get("selected_for_execution"):
            for comp in plan.get("components", []):
                if comp.get("component") == "trust":
                    impl = comp.get("implementation", "")
                    if "BPOM" in impl:
                        highlights["trust_elements"].append("BPOM")
                    if "Halal" in impl or "halal" in impl:
                        highlights["trust_elements"].append("Halal")
                    if "disclaimer" in impl.lower():
                        highlights["trust_elements"].append("disclaimer")
                    break
            break

    # Extract urgency type
    for plan in cro.get("plans", []):
        if plan.get("selected_for_execution"):
            for comp in plan.get("components", []):
                if comp.get("component") == "urgency":
                    strat = comp.get("strategy", "").lower()
                    if "fake" in strat or "countdown" in strat:
                        highlights["urgency_type"] = "fake"
                    elif "genuine" in strat or "calendar" in strat or "real" in strat:
                        highlights["urgency_type"] = "genuine"
                    else:
                        highlights["urgency_type"] = "unclear"
                    break
            break

    # Extract key messaging
    for plan in cro.get("plans", []):
        if plan.get("selected_for_execution"):
            for comp in plan.get("components", []):
                if comp.get("component") == "hero":
                    impl = comp.get("implementation", "")
                    # First 200 chars as summary
                    highlights["key_messaging"] = impl[:200]
                    break
            break

    return highlights


def extract_lp_structure(lp_dir):
    """Extract structure info from LP directory."""
    structure = {
        "sections": 0,
        "total_words": 0,
        "has_js": False,
        "has_fake_scarcity": False,
        "bpom_present": False,
        "disclaimer_present": False,
        "wa_placeholder_count": 0,
        "files": [],
    }

    if not os.path.isdir(lp_dir):
        return structure

    for root, dirs, files in os.walk(lp_dir):
        for f in sorted(files):
            if not f.endswith(".html"):
                continue
            fp = os.path.join(root, f)
            rel = os.path.relpath(fp, lp_dir)
            structure["files"].append(rel)

            with open(fp) as fh:
                content = fh.read()

            structure["total_words"] += len(content.split())
            structure["sections"] += 1

            # Check JS
            if "<script" in content or "Math.random()" in content:
                structure["has_js"] = True

            # Check fake scarcity
            if re.search(r"Math\.random|setInterval|countdown|timer", content, re.IGNORECASE):
                if re.search(r"stok|stock|sisa|tersisa", content, re.IGNORECASE):
                    structure["has_fake_scarcity"] = True

            # Check BPOM
            if re.search(r"BPOM|POM\s+TR", content, re.IGNORECASE):
                structure["bpom_present"] = True

            # Check disclaimer
            if re.search(
                r"tidak dimksudkan|mendiagnosis|menyembuhkan|mengganti.*obat|disclaimer",
                content,
                re.IGNORECASE,
            ):
                structure["disclaimer_present"] = True

            # Check wa.me placeholder
            wa_matches = re.findall(r'wa\.me/[^0-9"]', content)
            wa_empty = re.findall(r'wa\.me/"', content)
            structure["wa_placeholder_count"] += len(wa_matches) + len(wa_empty)

    return structure


def generate_audit_input(run_dir):
    """Generate 09-qa/audit-input.json from run artifacts."""
    run_id = os.path.basename(run_dir)

    # Read CRO plan
    cro_path = os.path.join(run_dir, "07-cro", "cro-plan.json")
    if not os.path.exists(cro_path):
        print(f"ERROR: {cro_path} not found")
        sys.exit(1)

    cro_highlights = extract_cro_highlights(cro_path)

    # Extract segment info from CRO metadata
    with open(cro_path) as f:
        cro = json.load(f)
    segment = cro.get("metadata", {}).get("segment_focus", run_id)
    brief_hash = cro.get("metadata", {}).get("brief_hash", "unknown")

    # Extract LP structures
    primary_dir = os.path.join(run_dir, "08-lp", "primary")
    challenger_dir = os.path.join(run_dir, "08-lp", "challenger")

    primary_structure = extract_lp_structure(primary_dir)
    challenger_structure = extract_lp_structure(challenger_dir)

    # Detect critical flags
    critical_flags = []
    for variant, struct in [("primary", primary_structure), ("challenger", challenger_structure)]:
        if struct["has_fake_scarcity"]:
            critical_flags.append(f"{variant}: fake scarcity detected")
        if not struct["bpom_present"]:
            critical_flags.append(f"{variant}: missing BPOM")
        if not struct["disclaimer_present"]:
            critical_flags.append(f"{variant}: missing disclaimer")
        if struct["wa_placeholder_count"] > 0:
            critical_flags.append(f"{variant}: {struct['wa_placeholder_count']} WhatsApp placeholder(s)")
        if struct["has_js"]:
            critical_flags.append(f"{variant}: JavaScript detected (no-JS policy violation)")

    # Build audit input
    audit_input = {
        "run_metadata": {
            "run_id": run_id,
            "brief_hash": brief_hash,
            "segment": segment,
            "timestamp": datetime.now().isoformat(),
        },
        "cro_highlights": cro_highlights,
        "lp_structure": {
            "primary": primary_structure,
            "challenger": challenger_structure,
        },
        "critical_flags": critical_flags,
    }

    # Write output
    output_dir = os.path.join(run_dir, "09-qa")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "audit-input.json")

    with open(output_path, "w") as f:
        json.dump(audit_input, f, indent=2, ensure_ascii=False)

    size_kb = os.path.getsize(output_path) / 1024
    print(f"✓ {output_path} ({size_kb:.1f} KB)")
    print(f"  Segment: {segment}")
    print(f"  Primary: {primary_structure['sections']} sections, {primary_structure['total_words']} words")
    print(f"  Challenger: {challenger_structure['sections']} sections, {challenger_structure['total_words']} words")
    print(f"  Critical flags: {len(critical_flags)}")
    for flag in critical_flags:
        print(f"    ⚠ {flag}")

    return audit_input


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <run_dir>")
        print(f"Example: {sys.argv[0]} ~/.hermes/runs/performance-ngegas/2026-06-11_010541_segment-01-muslim-taqwa")
        sys.exit(1)

    run_dir = os.path.expanduser(sys.argv[1])
    if not os.path.isdir(run_dir):
        print(f"ERROR: {run_dir} is not a directory")
        sys.exit(1)

    generate_audit_input(run_dir)
