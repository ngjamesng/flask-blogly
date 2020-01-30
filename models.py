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

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    img_url = db.Column(
        db.String(),
        nullable=False,
        default="https://lh5.googleusercontent.com/proxy/OaJpLjuFWgu-G_S7mrkjo4NsR5UxtJx33u7hBANMTFSGFJFzqYfbZGvW25CnqgD0_TubCqZ61kM5VdOFrXVgshprgY-GjlHtpPHbA_WYCyuZJuJWiPnECwkK_QNFh8OnymsfxEVt81jd2Ja9w71FWwgs"
    )

