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
from tenacity import retry, wait_exponential, stop_after_attempt

load_dotenv()

# Initialize LLM with retry logic for rate limiting
llm = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.2,
    timeout=30,
    max_retries=3,  # Built-in retry for transient errors
)

# Wrapper function with exponential backoff for 429 errors
@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
def invoke_with_retry(prompt):
    
    response = llm.invoke(prompt)

    if hasattr(response, "content"):
        return response.content.strip()

    return str(response).strip()
