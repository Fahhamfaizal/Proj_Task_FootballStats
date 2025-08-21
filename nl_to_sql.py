import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0,
    groq_api_key=os.getenv("GROQ_API_KEY")
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
            sql = sql.strip("`")
            sql = sql.replace("sql", "", 1).strip()
        return sql + " -- [AI GENERATED]"
    except Exception as e:
        return f"SELECT name, club, goals, assists FROM players; -- [RULE] (Groq failed: {e})"

if __name__ == "__main__":
    test_q = "Show me players with goals greater than 12."
    print("SQL:", nl_to_sql(test_q))

