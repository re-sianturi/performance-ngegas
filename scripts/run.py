#!/usr/bin/env python3
"""
Performance NgeGAS - Orchestrator Dispatcher
Spawns subagents per step, manages state, validates artifacts.
"""

import argparse
import json
import os
import sys
import hashlib
from datetime import datetime
from pathlib import Path

# Config
SKILL_DIR = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RUNS_DIR = Path.home() / ".hermes" / "runs" / "performance-ngegas"


def load_pipeline_config():
    with open(SKILL_DIR / "pipeline.yaml", "r") as f:
        import yaml
        return yaml.safe_load(f)


def create_run_folder(brief_path, run_name=None):
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    slug = run_name or "run"
    run_folder = RUNS_DIR / f"{timestamp}_{slug}"
    run_folder.mkdir(parents=True, exist_ok=True)

    # Create subdirectories
    folders = [
        "00-input", "01-analysis", "02-jtbd-v1", "03-jtbd-v2",
        "04-role-profile", "05-motivation", "06-strategy",
        "07-cro/plans", "07-cro/sections", "07-cro/ab-tests", "07-cro/archive",
        "08-lp", "09-qa", "qa"
    ]
    for folder in folders:
        (run_folder / folder).mkdir(parents=True, exist_ok=True)

    # Copy brief
    brief_dest = run_folder / "00-input" / "brief.md"
    with open(brief_path, "r") as src:
        brief_content = src.read()
    with open(brief_dest, "w") as dst:
        dst.write(brief_content)

    # Create brief.json
    brief_json = {
        "brief_text": brief_content,
        "brief_hash": hashlib.sha256(brief_content.encode()).hexdigest(),
        "timestamp": datetime.now().isoformat(),
        "source_file": str(brief_path)
    }
    with open(run_folder / "00-input" / "brief.json", "w") as f:
        json.dump(brief_json, f, indent=2)

    return run_folder


def init_state(run_folder, pipeline_config):
    state = {
        "run_id": run_folder.name,
        "pipeline_version": pipeline_config.get("version", "1.0.0"),
        "status": "running",
        "current_step": None,
        "steps": {},
        "started_at": datetime.now().isoformat(),
        "completed_at": None
    }
    for step in pipeline_config["pipeline"]["steps"]:
        state["steps"][step["id"]] = {
            "status": "pending",
            "agent": step.get("agent"),
            "output": step.get("output"),
            "qa_status": None
        }
    with open(run_folder / "state.json", "w") as f:
        json.dump(state, f, indent=2)
    return state


def validate_brief(brief_json, pipeline_config):
    """Pre-flight gate: check if brief has >= min_required elements"""
    validation = pipeline_config["pipeline"]["brief_validation"]
    required_elements = validation["required_elements"]
    min_required = validation["min_required"]

    brief_text = brief_json.get("brief_text", "").lower()
    found = []
    for element in required_elements:
        # Simple heuristic: check if element keywords exist in brief
        keywords = {
            "product_description": ["produk", "product", "jasa", "service", "aplikasi", "app"],
            "target_audience_hint": ["target", "audience", "customer", "user", "pasar", "market"],
            "value_proposition": ["value", "proposition", "keuntungan", "benefit", "nilai", "manfaat"],
            "pricing_model": ["harga", "price", "pricing", "biaya", "cost", "subscription", "langganan"],
            "competitive_context": ["kompetitor", "competitor", "kompetisi", "competition", "pasar", "market"]
        }
        element_keywords = keywords.get(element, [element])
        if any(kw in brief_text for kw in element_keywords):
            found.append(element)

    if len(found) < min_required:
        missing = [e for e in required_elements if e not in found]
        return False, f"Brief kurang {len(missing)} elemen: {missing}. Diperlukan minimal {min_required} dari {len(required_elements)}."
    return True, None


def update_checkpoint(run_folder, message):
    with open(run_folder / "checkpoint.md", "w") as f:
        f.write(f"# Checkpoint\n\n{message}\n\nUpdated: {datetime.now().isoformat()}\n")


def main():
    parser = argparse.ArgumentParser(description="Performance NgeGAS Pipeline Runner")
    parser.add_argument("--brief", required=True, help="Path to brief file")
    parser.add_argument("--run-name", default=None, help="Custom run name")
    parser.add_argument("--resume", action="store_true", help="Resume from state.json")
    parser.add_argument("--checkpoint", action="store_true", help="Enable manual checkpoint at Step 06")
    args = parser.parse_args()

    if not os.path.exists(args.brief):
        print(f"Error: Brief file not found: {args.brief}")
        sys.exit(1)

    pipeline_config = load_pipeline_config()

    if args.resume:
        # Find latest run with state.json
        runs = sorted(RUNS_DIR.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
        run_folder = None
        for r in runs:
            if (r / "state.json").exists():
                run_folder = r
                break
        if not run_folder:
            print("Error: No run found to resume")
            sys.exit(1)
        with open(run_folder / "state.json", "r") as f:
            state = json.load(f)
        print(f"Resuming run: {run_folder.name}")
    else:
        run_folder = create_run_folder(args.brief, args.run_name)
        state = init_state(run_folder, pipeline_config)
        print(f"Created run: {run_folder.name}")

        # Brief validation
        with open(run_folder / "00-input" / "brief.json", "r") as f:
            brief_json = json.load(f)
        valid, error = validate_brief(brief_json, pipeline_config)
        if not valid:
            print(f"BRIEF VALIDATION FAILED: {error}")
            state["status"] = "failed"
            state["steps"]["00"]["status"] = "failed"
            state["error"] = error
            with open(run_folder / "state.json", "w") as f:
                json.dump(state, f, indent=2)
            sys.exit(1)
        print("Brief validation: PASSED")

    print(f"\nRun folder: {run_folder}")
    print(f"State file: {run_folder / 'state.json'}")
    print("\nNext: Use 'hermes-agent spawn' or delegate_task to dispatch subagents per step.")
    print("See SKILL.md for orchestration instructions.")


if __name__ == "__main__":
    main()
