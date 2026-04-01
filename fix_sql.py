from llm import llm
def fix_sql(state):
    prompt = f"""
    Fix this SQL:
    give correct sql .
    {state['sql']}

    Error:
    {state['error']}
    """
    new_sql = llm.invoke(prompt)
    return {"sql": new_sql}