import os
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("sqlite:///football.db")

provider = os.getenv("LLM_PROVIDER", "groq").lower()

if provider == "openai":
    from langchain_openai import ChatOpenAI
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError("OPENAI_API_KEY is not set. Please export it before running.")
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        openai_api_key=openai_key
    )
elif provider == "groq":
    from langchain_groq import ChatGroq
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise ValueError("GROQ_API_KEY is not set. Please export it before running.")
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=groq_key
    )
else:
    raise ValueError("LLM_PROVIDER must be either 'openai' or 'groq'")

agent_executor = create_sql_agent(
    llm=llm,
    db=db,
    agent_type="openai-tools",
    verbose=True,
)

def agent_query(question: str) -> str:
    return agent_executor.invoke({"input": question})

print(f"Using provider: {provider.upper()} (model={getattr(llm, 'model', 'unknown')})")
