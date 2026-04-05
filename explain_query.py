from get_conn import get_conn

def explain_query(sql, database=None):
    """Execute EXPLAIN query on specified database."""
    # Validate database parameter
    if not database or database.strip() == "":
        return {"error": "Database name is required. Please select a database from settings or use 'USE database_name;' command."}
    
    conn = get_conn(database=database)
    if conn is None:
        return {"error": f"Failed to connect to database '{database}'. Please check if the database exists."}
    
    try:
        cursor = conn.cursor()
        cursor.execute(f"EXPLAIN {sql}")
        result = cursor.fetchall()
        cursor.close()
        return result
    except Exception as e:
        print(f"[ERROR] Explain query failed: {e}")
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()