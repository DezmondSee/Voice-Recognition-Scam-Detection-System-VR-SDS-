import streamlit as st
import os
from controllers import scan_controller, user_controller

def render(user):
    st.sidebar.title(f"User: {user['username']}")
    menu = st.sidebar.radio("Menu", ["Dashboard", "Scan Audio", "Scan Text", "History", "Trusted Contacts", "Report Scam"])
    
    if menu == "Dashboard":
        st.title("User Dashboard")
        st.info("System Protected")
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
        txt = st.text_area("Message Content")
        if st.button("Check"):
            res = scan_controller.process_text(user['user_id'], txt)
            if res.get('error'): st.error(res['error'])
            elif res['verdict'] == "SCAM": st.error("🚨 PHISHING DETECTED")
            else: st.success("✅ SAFE")
    elif menu == "History":
        st.dataframe(user_controller.get_history(user['user_id']))
    elif menu == "Trusted Contacts":
        c1, c2 = st.columns(2)
        with c1:
            n, p = st.text_input("Name"), st.text_input("Phone")
            if st.button("Add"): user_controller.add_trusted_contact(user['user_id'], n, p)
        with c2: st.table(user_controller.get_trusted_contacts(user['user_id']))
    elif menu == "Report Scam":
        p, c, d = st.text_input("Number"), st.selectbox("Type", ["Phishing", "Bank"]), st.text_area("Desc")
        if st.button("Report"): user_controller.submit_report(user['user_id'], p, c, d)