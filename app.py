
from flask import Flask, render_template, request, redirect, url_for
from database import get_connection

import webbrowser
from threading import Timer

app = Flask(__name__)


@app.route('/')
def home():

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    # Total students
    cursor.execute("SELECT COUNT(*) AS total FROM students")
    total_students = cursor.fetchone()["total"]

    # Average marks
    cursor.execute("SELECT AVG(marks) AS average FROM students")
    result = cursor.fetchone()
    average_marks = round(result["average"] or 0, 2)

    # Top performer
    cursor.execute("""
        SELECT * FROM students
        ORDER BY marks DESC
        LIMIT 1
    """)
    top_student = cursor.fetchone()

    # All students
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    # Chart data
    chart_labels = [student["name"] for student in students]
    chart_marks = [student["marks"] for student in students]

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        students=students,
        total_students=total_students,
        average_marks=average_marks,
        top_student=top_student,
        chart_labels=chart_labels,
        chart_marks=chart_marks
    )


@app.route('/add', methods=['POST'])
def add_student():

    name = request.form['name']
    email = request.form['email']
    course = request.form['course']
    marks = request.form['marks']
    attendance = request.form['attendance']

    connection = get_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO students (name, email, course, marks, attendance)
        VALUES (%s, %s, %s, %s, %s)
    """

    cursor.execute(
        query,
        (name, email, course, marks, attendance)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('home'))


@app.route('/search')
def search_student():

    keyword = request.args.get('keyword', '')

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM students WHERE name LIKE %s OR course LIKE %s",
        (f"%{keyword}%", f"%{keyword}%")
    )

    students = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template(
        "index.html",
        students=students,
        total_students=len(students),
        average_marks=0,
        top_student=None,
        chart_labels=[student["name"] for student in students],
        chart_marks=[student["marks"] for student in students]
    )


@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = %s",
        (id,)
    )

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('home'))


@app.route('/edit/<int:id>')
def edit_student(id):

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM students WHERE id = %s",
        (id,)
    )

    student = cursor.fetchone()

    cursor.close()
    connection.close()

    return render_template("edit.html", student=student)


@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):

    name = request.form['name']
    email = request.form['email']
    course = request.form['course']
    marks = request.form['marks']
    attendance = request.form['attendance']

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE students
        SET name=%s, email=%s, course=%s, marks=%s, attendance=%s
        WHERE id=%s
    """, (name, email, course, marks, attendance, id))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('home'))


# MAIN PROGRAM
if __name__ == '__main__':

    url = "http://127.0.0.1:5000/"

    print("Starting Flask Server...")

    Timer(3, lambda: webbrowser.open(url)).start()

    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False
    )
