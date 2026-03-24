import streamlit as st

def main():
    st.set_page_config(page_title="VR-SDS Multi-Portal", layout="centered")

    if 'portal' not in st.session_state:
        st.session_state['portal'] = None
    if 'admin_role' not in st.session_state:
        st.session_state['admin_role'] = None

    # Step 1: Portal Selection
    if st.session_state['portal'] is None:
        st.title("🛡️ VR-SDS Scam Detection System")
        st.subheader("Select Access Portal")
        
        c1, c2 = st.columns(2)
        with c1:
            if st.button("📱 User Portal", use_container_width=True):
                st.session_state['portal'] = 'user'
                st.rerun()
        with c2:
            if st.button("🔑 Admin Portal", use_container_width=True):
                st.session_state['portal'] = 'admin'
                st.rerun()

    # Step 2: Handle Admin Role Selection
    elif st.session_state['portal'] == 'admin' and st.session_state['admin_role'] is None:
        st.title("🔑 Admin Access")
        role = st.selectbox("Select Admin Type:", [
            "System Administrator", 
            "Security Analyst", 
            "Research Lead"
        ])
        if st.button("Confirm Role & Login"):
            st.session_state['admin_role'] = role
            st.rerun()
        if st.button("⬅️ Back"):
            st.session_state['portal'] = None
            st.rerun()

    # Step 3: Launch Selected App Logic
    else:
        if st.session_state['portal'] == 'admin':
            import admin_app
            admin_app.render_logic()
        else:
            import user_app
            user_app.render_logic()

if __name__ == "__main__":
    main()