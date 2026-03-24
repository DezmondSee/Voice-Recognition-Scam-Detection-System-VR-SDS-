import streamlit as st
from views import login_page, user_dashboard

def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Could not load CSS: {e}")

def render_logic():
    load_css("assets/user_style.css")
    
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['user'] = None

    if not st.session_state['logged_in']:
        login_page.render()
    else:
        user = st.session_state['user']
        if user['role'] == 'admin':
            st.error("🚨 Admins must use the Web Portal.")
            if st.button("Logout"):
                st.session_state['logged_in'] = False
                st.rerun()
        else:
            if st.sidebar.button("Logout / Switch Portal"):
                st.session_state['logged_in'] = False
                st.session_state['portal'] = None
                st.rerun()
            user_dashboard.render(user)

if __name__ == "__main__":
    st.set_page_config(page_title="VR-SDS Mobile App", layout="centered")
    render_logic() 