import streamlit as st
from services.auth_service import login_user, register_user, get_security_question

def render():
    # We removed the hardcoded st.title here because it is now handled 
    # individually in admin_app.py and user_app.py for a professional look.

    tab1, tab2, tab3 = st.tabs(["Sign In", "Register", "Forgot Password"])

    # --- SIGN IN TAB ---
    with tab1:
        u = st.text_input("Username", key="login_u")
        p = st.text_input("Password", type="password", key="login_p")
        
        if st.button("Sign In", type="primary"):
            if u and p:
                user = login_user(u, p)
                if user == "BANNED":
                    st.error("🚫 This account has been deactivated. Please contact the Administrator.")
                elif user:
                    # Store user data in session state for routing
                    st.session_state['user'] = user
                    st.session_state['logged_in'] = True
                    st.success(f"Welcome back, {user['username']}!")
                    st.rerun()
                else:
                    st.error("❌ Invalid Credentials. Please try again.")
            else:
                st.warning("⚠️ Please enter both username and password.")

    # --- REGISTER TAB ---
    with tab2:
        st.subheader("Create New Account")
        nu = st.text_input("New Username", help="Choose a unique username")
        ne = st.text_input("Email Address")
        np = st.text_input("New Password", type="password")
        sec_q = st.selectbox("Security Question", [
            "What was the name of your first pet?", 
            "What is your mother's maiden name?",
            "What was the name of your primary school?"
        ])
        sec_a = st.text_input("Security Answer")
        
        if st.button("Register"):
            if nu and np and ne and sec_a:
                # The service now automatically sets role='user' and is_active=1
                if register_user(nu, np, ne, sec_q, sec_a):
                    st.success("✅ Registration Successful! You can now Sign In.")
                else:
                    st.error("❌ Registration failed. Username might already be taken.")
            else:
                st.warning("⚠️ All fields are required for registration.")

    # --- FORGOT PASSWORD TAB ---
    with tab3:
        st.subheader("Reset Password")
        forgot_u = st.text_input("Enter Username to reset")
        if forgot_u:
            q = get_security_question(forgot_u)
            if q:
                st.info(f"Question: {q}")
                ans = st.text_input("Your Answer", key="reset_ans")
                new_p = st.text_input("New Password", type="password", key="reset_new_p")
                
                if st.button("Reset Password"):
                    # This logic would link to your reset_password service
                    st.info("Reset logic pending service integration.")
            else:
                st.error("User not found.")