from llm import invoke_with_retry
import re

def generate_sql(state):
    print("[DEBUG] Generating SQL for question:", state["question"])
    
    # Extract database name from question if mentioned
    question = state["question"]
    db_match = re.search(r'(?:in|from|use)\s+([a-zA-Z0-9_]+)\s*(?:database|db)?', question, re.IGNORECASE)
    
    if db_match and not state.get("db"):
        extracted_db = db_match.group(1)
        print(f"[INFO] Extracted database from question: {extracted_db}")
        state["db"] = extracted_db

    prompt = f"""
    You are a MySQL expert.

    Use the schema exactly as provided.

    Important rules:
    - Return ONLY valid MySQL SQL.
    - Do not include explanations, markdown, or code fences.
    - If an INSERT targets a table where `id` is an AUTO_INCREMENT field, do NOT include the id in the INSERT (let MySQL handle it).
    - If an INSERT targets a table where `id` is required but NOT auto-increment, you must provide a valid `id` value.
    - CRITICAL: MySQL does NOT allow subqueries on the same table in INSERT. For example, this fails:
      INSERT INTO products (id, name) VALUES ((SELECT MAX(id) + 1 FROM products), 'item');
    - To get the next ID safely in MySQL, wrap the subquery in a derived table:
      INSERT INTO products (id, name) VALUES ((SELECT next_id FROM (SELECT COALESCE(MAX(id), 0) + 1 as next_id FROM products) AS t), 'item');
    - Prefer using AUTO_INCREMENT IDs when possible instead of manually calculating.
    - If the user asks to avoid duplicates, generate SQL that respects the request.
    - For duplicate-safe INSERT ... SELECT statements, do NOT select directly FROM the target table in a way that can produce multiple rows.

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
        
        # Return SQL and database (if extracted)
        result = {"sql": sql}
        if state.get("db"):
            result["db"] = state["db"]
        
        return result
    except Exception as e:
        print("[ERROR] SQL generation failed:", e)
        return {"error": str(e)}
