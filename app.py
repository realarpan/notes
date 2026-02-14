from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Store notes as dictionaries
notes = []

# Simple admin credentials
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


@app.route("/")
def index():
    return render_template("index.html", notes=notes)


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


@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))

    return render_template("admin.html")


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin"))
    return render_template("admin.html", notes=notes, dashboard=True)


@app.route("/delete/<int:index>")
def delete_note(index):
    if not session.get("admin"):
        return redirect(url_for("admin"))

    if 0 <= index < len(notes):
        notes.pop(index)

    return redirect(url_for("admin_dashboard"))


@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
