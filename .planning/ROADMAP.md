# ROADMAP.md — Performance NgeGAS

## Milestone v1.0: Pipeline Berjalan

### Phase 1: Foundation
- Buat .planning/ (PROJECT.md, REQUIREMENTS.md, ROADMAP.md) ✓
- Buat folder structure: agents/, schemas/, prompts/ (refactor existing 8 prompts)
- Buat pipeline.yaml (DAG 7 step + checkpoint)
- Buat orchestrator SKILL.md (entry point)
- Buat orchestrator prompt (dispatch rules, context hygiene, QA gate)
- Buat QA agent persona + prompt
- Buat Fixer agent persona + prompt
- Buat Schema validator (JSON schema per step)
- Buat Brief Validator (pre-flight gate)

### Phase 2: Agent Personas
- agent-01.md: Market Researcher + Psychologist (Hat System)
- agent-02.md: JTBD Analyst + Psychologist + Decision Analyst (Hat System, merged v1+v2)
- agent-03.md: Psychologist + Data Architect (Hat System)
- agent-04.md: Behavioral Economist + Copywriter (Hat System)
- agent-05a.md: Competitive Analyst (Expert Team, parallel)
- agent-05b.md: Opportunity Sizer (Expert Team, parallel)
- agent-05c.md: Strategic Planner (Expert Team, merge)
- agent-06.md: CRO Specialist + UX Designer + A/B Testing Expert (Hat System)
- agent-07.md: LP Engineer + UX + Visual Designer (Hat System)
- agent-08.md: QA Reviewer + Red Team (Hat System)
- agent-qa.md: Universal QA (semua step)
- agent-fixer.md: Universal Fixer (semua step)

### Phase 3: Prompt Refactor
- Refactor 01-target-market.md: + input schema, output schema, role tags
- Refactor 02-jtbd.md (merged): + input schema, output schema, role tags
- Refactor 03-role-profile.md: + input schema, output schema
- Refactor 04-motivation.md: + input schema, output schema
- Refactor 05-strategic.md: + input schema, output schema, merge logic
- Refactor 06-cro.md: + input schema, output schema, CRO plan multiplicity
- Refactor 07-lp.md: + input schema, output schema, max 2 LP
- Refactor 08-review.md: + final QA checklist

### Phase 4: Schemas
- schema-01.json: Target Market artifact
- schema-02.json: JTBD artifact
- schema-03.json: Role Profile artifact
- schema-04.json: Motivation Database artifact
- schema-05.json: Strategic Opportunity artifact
- schema-06.json: CRO Plan artifact
- schema-07.json: Landing Page artifact
- schema-08.json: Final Review artifact
- schema-brief.json: Brief validation input

### Phase 5: Integration
- SKILL.md: update jadi orchestrator entry point
- Test run: brief sample (Wardah Baby / Klaim Garansi)
- Debug: step 1 → 2 → 3 → ... → 8
- Fix: QA fail loops, fixer logic
- Verify: manifest.json, state.json, resume capability

### Phase 6: Hardening
- Add retry logic untuk sub-agent crash
- Add timeout handling
- Add context limit monitoring
- Add human checkpoint wiring (Step 05)
- Add archive / retention logic
- Add SCORING.md transparency
- Add user override capability

### Phase 7: Ship
- Final QA of skill pack
- GSD audit: cross-phase UAT
- GitHub commit ke re-sianturi/knowledge-engine
- Skill pack registration ke Hermes
- Documentation: usage guide

---
*Last updated: 2026-06-10*
