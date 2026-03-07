import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(page_title="Text-to-SQL", page_icon="🤖")
st.title("🤖 Text-to-SQL Assistant")
st.markdown("Ask questions in plain English!")

# Database connection
@st.cache_resource
def get_connection():
    return sqlite3.connect('database/company.db')

conn = get_connection()

# Sidebar
with st.sidebar:
    st.header("📊 Database Schema")
    st.code("""
departments(dept_id, dept_name, location)
employees(emp_id, emp_name, dept_id, hire_date)
salaries(emp_id, salary, bonus)
    """)
    
    st.header("❓ Sample Questions")
    questions = [
        "Show all employees",
        "List employees in Engineering department",
        "Show employees with salary > 50000",
        "Count employees by department",
        "Show average salary by department",
        "Find employees hired in 2023",
        "Show total salary cost by location"
    ]
    
    for q in questions:
        if st.button(q):
            st.session_state['question'] = q

# Main area
question = st.text_input("Ask your question:", value=st.session_state.get('question', ''))

if question:
    st.subheader("📝 Your Question:")
    st.info(question)
    
    # Convert question to SQL
    sql = ""
    if "all employees" in question.lower():
        sql = "SELECT * FROM employees"
    elif "engineering" in question.lower():
        sql = """
        SELECT e.*, d.dept_name 
        FROM employees e
        JOIN departments d ON e.dept_id = d.dept_id
        WHERE d.dept_name = 'Engineering'
        """
    elif "salary > 50000" in question.lower():
        sql = """
        SELECT e.emp_name, s.salary 
        FROM employees e
        JOIN salaries s ON e.emp_id = s.emp_id
        WHERE s.salary > 50000
        """
    elif "count employees by department" in question.lower():
        sql = """
        SELECT d.dept_name, COUNT(e.emp_id) as emp_count
        FROM departments d
        LEFT JOIN employees e ON d.dept_id = e.dept_id
        GROUP BY d.dept_name
        """
    elif "average salary by department" in question.lower():
        sql = """
        SELECT d.dept_name, AVG(s.salary) as avg_salary
        FROM departments d
        JOIN employees e ON d.dept_id = e.dept_id
        JOIN salaries s ON e.emp_id = s.emp_id
        GROUP BY d.dept_name
        """
    elif "hired in 2023" in question.lower():
        sql = "SELECT * FROM employees WHERE hire_date LIKE '2023%'"
    elif "salary by location" in question.lower():
        sql = """
        SELECT d.location, SUM(s.salary) as total_salary
        FROM departments d
        JOIN employees e ON d.dept_id = e.dept_id
        JOIN salaries s ON e.emp_id = s.emp_id
        GROUP BY d.location
        """
    
    if sql:
        st.subheader("🔍 Generated SQL:")
        st.code(sql, language='sql')
        
        try:
            df = pd.read_sql(sql, conn)
            st.subheader("📊 Results:")
            st.dataframe(df)
            st.success(f"✅ Found {len(df)} records")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("🤔 I didn't understand the question. Try one from the sidebar!")

# Show raw data option
if st.checkbox("Show raw tables"):
    tab1, tab2, tab3 = st.tabs(["Employees", "Departments", "Salaries"])
    with tab1:
        st.dataframe(pd.read_sql("SELECT * FROM employees", conn))
    with tab2:
        st.dataframe(pd.read_sql("SELECT * FROM departments", conn))
    with tab3:
        st.dataframe(pd.read_sql("SELECT * FROM salaries", conn))

st.markdown("---")
st.caption("Built with Streamlit | Simple Text-to-SQL Demo")
