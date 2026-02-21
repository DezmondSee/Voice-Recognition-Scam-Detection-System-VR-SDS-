import streamlit as st
from services.auth_service import login_user, register_user, get_security_question, reset_password

def render():
    st.title("🛡️ VR-SDS Enterprise System")
    st.write("Voice Recognition & Scammer Detection System")
    
    tab1, tab2, tab3 = st.tabs(["Sign In", "Register", "Forgot Password"])

    with tab1:
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Password", type="password", key="login_p")
        if st.button("Sign In", type="primary"):
            user = login_user(u, p)
            if user == "BANNED": st.error("🚨 Account Banned.")
            elif user:
                st.session_state['user'] = user
                st.session_state['logged_in'] = True
                st.rerun()
            else: st.error("❌ Invalid Credentials")

    with tab2:
        nu, ne, np = st.text_input("New Username"), st.text_input("Email"), st.text_input("Password", type="password")
        sec_q = st.selectbox("Security Question", ["What was the name of your first pet?", "What city were you born in?", "What is your role?"])
        sec_a = st.text_input("Security Answer")
        if st.button("Register"):
            if register_user(nu, np, ne, sec_q, sec_a): st.success("✅ Account created!")
            else: st.error("❌ Username taken.")

    with tab3:
        forgot_u = st.text_input("Enter Username to reset")
        if forgot_u:
            q = get_security_question(forgot_u)
            if q:
                st.info(f"**Question:** {q}")
                ans = st.text_input("Answer")
                new_pw = st.text_input("New Password", type="password")
                if st.button("Reset Password"):
                    if reset_password(forgot_u, ans, new_pw): st.success("✅ Reset successful!")
                    else: st.error("❌ Incorrect answer.")
            else: st.warning("User not found.")