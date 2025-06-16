from flask import Flask, render_template, redirect, url_for, session
from auth import auth_bp
from students import student_bp
from database import init_db

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key in production

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)

@app.route('/')
def home():
    return render_template('index.html')  # Loads the welcome page

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
