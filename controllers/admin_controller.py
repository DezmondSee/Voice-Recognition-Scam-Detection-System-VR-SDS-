import pandas as pd
from config.db_config import get_db_connection

def get_system_stats():
    conn = get_db_connection()
    if not conn: return {"users": 0, "scams": 0, "reports": 0}
    stats = {}
    stats['users'] = pd.read_sql("SELECT COUNT(*) as c FROM users WHERE role='user'", conn).iloc[0]['c']
    stats['scams'] = pd.read_sql("SELECT COUNT(*) as c FROM call_logs WHERE verdict='SCAM'", conn).iloc[0]['c']
    stats['reports'] = pd.read_sql("SELECT COUNT(*) as c FROM scam_reports", conn).iloc[0]['c']
    conn.close()
    return stats

def get_scam_trend_data():
    conn = get_db_connection()
    if not conn: return pd.DataFrame()
    query = "SELECT DATE(timestamp) as date, COUNT(*) as scams_detected FROM call_logs WHERE verdict='SCAM' GROUP BY DATE(timestamp) ORDER BY date ASC LIMIT 30"
    df = pd.read_sql(query, conn)
    conn.close()
    if not df.empty: df['date'] = df['date'].astype(str)
    return df

def get_all_users():
    conn = get_db_connection()
    if not conn: return pd.DataFrame()
    df = pd.read_sql("SELECT user_id, username, email, role, is_active, created_at FROM users", conn)
    conn.close()
    return df

def ban_user(user_id):
    conn = get_db_connection()
    if not conn: return False
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET is_active=FALSE WHERE user_id=%s AND role='user'", (user_id,))
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0