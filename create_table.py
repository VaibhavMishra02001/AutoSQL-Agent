from get_conn import get_conn
def create_table(sql):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    return "Table created"