import streamlit as st
import streamlit.components.v1 as components
from fpdf import FPDF
import datetime

st.set_page_config(page_title="Radiology Prep Portal", page_icon="🏥", layout="wide")

# Detect Dark Mode using JavaScript
is_dark_mode = st.components.v1.html(
    """
    <script>
    var isDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (isDark) { document.write('dark'); } else { document.write('light'); }
    </script>
    """,
    height=0, width=0
)

# Define colors based on the mode
if "dark" in str(is_dark_mode):
    bg_color = "#121212"
    card_bg = "#1E1E1E"
    text_color = "#EAECEE"
    header_color = "#5DADE2"
    warn_bg = "#4A1919"
    warn_text = "#FADBD8"
    success_bg = "#144A38"
    success_text = "#D1F2EB"
else:
    bg_color = "#F4F7F6"
    card_bg = "#FFFFFF"
    text_color = "#2C3E50"
    header_color = "#1A5276"
    warn_bg = "#FDEDEC"
    warn_text = "#7B241C"
    success_bg = "#E8F8F5"
    success_text = "#145A32"

# Apply the CSS using the dynamic colors
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');

.stApp {{ background-color: {bg_color} !important; }}
html, body, [class*="css"] {{ font-family: 'Inter', sans-serif; color: {text_color} !important; }}
h1, h2, h3 {{ color: {header_color} !important; }}

.custom-card {{ 
    background-color: {card_bg} !important; 
    padding: 25px; 
    border-radius: 12px; 
    box-shadow: 0 6px 12px rgba(0,0,0,0.1); 
    margin-bottom: 20px; 
    border-top: 5px solid #3498DB; 
}}
.custom-card h4 {{ color: {header_color} !important; }}
.custom-card p {{ color: {text_color} !important; }}

.warning-box {{ 
    background-color: {warn_bg} !important; 
    border-left: 5px solid #E74C3C; 
    padding: 15px; 
    border-radius: 5px; 
    margin-bottom: 15px; 
}}
.warning-box, .warning-box b {{ color: {warn_text} !important; }}

.success-box {{ 
    background-color: {success_bg} !important; 
    border-left: 5px solid #1ABC9C; 
    padding: 15px; 
    border-radius: 5px; 
    margin-bottom: 15px; 
}}
.success-box, .success-box b {{ color: {success_text} !important; }}
</style>
""", unsafe_allow_html=True)

def card(title, text, icon=""):
    st.markdown(f'<div class="custom-card"><h4 style="margin-top:0; color:#1A5276;">{icon} {title}</h4><p style="margin-bottom:0; font-size:16px;">{text}</p></div>', unsafe_allow_html=True)

# ==========================================
# 2. PDF GENERATOR FUNCTION
# ==========================================
def create_pdf(checklist_items, modality):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt=f"Checklist: {modality}", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Date: {datetime.date.today()}", ln=True, align='C')
    pdf.ln(10)
    for item in checklist_items:
        pdf.cell(0, 10, txt=f"[ ] {item}", ln=True)
    return bytes(pdf.output()) # Fixed for latest fpdf2

# ==========================================
# 3. SIDEBAR
# ==========================================
with st.sidebar:
    st.header("Personalize Your App")
    persona = st.selectbox("Who is using this app?", ["Adult", "Child / Parent", "Senior", "Visual Impairment", "Hearing Impairment"])
    st.markdown("---")
    modality = st.selectbox("Select your scan:", ["CT Scan", "MRI", "X-Ray", "Ultrasound (USG)", "Mammography", "Fluoroscopy", "DEXA"])
    st.markdown("---")
    page = st.radio("Navigate:", ["Home & Prep", "Safety Triage", "Virtual 3D Room", "Download Checklist"])

if persona in ["Senior", "Visual Impairment"]:
    st.markdown("""<style>html, body, [class*="css"] { font-size: 22px !important; } h1 { font-size: 3rem !important; }</style>""", unsafe_allow_html=True)

# ==========================================
# 4. APP LOGIC
# ==========================================
if page == "Home & Prep":
    st.title(f"🏥 {modality} Preparation Guide")
    
    if modality == "CT Scan":
        card("Fasting & Meds", "Do not eat for 4 hours. Tell us if you take Metformin.", "🚫")
        st.markdown('<div class="warning-box"><b>Kidney Check:</b> We need your latest Creatinine blood test. If it is 30-45, a radiologist must approve the scan.</div>', unsafe_allow_html=True)
    elif modality == "MRI":
        card("Implants", "You MUST bring your implant passport or surgery records.", "📄")
    elif modality == "Mammography":
        card("Timing & Cosmetics", "Do not schedule during your cycle. Do not use deodorant on the day.", "🚺")
    elif modality == "DEXA":
        card("Preparation", "Do not take calcium supplements 24 hours before the test. Wear clothing without metal.", "🦴")
    elif modality == "Ultrasound (USG)":
        card("Preparation", "You may need to fast or have a full bladder. Drink water before the exam.", "💧")
    elif modality == "X-Ray":
        card("Preparation", "Remove metal jewelry. Tell us if you are pregnant.", "☢️")
    elif modality == "Fluoroscopy":
        card("Preparation", "You may need to fast. You will drink a contrast liquid.", "🥤")

elif page == "Safety Triage":
    st.title("🛡️ Interactive Safety Check")
    col1, col2 = st.columns(2)
    with col1:
        has_metal = st.checkbox("Metal implants / Pacemaker?")
        is_pregnant = st.checkbox("Pregnant or possibly pregnant?")
    with col2:
        is_claustrophobic = st.checkbox("Fear of closed spaces?")
        if modality in ["CT Scan", "MRI"]:
            creatinine = st.number_input("Latest Creatinine level (if known):", value=80)

    if st.button("Check My Safety"):
        if has_metal:
            st.error("🛑 **DANGER:** Do not enter the MRI room. Speak to staff immediately.")
        elif is_pregnant:
            st.warning("⚠️ **WARNING:** Tell the doctor immediately. Avoid CT/X-Ray unless necessary.")
        elif modality in ["CT Scan", "MRI"] and creatinine < 45:
            st.error("🚨 **KIDNEY ALERT:** Your Creatinine is below 45. A radiologist MUST review your blood test.")
        elif is_claustrophobic:
            st.info("💡 **NOTE:** We will prepare light anesthesia for you.")
        else:
            st.markdown('<div class="success-box"><b>✅ SAFE:</b> You are cleared for your scan.</div>', unsafe_allow_html=True)

elif page == "Virtual 3D Room":
    st.title(f"🧲 3D Room: {modality}")
    st.write("Click and drag to look around the room. This helps reduce anxiety.")
    
    # WOW FACTOR: A different 3D model for each modality
    if modality == "CT Scan":
        components.iframe("https://sketchfab.com/models/d9ab7662d1df4b7db3bc7935e1cb5581/embed", height=500)
    elif modality == "MRI":
        components.iframe("https://sketchfab.com/models/debdb59deea643249f30dea289f3f6dc/embed", height=500)
    elif modality == "X-Ray":
        components.iframe("https://sketchfab.com/models/8c7f17ae00324cc7a67e2fede13a8d58/embed", height=500)
    elif modality == "Ultrasound (USG)":
        components.iframe("https://sketchfab.com/models/17aa217cd9e4469cb2834d5fe9c09f72/embed", height=500)
    elif modality == "Mammography":
        components.iframe("https://sketchfab.com/models/293306631a5b4d1da411c9c6804bfa1b/embed", height=500)
    elif modality == "DEXA":
        components.iframe("https://sketchfab.com/models/681aa7ab7c3e4734929024c2f375edbe/embed", height=500)
    elif modality == "Fluoroscopy":
        components.iframe("https://sketchfab.com/models/9e4f12f999b344fcb257d805a05d24bd/embed", height=500)

elif page == "Download Checklist":
    st.title("📄 Personalized Checklist")
    checklist = ["Bring your ID and insurance card", "Arrive 15 minutes early"]
    
    if modality == "CT Scan":
        checklist.extend(["Bring your latest blood test (Creatinine)", "Do not eat 4 hours before"])
    elif modality == "MRI":
        checklist.extend(["Bring implant passports / surgery documents", "Remove all metal jewelry"])
    elif modality == "Mammography":
        checklist.extend(["Do not use deodorant on the day", "Schedule outside your menstrual cycle"])
    else:
        checklist.append("Wear comfortable clothing without metal")
        
    pdf_bytes = create_pdf(checklist, modality)
    st.download_button(label="⬇️ Download My Checklist (PDF)", data=pdf_bytes, file_name=f"{modality}_checklist.pdf", mime="application/pdf")