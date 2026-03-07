import sqlite3
import random

print("🚀 Creating database...")
conn = sqlite3.connect('database/company.db')
cursor = conn.cursor()

cursor.executescript('''
DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;
DROP TABLE IF EXISTS salaries;

CREATE TABLE departments (dept_id INTEGER PRIMARY KEY, dept_name TEXT NOT NULL, location TEXT);
CREATE TABLE employees (emp_id INTEGER PRIMARY KEY, emp_name TEXT NOT NULL, dept_id INTEGER, hire_date DATE, FOREIGN KEY (dept_id) REFERENCES departments(dept_id));
CREATE TABLE salaries (emp_id INTEGER PRIMARY KEY, salary REAL, bonus REAL, FOREIGN KEY (emp_id) REFERENCES employees(emp_id));
''')

departments = [(1,'Engineering','Bangalore'),(2,'Sales','Mumbai'),(3,'Marketing','Delhi'),(4,'HR','Bangalore'),(5,'Finance','Mumbai')]
cursor.executemany('INSERT INTO departments VALUES (?,?,?)', departments)

employees = [(i, f'Employee{i}', random.randint(1,5), f'202{random.randint(0,4)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}') for i in range(1,21)]
cursor.executemany('INSERT INTO employees VALUES (?,?,?,?)', employees)

for i in range(1,21):
    cursor.execute('INSERT INTO salaries VALUES (?,?,?)', (i, random.randint(30000,90000), random.randint(1000,10000)))

conn.commit()
conn.close()
print("✅ Database created!")
