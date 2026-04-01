from explain_query import explain_query
from list_tables import list_tables
from select_query import select_query   
from create_table import create_table


ALLOWED_PREFIXES = [
    "SELECT",
    "EXPLAIN",
    "SHOW TABLES",
    "CREATE TABLE"
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

        sql_upper = sql.upper()

        if not any(sql_upper.startswith(p) for p in ALLOWED_PREFIXES):
            print("[ERROR] Operation not permitted for SQL:", sql)
            return {"error": "Operation not permitted"}

        db_name = state.get("db", "test_db")

        if sql_upper.startswith("SELECT"):
            result = select_query(sql)
        elif sql_upper.startswith("EXPLAIN"):
            clean_sql = sql[len("EXPLAIN"):].strip()
            result = explain_query(clean_sql, db_name)
        elif sql_upper.startswith("SHOW TABLES"):
            result = list_tables(database=db_name)
        elif sql_upper.startswith("CREATE TABLE"):
            result = create_table(sql, db_name)
        else:
            result = {"error": "Unsupported SQL operation"}

        print("Execution result:", result)
        return {"result": result}

    except Exception as e:
        print("[ERROR] SQL execution failed:", e)
        return {"error": str(e)}