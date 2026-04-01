from get_conn import get_conn

def list_databases():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    return cursor.fetchall()