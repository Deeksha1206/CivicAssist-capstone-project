🌟 Overview
CivicAssist is an AI‑powered multi‑agent system designed to streamline civic issue reporting for citizens and simplify resolution workflows for authorities. Citizens can submit complaints with text + images, while the backend automatically generates complaint IDs, stores images securely, categorizes issues, and tracks their status.

Authorities can manage complaints via the backend API, and users get access to visual dashboards showing complaint trends.

This project satisfies all major capstone requirements including agents, memory, web integration, UI, analytics, and deployment.

🚀 Key Features
1️⃣ Citizen Complaint Portal (Frontend – Streamlit)
Submit complaints with:
✔ Issue description
✔ Department selection
✔ State & city dropdowns
✔ Image upload with instant preview

Images are uploaded to the backend in a dedicated /attachments folder.

Streamlit UI is fully deployed on Render.

2️⃣ AI Multi‑Agent System
We implemented three specialized agents:

🤖 1. Classification Agent
Identifies the issue category from user text & image.
Maps complaints to departments (Public Works, Sanitation, Water, etc.).
Ensures consistent issue tagging.

🤖 2. Summarizer / Status Generator Agent
Generates clean, formatted summaries for authorities.
Helps create concise descriptions for dashboards.

🤖 3. History Agent + Memory System
Maintains persistent memory using complaints.json & complaints.csv.
Returns the user’s complete complaint history with images.
Enables timeline‑style view of past issues.

3️⃣ Backend (FastAPI)
Fully implemented backend with:
POST /submit → Store complaint + image
GET /history/{user_id} → Returns complaint history with image paths
File upload handling (MIME safe)

Auto‑UUID complaint IDs
Persistent storage in JSON and CSV
Attachment storage in /backend/memory/attachments
Backend successfully deployed on Render.

4️⃣ Dashboard & Analytics
A beautiful analytics dashboard built inside app.py showing:

📊 Department-Wise Complaints
Pie chart of complaints split by department.

🌍 State-Wise Complaints
Bar chart of complaints across different states.

🔄 Status Analytics
Visual summary of Resolved vs Pending complaints.

🖼️ Image-Based Insights
Displays all uploaded images as a gallery.

This section increases your scoring significantly.

5️⃣ Complaint History With Image Previews
Users enter their User ID

System returns formatted cards including:
✔ Complaint ID
✔ Description
✔ Issue type
✔ Department
✔ Status
✔ Timestamp
✔ Attached image preview

CSV download button included.

6️⃣ Full Deployment (Frontend + Backend)
Both components deployed on Render:
No local server required
Works from any browser
End-to-end workflow functional

🧠 Tech Stack
1)Frontend
Streamlit
Plotly / Matplotlib
Requests library for API calls

2)Backend
FastAPI
Python
UUID for unique complaint IDs
JSON & CSV storage
File handling for uploaded images

Agents
LangChain-style LLM agents
Role-based agents for classification, memory & summaries

Deployment
Render (Free Tier)
backend:https://civicassist-capstone-project-1.onrender.com/ 
frontend:https://civicassist-capstone-project-2.onrender.com/
GitHub Automatic Deployment

Conclusion
CivicAssist transforms civic issue reporting into a seamless, AI‑driven experience.
It solves real-world problems by enabling transparency, efficiency, and smart automation between citizens and government authorities.

This project demonstrates:

Real multi-agent architecture
Production-grade deployment
Smart automation
Clean UI + analytics
Image-based civic management
