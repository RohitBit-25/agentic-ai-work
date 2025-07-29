# Streamlit app

from dotenv import load_dotenv
load_dotenv()
import os   
import streamlit as st
import sqlite3

import google.generativeai as genai
# comfigure out API key

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# function to load google model and provide sql query as a response

def get_gemini_response(question,prompt):
    model= genai.GenerativeModel('models/gemini-1.5-flash')
    response= model.generate_content([prompt[0],question])
    # Clean the response to extract only the SQL query (first line with SELECT/INSERT/UPDATE/DELETE)
    lines = response.text.strip().splitlines()
    for line in lines:
        line = line.strip()
        if line.upper().startswith(("SELECT", "INSERT", "UPDATE", "DELETE")):
            return line
    # fallback: return the whole response if no SQL found
    return response.text.strip()

# function to retrieve query from the database

def read_sql_query(sql,db):
    try:
        conn=sqlite3.connect(db)
        cur=conn.cursor()
        cur.execute(sql)
        rows=cur.fetchall()
        conn.commit()
        conn.close()
        for row in rows:
            print(row)
        return rows
    except sqlite3.OperationalError as e:
        if 'no such table' in str(e):
            return "Error: The 'Student' table does not exist. Please run the database setup script (sql.py) first."
        else:
            print(f"SQL execution error: {e}")
            return f"SQL execution error: {e}"
    except Exception as e:
        print(f"SQL execution error: {e}")
        return f"SQL execution error: {e}"

## Define Your Prompt

prompt=[
    """
  You are an expert AI assistant specializing in converting natural language questions into answers

The SQL database is named **Student** and contains the following columns:
**Name** (Varchar)
**Class** (Varchar)
**Section** (Varchar)
**Marks** (Int)

Follow the guidelines when generating SQL queries:
1. Ensure the output contains only the SQL query-do-not include explanations, formatting mannered.
2. Use proper SQL syntax while maintaing accuracy and efficiency.
3. If the query involves filtering, apply appropriate 'Where' clauses.
4. If an aggregation is requried (e.g., counting records, averaging values), use fuctions 

### **Examples**

   **Question**: "How many student records are present?"
   **SQL Query**: SELECT COUNT(*) FROM Student;

   **Question**: "List all students in the Data Science class."
   **SQL Query**: SELECT * FROM Student WHERE Class = 'Data Science';

Now, generate an SQL query based on the following question:

"""]

## Streamlit App

# Set page configuration with a title and icon
st.set_page_config(
    page_title="SQL Query Generator", page_icon="📊", layout="wide"
)
# Display the Header
st.markdown("<h1 style='text-align: center;'>SQL Query Generator</h1>", unsafe_allow_html=True)
st.markdown("Ask any question, and I'll generate the SQL query for You!")

# User input for the question
question = st.text_input("Enter your query in English:",key="input")

# Submit button with an Design
submit = st.button("Generate SQL Query",type="primary")

# if submit is clicked
if submit:
   sql_query = get_gemini_response(question,prompt)
   st.subheader("Generated SQL Query:")
   st.code(sql_query, language="sql")
   result = read_sql_query(sql_query,'student.db')
   st.subheader("The Response is")
   if isinstance(result, str):
       st.error(result)
   elif result:
       for row in result:
           print(row)
           st.header(row)
   else:
       st.info("No results found.")






