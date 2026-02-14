from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey123"  # Change this in production

# Store notes in memory (temporary storage)
notes = []

# Admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


# =========================
# Home Page (User Side)
# =========================
@app.route("/")
def index():
    return render_template("index.html")


# =========================
# Add Note (User)
# =========================
@app.route("/add", methods=["POST"])
def add_note():
    username = request.form.get("username")
    note_text = request.form.get("note")

    if username and note_text:
        notes.append({
            "user": username.strip(),
            "text": note_text.strip()
        })

    return redirect(url_for("index"))


# =========================
# Admin Login
# =========================
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin_logged_in"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin.html", error="Invalid credentials")

    return render_template("admin.html")


# =========================
# Admin Dashboard
# =========================
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))

    return render_template("admin.html", notes=notes, dashboard=True)


# =========================
# Delete Note (Admin Only)
# =========================
@app.route("/delete/<int:index>")
def delete_note(index):
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))

    if 0 <= index < len(notes):
        notes.pop(index)

    return redirect(url_for("admin_dashboard"))


# =========================
# Logout
# =========================
@app.route("/logout")
def logout():
    session.pop("admin_logged_in", None)
    return redirect(url_for("index"))


# =========================
# Run App
# =========================
if __name__ == "__main__":
    app.run(debug=True)
