from graph import build_graph

def run_agent():
    print("\n🚀 Starting SQL Agent...")

    # Initial state
    state = {
        "question": "Show all record with price greater than 20000 from products table",
        "schema": "",
        "sql": "",
        "result": "",
        "error": "",
    }
    print("[DEBUG] Initial State:", state)

    # Execute graph
    try:
        
        result = build_graph().invoke(state)
        
    except Exception as e:
        print("[ERROR] Graph execution failed:", e)
        result = {"error": str(e)}

    # Log final output
    print("\n✅ Final Output:")
    print("Generated SQL:", result.get("sql"))
    print("Query Result:", result.get("result"))

    if result.get("error"):
        print("\n❌ Error:", result.get("error"))

if __name__ == "__main__":
    run_agent()