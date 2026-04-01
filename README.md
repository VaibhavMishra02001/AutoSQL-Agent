# AutoSQL-Agent
An AI-powered SQL agent that converts natural language queries into executable SQL and runs them on a MySQL database. Uses an LLM to generate queries and automatically correct errors when execution fails.   Built with LangGraph to manage workflow, decision-making, and retry logic. Enables users to interact with databases without writing SQL manually. Demonstrates a self-healing, agentic approach to database querying. 

<img width="800" height="700" alt="mermaid-diagram (1)" src="https://github.com/user-attachments/assets/0732706d-0c8d-42b7-9f36-941a1220cc7b" />

## 🧠 Project Overview

This project builds a **self-healing SQL agent** using:

- 🔗 LangGraph (workflow orchestration)
- 🤖 LLM (Gemini / OpenAI / Groq)
- 🗄 MySQL (database)
---
## Setup Instructions 

### Clone Repo 
```
git clone <your-repo-url>
cd sql-agent
```
---
### Install Dependencies
```
uv add -r requirements.txt
```  
---

### Setup Environment Variables
```
GOOGLE_API_KEY=your_gemini_key
```
### OR 
```
GROQ_API_KEY=your_groq_key
```
---

### Setup MySQL Connection
```
import mysql.connector
def get_conn():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="your_db"
    )
```
---
### Run Agent
```
uv run python main.py`
```
---
