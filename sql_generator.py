import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()
#client = genai.Client(api_key=st.secrets["api_key"])
api_key = os.getenv("GEMINI_API_KEY")

# If running on Streamlit Cloud
if not api_key:
    api_key = st.secrets.get("GEMINI_API_KEY")
    st.stop()

if not api_key:
    st.error("GEMINI_API_KEY not found.")
    st.stop()
client = genai.Client(api_key=api_key)
#model = genai.GenerativeModel("gemini-3.5-flash-lite")

st.title("🧠 AI SQL Query Generator")
st.write("Describe your table structure and ask a question in plain English — I'll generate the SQL for you.")

st.subheader("1️⃣ Describe Your Table Schema")
#if st.button("📋 Load Example Schema"):
if "schema_input" not in st.session_state:
     st.session_state["schema_input"] = ""
if "question_input" not in st.session_state:
      st.session_state["question_input"] = ""

def load_example():
      st.session_state["schema_input"] = "Table: orders\nColumns: order_id, customer_name, product, quantity, price, order_date"
      st.session_state["question_input"] = "Show me the top 5 customers by total order value in 2024."      
st.button("📋 Load Example Schema", on_click=load_example)
# st.write("DEBUG session_state:", st.session_state)
schema_input = st.text_area(
    "Enter table name and columns",
    key="schema_input",
    placeholder="Example:\nTable: orders\nColumns: order_id, customer_name, product, quantity, price, order_date",
    height=120
)

st.subheader("2️⃣ Ask Your Question")
question_input = st.text_area(
    "What do you want to know?",
    key="question_input",
    placeholder="Example: Show me the top 5 customers by total order value in 2024.",
    height=80
)

generate_button = st.button("Generate SQL Query")

with st.sidebar:
    st.header("ℹ️ How to Use")
    st.markdown("""
    1. Describe your table(s) — name and columns.
    2. Type your question in plain English.
    3. Click **Generate SQL Query**.
    4. Copy the query using the icon in the top-right of the code box.
    """)
    st.markdown("---")
    st.caption("Powered by Google gemini-3.5-flash-lite")
if generate_button:
    if schema_input.strip() == "":
        st.error("⚠️ Please describe your table schema first.")
    elif question_input.strip() == "":
        st.error("⚠️ Please enter a question.")
    else:
        prompt = f"""
You are an expert SQL developer. Based on the following database schema, write a single, correct SQL query that answers the user's question.

Schema:
{schema_input}

Question:
{question_input}

Rules:
- Return ONLY the SQL query, no explanations, no markdown code fences.
- Use standard SQL syntax compatible with PostgreSQL/MySQL.
- If the question cannot be answered with the given schema, respond with: -- Cannot generate query: missing information in schema.
"""

        with st.spinner("Generating SQL query..."):
                        try:
                                response = client.models.generate_content(
                                    model="gemini-3.5-flash-lite",
                                    contents=prompt
                                )
                                sql_query = response.text.strip()

                                st.subheader("📝 Generated SQL Query")
                                st.code(sql_query, language="sql")

                                explain_prompt = f"""
                                    Explain the following SQL query in simple, plain English for someone with basic SQL knowledge. Keep it to 2-3 sentences.

                                    SQL Query:
                                    {sql_query}
                                    """
                                explanation_response = client.models.generate_content(
                                    model="gemini-3.5-flash-lite",
                                    contents=explain_prompt
                                )
                                explanation = explanation_response.text.strip()

                                st.subheader("💡 What This Query Does")
                                st.info(explanation)

                        except Exception as e:
                                st.error(f"⚠️ Something went wrong: {e}")