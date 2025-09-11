from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# In-memory storage (simple, will reset when server restarts)
users = {"admin": "yuvi1991"}  # admin credentials
profiles = {}  # store user profiles

# Upload settings
UPLOAD_FOLDER = os.path.join('static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """Check if uploaded file has a valid extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Home page
@app.route('/')
def home():
    return render_template('index.html')


# Login
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    if username in users and users[username] == password:
        session['username'] = username
        if username == 'admin':
            return redirect(url_for('admin'))
        return redirect(url_for('user_form'))
    return "Invalid username or password. <a href='/'>Go back</a>"


# Register
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    if username in users:
        return "Username already exists! <a href='/'>Go back</a>"
    if password != confirm_password:
        return "Passwords do not match! <a href='/'>Go back</a>"
    if len(username) < 3 or len(password) < 4:
        return "Username must be at least 3 chars and password 4+ chars! <a href='/'>Go back</a>"

    users[username] = password
    return redirect(url_for('home'))


# Admin dashboard
@app.route('/admin')
def admin():
    if session.get('username') != "admin":
        return redirect(url_for('home'))
    return render_template('admin.html', profiles=profiles)


# Logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))


# User profile form
@app.route('/user_form')
def user_form():
    username = session.get('username')
    if not username or username == 'admin':
        return redirect(url_for('home'))
    return render_template('user_form.html', profile=profiles.get(username))


# Handle profile submission
@app.route('/submit_user_form', methods=['POST'])
def submit_user_form():
    username = session.get('username')
    if not username or username == 'admin':
        return redirect(url_for('home'))

    # Handle photo upload
    photo = request.files.get('photo')
    photo_filename = None
    if photo and allowed_file(photo.filename):
        filename = secure_filename(photo.filename)
        photo_filename = f"{username}_{filename}"
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))

    # Save profile data
    profiles[username] = {
        'full_name': request.form.get('full_name'),
        'address': request.form.get('address'),
        'dob': request.form.get('dob'),
        'mobile': request.form.get('mobile'),
        'qualification': request.form.get('qualification'),
        'expectation': request.form.get('expectation'),
        'photo': photo_filename
    }

    return f"Thank you {profiles[username]['full_name']}, your profile has been saved! <a href='/user_form'>Back</a>"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
