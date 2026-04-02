from llm import invoke_with_retry

def fix_sql(state):
    prompt = f"""
    You are a MySQL expert.

    Fix the SQL query using the database error below.

    Return ONLY the corrected SQL query.
    Do not include explanations, markdown, code fences, or extra text.

    SQL:
    {state['sql']}

    Error:
    {state['error']}
    """
    try:
        new_sql = invoke_with_retry(prompt).strip()

        if new_sql.startswith("```sql"):
            new_sql = new_sql.strip("`\n ").replace("sql", "", 1).strip()
        elif new_sql.startswith("```"):
            new_sql = new_sql.strip("`\n ").strip()

        return {"sql": new_sql}
    except Exception as e:
        print(f"[ERROR] SQL fix failed: {e}")
        return {"error": str(e)}
