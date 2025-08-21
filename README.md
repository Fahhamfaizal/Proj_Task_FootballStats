PROJECT : 
A simple project where i created a small football database and then integrated it with Groq LLM via LangChain so that it can convert natural language questions into SQL.

LanGraph Structure :
We use LangGraph to define the flow of natural language queries -> SQL execution -> result handling.

Nodes - Input Node – accepts user’s plain English question.
NL-to-SQL Node – converts natural language into SQL using the LLM.
Database Query Node – executes the SQL against our SQLite database
Summarization Node – interprets the query results and produces a concise text answer.
Visualization Node – generates charts (e.g., bar, line, scatter) for better insights.

Edges: connect the nodes in sequence: Input -> NL-to-SQL -> Database Query -> Summarization -> Visualization -> Output
Flow: ensures user queries pass smoothly from text input to final dashboard output.

SQL Agent Construction :
we used sqlite3 for executing local SQL database and a Groq (Mixtral-8x7b) LLM model for query understanding and sql generation

Summarization :
The LLM looks at the numbers from the database and explains them in plain English.

Visualization :
We use Matplotlib to draw graphs like bar charts or line charts.Then we use Streamlit to show both the text answer and the graph on the webpage. This way, users can read the answer and also see it visually in a chart.
