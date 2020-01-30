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

    def __repr__(self):
        """Show user info"""

        return f"<full name: {self.first_name} {self.last_name}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    img_url = db.Column(
        db.String(),
        nullable=False,
        default=default_img_url
    )


class Post(db.Model):
    """ post model"""

    __tablename__ = "posts"

    def __repr__(self):
        """show post title"""

        return f"<title of post: {self.title}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    # need to check if date/timestamp works
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # created_at = db.Column(db.TIMESTAMP(timezone=True), server_default=text('now()'))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    user = db.relationship('User', backref='posts')

