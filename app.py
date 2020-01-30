"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True

app.config["SECRET_KEY"] = "keyyyy"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def show_home():
    # TODO: GRAB USER LIST first name, last name
    # pass user list into render_template

    users = User.query.all()

    return render_template("index.html", users=users)


@app.route("/user_form")
def show_new_user_form():
    return render_template("new-user-form.html")


@app.route("/user_form", methods=["POST"])
def create_new_user():
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form.get(
        "img-url", None
    )  # be aware of refactoring for later if none

    # send info to DB, then get ID

    user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/user/{user.id}")


@app.route("user/<int:user_id>")
def show_user(user_id):

    user = User.query.get(user_id)

    return render_template("user-page.html", user=user)


@app.route("/edit_user/<int:user_id>")
def show_edit_user_form(user_id):

    user = User.query.get(user_id)

    return render_template("edit-user.html", user=user)


@app.route("/edit_user/<int:user_id>", methods=["POST"])
def update_user(user_id):

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form.get("img-url", None)

    user = User.query.get(user_id)

    user.first_name = first_name
    user.last_name = last_name
    user.img_url = img_url
    # need to update DB, test and see if this updates correctly
    db.session.commit()

    return redirect(f"/user/{user.id}")
