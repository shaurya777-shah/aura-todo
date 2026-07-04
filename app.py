from flask import Flask, render_template, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "aura_secret_key"

subjects = [
    "Maths",
    "Gujarati",
    "Hindi",
    "English",
    "Science",
    "SS"
]

# ---------------- DATABASE ----------------

def init_db():

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        task TEXT,
        subject TEXT,
        due TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )

        user = c.fetchone()

        conn.close()

        if user:

            session["user"] = username

            return redirect("/dashboard")

        return "Invalid Login"

    return render_template("login.html")

# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        c = conn.cursor()

        c.execute(
            "INSERT INTO users VALUES (NULL, ?, ?)",
            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

# ---------------- HOME ----------------

@app.route("/")
def home():

    return redirect("/dashboard")

# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect("/login")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM tasks WHERE user=?",
        (session["user"],)
    )

    rows = c.fetchall()

    conn.close()

    tasks = []

    now = datetime.now()

    for r in rows:

        due_raw = r[4]
        status = "ok"
        due_sort = datetime.max

        if due_raw and due_raw.strip():

            try:

                due = datetime.strptime(
                    due_raw,
                    "%Y-%m-%dT%H:%M"
                )

                due_sort = due

                diff = (due - now).total_seconds() / 3600

                if due < now:

                    status = "overdue"

                elif diff <= 4:

                    status = "due_soon"

                else:

                    status = "ok"

            except:

                status = "invalid"

        else:

            status = "no_date"

        tasks.append({
            "id": r[0],
            "task": r[2],
            "subject": r[3],
            "due": due_raw if due_raw else "No Due Date",
            "status": status,
            "sort_due": due_sort
        })

    tasks.sort(key=lambda x: x["sort_due"])

    return render_template(
        "dashboard.html",
        tasks=tasks,
        subjects=subjects
    )

# ---------------- ADD TASK ----------------

@app.route("/add", methods=["POST"])
def add():

    if "user" not in session:

        return redirect("/login")

    task = request.form["task"]
    subject = request.form["subject"]
    due = request.form["due"]

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "INSERT INTO tasks VALUES (NULL, ?, ?, ?, ?)",
        (session["user"], task, subject, due)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# ---------------- DONE TASK ----------------

@app.route("/done/<int:id>")
def done(id):

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "DELETE FROM tasks WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/dashboard")

# ---------------- SUBJECT PAGE ----------------

@app.route("/subject/<name>")
def subject(name):

    if "user" not in session:

        return redirect("/login")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM tasks WHERE user=? AND subject=?",
        (session["user"], name)
    )

    rows = c.fetchall()

    conn.close()

    return render_template(
        "subject.html",
        subject=name,
        tasks=rows
    )

# ---------------- CALENDAR ----------------

@app.route("/calendar")
def calendar():

    if "user" not in session:

        return redirect("/login")

    conn = sqlite3.connect("users.db")
    c = conn.cursor()

    c.execute(
        "SELECT * FROM tasks WHERE user=? ORDER BY due",
        (session["user"],)
    )

    tasks = c.fetchall()

    conn.close()

    return render_template(
        "calendar.html",
        tasks=tasks
    )

# ---------------- EXAM PAGE ----------------

@app.route("/exam", methods=["GET", "POST"])
def exam():

    result = None

    if request.method == "POST":

        marks = []

        for s in subjects:

            value = request.form.get(s)

            if value:

                marks.append(int(value))

            else:

                marks.append(0)

        avg = sum(marks) / len(marks)

        weakest = subjects[
            marks.index(min(marks))
        ]

        result = {
            "avg": round(avg, 2),
            "weakest": weakest
        }

    return render_template(
        "exam.html",
        subjects=subjects,
        result=result
    )

# ---------------- RUN APP ----------------

if __name__ == "__main__":

    app.run(debug=True)