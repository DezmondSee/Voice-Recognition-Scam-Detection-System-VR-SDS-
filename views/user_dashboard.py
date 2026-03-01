import streamlit as st
import os
import time
from controllers import scan_controller, user_controller
from realtime_processor import RealTimeScamDetector

def render(user):
    st.sidebar.title(f"User: {user['username']}")
    menu = st.sidebar.radio("Menu", [
        "Dashboard", 
        "Real-Time Call Shield", 
        "Scan Audio", 
        "Scan Text", 
        "History", 
        "Trusted Contacts", 
        "Report Scam"
    ])
    
    if menu == "Dashboard":
        st.title("User Dashboard")
        st.info("System Protected")

    elif menu == "Real-Time Call Shield":
        st.header("🛡️ VR-SDS Real-Time Call Shield")
        
        # Permission Gate
        if "mic_permission" not in st.session_state:
            st.session_state.mic_permission = False

        if not st.session_state.mic_permission:
            st.warning("Microphone Permission Required")
            st.write("To protect you from scams in real-time, the system needs permission to analyze incoming call audio.")
            if st.button("Grant Permission"):
                st.session_state.mic_permission = True
                st.rerun()
            return

        # Monitoring Setup
        if "detector" not in st.session_state:
            st.session_state.detector = RealTimeScamDetector()
            st.session_state.is_monitoring = False
            st.session_state.last_res = ("LISTENING", 0)

        def update_ui(pred, conf):
            st.session_state.last_res = (pred, conf)

        col1, col2 = st.columns(2)
        if col1.button("🚀 Start Monitoring", disabled=st.session_state.is_monitoring):
            st.session_state.is_monitoring = True
            st.session_state.detector.start(update_ui)
            st.rerun()

        if col2.button("🛑 Stop Monitoring", disabled=not st.session_state.is_monitoring):
            st.session_state.detector.stop()
            st.session_state.is_monitoring = False
            st.rerun()

        # Results Display
        verdict, conf = st.session_state.last_res
        if st.session_state.is_monitoring:
            st.divider()
            if verdict == "SCAM":
                st.error(f"🚨 ALERT: High Scam Probability Detected! ({conf}%)")
            elif verdict == "SAFE":
                st.success(f"✅ Conversation appears Safe ({conf}%)")
            else:
                st.info("🎤 Active Monitoring... Listening to segments.")
            
            time.sleep(1)
            st.rerun()

    elif menu == "Scan Audio":
        st.header("Analyze Audio")
        uploaded = st.file_uploader("Upload Audio", type=['wav', 'mp3'])
        if uploaded and st.button("Scan"):
            with open("temp.wav", "wb") as f: f.write(uploaded.getbuffer())
            res = scan_controller.process_audio(user['user_id'], "temp.wav")
            if "error" in res: st.error(res['error'])
            elif res['verdict'] == "SCAM": st.error(f"🚨 SCAM! ({res['confidence']}%)")
            else: st.success(f"✅ SAFE ({res['confidence']}%)")
            if os.path.exists("temp.wav"): os.remove("temp.wav")

    elif menu == "Scan Text":
        st.header("Scan Message Text")
        txt = st.text_area("Message Content")
        if st.button("Check"):
            res = scan_controller.process_text(user['user_id'], txt)
            if res.get('error'): st.error(res['error'])
            elif res['verdict'] == "SCAM": st.error("🚨 PHISHING DETECTED")
            else: st.success("✅ SAFE")

    elif menu == "History":
        st.header("Scan History")
        st.dataframe(user_controller.get_history(user['user_id']))

    elif menu == "Trusted Contacts":
        st.header("Trusted Contacts")
        c1, c2 = st.columns(2)
        with c1:
            n, p = st.text_input("Name"), st.text_input("Phone")
            if st.button("Add"): 
                user_controller.add_trusted_contact(user['user_id'], n, p)
                st.success("Contact Added")
        with c2: 
            st.table(user_controller.get_trusted_contacts(user['user_id']))

    elif menu == "Report Scam":
        st.header("Submit Scam Report")
        p, c, d = st.text_input("Number"), st.selectbox("Type", ["Phishing", "Bank", "Voice"]), st.text_area("Desc")
        if st.button("Report"): 
            user_controller.submit_report(user['user_id'], p, c, d)
            st.success("Report Submitted")