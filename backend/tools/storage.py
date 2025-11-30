import json
import os

memory_file = "backend/memory/complaints.json"

def save_complaint(complaint_id, complaint_data, classifier, department, planner):
    if not os.path.exists(memory_file):
        with open(memory_file, "w") as f:
            json.dump([], f)

    with open(memory_file, "r") as f:
        data = json.load(f)

    entry = {
        "complaint_id": complaint_id,
        "user_id": complaint_data["user_id"],
        "complaint_text": complaint_data["complaint_text"],
        "classification": classifier,
        "department": department,
        "action_plan": planner
    }

    data.append(entry)

    with open(memory_file, "w") as f:
        json.dump(data, f, indent=4)
