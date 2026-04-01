from rag.vector_store import vector_db

def retrieve_schema(state):
    question = state["question"]

    # 🔹 Get top relevant schema chunks
    docs = vector_db.similarity_search(question, k=3)

    schema = "\n\n".join([doc.page_content for doc in docs])

    return {"schema": schema}