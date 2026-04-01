from get_conn import get_conn
def explain_query(sql):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(f"EXPLAIN {sql}")
    return cursor.fetchall()