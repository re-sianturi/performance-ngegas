Kalau tujuan akhirnya adalah bikin **knowledge base pelanggan** yang bisa dipakai berkali-kali untuk:

* Positioning
* Offer
* Copywriting
* Sales Script
* Product Strategy
* Content Strategy

Maka saya sarankan output **JSON terstruktur**, bukan narasi panjang.

Dan saya akan bikin lebih dalam daripada format persona biasa.

---

# Struktur Role Profile yang Saya Rekomendasikan

```json
{
  "profile_name": "",
  "profile_type": "Primary ICP | Secondary ICP | Influencer | Decision Maker",

  "confidence_score": 0,

  "executive_summary": {
    "one_sentence_summary": "",
    "why_they_buy": "",
    "core_problem": "",
    "core_desired_outcome": ""
  },

  "identity": {
    "role_title": "",
    "industry": "",
    "company_size": "",
    "revenue_range": "",
    "experience_level": "",
    "education_level": "",
    "location": "",
    "life_stage": "",
    "demographic_summary": ""
  },

  "business_context": {
    "primary_responsibilities": [],
    "success_metrics": [],
    "daily_kpis": [],
    "major_business_pressures": [],
    "stakeholders": [],
    "decision_authority_level": ""
  },

  "current_reality": {
    "current_state_summary": "",
    "current_workflow": [],
    "current_tools": [],
    "existing_solutions": [],
    "workarounds": [],
    "current_frustrations": [],
    "current_limitations": [],
    "what_is_working": [],
    "what_is_not_working": [],
    "why_they_have_not_changed_yet": []
  },

  "desired_future": {
    "desired_state_summary": "",
    "ideal_workflow": [],
    "desired_outcomes": [],
    "success_definition": [],
    "business_goals": [],
    "personal_goals": [],
    "status_goals": []
  },

  "jtbd": {
    "core_job_statement": "",
    "functional_jobs": [],
    "emotional_jobs": [],
    "social_jobs": [],
    "job_priority_ranking": []
  },

  "switching_forces": {
    "push_forces": [],
    "pull_forces": [],
    "anxiety_forces": [],
    "habit_forces": []
  },

  "decision_psychology": {
    "buying_triggers": [],
    "decision_criteria": [],
    "trust_builders": [],
    "risk_factors": [],
    "objections": [],
    "decision_making_style": "",
    "information_sources": [],
    "who_influences_the_decision": [],
    "who_blocks_the_decision": []
  },

  "emotional_drivers": {
    "top_fears": [],
    "top_frustrations": [],
    "top_desires": [],
    "top_aspirations": [],
    "identity_goals": [],
    "status_drivers": [],
    "emotional_language_patterns": []
  },

  "customer_language": {
    "common_phrases": [],
    "complaints": [],
    "desired_outcome_language": [],
    "search_queries": [],
    "internal_dialogue": [],
    "keywords_they_resonate_with": [],
    "keywords_they_reject": []
  },

  "competitive_perception": {
    "current_alternatives": [],
    "liked_about_current_solution": [],
    "disliked_about_current_solution": [],
    "reasons_to_stay": [],
    "reasons_to_switch": []
  },

  "opportunity_analysis": {
    "underserved_needs": [],
    "unmet_expectations": [],
    "market_gaps": [],
    "high_value_opportunities": [],
    "quick_win_opportunities": []
  },

  "evidence_rating": {
    "verified": [],
    "strong_inference": [],
    "weak_inference": [],
    "assumptions": []
  },

  "validation_needed": {
    "critical_unknowns": [],
    "questions_for_customer_interview": [],
    "highest_risk_assumptions": []
  },

  "red_team_review": {
    "weak_assumptions": [],
    "unsupported_claims": [],
    "potential_biases": [],
    "internal_contradictions": [],
    "missing_data": [],
    "confidence_by_section": {
      "identity": 0,
      "current_reality": 0,
      "desired_future": 0,
      "jtbd": 0,
      "decision_psychology": 0,
      "emotional_drivers": 0,
      "customer_language": 0,
      "opportunity_analysis": 0
    },
    "overall_confidence": 0,
    "recommended_next_research_steps": []
  },

  "top_20_actionable_insights": [
    {
      "insight": "",
      "impact": "High | Medium | Low",
      "confidence": 0,
      "evidence_type": ""
    }
  ]
}
```

---

# Tambahan Prompt Red Team yang Lebih Keras

Tambahkan instruksi ini setelah output:

> Setelah menyelesaikan seluruh Role Profile:
>
> Lakukan Red Team Review terhadap seluruh profil.
>
> Anggap bahwa seluruh hasil riset berpotensi salah.
>
> Cari:
>
> * Asumsi yang tidak memiliki bukti kuat
> * Insight yang terlalu spekulatif
> * Generalisasi berlebihan
> * Bias konfirmasi
> * Bias survivorship
> * Bias industri
> * Kontradiksi internal
> * Informasi yang tidak cukup untuk mengambil keputusan bisnis
>
> Untuk setiap temuan:
>
> 1. Jelaskan masalahnya
> 2. Tingkat risiko (Low/Medium/High)
> 3. Dampak terhadap strategi bisnis
> 4. Cara memvalidasinya melalui wawancara pelanggan
>
> Berikan:
>
> * Overall Confidence Score (0–100)
> * Confidence Score per section
> * Top 10 Highest-Risk Assumptions
> * Top 20 Interview Questions yang paling efektif untuk memvalidasi profil ini
>
> Jangan mempertahankan asumsi hanya karena terlihat masuk akal.
>
> Bersikap skeptis dan kritis seperti seorang Principal Researcher yang sedang mengaudit hasil riset tim lain.
