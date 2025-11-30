def orchestrate(user_id, complaint_text, attachments=[]):
    # 1. ClassifierAgent -> issue type
    classifier_out = {
        "issue_type": "Water supply",
        "confidence": 0.93,
        "highlights": ["no water"]
    }

    # 2. MapperAgent -> department mapping
    mapper_out = {
        "department": "Water Board",
        "contact": {"portal": "https://water.gov", "phone": "0801234567"},
        "confidence": 0.91,
        "justification": "Complaint contains water outage keywords."
    }

    # 3. PlannerAgent -> action plan
    planner_out = {
        "steps": [
            "Take a photo of meter.",
            "Submit complaint on Water Board portal.",
            "Escalate if unresolved in 72 hours."
        ],
        "estimated_resolution_time": "48-72 hours"
    }

    final = {
        "complaint_id": "c001",
        "user_id": user_id,
        "classification": classifier_out,
        "department": mapper_out,
        "action_plan": planner_out,
        "file_options": {"can_file": True, "file_payload": {}},
        "memory_saved": True,
        "explainability": "Mapped to Water Board based on keywords.",
        "timestamps": {"created_at": "2025-11-29T00:00:00Z"}
    }

    return final
