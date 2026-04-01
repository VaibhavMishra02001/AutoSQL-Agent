from llm import llm

def generate_sql(state):
    print("[DEBUG] Generating SQL for question:", state['question'])

    prompt = f"""
    You are a MySQL expert.

    Schema:
    {state['schema']}

    Question:
    {state['question']}

    Generate SQL for the operation asked in the question based on the provided schema.
    """
   
    try:
        sql = llm.invoke(prompt)

        if isinstance(sql, str):
            sql = sql.strip()
            if sql.startswith("```sql"):
                sql = sql.strip("`\n ").replace("sql", "", 1).strip()

        print("Generated SQL:", sql)
        return {"sql": sql}
    except Exception as e:
        print("[ERROR] SQL generation failed:", e)
        return {"error": str(e)}