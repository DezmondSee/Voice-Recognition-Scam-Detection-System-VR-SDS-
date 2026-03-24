import streamlit as st
from views import login_page, admin_dashboard

def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not load CSS: {e}")

def render_logic():
    load_css("assets/admin_style.css")
    role_info = st.session_state.get('admin_role', 'Admin')
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['user'] = None

    if not st.session_state['logged_in']:
        st.markdown(f"<h1 style='text-align: center; color: #4DA8DA;'>🏢 VR-SDS {role_info} Portal</h1>", unsafe_allow_html=True)
        st.divider()
        login_page.render()
    else:
        user = st.session_state['user']
        if user['role'] != 'admin':
            st.error("🚨 Access Denied: Admin account required.")
            if st.button("Logout"):
                st.session_state['logged_in'] = False
                st.rerun()
        else:
            if st.sidebar.button("Logout / Switch Portal"):
                st.session_state['logged_in'] = False
                st.session_state['portal'] = None
                st.session_state['admin_role'] = None
                st.rerun()
            admin_dashboard.render()

if __name__ == "__main__":
    st.set_page_config(page_title="VR-SDS Admin Portal", layout="wide")
    render_logic()