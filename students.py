# student.py
from flask import Blueprint, render_template, request, redirect, url_for, session, send_file, flash
import sqlite3
import io
import re
from fpdf import FPDF

student_bp = Blueprint('student_bp', __name__)

def get_db_connection():
    return sqlite3.connect('students.db')

# --- Validation Functions ---
def is_valid_name(name):
    return re.fullmatch(r'[A-Za-z ]+', name)

def is_valid_email(email):
    return re.fullmatch(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def is_valid_phone(phone):
    return re.fullmatch(r'\d{10}', phone)

def is_valid_address(address):
    return re.fullmatch(r'^[\w\s,.-]+$', address)

# --- Routes ---
@student_bp.route('/students')
def view_students():
    if 'admin' not in session:
        return redirect(url_for('auth_bp.login'))

    search = request.args.get('search', '')
    conn = get_db_connection()
    cursor = conn.cursor()

    if search:
        cursor.execute("SELECT * FROM students WHERE name LIKE ? OR email LIKE ?", (f'%{search}%', f'%{search}%'))
    else:
        cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('students.html', students=students, search=search)

@student_bp.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']

    if not is_valid_name(name):
        flash("\u274C Name should contain only letters and spaces.")
    elif not is_valid_email(email):
        flash("\u274C Invalid email format.")
    elif not is_valid_phone(phone):
        flash("\u274C Phone number must be exactly 10 digits.")
    elif not is_valid_address(address):
        flash("\u274C Address can contain only letters, numbers, spaces, commas, dots, and hyphens.")
    else:
        conn = get_db_connection()
        conn.execute("INSERT INTO students (name, email, phone, address) VALUES (?, ?, ?, ?)",
                     (name, email, phone, address))
        conn.commit()
        conn.close()
        flash("\u2705 Student added successfully.")

    return redirect(url_for('student_bp.view_students'))

@student_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        if not is_valid_name(name):
            flash("\u274C Name should contain only letters and spaces.")
        elif not is_valid_email(email):
            flash("\u274C Invalid email format.")
        elif not is_valid_phone(phone):
            flash("\u274C Phone number must be exactly 10 digits.")
        elif not is_valid_address(address):
            flash("\u274C Address can contain only letters, numbers, spaces, commas, dots, and hyphens.")
        else:
            conn.execute("UPDATE students SET name=?, email=?, phone=?, address=? WHERE id=?",
                         (name, email, phone, address, id))
            conn.commit()
            conn.close()
            flash("\u2705 Student updated successfully.")
            return redirect(url_for('student_bp.view_students'))

    cursor = conn.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()
    conn.close()
    return render_template('edit.html', student=student)

@student_bp.route('/delete/<int:id>')
def delete_student(id):
    conn = get_db_connection()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    flash("\U0001f5d1\ufe0f Student deleted.")
    return redirect(url_for('student_bp.view_students'))

@student_bp.route('/export')
def export_pdf():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Student List", ln=True, align='C')
    for s in students:
        pdf.cell(200, 10, txt=f"ID: {s[0]}, Name: {s[1]}, Email: {s[2]}, Phone: {s[3]}, Address: {s[4]}", ln=True)

    pdf_output = pdf.output(dest='S').encode('latin1')
    output = io.BytesIO(pdf_output)

    return send_file(output, download_name="students.pdf", as_attachment=True)

@student_bp.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect(url_for('auth_bp.login'))

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM students ORDER BY id DESC LIMIT 5")
    recent_students = cursor.fetchall()

    conn.close()
    return render_template('dashboard.html', total_students=total_students, recent_students=recent_students)
