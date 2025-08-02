from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def anasayfa():
    return render_template("main.html")

@app.route("/forum")
def forum():
    return render_template("forum.html")

@app.route("/myquestions")
def myquestions():
    return render_template("myquestions.html")

@app.route("/progress")
def progress():
    return render_template("progress.html")

@app.route("/exams")
def exams():
    return render_template("exams.html")

@app.route("/mail")
def mail():
    return render_template("mail.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/base_auth")
def base_auth():
    return render_template("base_auth.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
