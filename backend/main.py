# backend/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import datetime
import random
import json
import os

app = FastAPI()

@app.get("/")
def home():
    return {"message": "CivicAssist backend is running successfully!"}

# ------------------ SIMPLE RULE-BASED CLASSIFIER ------------------ #
def simple_classify(text: str) -> dict:
    t = text.lower()
    highlights = []

    if any(k in t for k in ["no water", "water supply", "water", "tap", "meter"]):
        highlights.append("no water" if "no water" in t else "water")
        return {"issue_type": "Water supply", "confidence": 0.93, "highlights": highlights}

    if any(k in t for k in ["no electricity", "power cut", "power outage", "electricity", "meter not working"]):
        highlights.append("no electricity")
        return {"issue_type": "Electricity supply", "confidence": 0.92, "highlights": highlights}

    if any(k in t for k in ["garbage", "trash", "rubbish", "waste"]):
        highlights.append("garbage")
        return {"issue_type": "Garbage collection", "confidence": 0.9, "highlights": highlights}

    if any(k in t for k in ["pothole", "road", "accident", "street", "traffic"]):
        highlights.append("road damage")
        return {"issue_type": "Road maintenance", "confidence": 0.9, "highlights": highlights}

    return {"issue_type": "General civic", "confidence": 0.6, "highlights": []}

# ------------------ DEPARTMENT MAPPER ------------------ #
def simple_map_department(classification: dict) -> dict:
    issue = classification.get("issue_type", "").lower()

    if "water" in issue:
        return {
            "name": "Water Board",
            "contact": {"portal": "https://bwssb.karnataka.gov.in/info-1/About+BWSSB/en", "phone": "0801234567"},
            "confidence": 0.9,
            "justification": "Water issues handled by Water Board."
        }

    if "electric" in issue:
        return {
            "name": "Electricity Dept",
            "contact": {"portal": "https://bescom.karnataka.gov.in/english", "phone": "0807654321"},
            "confidence": 0.9,
            "justification": "Power outages handled by the Electricity Dept."
        }

    if "garbage" in issue:
        return {
            "name": "Sanitation Dept",
            "contact": {"portal": "https://bwssb.karnataka.gov.in/info-1/About+BWSSB/en", "phone": "0801112222"},
            "confidence": 0.9,
            "justification": "Garbage management handled by Sanitation Dept."
        }

    if "road" in issue:
        return {
            "name": "Public Works",
            "contact": {"portal": "https://kpwd.karnataka.gov.in/english", "phone": "0803334444"},
            "confidence": 0.9,
            "justification": "Road maintenance handled by Public Works."
        }

    return {
        "name": "Civic Helpdesk",
        "contact": {"portal": "https://civicspace.in/", "phone": "0800000000"},
        "confidence": 0.7,
        "justification": "General civic category."
    }

# ------------------ ACTION PLAN ------------------ #
def simple_plan(classification: dict) -> dict:
    itype = classification.get("issue_type", "").lower()

    if "water" in itype:
        steps = [
            "Take a photo of water meter.",
            "Submit complaint on Water Board portal.",
            "If unresolved in 48 hours, escalate."
        ]
        eta = "48-72 hours"

    elif "electric" in itype:
        steps = [
            "Note the outage time.",
            "Check with neighbours.",
            "Report to Electricity Dept portal.",
            "Escalate after 24 hours."
        ]
        eta = "24-48 hours"

    elif "garbage" in itype:
        steps = [
            "Take photo of garbage pile.",
            "Submit complaint on Sanitation portal.",
            "Escalate if not cleared in 48 hours."
        ]
        eta = "24-72 hours"

    elif "road" in itype:
        steps = [
            "Take photo of pothole.",
            "Mark location & submit to Public Works portal.",
            "Escalate for urgent repairs if safety risk."
        ]
        eta = "7-14 days"

    else:
        steps = ["Log complaint on Civic Helpdesk.", "Follow up after 72 hours."]
        eta = "72+ hours"

    return {"steps": steps, "estimated_resolution_time": eta}

# ------------------ REQUEST & RESPONSE MODELS ------------------ #
class ComplaintRequest(BaseModel):
    user_id: str
    complaint_text: str
    attachments: list = []

class ComplaintResponse(BaseModel):
    complaint_id: str
    classification: dict
    department: dict
    action_plan: dict
    status: str
    file_options: dict
    memory_saved: bool

# ------------------ RESOLVE ENDPOINT ------------------ #
@app.post("/agent/resolve", response_model=ComplaintResponse)
def resolve(complaint: ComplaintRequest):

    classification = simple_classify(complaint.complaint_text)
    department = simple_map_department(classification)
    action_plan = simple_plan(classification)

    complaint_id = "c-" + str(uuid.uuid4())
    status = random.choice(["Pending", "In Progress", "Resolved"])

    try:
        memory_file = "backend/memory/complaints.json"
        os.makedirs(os.path.dirname(memory_file), exist_ok=True)

        entry = {
            "complaint_id": complaint_id,
            "user_id": complaint.user_id,
            "complaint_text": complaint.complaint_text,
            "classification": classification,
            "department": department,
            "action_plan": action_plan,
            "status": status,
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

        # Load JSON memory
        data = []
        if os.path.exists(memory_file):
            with open(memory_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except:
                    data = []

        data.append(entry)

        with open(memory_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        # --- ALSO SAVE CSV FORMAT (NEW) ---
        import csv
        csv_file = "backend/memory/complaints.csv"
        csv_exists = os.path.exists(csv_file)

        with open(csv_file, "a", newline="", encoding="utf-8") as csvf:
            writer = csv.writer(csvf)

            if not csv_exists:
                writer.writerow([
                    "complaint_id",
                    "user_id",
                    "complaint_text",
                    "issue_type",
                    "department",
                    "status",
                    "timestamp"
                ])

            writer.writerow([
                complaint_id,
                complaint.user_id,
                complaint.complaint_text,
                classification.get("issue_type"),
                department.get("name"),
                status,
                entry["timestamp"]
            ])

        saved = True

    except Exception:
        saved = False

    return {
        "complaint_id": complaint_id,
        "classification": classification,
        "department": department,
        "action_plan": action_plan,
        "status": status,
        "file_options": {"can_file": False, "file_payload": {}},
        "memory_saved": saved
    }

# ------------------ HISTORY ENDPOINT ------------------ #
@app.get("/agent/history/{user_id}")
def get_history(user_id: str):
    memory_file = "backend/memory/complaints.json"

    if not os.path.exists(memory_file):
        return {"history": []}

    try:
        with open(memory_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        raise HTTPException(status_code=500, detail="Could not read history file")

    user_history = [c for c in data if c.get("user_id") == user_id]

    return {"history": user_history}
