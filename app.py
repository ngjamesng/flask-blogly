"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, default_img_url, Post, Tag
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


######################################
# user routes
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
    img_url = request.form["img-url"] or None

    # send info to DB, then get ID

    user = User(first_name=first_name, last_name=last_name, img_url=img_url)
    db.session.add(user)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """ Show user """

    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template("user-page.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit")
def show_edit_user_form(user_id):
    """ Show edit user form """

    user = User.query.get_or_404(user_id)

    return render_template("edit-user.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """ Handle post / update user in database with new info """

    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    img_url = request.form["img-url"] or default_img_url

    # Edit USER
    user = User.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.img_url = img_url

    # need to update DB
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """ Handle Post / Delete user """

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


######################################
# post routes


@app.route("/users/<int:user_id>/posts/new")
def show_create_post_form(user_id):
    """show create post form"""

    user = User.query.get_or_404(user_id)

    return render_template("new-post-form.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def create_new_post(user_id):
    """" handle post route for new posts """
    title = request.form["title"]
    content = request.form["content"]

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/posts/{post.id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """ show post page"""

    post = Post.query.get_or_404(post_id)

    return render_template("post-page.html", post=post, user=post.user)


@app.route("/posts/<int:post_id>/edit")
def show_edit_post_form(post_id):
    """ show post edit form"""

    post = Post.query.get_or_404(post_id)

    return render_template("edit-post.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def update_post(post_id):
    """ handle edit post form """

    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]

    # Do we need this?
    # post.title = title
    # post.content = content

    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """ handle delete post request """

    post = Post.query.get_or_404(post_id)
    user = post.user
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{user.id}")


######################################
# tag routes


@app.route("/tags")
def list_tags():
    # query tag
    tags = Tag.query.all()

    return render_template("list-tags.html", tags=tags)


@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template("show-tag.html", tag=tag, posts=posts)


@app.route("/tags/new")
def show_new_tag_form():

    return render_template("new-tag-form.html")


@app.route("/tags/new", methods=["POST"])
def create_new_tag():

    name = request.form["tag-name"]
    tag = Tag(name=name)

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")

@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):

    tag = Tag.query.get(tag_id)

    return render_template('/edit-tag.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):

    tag = Tag.query.get(tag_id)
    tag.name = request.form['tag-name']

    db.session.commit()

    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):

    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')