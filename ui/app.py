import streamlit as st
import requests
import base64
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="CivicAssist", layout="centered")

# ---------------- HEADER -----------------
st.title("🛠️ CivicAssist — Citizen Complaint Resolver")
st.markdown(
    "<p style='font-size:17px;color:#bbb;'>"
    "Submit a civic issue and the AI agent will classify it, identify the department, "
    "and generate an action plan."
    "</p>",
    unsafe_allow_html=True,
)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("---")
st.sidebar.header("⚙️ Settings")
backend_url = st.sidebar.text_input("Backend URL", "http://127.0.0.1:8000")

# -------- Helper: status badge HTML -------
def status_badge_html(status: str) -> str:
    s = (status or "").lower()
    if s == "pending":
        bg = "#f0c14b"; emoji = "🟡"
    elif s in ["in progress", "in-progress"]:
        bg = "#f39c12"; emoji = "🟠"
    elif s == "resolved":
        bg = "#2ecc71"; emoji = "🟢"
    else:
        bg = "#95a5a6"; emoji = "⚪"
    return f'<span style="background:{bg};color:#000;padding:6px 10px;border-radius:12px;font-weight:600">{emoji} {status}</span>'

# ---------------- STATE → CITY DATA ----------------
states_cities = {
    "Karnataka": ["Bengaluru", "Mysuru", "Mangaluru", "Hubballi", "Belagavi", "Shivamogga", "Davanagere"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Salem", "Trichy", "Vellore"],
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad", "Kolhapur"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Khammam"],
    "Kerala": ["Kochi", "Thiruvananthapuram", "Kozhikode", "Kannur"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot"],
    "Rajasthan": ["Jaipur", "Udaipur", "Jodhpur", "Kota"],
    "Punjab": ["Amritsar", "Ludhiana", "Jalandhar", "Patiala"],
    "West Bengal": ["Kolkata", "Howrah", "Siliguri", "Durgapur"],
    "Bihar": ["Patna", "Gaya", "Muzaffarpur", "Bhagalpur"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Varanasi", "Agra"],
    "Madhya Pradesh": ["Indore", "Bhopal", "Gwalior", "Jabalpur"]
}

# ---------------- COMPLAINT FORM ----------------
st.subheader("📝 Submit a Complaint")

# --- Dynamic State / City Handling ---
state = st.selectbox("Select State", list(states_cities.keys()), key="state_select")

if "last_state" not in st.session_state or st.session_state.last_state != state:
    st.session_state.last_state = state
    st.session_state.city = states_cities[state][0]

city = st.selectbox("Select City", states_cities[state], key="city_select_dynamic")

# ---- IMAGE UPLOAD ----
uploaded_image = st.file_uploader("Upload Image (optional)", type=["png", "jpg", "jpeg"])
# ---- SHOW IMAGE PREVIEW ----
if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image Preview", width=250)


attachment_b64 = None
if uploaded_image:
    attachment_b64 = base64.b64encode(uploaded_image.read()).decode("utf-8")

with st.form("complaint_form"):
    user_id = st.text_input("User ID", value="user1")
    complaint_text = st.text_area("Complaint Details", height=140)
    submitted = st.form_submit_button("Submit Complaint")

if submitted:
    if not complaint_text.strip():
        st.error("⚠️ Please enter a complaint before submitting.")
    else:

        payload = {
            "user_id": user_id,
            "complaint_text": complaint_text,
            "state": state,
            "city": city,
            "attachments": [attachment_b64] if attachment_b64 else []
        }

        try:
            with st.spinner("Processing your complaint..."):
                resp = requests.post(f"{backend_url}/agent/resolve", json=payload)
                resp.raise_for_status()
                result = resp.json()

            st.success("🎉 Complaint processed successfully!")

            # Classification
            st.markdown("### 🔍 Classification")
            cls = result.get("classification", {})
            st.markdown(
                f"""
                <div style="padding:12px;border-radius:8px;border:1px solid #555;">
                <b>Issue type:</b> {cls.get('issue_type')} <br>
                <b>Confidence:</b> {cls.get('confidence')}
                </div>
                """,
                unsafe_allow_html=True
            )

            if cls.get("highlights"):
                st.markdown("**Highlights:**")
                for h in cls["highlights"]:
                    st.write(f"- {h}")

            # Department
            st.markdown("### 🏛 Department")
            dep = result.get("department", {})
            st.markdown(
                f"""
                <div style="padding:12px;border-radius:8px;border:1px solid #555;">
                <b>{dep.get('name')}</b><br>
                <b>Portal:</b> <a href="{dep.get('contact', {}).get('portal')}" target="_blank" style="color:#4da6ff;">
                {dep.get('contact', {}).get('portal')}
                </a><br>
                <b>Phone:</b> {dep.get('contact', {}).get('phone')}<br>
                <b>Justification:</b> {dep.get('justification')}<br>
                <b>Confidence:</b> {dep.get('confidence')}
                </div>
                """,
                unsafe_allow_html=True
            )

            # Action Plan
            st.markdown("### 🧭 Action Plan")
            plan = result.get("action_plan", {})
            st.markdown("<ul>", unsafe_allow_html=True)
            for step in plan.get("steps", []):
                st.markdown(f"<li>{step}</li>", unsafe_allow_html=True)
            st.markdown("</ul>", unsafe_allow_html=True)

            st.markdown(f"**Estimated resolution time:** {plan.get('estimated_resolution_time')}")

            # Status
            st.markdown("### 📌 Complaint Status")
            status = result.get("status", "Pending")
            st.markdown(status_badge_html(status), unsafe_allow_html=True)

            st.caption(f"Processed at {datetime.utcnow()}")

        except Exception as e:
            st.error(f"❌ Error communicating with backend: {e}")

# ---------------- HISTORY SECTION ----------------
st.write("---")
st.subheader("📚 Complaint History")

hist_user = st.text_input("User ID for history", "user1", key="history")

if st.button("Get History"):
    try:
        r = requests.get(f"{backend_url}/agent/history/{hist_user}")

        if r.status_code == 200:
            history = r.json().get("history", [])

            if not history:
                st.info("ℹ️ No complaints found for this user.")
            else:
                st.markdown("### 📜 Past Complaints")

                is_dark = st.get_option("theme.base") == "dark"
                card_bg = "#1e1e1e" if is_dark else "#f7f7f7"
                card_border = "#444" if is_dark else "#ddd"
                text_color = "#fff" if is_dark else "#000"

                for item in history:
                    stat = item.get("status", "Pending")
                    badge_html = status_badge_html(stat)

                    st.markdown(
                        f"""
                        <div style="
                            padding:15px;
                            margin-bottom:14px;
                            border-radius:10px;
                            background:{card_bg};
                            border:1px solid {card_border};
                            color:{text_color};
                        ">
                            <b>🆔 Complaint ID:</b> {item.get('complaint_id')}<br>
                            <b>📝 Complaint:</b> {item.get('complaint_text')}<br>
                            <b>🏷 Issue:</b> {item.get('classification', {}).get('issue_type')}<br>
                            <b>🏛 Department:</b> {item.get('department', {}).get('name')}<br>
                            <b>📌 Status:</b> {badge_html}<br>
                            <b>📅 Timestamp:</b> {item.get('timestamp')}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # ---- IMAGE PREVIEW ----
                    if item.get("attachments"):
                        st.markdown("📷 **Attached Image:**")
                        for img_b64 in item["attachments"]:
                            st.image(base64.b64decode(img_b64), width=120)

        else:
            st.error("❌ Could not fetch history from backend.")
    except Exception as e:
        st.error(f"❌ Error: {e}")

if st.button("⬇️ Download CSV"):
    df = pd.read_csv("backend/memory/complaints.csv")
    st.dataframe(df)
# ---------------- ANALYTICS DASHBOARD ----------------
st.write("---")
st.subheader("📊 Analytics Dashboard")

if st.button("Show Dashboard"):
    try:
        df = pd.read_csv("backend/memory/complaints.csv")

        if df.empty:
            st.info("No complaint data available yet.")
        else:
            st.markdown("### 📌 Complaints per Department")
            dep_counts = df["department"].value_counts()
            st.bar_chart(dep_counts)

            st.markdown("### 🏙 Complaints per State")
            state_counts = df["state"].value_counts()
            st.bar_chart(state_counts)

            st.markdown("### 🟢 Resolved vs 🟡 Pending vs 🟠 In‑Progress")
            status_counts = df["status"].value_counts()
            st.bar_chart(status_counts)

            # IMAGE COUNT ANALYSIS
            st.markdown("### 🖼 Complaints with Image Attachments")
            df["has_image"] = df["complaint_id"].isin(
                [item["complaint_id"] for item in requests.get(f"{backend_url}/agent/history/user1").json().get("history", []) if item.get("attachments")]
            )
            image_counts = df["has_image"].value_counts().rename({True: "With Image", False: "Without Image"})
            st.bar_chart(image_counts)

    except Exception as e:
        st.error(f"Error loading dashboard: {e}")

