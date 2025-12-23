import os
import sqlite3
from flask import Flask, render_template, request, redirect, session


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

def get_db():
    return sqlite3.connect(DB_PATH)

UPLOAD_FOLDER = "static/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


app = Flask(__name__)
app.secret_key = "careeraxis_super_secret_key"

def get_db():
    return sqlite3.connect("database.db")

@app.route("/")
def home():
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        role = request.form["role"]

        db = get_db()
        cur = db.cursor()
        cur.execute(
            "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
            (name, email, password, role)
        )
        db.commit()
        db.close()

        return redirect("/login")

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = get_db().cursor()
        cur.execute(
            "SELECT id, name, role FROM users WHERE email=? AND password=?",
            (email, password)
        )
        user = cur.fetchone()

        if user:
            session['user_id'] = user[0]
            session['name'] = user[1]
            session['role'] = user[2]   # 🔴 THIS IS CRITICAL

            return redirect('/dashboard')
        else:
            return "Invalid credentials"

    return render_template('login.html')


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    role = session["role"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    # ✅ Get user name
    cur.execute("SELECT name FROM profiles WHERE user_id=?", (user_id,))
    profile = cur.fetchone()
    user_name = profile[0] if profile else "User"

    pending_applications = 0
    total_jobs = 0

    if role == "admin":
        # ✅ Only jobs posted by THIS admin
        cur.execute("SELECT COUNT(*) FROM jobs WHERE admin_id=?", (user_id,))
        total_jobs = cur.fetchone()[0]

        # ✅ Pending applications for THIS admin's jobs
        cur.execute("""
            SELECT COUNT(*)
            FROM applications
            JOIN jobs ON applications.job_id = jobs.id
            WHERE jobs.admin_id=? AND applications.status='Pending'
        """, (user_id,))
        pending_applications = cur.fetchone()[0]

    else:
        # ✅ Pending applications for logged-in user
        cur.execute("""
            SELECT COUNT(*)
            FROM applications
            WHERE user_id=? AND status='Pending'
        """, (user_id,))
        pending_applications = cur.fetchone()[0]

        # ✅ Total available jobs
        cur.execute("SELECT COUNT(*) FROM jobs")
        total_jobs = cur.fetchone()[0]

    conn.close()

    return render_template(
        "dashboard.html",
        role=role,
        user_name=user_name,
        pending_applications=pending_applications,
        total_jobs=total_jobs
    )
    


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/add_job", methods=["GET", "POST"])
def add_job():
    if session.get("role") != "admin":
        return redirect("/dashboard")

    if request.method == "POST":
        title = request.form["title"]
        company = request.form["company"]
        description = request.form["description"]
        admin_id = session["user_id"]

        db = get_db()
        cur = db.cursor()

        cur.execute("""
            INSERT INTO jobs (title, company, description, admin_id)
            VALUES (?, ?, ?, ?)
        """, (title, company, description, admin_id))

        db.commit()
        db.close()

        return redirect("/dashboard")

    return render_template("add_job.html")



@app.route("/jobs")
def jobs():
    db = get_db()
    cur = db.cursor()

    if session.get("role") == "admin":
        admin_id = session["user_id"]
        cur.execute("SELECT * FROM jobs WHERE admin_id=?", (admin_id,))
    else:
        cur.execute("SELECT * FROM jobs")

    jobs = cur.fetchall()
    db.close()

    return render_template("jobs.html", jobs=jobs, role=session.get("role"))


@app.route("/admin/jobs")
def admin_jobs():
    admin_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM jobs
        WHERE admin_id=?
    """, (admin_id,))

    jobs = cur.fetchall()
    conn.close()

    return render_template("admin_jobs.html", jobs=jobs)

@app.route("/admin/applications")
def admin_applications():
    admin_id = session["user_id"]

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT a.id, u.name, j.title, a.status
        FROM applications a
        JOIN users u ON a.user_id = u.id
        JOIN jobs j ON a.job_id = j.id
        WHERE j.admin_id=?
    """, (admin_id,))

    apps = cur.fetchall()
    conn.close()

    return render_template("admin_applications.html", apps=apps)



@app.route("/apply/<int:job_id>")
def apply(job_id):
    if session.get("role") != "user":
        return redirect("/jobs")

    user_id = session.get("user_id")

    db = get_db()
    cur = db.cursor()
    cur.execute(
        "INSERT INTO applications (user_id, job_id, status) VALUES (?,?,?)",
        (user_id, job_id, "Pending")
    )
    db.commit()
    db.close()

    return redirect("/jobs")

@app.route("/admin_applicants/<int:job_id>")
def admin_applicants(job_id):
    if session.get("role") != "admin":
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT profiles.name,
               profiles.skills,
               profiles.photo,
               applications.status,
               applications.id
        FROM applications
        JOIN profiles ON applications.user_id = profiles.user_id
        WHERE applications.job_id = ?
    """, (job_id,))

    applicants = cur.fetchall()
    conn.close()

    return render_template(
        "admin_applicants.html",
        applicants=applicants
    )



@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "user_id" not in session:
        return redirect("/login")

    db = get_db()
    cur = db.cursor()

    # Check if profile already exists
    cur.execute("SELECT * FROM profiles WHERE user_id=?", (session["user_id"],))
    existing = cur.fetchone()

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        location = request.form["location"]
        skills = request.form["skills"]
        education = request.form["education"]

        photo = request.files["photo"]
        filename = "default.png"

        if photo and photo.filename != "":
            filename = secure_filename(photo.filename)
            photo.save(os.path.join("static/uploads", filename))

        cur.execute("""
        INSERT INTO profiles (user_id, name, age, location, skills, education, photo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (session["user_id"], name, age, location, skills, education, filename))

        db.commit()
        db.close()
        return redirect("/dashboard")

    db.close()

    # If profile exists → redirect to view profile
    if existing:
        return redirect("/view_profile")

    return render_template("profile.html")



@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        location = request.form["location"]
        skills = request.form["skills"]
        education = request.form["education"]

        photo = request.files["photo"]
        filename = None

        if photo and photo.filename != "":
            filename = photo.filename
            upload_path = os.path.join("static/uploads", filename)
            os.makedirs("static/uploads", exist_ok=True)
            photo.save(upload_path)

            cur.execute("""
                UPDATE profiles
                SET name=?, age=?, location=?, skills=?, education=?, photo=?
                WHERE user_id=?
            """, (name, age, location, skills, education, filename, session["user_id"]))
        else:
            cur.execute("""
                UPDATE profiles
                SET name=?, age=?, location=?, skills=?, education=?
                WHERE user_id=?
            """, (name, age, location, skills, education, session["user_id"]))

        conn.commit()
        conn.close()
        return redirect("/view_profile")

    cur.execute("SELECT * FROM profiles WHERE user_id=?", (session["user_id"],))
    profile = cur.fetchone()
    conn.close()

    return render_template("edit_profile.html", profile=profile)




@app.route("/admin_profiles")
def admin_profiles():
    if session.get("role") != "admin":
        return redirect("/dashboard")

    db = get_db()
    cur = db.cursor()
    cur.execute("""
    SELECT profiles.id, users.name, profiles.age, profiles.location,
           profiles.skills, profiles.education
    FROM profiles
    JOIN users ON profiles.user_id = users.id
    """)
    profiles = cur.fetchall()
    db.close()

    return render_template("admin_profiles.html", profiles=profiles)




@app.route("/update_status/<int:app_id>/<status>")
def update_status(app_id, status):
    if session.get("role") != "admin":
        return redirect("/dashboard")

    db = get_db()
    cur = db.cursor()

    cur.execute(
        "UPDATE applications SET status=? WHERE id=?",
        (status, app_id)
    )

    db.commit()
    db.close()

    return redirect("/jobs")


@app.route("/job_applicants/<int:job_id>")
def job_applicants(job_id):
    if session.get("role") != "admin":
        return redirect("/dashboard")

    admin_id = session["user_id"]

    db = get_db()
    cur = db.cursor()

    # 🔐 Check job belongs to THIS admin
    cur.execute("""
        SELECT id, title, company FROM jobs
        WHERE id=? AND admin_id=?
    """, (job_id, admin_id))

    job = cur.fetchone()

    if not job:
        db.close()
        return "Unauthorized access", 403

    cur.execute("""
        SELECT applications.id, users.name,
               profiles.age, profiles.location,
               profiles.skills, profiles.education,
               applications.status
        FROM applications
        JOIN users ON applications.user_id = users.id
        JOIN profiles ON profiles.user_id = users.id
        WHERE applications.job_id=?
    """, (job_id,))

    applicants = cur.fetchall()
    db.close()

    return render_template(
        "job_applicants.html",
        job=job,
        applicants=applicants
    )



@app.route("/notifications")
def notifications():
    if session.get("role") != "user":
        return redirect("/login")

    user_id = session.get("user_id")

    conn = sqlite3.connect("database.db")
    cur = conn.cursor()

    cur.execute("""
        SELECT jobs.title,
               jobs.company,
               applications.status
        FROM applications
        JOIN jobs ON applications.job_id = jobs.id
        WHERE applications.user_id = ?
    """, (user_id,))

    notifications = cur.fetchall()
    conn.close()

    return render_template(
        "notifications.html",
        notifications=notifications
    )


@app.route("/view_profile")
def view_profile():
    if session.get("role") != "user":
        return redirect("/dashboard")

    db = get_db()
    cur = db.cursor()

    cur.execute("SELECT * FROM profiles WHERE user_id=?", (session["user_id"],))
    profile = cur.fetchone()
    db.close()

    return render_template("view_profile.html", profile=profile)




if __name__ == "__main__":
    app.run()








