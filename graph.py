from langgraph.graph import StateGraph
from list_databases import list_databases
from list_tables import list_tables 
from generate_sql import generate_sql
from execute_sql import execute_tool
from fix_sql import fix_sql
from state import State
from rag.retriever import retrieve_schema


def build_graph():
    """
    Build and return the LangGraph SQL agent
    """

    builder = StateGraph(State)

    # 🔹 Add nodes
    builder.add_node("rag", retrieve_schema)
    builder.add_node("generate", generate_sql)
    builder.add_node("execute", execute_tool)
    
    # Create wrapper function to increment attempts before fixing
    def increment_and_fix(state):
        state["attempts"] = state.get("attempts", 0) + 1
        return fix_sql(state)
    
    builder.add_node("fix", increment_and_fix)

    # 🔹 Entry point
    builder.set_entry_point("rag")

    # 🔹 Flow
    builder.add_edge("rag", "generate")
    builder.add_edge("generate", "execute")

    # 🔹 Conditional retry logic with max attempts limit (5)
    def should_retry(state):
        # Check if there's an error
        if not state.get("error"):
            return "__end__"
        
        # Get current attempt count
        attempts = state.get("attempts", 0)
        
        # Limit fix attempts to 5
        if attempts >= 5:
            print("[INFO] Max fix attempts (5) reached. Stopping retry.")
            return "__end__"
        
        return "fix"
    
    builder.add_conditional_edges(
        "execute",
        should_retry,
        {
            "fix": "fix",
            "__end__": "__end__"
        }
    )
    
    builder.add_edge("fix", "execute")
    
    # 🔹 Compile graph
    graph = builder.compile()

    return graph