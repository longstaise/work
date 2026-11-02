import streamlit as st
import streamlit.components.v1 as components
from fpdf import FPDF
import datetime

# ==========================================
# 1. PAGE CONFIG & DYNAMIC LIGHT/DARK MODE
# ==========================================
st.set_page_config(page_title="Radiology Prep Portal", page_icon="🏥", layout="wide")

# Detect Dark Mode using JavaScript to prevent patchy colors
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
    st.markdown(f'<div class="custom-card"><h4 style="margin-top:0;">{icon} {title}</h4><p style="margin-bottom:0; font-size:16px;">{text}</p></div>', unsafe_allow_html=True)

# ==========================================
# 2. PDF GENERATOR (With Visual Guide)
# ==========================================
def create_pdf(checklist_items, modality):
    pdf = FPDF()
    pdf.add_page()
    
    # Header
    pdf.set_font("Arial", size=18, style='B')
    pdf.set_text_color(26, 82, 118)
    pdf.cell(200, 10, txt="ACCREMeter Patient Guide", ln=True, align='C')
    
    pdf.set_font("Arial", size=12, style='I')
    pdf.set_text_color(100, 100, 100)
    pdf.cell(200, 8, txt=f"Preparation Checklist: {modality}", ln=True, align='C')
    pdf.cell(200, 8, txt=f"Date: {datetime.date.today()}", ln=True, align='C')
    pdf.ln(10)
    
    # Checklist Body
    pdf.set_font("Arial", size=14, style='B')
    pdf.set_text_color(0, 0, 0)
    pdf.cell(200, 10, txt="What to bring and do:", ln=True)
    
    pdf.set_font("Arial", size=12)
    for item in checklist_items:
        pdf.cell(0, 8, txt=f"[  ]  {item}", ln=True)
    
    pdf.ln(10)
    
    # Visual Guide for Elderly
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 10, txt="Visual Guide:", ln=True)
    pdf.ln(2)
    
    if modality == "MRI":
        img_do = "https://cdn-icons-png.flaticon.com/512/2966/2966486.png" 
        img_dont = "https://cdn-icons-png.flaticon.com/512/190/190412.png" 
        text_do = "DO: Listen to staff"
        text_dont = "DON'T: Bring Metal"
    elif modality == "CT Scan":
        img_do = "https://cdn-icons-png.flaticon.com/512/2966/2966486.png" 
        img_dont = "https://cdn-icons-png.flaticon.com/512/564/564619.png" 
        text_do = "DO: Drink Water"
        text_dont = "DON'T: Eat 4h before"
    else:
        img_do = "https://cdn-icons-png.flaticon.com/512/2966/2966486.png"
        img_dont = "https://cdn-icons-png.flaticon.com/512/564/564619.png"
        text_do = "DO: Follow rules"
        text_dont = "DON'T: Wear Jewelry"

    try:
        y_pos = pdf.get_y()
        pdf.image(img_do, x=40, y=y_pos, w=30) 
        pdf.image(img_dont, x=130, y=y_pos, w=30) 
        pdf.set_y(y_pos + 35) 
        
        pdf.set_font("Arial", size=12)
        pdf.cell(80, 10, txt=text_do, align='C')
        pdf.cell(80, 10, txt=text_dont, align='C', ln=True)
    except Exception:
        pdf.cell(200, 10, txt="(Visual guide could not be loaded)", ln=True)

    pdf.ln(10)
    
    # Warning Section
    pdf.set_font("Arial", size=14, style='B')
    pdf.set_text_color(200, 0, 0)
    pdf.cell(200, 10, txt="Important Safety Reminders:", ln=True)
    
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    
    if modality == "MRI":
        pdf.multi_cell(0, 8, txt="- DO NOT enter the MRI room with any metal (keys, watches, pacemakers). It is extremely dangerous.\n- If you have implants, you MUST bring your implant passport.")
    elif modality == "CT Scan":
        pdf.multi_cell(0, 8, txt="- Tell the staff if you are pregnant.\n- If you take Metformin, tell the staff.\n- We must check your Creatinine level. If it is below 45, the scan may be delayed.")
    else:
        pdf.multi_cell(0, 8, txt="- Tell the staff if you are pregnant.\n- Remove any metal jewelry or glasses.")
        
    pdf.ln(10)
    
    # Footer
    pdf.set_font("Arial", size=10, style='I')
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, txt="The machine is open, and the radiographer can see and hear you at all times.", ln=True, align='C')
    pdf.cell(0, 10, txt="Generated by ACCREMeter.", ln=True, align='C')

    return bytes(pdf.output())

# ==========================================
# 3. SIDEBAR
# ==========================================
with st.sidebar:
    st.header("Personalize Your App")
    persona = st.selectbox("Who is using this app?", ["Adult", "Child / Parent", "Senior", "Visual Impairment", "Hearing Impairment"])
    st.markdown("---")
    modality = st.selectbox("Select your scan:", ["CT Scan", "MRI", "X-Ray", "Ultrasound (USG)", "Mammography", "Fluoroscopy", "DEXA"])
    st.markdown("---")
    page = st.radio("Navigate:", ["Home & Prep", "Safety Triage", "Virtual 3D Room", "Download Checklist", "FAQ"])

if persona in ["Senior", "Visual Impairment"]:
    st.markdown("""<style>html, body, [class*="css"] { font-size: 22px !important; } h1 { font-size: 3rem !important; }</style>""", unsafe_allow_html=True)

# ==========================================
# 4. APP LOGIC
# ==========================================
if page == "Home & Prep":
    st.title(f"🏥 {modality} Preparation Guide")
    
    # --- NEW: Anxiety Slider ---
    st.markdown("### How are you feeling today?")
    anxiety_level = st.slider("Slide to show your anxiety level (1 = Calm, 10 = Very Scared)", 1, 10, 5)
    
    if anxiety_level >= 7:
        st.info("💙 **It is completely normal to feel scared.** We are here to help you. Take a deep breath in for 4 seconds, hold for 4 seconds, and breathe out for 4 seconds. You are safe.")
    elif anxiety_level >= 4:
        st.success("😊 **You are doing great.** Just follow the steps, and remember the radiographer is there to help you.")
    else:
        st.success("🌟 **That's wonderful to hear!** You are well-prepared for your scan today.")

    st.markdown("---")
    
    # Timeline
    st.markdown("### 🗺️ What happens on the day:")
    st.markdown("**1. Arrive & Check-in** ➡️ **2. The Scan (15-30 mins)** ➡️ **3. Go Home**")
    st.markdown("---")
    
    # Dynamic Content
    if modality == "CT Scan":
        card("Fasting & Meds", "Do not eat for 4 hours. Tell us if you take Metformin.", "🚫")
        st.markdown('<div class="warning-box"><b>Kidney Check:</b> We need your latest Creatinine blood test. If it is 30-45, a radiologist must approve the scan.</div>', unsafe_allow_html=True)
    elif modality == "MRI":
        card("Implants", "You MUST bring your implant passport or surgery records.", "📄")
        st.warning("📄 **Don't forget your implant passport!**")
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
    st.write("Please answer these questions so we can ensure your safety during the scan.")
    
    col1, col2 = st.columns(2)
    
    # A subtle, elegant style for the question boxes
    box_style = "background-color: #E8F0F8; color: #1A5276 !important; padding: 15px; border-radius: 8px; margin-top: 10px; margin-bottom: 10px; font-weight: 600; border-left: 4px solid #3498DB;"
    
    with col1:
        st.markdown(f'<div style="{box_style}">1. Do you have any metal implants or a pacemaker?</div>', unsafe_allow_html=True)
        has_metal = st.checkbox("Yes, I have metal", label_visibility="collapsed")
        
        st.markdown(f'<div style="{box_style}">2. Are you pregnant or possibly pregnant?</div>', unsafe_allow_html=True)
        is_pregnant = st.checkbox("Yes, I am pregnant", label_visibility="collapsed")
        
    with col2:
        st.markdown(f'<div style="{box_style}">3. Do you have a severe fear of closed spaces?</div>', unsafe_allow_html=True)
        is_claustrophobic = st.checkbox("Yes, I have claustrophobia", label_visibility="collapsed")
        
        if modality in ["CT Scan", "MRI"]:
            st.markdown(f'<div style="{box_style}">4. What is your latest Creatinine level?</div>', unsafe_allow_html=True)
            creatinine = st.number_input("Creatinine", min_value=0, max_value=2000, value=80, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("Check My Safety", type="primary"):
        if has_metal:
            st.error("🛑 **DANGER:** Do not enter the MRI room. Speak to staff immediately.")
        elif is_pregnant:
            st.warning("⚠️ **WARNING:** Tell the doctor immediately. Avoid CT/X-Ray unless necessary.")
        elif modality in ["CT Scan", "MRI"] and creatinine < 45:
            st.error("🚨 **KIDNEY ALERT:** Your Creatinine is below 45. A radiologist MUST review your blood test.")
        elif is_claustrophobic:
            st.info("💡 **NOTE:** We will prepare light anesthesia for you.")
        else:
            st.success("✅ **SAFE:** You are cleared for your scan.")

elif page == "Virtual 3D Room":
    st.title(f"🧲 3D Room: {modality}")
    st.write("Explore the room to help you feel prepared.")
    
    # YOUR SKETCHFAB 3D MODELS (Kept exactly as you had them)
    if modality == "CT Scan":
        components.iframe("https://sketchfab.com/models/ef06495bdf0f4dbc94e0dbc7c05dd21c/embed", height=500)
    elif modality == "MRI":
        components.iframe("https://sketchfab.com/models/74bc0dea266c4b228fcee69da6535330/embed", height=500)
    elif modality == "Fluoroscopy":
        components.iframe("https://sketchfab.com/models/9e4f12f999b344fcb257d805a05d24bd/embed", height=500)
        st.info("💡 Note: The Fluoroscopy machine is called a 'C-arm' because of its shape. You will lie on a table while the C-arm moves around you.")
    elif modality == "X-Ray":
        components.iframe("https://sketchfab.com/models/8c7f17ae00324cc7a67e2fede13a8d58/embed", height=500) 
    elif modality == "Ultrasound (USG)":
        components.iframe("https://sketchfab.com/models/17aa217cd9e4469cb2834d5fe9c09f72/embed", height=500)  
    elif modality == "Mammography":
        components.iframe("https://sketchfab.com/models/293306631a5b4d1da411c9c6804bfa1b/embed", height=500)  
    elif modality == "DEXA":
        components.iframe("https://sketchfab.com/models/681aa7ab7c3e4734929024c2f375edbe/embed", height=500) 
    else:
        st.info("A specific 3D model is not available for this room, but you will be in a standard imaging room.")

elif page == "Download Checklist":
    st.title("📄 Personalized Checklist")
    st.write("Check off the items below as you pack for your visit.")
    
    checklist = ["Bring your ID and insurance card", "Arrive 15 minutes early"]
    
    if modality == "CT Scan":
        checklist.extend(["Bring your latest blood test (Creatinine)", "Do not eat 4 hours before"])
    elif modality == "MRI":
        checklist.extend(["Bring implant passports / surgery documents", "Remove all metal jewelry"])
    elif modality == "Mammography":
        checklist.extend(["Do not use deodorant on the day", "Schedule outside your menstrual cycle"])
    else:
        checklist.append("Wear comfortable clothing without metal")

    st.subheader(f"Your {modality} Checklist:")
    
    # --- Interactive Checkboxes ---
    checked_count = 0
    for i, item in enumerate(checklist):
        if st.checkbox(item, key=f"check_{i}"):
            checked_count += 1
            
    # --- Progress Bar ---
    total_items = len(checklist)
    progress = checked_count / total_items
    st.progress(progress)
    
    if checked_count == total_items:
        st.balloons()
        st.success("🎉 **You are fully prepared for your scan!** You can now download your PDF.")
    elif checked_count > 0:
        st.info(f"You have checked {checked_count} out of {total_items} items. Keep going!")
        
    st.markdown("---")
    
    # --- PDF Download ---
    if checked_count == total_items:
        pdf_bytes = create_pdf(checklist, modality)
        st.download_button(
            label="⬇️ Download My Checklist (PDF)", 
            data=pdf_bytes, 
            file_name=f"{modality}_checklist.pdf", 
            mime="application/pdf"
        )
    else:
        st.warning("Please check all the boxes above to unlock your PDF download.")

elif page == "FAQ":
    st.title("❓ Frequently Asked Questions")
    
    with st.expander("Is radiation dangerous?"):
        st.write("We use the lowest possible dose. The benefit of early diagnosis is much higher than the small risk.")
    
    with st.expander("Why can't I bring metal into an MRI room?"):
        st.write("MRI uses very strong magnets. Metal objects (like keys, watches, or pacemakers) can be pulled into the machine and cause serious injury.")
    
    with st.expander("Are contrast dyes dangerous?"):
        st.write("They are usually safe, but they can affect people with kidney problems. That is why we check your Creatinine level.")
        
    with st.expander("How do I read my radiology report?"):
        st.write("Your report will be sent to your doctor. Don't panic if you see medical words you don't understand. Your doctor will explain the results to you and what the next steps are.")
