import streamlit as st
from views import login_page, admin_dashboard

# WIDE layout
st.set_page_config(page_title="VR-SDS Admin Portal", layout="wide")

# ==========================================
# LOAD EXTERNAL CSS
# ==========================================
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not load CSS: {e}")

load_css("assets/admin_style.css")

# ==========================================
# ROUTING LOGIC
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user'] = None

if not st.session_state['logged_in']:
    st.markdown("<h1 style='text-align: center; color: #4DA8DA;'>🏢 VR-SDS Enterprise Portal</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #A0A0A0;'>Authorized Personnel Only</p>", unsafe_allow_html=True)
    st.divider()
    login_page.render()
else:
    user = st.session_state['user']
    if user['role'] != 'admin':
        st.error("🚨 Access Denied: This portal is for Administrators only. Please use the Mobile App on Port 8502.")
        if st.button("Logout"):
            st.session_state['logged_in'] = False
            st.rerun()
    else:
        if st.sidebar.button("Logout"):
            st.session_state['logged_in'] = False
            st.session_state['user'] = None
            st.rerun()
        admin_dashboard.render()