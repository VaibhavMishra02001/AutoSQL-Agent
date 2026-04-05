from get_conn import get_conn

def create_table(sql, database=None):
    """Create table in specified database."""
    # Validate database parameter
    if not database or database.strip() == "":
        return {"error": "Database name is required. Please select a database from settings or use 'USE database_name;' command."}
    
    conn = get_conn(database=database)
    if conn is None:
        return {"error": f"Failed to connect to database '{database}'. Please check if the database exists."}
    
    try:
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        return "Table created"
    except Exception as e:
        print(f"[ERROR] Create table failed: {e}")
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()