# Pipeline Orchestration Pattern

## YAML-Based DAG Configuration

Pipeline didefinisikan dalam `pipeline.yaml` sebagai single source of truth. Orchestrator cuma baca file ini + `state.json` + file path. Tidak boleh baca isi artifact.

### Struktur pipeline.yaml

```yaml
pipeline:
  total_steps: 9
  active_steps: 8
  qa_step: 09

  brief_validation:
    enabled: true
    required_elements: [product_description, target_audience_hint, ...]
    min_required: 3
    fail_action: "pause_and_request_brief"

  steps:
    - id: "01"
      name: "Target Market Analysis"
      agent: "agent-01"
      type: "hat_system"
      input: ["00-input/brief.json"]
      output: "01-analysis/target-market.json"
      schema: "schema-01.json"
      dependencies: []
      parallel: false

    - id: "06"
      name: "Strategic Opportunity"
      type: "expert_team"
      parallel_subagents: true
      subagents:
        - id: "06a"
          agent: "agent-06a"
          output: "06-strategy/competitive-analysis.json"
        - id: "06b"
          agent: "agent-06b"
          output: "06-strategy/opportunity-size.json"
        - id: "06c"
          agent: "agent-06c"
          output: "06-strategy/strategic-positioning.json"
          merge: true

  qa_gates:
    confidence_threshold: 0.6
    schema_validation: true
    fixer_loop:
      enabled: true
      max_retries: 2
      escalate_after: true

  checkpoints:
    - step: "06"
      type: "auto_jalan"
      action: "log_summary_to_chat"
      pause: false

  resume:
    state_file: "state.json"
    checkpoint_file: "checkpoint.md"
    manifest_file: "manifest.json"
```

### Agent Persona YAML

Setiap agent didefinisikan dalam `agents/agent-XX.yml`:

```yaml
name: agent-01
role: Senior Market Researcher + Consumer Psychologist
step: 01
type: hat_system

description: "..."

system_prompt: |
  Kamu adalah ...
  Tugas: ...
  Aturan: ...

input_artifacts:
  - path: "00-input/brief.json"
    required: true

output_artifact:
  path: "01-analysis/target-market.json"
  schema: "schemas/schema-01.json"
  description: "Hasil analisis target market"

dependencies: []
```

### JSON Schema per Step

Setiap step punya schema di `schemas/schema-XX.json` yang mendefinisikan:
- `metadata` (step, agent, timestamp, brief_hash)
- Required fields dan structure
- Confidence scores (0.0-1.0)
- Array constraints (minItems/maxItems)

### Python Dispatcher

`scripts/run.py` adalah entry point yang:
1. Parse `pipeline.yaml`
2. Create run folder: `YYYY-MM-DD_HHMMSS_<slug>/`
3. Copy brief ke `00-input/`
4. Validate brief (pre-flight gate)
5. Init `state.json`
6. Update `checkpoint.md`
7. Hand off ke subagent dispatcher (hermes-agent spawn atau delegate_task)

## Orchestrator Context Hygiene

| Rule | Budget | Alasan |
|------|--------|--------|
| Orchestrator cuma baca file path | ~15% context | Nggak baca isi artifact |
| Sub-agent dapat fresh context | ~85% context | Heavy lifting di sub-agent |
| Tiap task = 1 agent invocation | 100% fresh | Spawn, jalan, output, mati |

## Resume Capability

```json
// state.json
{
  "run_id": "2026-06-10_150305_wardah-baby",
  "pipeline_version": "1.0.2",
  "status": "running",
  "current_step": "05",
  "steps": {
    "01": {"status": "done", "qa": "PASS"},
    "02": {"status": "done", "qa": "PASS"},
    "03": {"status": "done", "qa": "PASS"},
    "04": {"status": "done", "qa": "PASS"},
    "05": {"status": "in_progress", "qa": null}
  }
}
```

Orchestrator baca `state.json` kalau ada. Resume dari step terakhir, tidak dari 0.
