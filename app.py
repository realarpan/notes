from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

notes = []

@app.route("/")
def index():
    return render_template("index.html", notes=notes)

@app.route("/add", methods=["POST"])
def add_note():
    note = request.form.get("note")
    if note and note.strip():
        notes.append(note.strip())
    return redirect(url_for("index"))

@app.route("/delete", methods=["POST"])
def delete_note():
    index = int(request.form.get("index"))
    if 0 <= index < len(notes):
        notes.pop(index)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
