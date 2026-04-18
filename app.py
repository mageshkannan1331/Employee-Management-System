from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

# Database Setup
def init_db():
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS employees(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        department TEXT NOT NULL,
        salary REAL NOT NULL
    )
    """)

    conn.commit()
    conn.close()

init_db()

# Home
@app.route('/')
def index():
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees")
    data = cur.fetchall()
    conn.close()
    return render_template("index.html", employees=data)

# Add Employee
@app.route('/add', methods=['POST'])
def add():
    try:
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        dept = request.form['department'].strip()
        salary = request.form['salary'].strip()

        # Validation
        if not name:
            flash("Name is required")
            return redirect('/')

        if '@' not in email:
            flash("Invalid email")
            return redirect('/')

        if not dept:
            flash("Department required")
            return redirect('/')

        if not salary.replace('.', '', 1).isdigit():
            flash("Salary must be numeric")
            return redirect('/')

        conn = sqlite3.connect("employees.db")
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO employees(name,email,department,salary) VALUES(?,?,?,?)",
            (name, email, dept, salary)
        )

        conn.commit()
        conn.close()

        flash("Employee added successfully")

    except sqlite3.IntegrityError:
        flash("Email already exists")

    except Exception:
        flash("Something went wrong")

    return redirect('/')

# Delete
@app.route('/delete/<int:id>')
def delete(id):
    try:
        conn = sqlite3.connect("employees.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE id=?", (id,))
        conn.commit()
        conn.close()

        flash("Deleted successfully")

    except Exception:
        flash("Delete failed")

    return redirect('/')

# Edit Page
@app.route('/edit/<int:id>')
def edit(id):
    conn = sqlite3.connect("employees.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees WHERE id=?", (id,))
    employee = cur.fetchone()
    conn.close()

    return render_template("edit.html", emp=employee)

# Update
@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    try:
        name = request.form['name']
        email = request.form['email']
        dept = request.form['department']
        salary = request.form['salary']

        if not name:
            flash("Name required")
            return redirect('/')

        conn = sqlite3.connect("employees.db")
        cur = conn.cursor()

        cur.execute("""
        UPDATE employees
        SET name=?, email=?, department=?, salary=?
        WHERE id=?
        """, (name, email, dept, salary, id))

        conn.commit()
        conn.close()

        flash("Updated successfully")

    except Exception:
        flash("Update failed")

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)