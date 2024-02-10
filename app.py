from flask import Flask, render_template, request, redirect, url_for
from flask_ngrok import run_with_ngrok
import sqlite3

app = Flask(__name__)
run_with_ngrok(app)
# SQLite database setup
conn = sqlite3.connect('brugg.db', check_same_thread=False)
cursor = conn.cursor()

# Create tables if they don't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    firstname TEXT NOT NULL,
                    lastname TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT NOT NULL
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    manager_id INTEGER NOT NULL,
                    FOREIGN KEY (manager_id) REFERENCES users (id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS team_members (
                    id INTEGER PRIMARY KEY,
                    project_id INTEGER NOT NULL,
                    member_id INTEGER NOT NULL,
                    FOREIGN KEY (project_id) REFERENCES projects (id),
                    FOREIGN KEY (member_id) REFERENCES users (id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS timesheets (
                    id INTEGER PRIMARY KEY,
                    project_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT NOT NULL,
                    jointer_name TEXT NOT NULL,
                    approval_status TEXT NOT NULL,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS complaints (
                    id INTEGER PRIMARY KEY,
                    project_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    complaint_title TEXT NOT NULL,
                    complainer TEXT NOT NULL,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS photos_videos (
                    id INTEGER PRIMARY KEY,
                    project_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    uploader TEXT NOT NULL,
                    file_path TEXT NOT NULL,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS delays (
                    id INTEGER PRIMARY KEY,
                    project_id INTEGER NOT NULL,
                    date TEXT NOT NULL,
                    submitter TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    FOREIGN KEY (project_id) REFERENCES projects (id)
                )''')
conn.commit()
conn.close()
# Routes
@app.route('/')
def home():
    return render_template('home.html')
# Route for signup page

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Extract form data
        firstname = request.form['firstName']
        lastname = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        # Insert new user into database
        cursor.execute("INSERT INTO users (firstname,lastname,email, password, role) VALUES (?, ?, ?, ?, ?)", (firstname, lastname,email, password, role))
        conn.commit()

        return redirect(url_for('login'))
    return render_template('signup.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        # Example: Validate login credentials
        email = request.form['email']
        password = request.form['password']
        if email == 'pmEmail' and password == 'pmPassword':
            # Redirect to PM dashboard if login is successful
            return redirect(url_for('pm_dashboard'))
        elif email == 'jointerEmail' and password == 'jointerPassword':
            # Redirect to Jointer dashboard if login is successful
            return redirect(url_for('jointer_dashboard'))
        else:
            # Redirect back to login page with error message
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html', error=None)

# Route for project manager dashboard
@app.route('/pm-dashboard')
def pm_dashboard():
    return render_template('pm-dashboard.html')

# Route for jointer dashboard
@app.route('/jointer-dashboard')
def jointer_dashboard():
    return render_template('jointer-dashboard.html')

# Route for project manager project page
@app.route('/pm-project/<project_id>')
def pm_project(project_id):
    return render_template('pm-project.html', project_id=project_id)

# Route for jointer project page
@app.route('/jointer-project/<project_id>')
def jointer_project(project_id):
    return render_template('jointer-project.html', project_id=project_id)
