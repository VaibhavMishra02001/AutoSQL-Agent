from llm import invoke_with_retry

def generate_sql(state):
    print("[DEBUG] Generating SQL for question:", state["question"])

    prompt = f"""
    You are a MySQL expert.

    Use the schema exactly as provided.

    Important rules:
    - Return ONLY valid MySQL SQL.
    - Do not include explanations, markdown, or code fences.
    - If an INSERT targets a table where `id` is required and has no default/auto increment, include a valid `id` value in the INSERT.
    - If the user asks to avoid duplicates, generate SQL that respects the request.
    - if possible use  the max_id +1 approach to generate the next id for the record to be inserted.
    - For duplicate-safe INSERT ... SELECT statements, do NOT select directly FROM the target table in a way that can produce multiple rows.
    - If you need the next `id`, use a scalar subquery like `(SELECT COALESCE(MAX(id), 0) + 1 FROM products)` so the INSERT produces exactly one row.

    Schema:
    {state['schema']}

    Question:
    {state['question']}

    Generate SQL for the operation asked in the question based on the provided schema.
    """

    try:
        sql = invoke_with_retry(prompt)

        if isinstance(sql, str):
            sql = sql.strip()
            if sql.startswith("```sql"):
                sql = sql.strip("`\n ").replace("sql", "", 1).strip()
            elif sql.startswith("```"):
                sql = sql.strip("`\n ").strip()

        print("\n[GENERATED SQL]")
        print(sql)
        return {"sql": sql}
    except Exception as e:
        print("[ERROR] SQL generation failed:", e)
        return {"error": str(e)}
