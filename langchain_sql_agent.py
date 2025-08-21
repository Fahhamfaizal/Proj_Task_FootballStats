import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

groq_key = os.getenv("GROQ_API_KEY")
if not groq_key:
    raise ValueError("Groq API key not found. Please set GROQ_API_KEY in secrets or environment.")

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=groq_key
)

prompt = PromptTemplate.from_template("""
You are an assistant that translates natural language questions into SQL queries.
The database has a table called `players(name, club, goals, assists)`.
Return ONLY the SQL query.
Question: {question}
SQL:
""")

def nl_to_sql(question: str) -> str:
    response = llm.invoke(prompt.format(question=question))
    sql = response.content.strip()
    if sql.startswith("```"):
        sql = sql.strip("`")
        sql = sql.replace("sql", "", 1).strip()
    return sql


