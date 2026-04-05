from get_conn import get_conn

def insert_record(sql, database=None):
    """Execute INSERT statement and commit to database."""
    # Validate database parameter
    if not database or database.strip() == "":
        return {"error": "Database name is required. Please select a database from settings or use 'USE database_name;' command."}
    
    try:
        conn = get_conn(database=database)
        if conn is None:
            return {"error": f"Failed to connect to database '{database}'. Please check if the database exists."}
        
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "success", "message": f"Record inserted successfully"}
    except Exception as e:
        print(f"[ERROR] Insert failed: {e}")
        return {"error": str(e)}