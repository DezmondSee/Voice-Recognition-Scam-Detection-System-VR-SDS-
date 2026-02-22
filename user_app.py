import streamlit as st
from views import login_page, user_dashboard

# CENTERED layout
st.set_page_config(page_title="VR-SDS Mobile App", layout="centered")

# ==========================================
# LOAD EXTERNAL CSS
# ==========================================
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not load CSS: {e}")

load_css("assets/user_style.css")

# ==========================================
# ROUTING LOGIC
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user'] = None

if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align: center; color: #2E66FF;'>📱 VR-SDS Scanner</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666666;'>AI Voice Scam Detection</p>", unsafe_allow_html=True)
    st.divider()
    login_page.render()
else:
    user = st.session_state['user']
    if user['role'] == 'admin':
        st.error("🚨 Admins cannot use the mobile app. Please log in through the Web Portal (Port 8501).")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
    else:
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['user'] = None
            st.rerun()
        user_dashboard.render(user)