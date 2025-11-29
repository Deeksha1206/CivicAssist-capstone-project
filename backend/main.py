from fastapi import FastAPI
from pydantic import BaseModel
import uuid
import json

from backend.tools.department_lookup import map_department
from backend.tools.storage import save_complaint

app = FastAPI()
@app.get("/")
def home():
    return {"message": "CivicAssist backend is running successfully!"}


# Request Model
class ComplaintRequest(BaseModel):
    user_id: str
    complaint_text: str
    attachments: list = []

# Response Model
class ComplaintResponse(BaseModel):
    complaint_id: str
    classification: dict
    department: dict
    action_plan: dict
    file_options: dict
    memory_saved: bool


@app.post("/agent/resolve", response_model=ComplaintResponse)
def resolve(complaint: ComplaintRequest):

    # 1. CLASSIFIER AGENT (Hardcoded stub for now)
    classifier_output = {
        "issue_type": "Water supply",
        "confidence": 0.93,
        "highlights": ["no water"]
    }

    # 2. MAPPER AGENT (using department lookup tool)
    department_output = map_department(classifier_output["issue_type"])

    # 3. PLANNER AGENT (Simple stub)
    planner_output = {
        "steps": [
            "Take a photo of water meter.",
            "Submit complaint on Water Board portal.",
            "If unresolved in 48 hours, escalate."
        ],
        "estimated_resolution_time": "48-72 hours"
    }

    # 4. Create final complaint ID
    complaint_id = f"c-{uuid.uuid4()}"

    # 5. Save to memory
    save_complaint(complaint_id, complaint.dict(), classifier_output, department_output, planner_output)

    # 6. Final response
    return {
        "complaint_id": complaint_id,
        "classification": classifier_output,
        "department": department_output,
        "action_plan": planner_output,
        "file_options": {"can_file": True, "file_payload": {}},
        "memory_saved": True
    }
