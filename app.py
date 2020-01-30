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
def redirect_user_list():
    return redirect("/users")


@app.route("/users")
def show_users():
    """ Show user list """

    users = User.query.all()

    return render_template("index.html", users=users)


@app.route("/users/new")
def show_new_user_form():
    """ Show new user form """

    return render_template("new-user-form.html")


@app.route("/users/new", methods=["POST"])
def create_new_user():
    """ Handle post / update database with new user """

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form.get(
        "img-url", None
    )  # be aware of refactoring for later if none

    # send info to DB, then get ID

    user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """ Show user """

    user = User.query.get(user_id)

    return render_template("user-page.html", user=user)


@app.route("/users/<int:user_id>/edit")
def show_edit_user_form(user_id):
    """ Show edit user form """

    user = User.query.get(user_id)

    return render_template("edit-user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """ Handle post / update user in database with new info """

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form.get("img-url", None)

    # ADDS NEW USER
    user = User.query.get(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.img_url = img_url

    # need to update DB
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """ Handle Post / Delete user """

    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')
