import streamlit as st
from views import login_page, user_dashboard, admin_dashboard

st.set_page_config(page_title="VR-SDS Enterprise", layout="wide")
if 'logged_in' not in st.session_state: st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login_page.render()
else:
    user = st.session_state['user']
    if st.sidebar.button("Logout"):
        st.session_state['logged_in'] = False
        st.rerun()
        
    if user['role'] == 'admin': admin_dashboard.render()
    else: user_dashboard.render(user)