import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

# Load key: first try st.secrets (Streamlit Cloud), then fallback to os.getenv (local)
groq_key = st.secrets.get("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", os.getenv("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"))
if not groq_key:
    raise ValueError("Groq API key not found. Please set GROQ_API_KEY in secrets or environment.")

# Initialize Groq LLM
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
    try:
        response = llm.invoke(prompt.format(question=question))
        sql = response.content.strip()
        if sql.startswith("```"):
            sql = sql.strip("`").replace("sql", "", 1).strip()
        return sql + " -- [AI GENERATED]"
    except Exception as e:
        return f"SELECT name, club, goals, assists FROM players; -- [RULE] (Groq failed: {e})"

