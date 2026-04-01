from get_conn import get_conn

def select_query(sql):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(sql)
    return cursor.fetchall()