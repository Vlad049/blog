from flask import Flask, render_template, render_template, redirect, request, url_for

from data.db.base import create_db, Session
from data.db import db_action
from data.db.models import Post

app = Flask(__name__)

@app.get("/")
def index():
    with Session() as session:
        posts = session.query(Post).all()
        return render_template("index.html", posts=posts)


@app.route("/add_post/", methods = ["GET", "POST"])
def add_post():
    if request.method == "POST":
        title = request.form.get("title")
        text = request.form.get("text")
        author_id = request.form.get("author_id")
        db_action.add_post(title=title, text=text, author_id=author_id)
        return redirect(url_for("index"))

    authors = db_action.get_authors()
    return render_template("add_post.html", authors=authors)


@app.route("/add_author/", methods = ["GET", "POST"])
def add_author():
    if request.method == "POST":
        name = request.form.get("name")
        country = request.form.get("country")
        db_action.add_author(name=name, country=country)

    return render_template("add_author.html")



if __name__ == "__main__":
    create_db()
    app.run(debug=True, port=90)