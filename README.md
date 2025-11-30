# 🏛️ CivicAssist – AI-Powered Civic Issue Reporting System  

**CivicAssist** is an AI-driven, multi-agent platform designed to make civic complaint reporting simple for citizens and highly efficient for authorities.  
Users can submit complaints with text + images, while authorities manage them through a backend API with complete analytics and automated workflows.

---

## ✨ Overview  
CivicAssist combines **AI agents**, **persistent memory**, **image processing**, **web integration**, and **full-stack deployment** to create a seamless civic issue management system.

The system includes:  
✔ Streamlit frontend for citizens  
✔ FastAPI backend for authorities  
✔ AI multi-agent workflow  
✔ Complaint history memory  
✔ Analytics dashboard  
✔ End-to-end deployment on Render  

---

# 🚀 Key Features  

## 1️⃣ Citizen Complaint Portal (Streamlit Frontend)
Users can submit complaints with:  
- ✔ Issue description  
- ✔ Department selection  
- ✔ State & city dropdowns  
- ✔ Image upload (with instant preview)

Uploaded images are stored under `/attachments` in the backend.

The Streamlit UI is fully deployed on Render.

---

## 2️⃣ 🤖 AI Multi-Agent System  

### **1. Classification Agent**  
- Identifies complaint category from text + images  
- Maps issues to departments (Sanitation, Water, Public Works, etc.)  
- Ensures consistent classification  

### **2. Summarizer / Status Generator Agent**  
- Creates clean summaries for authorities  
- Helps generate dashboard-friendly descriptions  

### **3. History Agent + Memory System**  
- Maintains persistent complaint history  
- Uses `complaints.json` and `complaints.csv`  
- Returns full timeline of user complaints with images  
- Enables timeline-style view of past issues  

---

## 3️⃣ 📡 Backend (FastAPI)

Fully implemented backend with:

### 🔥 Endpoints  
| Method | Endpoint | Description |
|-------|----------|-------------|
| **POST** | `/submit` | Submit complaint + image |
| **GET** | `/history/{user_id}` | Fetch complaint history with images |

### Backend Capabilities  
- Auto-generated UUID complaint IDs  
- Image storage under `/backend/memory/attachments`  
- Persistent storage in **JSON + CSV**  
- MIME-safe file upload handling  

Backend is deployed on Render.

---

## 4️⃣ 📊 Dashboard & Analytics  

A complete analytics dashboard is integrated into `app.py`, showing:

- **Department-wise complaints** (pie chart)  
- **State-wise complaints** (bar chart)  
- **Status analytics** (resolved vs pending)  
- **Image gallery** of all uploaded images  

This dashboard significantly strengthens the project’s outcome and evaluation.

---

## 5️⃣ 🕒 Complaint History With Image Previews  

Users can enter their **User ID** and view formatted complaint cards including:

- Complaint ID  
- Description  
- Issue type  
- Department  
- Status  
- Timestamp  
- Attached image preview  

A **CSV download button** is included.

---

## 6️⃣ 🌐 Full Deployment (Frontend + Backend)  

Both components deployed on Render (Free Tier):  
- 🔗 **Backend:** https://civicassist-capstone-project-1.onrender.com/  
- 🔗 **Frontend:** https://civicassist-capstone-project-2.onrender.com/

Features:  
✔ No local server needed  
✔ Works from any browser  
✔ Supports images + JSON  
✔ Automatic GitHub deployment  

---

# 🧠 Tech Stack  

### **Frontend**  
- Streamlit  
- Plotly / Matplotlib  
- Requests  

### **Backend**  
- FastAPI  
- Python  
- UUID  
- JSON / CSV storage  
- Image file handling  

### **AI Agents**  
- LangChain-style agent workflow  
- Role-based agents for:
  - Classification  
  - Memory  
  - Summaries  

### **Deployment**  
- Render (free tier)  
- GitHub auto-deployment  

---

# 🏁 Conclusion  

CivicAssist transforms civic issue reporting using **AI-powered automation**, **multi-agent intelligence**, and **clean UI/analytics**.  
It provides a **real-world, deployable civic management solution** with:

- ✔ Multi-agent architecture  
- ✔ Production-ready deployment  
- ✔ Persistent memory system  
- ✔ Smart complaint automation  
- ✔ Image-based civic issue tracking  
- ✔ Full analytics dashboard  

---

