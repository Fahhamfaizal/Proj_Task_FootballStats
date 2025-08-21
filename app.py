import streamlit as st
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

from nl_to_sql import nl_to_sql

st.set_page_config(page_title="Football Data Explorer", layout="wide")
st.title("⚽ Football Data Explorer")

st.sidebar.success("Using AI Provider: Groq (Mixtral-8x7b)")

question = st.text_input("Ask me a football question in plain English:")

if question:
    st.write(f"You asked: {question}")

    sql_query = nl_to_sql(question)

    if "-- [AI GENERATED]" in sql_query:
        st.success("SQL generated using AI (LangChain + LLM)")
    elif "-- [RULE]" in sql_query:
        st.info("SQL generated using Rule-based Fallback")
    else:
        st.warning("Could not detect SQL source")

    st.code(sql_query, language="sql")

    try:
        conn = sqlite3.connect("football.db")
        clean_sql = sql_query.split("--")[0].strip()
        df = pd.read_sql_query(clean_sql, conn)
        conn.close()

        if df.empty:
            st.warning("No results found for this query.")
        else:
            st.subheader("Query Results")
            st.dataframe(df, use_container_width=True)

            fig, ax = plt.subplots()

            if "goals" in df.columns and "name" in df.columns and "assists" not in df.columns:
                df.plot(kind="bar", x="name", y="goals", ax=ax, legend=False, color="blue")
                ax.set_ylabel("Goals")
                ax.set_title("Goals by Player")
                st.pyplot(fig)

            elif "assists" in df.columns and "name" in df.columns and "goals" not in df.columns:
                df.plot(kind="bar", x="name", y="assists", ax=ax, legend=False, color="orange")
                ax.set_ylabel("Assists")
                ax.set_title("Assists by Player")
                st.pyplot(fig)

            elif "club" in df.columns and "total_goals" in df.columns:
                df.plot(kind="bar", x="club", y="total_goals", ax=ax, legend=False, color="green")
                ax.set_ylabel("Total Goals")
                ax.set_title("Goals by Club")
                st.pyplot(fig)

            elif "club" in df.columns and "total_assists" in df.columns:
                df.plot(kind="bar", x="club", y="total_assists", ax=ax, legend=False, color="purple")
                ax.set_ylabel("Total Assists")
                ax.set_title("Assists by Club")
                st.pyplot(fig)

            elif {"goals", "assists", "name"}.issubset(df.columns):
                df.plot(kind="bar", x="name", y=["goals", "assists"], ax=ax)
                ax.set_ylabel("Count")
                ax.set_title("Goals & Assists by Player")
                st.pyplot(fig)

            elif "performance" in df.columns and "club" in df.columns:
                df.plot(kind="bar", x="club", y="performance", ax=ax, legend=False, color="red")
                ax.set_ylabel("Performance (Goals + Assists)")
                ax.set_title("Overall Club Performance")
                st.pyplot(fig)

            else:
                st.info("Showing table above — no matching chart rule found.")

    except Exception as e:
        st.error("Something went wrong while processing your query.")
        st.exception(e)
