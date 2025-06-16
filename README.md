<<<<<<< HEAD
# Student Management System 🧑‍🎓

A web-based Student Management System built using **Python**, **Flask**, **HTML**, **CSS**, and **SQLite**. It allows an admin to manage student records efficiently with functionality like add, edit, delete, search, export (PDF/Excel), and view dashboard analytics.

---

## 🚀 Features

- Admin login and secure session handling
- Add, view, edit, and delete student details
- Search students by name or email
- Export student data to PDF and Excel
- Dashboard with student statistics
- Clean responsive UI with polished styles

---

## 🛠️ Tech Stack

- **Backend**: Python, Flask
- **Frontend**: HTML5, CSS3, Bootstrap (optional)
- **Database**: SQLite3
- **Export**: pandas, xhtml2pdf

---

## 📁 Folder Structure

```text student-management-system/ │ ├── static/ │ └── style.css ├── templates/ │ ├── login.html │ ├── index.html │ ├── students.html │ └── edit.html ├── images/ │ ├── login.png │ └── dashboard.png │ ├── auth.py ├── students.py ├── database.py ├── main.py ├── requirements.txt └── README.md ```



## 🔧 Installation

1. **Clone the repo**:
   ```bash
   git clone https://github.com/Karripravallika/student-management-system.git
   cd student-management-system

## Create a virtual environment (optional but recommended): 

python -m venv venv
venv\Scripts\activate   # Windows

## Install dependencies:
pip install -r requirements.txt

## Run the application:
python main.py

## 🔑 Admin Credentials

Username: admin
Password: admin123
You can change this in auth.py.

## 📤 Export Functions

PDF: Uses xhtml2pdf
Excel: Uses pandas

=======

