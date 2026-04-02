from get_conn import get_conn

def insert_record(sql, db_name=None):
    """Execute INSERT statement and commit to database."""
    try:
        conn = get_conn()
        if conn is None:
            return {"error": "Database connection failed"}
        
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success", "message": f"Record inserted successfully"}
    except Exception as e:
        print(f"[ERROR] Insert failed: {e}")
        return {"error": str(e)}