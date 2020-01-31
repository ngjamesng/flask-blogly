"""Models for Blogly."""

import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
default_img_url = "https://images.unsplash.com/photo-1580329503754-35ddb65d49a8?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60"


def connect_db(app):
    """connects to database!"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """user model"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    img_url = db.Column(db.String(), nullable=False, default=default_img_url)

    def __repr__(self):
        """Show user info"""

        return f"<full name: {self.first_name} {self.last_name}>"


class Post(db.Model):
    """ post model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=text('now()'))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    user = db.relationship("User", backref="posts")

    posttags = db.relationship("Tag", secondary="post_tags", backref="posts")

    def __repr__(self):
        """show post title"""

        return f"<title of post: {self.title}>"


class Tag(db.Model):
    """Tag model"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        """ show tag """

        return f"<tag name: {self.name}>"


class PostTag(db.Model):
    """PostTag model"""

    __tablename__ = "post_tags"

    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

