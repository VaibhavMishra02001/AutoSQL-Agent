# from dotenv import load_dotenv
# import os
# from langchain_google_genai import ChatGoogleGenerativeAI

# # 🔹 Load env variables
# load_dotenv()

# # 🔹 Get API key
# api_key = os.getenv("GOOGLE_API_KEY")

# if not api_key:
#     raise ValueError("GOOGLE_API_KEY not found in .env")

# # 🔹 Initialize Gemini model
# llm = ChatGoogleGenerativeAI(
#     model="gemini-2.5-flash-lite",   
#     google_api_key=api_key,
#     temperature=0.2,
#     timeout=10   # 🔥 prevents hanging
# )
from dotenv import load_dotenv
import os       
from langchain_groq import ChatGroq
load_dotenv()
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
    timeout=10
)