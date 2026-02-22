from config.db_config import get_db_connection
import streamlit as st

def login_user(username, password):
    conn = get_db_connection()
    if not conn: return None
    cursor = conn.cursor(dictionary=True)
    
    # Strip spaces to prevent accidental "Invalid Credentials"
    username = username.strip()
    password = password.strip()
    
    cursor.execute("SELECT * FROM users WHERE username=%s AND password_hash=%s", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    # If user exists but is_active is 0 or False
    if user and not user.get('is_active', True): 
        return "BANNED"
        
    return user

def register_user(username, password, email, sec_question, sec_answer):
    conn = get_db_connection()
    if not conn: return False
    try:
        cursor = conn.cursor()
        # FIX: Added 'is_active' and 'role' to the INSERT statement
        cursor.execute("""
            INSERT INTO users 
            (username, password_hash, email, security_question, security_answer, is_active, role) 
            VALUES (%s, %s, %s, %s, %s, 1, 'user')
        """, (username.strip(), password.strip(), email.strip(), sec_question, sec_answer.lower().strip()))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"🚨 DATABASE ERROR: {e}")
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
    cursor.execute("UPDATE users SET password_hash=%s WHERE username=%s AND security_answer=%s", 
                   (new_password.strip(), username.strip(), sec_answer.lower().strip()))
    conn.commit()
    success = cursor.rowcount > 0
    conn.close()
    return success