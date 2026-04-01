from get_conn import get_conn
def list_tables(database):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    return cursor.fetchall()