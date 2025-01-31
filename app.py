import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
DB_FILE = 'database.db'

def create_database():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS Employees")
    cursor.execute("DROP TABLE IF EXISTS Departments")

    cursor.execute('''
        CREATE TABLE Departments (
            ID INTEGER PRIMARY KEY,
            Name TEXT UNIQUE NOT NULL,
            Manager TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE Employees (
            ID INTEGER PRIMARY KEY,
            Name TEXT NOT NULL,
            Department INTEGER,
            Salary INTEGER,
            Hire_Date DATE,
            FOREIGN KEY (Department) REFERENCES Departments(ID) ON DELETE CASCADE
        )
    ''')

    departments = [
        (1, 'sales', 'Alice'),
        (2, 'engineering', 'Bob'),
        (3, 'marketing', 'Charlie'),
        (4, 'hr', 'Diane'),
        (5, 'finance', 'Edward'),
        (6, 'operations', 'Fiona'),
        (7, 'it', 'George')
    ]

    cursor.executemany("INSERT INTO Departments (ID, Name, Manager) VALUES (?, ?, ?)", departments)

    employees = [
        (1, 'Alice', 1, 50000, '2021-01-15'),
        (2, 'Bob', 2, 70000, '2020-06-10'),
        (3, 'Charlie', 3, 60000, '2022-03-20'),
        (4, 'David', 2, 75000, '2019-05-25'),
        (5, 'Eve', 4, 55000, '2018-07-30'),
        (6, 'Frank', 5, 80000, '2021-09-17'),
        (7, 'Grace', 6, 62000, '2023-04-01'),
        (8, 'Hank', 7, 78000, '2022-11-12'),
        (9, 'Ivy', 1, 53000, '2021-06-20'),
        (10, 'Jack', 3, 58000, '2019-02-18'),
        (11, 'Karen', 5, 85000, '2020-12-22'),
        (12, 'Leo', 6, 67000, '2019-08-05'),
        (13, 'Mia', 4, 52000, '2023-01-14'),
        (14, 'Nathan', 7, 90000, '2021-03-28'),
        (15, 'Olivia', 2, 72000, '2022-09-10'),
        (16, 'Peter', 1, 49000, '2023-05-22'),
        (17, 'Quinn', 3, 61000, '2018-12-31'),
        (18, 'Ryan', 4, 54000, '2022-08-07'),
        (19, 'Sophia', 5, 87000, '2020-10-29'),
        (20, 'Thomas', 6, 65000, '2021-11-11')
    ]

    cursor.executemany("INSERT INTO Employees (ID, Name, Department, Salary, Hire_Date) VALUES (?, ?, ?, ?, ?)", employees)

    conn.commit()
    conn.close()


@app.route('/query', methods=['POST'])
def query_database():
    user_query = request.json.get('query', '').lower()
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        if "show me all employees in" in user_query:
            dept = user_query.split(" in ")[1].split(" department")[0].strip()
            cursor.execute("SELECT Employees.ID, Employees.Name, Departments.Name, Employees.Salary, Employees.Hire_Date FROM Employees JOIN Departments ON Employees.Department = Departments.ID WHERE Departments.Name = ?", (dept,))
            results = cursor.fetchall()
            response = [dict(ID=row[0], Name=row[1], Department=row[2], Salary=row[3], Hire_Date=row[4]) for row in results]
            return jsonify(response if response else {"message": "No employees found in this department."})
        
        elif "who is the manager of" in user_query:
            dept = user_query.split(" of ")[1].split(" department")[0].strip()
            cursor.execute("SELECT Manager FROM Departments WHERE Name = ?", (dept,))
            result = cursor.fetchone()
            return jsonify({"Manager": result[0]} if result else {"message": "Department not found."})
        
        elif "list all employees hired after" in user_query:
            date = user_query.split(" after ")[1].strip()
            cursor.execute("SELECT * FROM Employees WHERE Hire_Date > ?", (date,))
            results = cursor.fetchall()
            response = [dict(ID=row[0], Name=row[1], Department=row[2], Salary=row[3], Hire_Date=row[4]) for row in results]
            return jsonify(response if response else {"message": "No employees found hired after this date."})
        
        elif "what is the total salary expense for" in user_query:
            dept = user_query.split(" for ")[1].split(" department")[0].strip()
            cursor.execute("SELECT SUM(Employees.Salary) FROM Employees JOIN Departments ON Employees.Department = Departments.ID WHERE Departments.Name = ?", (dept,))
            result = cursor.fetchone()
            return jsonify({"Total Salary Expense": result[0]} if result and result[0] else {"message": "Department not found or no employees."})
        
        else:
            return jsonify({"message": "Unsupported query. Please try again."})
    
    except Exception as e:
        return jsonify({"error": str(e)})
    
    finally:
        conn.close()

if __name__ == '__main__':
    create_database()
    app.run(host='0.0.0.0', port=3000, debug=True)