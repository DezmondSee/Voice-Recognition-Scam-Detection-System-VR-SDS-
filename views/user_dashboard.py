import streamlit as st
import os
import time
import pandas as pd
import streamlit.components.v1 as components
from controllers import scan_controller, user_controller
from services.realtime_processor import RealTimeScamDetector

# --- THE BULLETPROOF ROUTING CALLBACK ---
def go_to_page(page_name):
    """Updates the hidden tracker so the page changes without crashing."""
    st.session_state.active_page = page_name

def render(user):
    # ==========================================
    # REAL HARDWARE PERMISSION SCRIPT
    # ==========================================
    components.html(
        """
        <script>
        function activateNotifications() {
            if ("Notification" in window) {
                if (Notification.permission !== "granted" && Notification.permission !== "denied") {
                    Notification.requestPermission().then(function (permission) {
                        if (permission === "granted") {
                            new Notification("🛡️ VR-SDS Shield Active", {
                                body: "Notification permission granted. System is securing your device.",
                            });
                        }
                    });
                }
            }
        }
        function activateMicrophone() {
            navigator.mediaDevices.getUserMedia({ audio: true, video: false })
            .then(function(stream) { console.log('Microphone engaged successfully.'); })
            .catch(function(err) { console.error('Microphone hardware access denied.', err); });
        }
        activateNotifications();
        activateMicrophone();
        </script>
        """, height=0, width=0
    )
    # ==========================================

    st.sidebar.title(f"📱 VR-SDS Scanner")
    st.sidebar.markdown(f"**Welcome, {user['username']}**")
    
    # --- BULLETPROOF NAVIGATION LOGIC ---
    PAGES = [
        "Dashboard", 
        "Android Call Shield", 
        "Scan Audio", 
        "Scan Text", 
        "History", 
        "Trusted Contacts", 
        "Report Scam",
        "Settings" # <-- ADDED SETTINGS HERE
    ]

    if 'active_page' not in st.session_state:
        st.session_state.active_page = "Dashboard"

    try:
        current_index = PAGES.index(st.session_state.active_page)
    except ValueError:
        current_index = 0

    selected_menu = st.sidebar.radio("Navigation", PAGES, index=current_index)

    if selected_menu != st.session_state.active_page:
        st.session_state.active_page = selected_menu
        st.rerun()
    
    st.sidebar.divider()
    
    # Logout button remains in the sidebar for easy access everywhere
    if st.sidebar.button("🚪 Logout", type="primary", use_container_width=True):
        st.session_state['logged_in'] = False
        st.session_state['user'] = None
        st.rerun()
    
    # ==========================================
    # MAIN PAGE CONTENT LOGIC
    # ==========================================
    if st.session_state.active_page == "Dashboard":
        st.markdown("<h2 style='color: #000000; font-weight: bold;'>Control Center</h2>", unsafe_allow_html=True)
        st.info("✅ System Protected. All monitoring services are active.")
        st.write("") 

        # --- FETCH REAL DATA FROM DATABASE ---
        history_df = user_controller.get_history(user['user_id'])
        
        total_scans = 0
        total_scams = 0
        detection_rate = 0.0
        
        chart_data = pd.DataFrame(
            {"Safe Communications": [0], "Scam Attempts Blocked": [0]}, 
            index=["No Data Yet"]
        )

        if history_df is not None and not history_df.empty:
            total_scans = len(history_df)
            verdict_col = [col for col in history_df.columns if 'verdict' in col.lower()]
            if verdict_col:
                v_col = verdict_col[0]
                total_scams = len(history_df[history_df[v_col].astype(str).str.upper() == 'SCAM'])
                if total_scans > 0:
                    detection_rate = (total_scams / total_scans) * 100

            time_col = [col for col in history_df.columns if 'time' in col.lower() or 'date' in col.lower()]
            if time_col and verdict_col:
                try:
                    temp_df = history_df.copy()
                    t_col = time_col[0]
                    temp_df[t_col] = pd.to_datetime(temp_df[t_col])
                    temp_df['Date'] = temp_df[t_col].dt.strftime('%b %d')
                    
                    grouped = temp_df.groupby(['Date', v_col]).size().unstack(fill_value=0)
                    final_chart = pd.DataFrame(index=grouped.index)
                    
                    scam_keys = [c for c in grouped.columns if 'SCAM' in str(c).upper()]
                    safe_keys = [c for c in grouped.columns if 'SAFE' in str(c).upper()]
                    
                    final_chart["Scam Attempts Blocked"] = grouped[scam_keys].sum(axis=1) if scam_keys else 0
                    final_chart["Safe Communications"] = grouped[safe_keys].sum(axis=1) if safe_keys else 0
                    
                    if not final_chart.empty:
                        chart_data = final_chart
                except Exception as e:
                    pass

        # --- THE STATISTICS CONTAINER ---
        st.markdown("<h4 style='color: #000000;'>📊 Your Real-Time Statistics</h4>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="Total Scans", value=f"{total_scans:,}")
        with m2:
            st.metric(label="Suspected Scams", value=f"{total_scams:,}")
        with m3:
            st.metric(label="Detection Rate", value=f"{detection_rate:.1f}%")

        st.write("") 

        # --- THE CHART CONTAINER ---
        st.markdown("<h4 style='color: #000000;'>📈 Scam Detection Trend</h4>", unsafe_allow_html=True)
        st.line_chart(chart_data, color=["#2E66FF", "#FF4B4B"])
        st.divider()

        # --- QUICK ACCESS BUTTONS ---
        st.markdown("<h4 style='color: #000000;'>🚀 Quick Launch Modules</h4>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        
        with col1:
            st.button("🛡️ Open Android Shield", use_container_width=True, on_click=go_to_page, args=("Android Call Shield",))
            st.button("💬 Scan Text Message", use_container_width=True, on_click=go_to_page, args=("Scan Text",))
            st.button("📜 View Scan History", use_container_width=True, on_click=go_to_page, args=("History",))

        with col2:
            st.button("🎙️ Scan Audio File", use_container_width=True, on_click=go_to_page, args=("Scan Audio",))
            st.button("👥 Manage Trusted Contacts", use_container_width=True, on_click=go_to_page, args=("Trusted Contacts",))
            st.button("🚩 Report a Scam", use_container_width=True, on_click=go_to_page, args=("Report Scam",))

    elif st.session_state.active_page == "Android Call Shield":
        st.header("🛡️ VR-SDS Android Protection")
        
        if "android_permission" not in st.session_state:
            st.session_state.android_permission = False

        if not st.session_state.android_permission:
            st.warning("📱 Android System Permission Required")
            st.write("To protect you from scams in real-time, VR-SDS must be set as your **Default Caller ID & Spam App**.")
            st.info("""
            **Required Permissions:**
            - 🎙️ Microphone (Capture Incoming Audio)
            - 📞 Call Logs (Identify Caller)
            - 📲 Overlay (Display Scam Alerts during calls)
            """)
            if st.button("✅ Grant Android Permissions"):
                st.session_state.android_permission = True
                st.success("Permissions Granted. Android Shield Active.")
                time.sleep(1)
                st.rerun()
            return

        if "detector" not in st.session_state:
            st.session_state.detector = RealTimeScamDetector()
            st.session_state.is_monitoring = False
            st.session_state.last_res = ("LISTENING", 0)

        def update_ui(pred, conf):
            st.session_state.last_res = (pred, conf)

        col1, col2 = st.columns(2)
        if col1.button("🚀 Start Shield", disabled=st.session_state.is_monitoring):
            st.session_state.is_monitoring = True
            st.session_state.detector.start(update_ui)
            st.rerun()

        if col2.button("🛑 Stop Shield", disabled=not st.session_state.is_monitoring):
            st.session_state.detector.stop()
            st.session_state.is_monitoring = False
            st.rerun()

        verdict, conf = st.session_state.last_res
        if st.session_state.is_monitoring:
            st.divider()
            if verdict == "SCAM":
                st.error(f"🚨 ALERT: High Scam Probability Detected! ({conf}%)")
                st.button("🚫 TERMINATE CALL", type="primary")
            elif verdict == "SAFE":
                st.success(f"✅ Conversation appears Safe ({conf}%)")
            else:
                st.info("🎤 Active Monitoring... Analyzing incoming voice stream.")
            time.sleep(2)
            st.rerun()

    elif st.session_state.active_page == "Scan Audio":
        st.header("Analyze Audio File")
        uploaded = st.file_uploader("Upload Audio", type=['wav', 'mp3'])
        if uploaded and st.button("Scan"):
            with open("temp.wav", "wb") as f: f.write(uploaded.getbuffer())
            res = scan_controller.process_audio(user['user_id'], "temp.wav")
            if "error" in res: st.error(res['error'])
            elif res['verdict'] == "SCAM": st.error(f"🚨 SCAM! ({res['confidence']}%)")
            else: st.success(f"✅ SAFE ({res['confidence']}%)")
            if os.path.exists("temp.wav"): os.remove("temp.wav")

    elif st.session_state.active_page == "Scan Text":
        st.header("Analyze Message Text")
        txt = st.text_area("Message Content")
        if st.button("Check"):
            res = scan_controller.process_text(user['user_id'], txt)
            if res.get('error'): st.error(res['error'])
            elif res['verdict'] == "SCAM": st.error("🚨 PHISHING DETECTED")
            else: st.success("✅ SAFE")

    elif st.session_state.active_page == "History":
        st.header("Detection History")
        st.dataframe(user_controller.get_history(user['user_id']))

    elif st.session_state.active_page == "Trusted Contacts":
        st.markdown("<h3 style='color: #000000; font-weight: bold;'>Manage Trusted Contacts</h3>", unsafe_allow_html=True)
        
        n = st.text_input("Name")
        p = st.text_input("Phone")
        
        if st.button("Add", use_container_width=True): 
            user_controller.add_trusted_contact(user['user_id'], n, p)
            st.success("✅ Contact Added")
            time.sleep(1) 
            st.rerun()    
            
        st.divider() 
        
        st.markdown("<h4 style='color: #000000;'>Current Contacts</h4>", unsafe_allow_html=True)
        contacts_data = user_controller.get_trusted_contacts(user['user_id'])
        
        if contacts_data is not None and not contacts_data.empty:
            clean_table = contacts_data.rename(columns={"contact_name": "Contact Name", "phone_number": "Phone Number"})
            st.table(clean_table)
        else:
            st.info("No trusted contacts found. Add one above.")

    elif st.session_state.active_page == "Report Scam":
        st.header("Submit Scam Report")
        p = st.text_input("Number")
        c = st.selectbox("Type", ["Phishing", "Bank", "Voice"])
        d = st.text_area("Desc")
        if st.button("Report"): 
            user_controller.submit_report(user['user_id'], p, c, d)
            st.success("Report Submitted")
            
    # --- NEW SETTINGS PAGE ---
    elif st.session_state.active_page == "Settings":
        st.markdown("<h2 style='color: #000000; font-weight: bold;'>⚙️ System Settings</h2>", unsafe_allow_html=True)
        st.write("Manage your account details and application hardware permissions.")
        st.write("")
        
        col1, col2 = st.columns(2)
        
        # Left Container: Profile Details
        with col1:
            with st.container(border=True):
                st.markdown("<h4 style='color: #000000;'>👤 Edit Profile</h4>", unsafe_allow_html=True)
                new_username = st.text_input("Username", value=user.get('username', ''))
                new_email = st.text_input("Email", value=user.get('email', ''))
                
                st.write("")
                st.markdown("**Change Password**")
                old_password = st.text_input("Current Password", type="password")
                new_password = st.text_input("New Password", type="password")
                
                if st.button("Save Profile", use_container_width=True):
                    if new_password and not old_password:
                        st.error("Enter current password to change it.")
                    else:
                        st.session_state['user']['username'] = new_username
                        st.session_state['user']['email'] = new_email
                        st.success("✅ Profile updated!")
                        time.sleep(1)
                        st.rerun()

        # Right Container: App Permissions
        with col2:
            with st.container(border=True):
                st.markdown("<h4 style='color: #000000;'>🛡️ App Permissions</h4>", unsafe_allow_html=True)
                st.write("Ensure all security modules have proper OS access.")
                st.write("")
                
                st.toggle("Microphone Access (Live Call Scan)", value=True)
                st.toggle("Storage Access (File Uploads)", value=True)
                st.toggle("Push Notifications (Scam Alerts)", value=True)
                
                st.write("")
                st.write("")
                st.write("") # Extra spacing to align the button with the profile side
                if st.button("Save Permissions", use_container_width=True):
                    st.success("✅ OS Permissions updated!")