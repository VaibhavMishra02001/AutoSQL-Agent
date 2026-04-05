from explain_query import explain_query
from list_tables import list_tables
from select_query import select_query   
from create_table import create_table
from insert_record import insert_record


ALLOWED_PREFIXES = [
    "SELECT",
    "EXPLAIN",
    "SHOW TABLES",
    "CREATE TABLE",
    "INSERT",
    "USE"
]

def execute_tool(state):
    

    try:
        sql = state["sql"]

        # Handle AIMessage
        if not isinstance(sql, str):
            if hasattr(sql, "content"):
                sql = sql.content
            else:
                sql = str(sql)

        sql = sql.strip()

        # Remove markdown-like syntax if present
        if sql.startswith("```sql"):
            sql = sql.strip("`\n ").replace("sql", "", 1).strip()
        elif sql.startswith("```"):
            sql = sql.strip("`\n ").strip()

        print("\n[EXECUTING SQL]")
        print(sql)

        sql_upper = sql.upper()

        if not any(sql_upper.startswith(p) for p in ALLOWED_PREFIXES):
            print("[ERROR] Operation not permitted for SQL:", sql)
            return {"error": "Operation not permitted"}

        db_name = state.get("db", "test_db")

        # Handle USE database command
        if sql_upper.startswith("USE"):
            try:
                # Extract database name from USE statement
                db_to_use = sql[3:].strip().rstrip(";")
                print(f"[INFO] Switching to database: {db_to_use}")
                # Update state with selected database
                return {"result": f"Switched to database: {db_to_use}", "db": db_to_use}
            except Exception as e:
                print(f"[ERROR] Failed to switch database: {e}")
                return {"error": str(e)}

        if sql_upper.startswith("SELECT"):
            result = select_query(sql, database=db_name)
        elif sql_upper.startswith("EXPLAIN"):
            clean_sql = sql[len("EXPLAIN"):].strip()
            result = explain_query(clean_sql, db_name)
        elif sql_upper.startswith("SHOW TABLES"):
            result = list_tables(database=db_name)
        elif sql_upper.startswith("CREATE TABLE"):
            result = create_table(sql, database=db_name)
        elif sql_upper.startswith("INSERT"):
            result = insert_record(sql, database=db_name)
        else:
            result = {"error": "Unsupported SQL operation"}

        print("Execution result:", result)
        return {"result": result}

    except Exception as e:
        print("[ERROR] SQL execution failed:", e)
        return {"error": str(e)}
