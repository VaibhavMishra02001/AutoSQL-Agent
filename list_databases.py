from get_conn import get_conn

def list_databases():
    """List all available databases, returning names as strings."""
    conn = get_conn()
    if conn is None:
        return []
    
    try:
        cursor = conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        cursor.close()
        
        # Extract database names from tuples
        # MySQL returns tuples like ('database_name',), we need just 'database_name'
        db_list = [db[0] for db in databases]
        return db_list
    except Exception as e:
        print(f"[ERROR] List databases failed: {e}")
        return []
    finally:
        if conn:
            conn.close()