import json

def map_department(issue_type: str):
    dept_mapping = {
        "Water supply": {
            "name": "Water Board",
            "contact": {"portal": "https://water.gov", "phone": "0801234567"},
            "confidence": 0.90,
            "justification": "Water issues are handled by Water Board."
        },
        "Electricity": {
            "name": "Electricity Board",
            "contact": {"portal": "https://electricity.gov", "phone": "0809876543"},
            "confidence": 0.90,
            "justification": "Power issues fall under the Electricity Board."
        },
        "Garbage/Waste": {
            "name": "Municipal Corporation",
            "contact": {"portal": "https://municipal.gov", "phone": "0803456789"},
            "confidence": 0.88,
            "justification": "Garbage issues are handled by the municipality."
        }
    }

    return dept_mapping.get(issue_type, {
        "name": "Unknown",
        "contact": {},
        "confidence": 0.0,
        "justification": "No mapping found."
    })
