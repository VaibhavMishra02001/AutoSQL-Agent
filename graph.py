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
    builder.add_node("fix", fix_sql)

    # 🔹 Entry point
    builder.set_entry_point("rag")

    # 🔹 Flow
    builder.add_edge("rag", "generate")
    builder.add_edge("generate", "execute")

    # 🔹 Conditional retry logic
    builder.add_conditional_edges(
            "execute",
            lambda s: "fix" if s.get("error") else "__end__",
                {
            "fix":"fix",
            "__end__":"__end__"
                }
        )
    builder.add_edge("fix", "execute")

    # 🔹 Compile graph
    graph = builder.compile()

    return graph