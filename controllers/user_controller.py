import pandas as pd
from config.db_config import get_db_connection

def get_history(user_id):
    conn = get_db_connection()
    df = pd.read_sql(f"SELECT timestamp, scan_type, verdict, confidence FROM call_logs WHERE user_id={user_id} ORDER BY timestamp DESC", conn)
    conn.close()
    return df

def add_trusted_contact(user_id, name, phone):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO trusted_contacts (user_id, contact_name, phone_number) VALUES (%s, %s, %s)", (user_id, name, phone))
    conn.commit()
    conn.close()

def get_trusted_contacts(user_id):
    conn = get_db_connection()
    df = pd.read_sql(f"SELECT contact_name, phone_number FROM trusted_contacts WHERE user_id={user_id}", conn)
    conn.close()
    return df

def submit_report(user_id, phone, category, desc):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO scam_reports (user_id, phone_number, category, description) VALUES (%s, %s, %s, %s)", (user_id, phone, category, desc))
    conn.commit()
    conn.close()