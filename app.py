import streamlit as st
import pandas as pd
from graph import build_graph
from list_databases import list_databases
from list_tables import list_tables

# Page config
st.set_page_config(
    page_title="AutoSQL Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
    }
    .success-box {
        background-color: #90EE90;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .error-box {
        background-color: #FFB6C6;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .info-box {
        background-color: #ADD8E6;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("🤖 AutoSQL Agent")
st.markdown("Convert natural language to SQL queries and execute them instantly!")

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Database selection section
    st.subheader("📊 Select Database")
    try:
        databases = list_databases()
        
        if databases:
            # Database selector
            selected_db = st.selectbox(
                "Choose a database:",
                options=databases,
                key="sidebar_db_selector"
            )
            
            # Store selected database in session state
            if "selected_db" not in st.session_state:
                st.session_state.selected_db = selected_db
            else:
                st.session_state.selected_db = selected_db
            
            st.success(f"✅ Database: {st.session_state.selected_db}")
            
            with st.expander("View All Databases"):
                st.write(f"Connected to {len(databases)} database(s):")
                for db in databases:
                    st.write(f"• {db}")
        else:
            st.error("❌ No databases found")
    except Exception as e:
        st.error(f"❌ Could not fetch databases: {str(e)}")
    
    st.divider()
    
    # Example queries
    st.subheader("💡 Example Queries")
    examples = [
        "List all products",
        "Show users with orders",
        "Get total sales by category",
        "Find customers in New York",
        "Display last 10 transactions"
    ]
    for example in examples:
        st.caption(f"→ {example}")

# Main content
tab1, tab2, tab3 = st.tabs(["💬 Query", "📋 Schema", "📊 Results History"])

with tab1:
    st.subheader("Ask Your Question")
    
    # Input area
    question = st.text_area(
        "Enter your query in natural language:",
        height=150,
        placeholder="e.g., Show me all products with price greater than 100",
        key="question_input"
    )
    
    col1, col2, col3 = st.columns(3)
    with col1:
        execute_btn = st.button("🚀 Execute Query", use_container_width=True)
    with col2:
        clear_btn = st.button("🗑️ Clear", use_container_width=True)
    with col3:
        st.write("")  # Placeholder for alignment
    
    if clear_btn:
        st.rerun()
    
    # Execute agent
    if execute_btn and question.strip():
        st.divider()
        
        # Check if database is selected
        if "selected_db" not in st.session_state or not st.session_state.selected_db:
            st.error("❌ Please select a database from the Settings panel first")
        else:
            with st.spinner("🔄 Processing your query..."):
                try:
                    # Initial state with selected database
                    state = {
                        "question": question,
                        "schema": "",
                        "sql": "",
                        "result": "",
                        "error": "",
                        "attempts": 0,
                        "db": st.session_state.selected_db
                    }
                    
                    # Build and execute graph
                    graph = build_graph()
                    result = graph.invoke(state)
                    
                    # Display Generated SQL
                    st.subheader("📝 Generated SQL")
                    if result.get("sql"):
                        st.code(result.get("sql"), language="sql")
                    else:
                        st.warning("⚠️ No SQL was generated")
                    
                    st.divider()
                    
                    # Display Results
                    if result.get("error"):
                        st.markdown(f"<div class='error-box'><strong>❌ Error:</strong> {result.get('error')}</div>", unsafe_allow_html=True)
                    elif result.get("result"):
                        st.subheader("✅ Query Results")
                        
                        # Try to display as dataframe if possible
                        try:
                            if isinstance(result.get("result"), list):
                                if result["result"]:
                                    # Convert list of tuples/dicts to dataframe
                                    if isinstance(result["result"][0], dict):
                                        df = pd.DataFrame(result["result"])
                                    elif isinstance(result["result"][0], (tuple, list)):
                                        df = pd.DataFrame(result["result"])
                                    else:
                                        df = pd.DataFrame({"Result": result["result"]})
                                    
                                    st.dataframe(df, use_container_width=True)
                                    st.info(f"📊 Total rows: {len(result['result'])}")
                            else:
                                st.write(result.get("result"))
                        except Exception as e:
                            st.write(result.get("result"))
                    else:
                        st.info("ℹ️ Query executed successfully with no results")
                    
                    # Store in session for history
                    if "queries_history" not in st.session_state:
                        st.session_state.queries_history = []
                    
                    st.session_state.queries_history.append({
                        "question": question,
                        "sql": result.get("sql"),
                        "success": not result.get("error")
                    })
                    
                except Exception as e:
                    st.error(f"❌ Error executing query: {str(e)}")
                    st.write("Please check your connection and try again.")
    
    elif execute_btn:
        st.warning("⚠️ Please enter a question")

with tab2:
    st.subheader("📋 Database Schema")
    
    try:
        databases = list_databases()
        selected_db = st.selectbox("Select Database", databases)
        
        if selected_db:
            tables = list_tables(selected_db)
            st.success(f"✅ Found {len(tables)} table(s) in '{selected_db}'")
            
            if tables:
                selected_table = st.selectbox("Select Table", tables)
                st.info(f"📌 Schema for table: `{selected_table}`")
                st.caption("(Schema information would be displayed here)")
            else:
                st.info("No tables found in this database")
    
    except Exception as e:
        st.error(f"Could not fetch schema: {str(e)}")

with tab3:
    st.subheader("📊 Query History")
    
    if "queries_history" in st.session_state and st.session_state.queries_history:
        for idx, query in enumerate(reversed(st.session_state.queries_history), 1):
            with st.expander(f"Query {idx}: {query['question'][:50]}..."):
                st.markdown("**Question:**")
                st.write(query["question"])
                
                st.markdown("**SQL:**")
                st.code(query["sql"], language="sql")
                
                status = "✅ Success" if query["success"] else "❌ Failed"
                st.markdown(f"**Status:** {status}")
    else:
        st.info("ℹ️ No queries executed yet. Start by asking a question in the Query tab!")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.8rem; margin-top: 20px;'>
    <p>🤖 SQL Agent | Powered by LangGraph & LLM</p>
</div>
""", unsafe_allow_html=True)
