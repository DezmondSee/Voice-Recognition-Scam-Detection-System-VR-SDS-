from config.db_config import get_db_connection

def login_user(username, password):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s AND password_hash=%s", (username, password))
    user = cursor.fetchone()
    conn.close()
    if user and not user['is_active']: return "BANNED"
    return user

def register_user(username, password, email, sec_question, sec_answer):
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password_hash, email, security_question, security_answer) VALUES (%s, %s, %s, %s, %s)", 
                       (username, password, email, sec_question, sec_answer.lower()))
        conn.commit()
        return True
    except Exception as e:
        import streamlit as st
        st.error(f"🚨 REAL DATABASE ERROR: {e}")  # This forces the real error onto the screen!
        return False
    finally: conn.close()

def get_security_question(username):
    conn = get_db_connection()
    
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT security_question FROM users WHERE username=%s", (username,))
    user = cursor.fetchone()
    conn.close()
    return user['security_question'] if user else None

def reset_password(username, sec_answer, new_password):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password_hash=%s WHERE username=%s AND security_answer=%s", (new_password, username, sec_answer.lower()))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success