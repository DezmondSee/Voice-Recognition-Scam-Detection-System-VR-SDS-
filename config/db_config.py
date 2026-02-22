import mysql.connector
import os
import time

def get_db_connection():
    # Retry logic for Docker (Database takes time to start up)
    retries = 5
    while retries > 0:
        try:
            return mysql.connector.connect(
                host=os.getenv("DB_HOST", "db"),
                user=os.getenv("DB_USER", "root"),
                password=os.getenv("DB_PASSWORD", "Wnq57177"),
                database=os.getenv("DB_NAME", "vrsds_enterprise")
            )
        except mysql.connector.Error:
            retries -= 1
            time.sleep(2)
    return None