import streamlit as st
import mysql.connector
import pandas as pd

st.set_page_config(page_title="Data Query Prompt Lab", page_icon="💰", layout="centered")

# --- DATABASE CONNECTION ---
def run_db_query(query):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="prompt_lab_db"
        )
        # Use pandas to read the SQL directly into a dataframe
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        st.error(f"XAMPP Database Error: {e}")
        return None

# --- STREAMLIT UI ---
st.title("💰 Salary Prompt Analytics Tool")
st.write("Ask questions about employee salaries, and our logic will parse the intent against the live XAMPP database.")

st.markdown("---")

# Show the current database table state
with st.expander("📊 View Current XAMPP Dataset"):
    raw_data = run_db_query("SELECT name, department, role, salary FROM employee_salaries")
    if raw_data is not None:
        st.dataframe(raw_data, use_container_width=True)

# User Prompt Input
user_prompt = st.text_input("Enter your prompt / question:", placeholder="e.g., What is the highest salary?")

if user_prompt:
    prompt_clean = user_prompt.lower().strip()
    
    st.subheader("🔍 Processing Intent Matrix")
    
    # Simple semantic rule router mimicking intent analysis
    if "highest salary" in prompt_clean or "maximum salary" in prompt_clean or "max salary" in prompt_clean:
        sql_to_run = "SELECT name, role, salary FROM employee_salaries ORDER BY salary DESC LIMIT 1"
        result_df = run_db_query(sql_to_run)
        
        if result_df is not None and not result_df.empty:
            highest_name = result_df.iloc[0]['name']
            highest_val = result_df.iloc[0]['salary']
            highest_role = result_df.iloc[0]['role']
            
            st.success(f"**Highest Salary Found!**")
            st.metric(label=f"{highest_name} ({highest_role})", value=f"${highest_val:,}")
            
    elif "average salary" in prompt_clean or "avg salary" in prompt_clean:
        sql_to_run = "SELECT AVG(salary) as avg_sal FROM employee_salaries"
        result_df = run_db_query(sql_to_run)
        
        if result_df is not None:
            avg_val = int(result_df.iloc[0]['avg_sal'])
            st.info(f"**Calculated Dataset Average:**")
            st.metric(label="Average Employee Salary", value=f"${avg_val:,}")
            
    elif "engineering" in prompt_clean:
        sql_to_run = "SELECT name, role, salary FROM employee_salaries WHERE department = 'Engineering'"
        result_df = run_db_query(sql_to_run)
        
        if result_df is not None:
            st.write("**Engineering Department Staff & Compensation:**")
            st.dataframe(result_df, hide_index=True)
            
    else:
        st.warning("Prompt intent not recognized. Try asking: *'What is the highest salary?'*, *'What is the average salary?'*, or *'Show engineering salaries'*.")