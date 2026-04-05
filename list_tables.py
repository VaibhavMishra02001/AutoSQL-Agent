from get_conn import get_conn

def list_tables(database):
    """List all tables in specified database."""
    # Validate database parameter
    if not database or database.strip() == "":
        return {"error": "Database name is required. Please select a database from settings or use 'USE database_name;' command."}
    
    conn = get_conn(database=database)
    if conn is None:
        return {"error": f"Failed to connect to database '{database}'. Please check if the database exists."}
    
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        result = cursor.fetchall()
        cursor.close()
        
        # Extract table names from tuples
        # MySQL returns tuples like ('table_name',), we need just 'table_name'
        tables = [table[0] for table in result]
        return tables
    except Exception as e:
        print(f"[ERROR] List tables failed: {e}")
        return {"error": str(e)}
    finally:
        if conn:
            conn.close()