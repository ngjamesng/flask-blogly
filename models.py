"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    img_url = db.Column(
        db.String(),
        nullable=False,
        default="https://image.shutterstock.com/image-vector/profile-blank-icon-empty-photo-260nw-535853269.jpg",
    )

