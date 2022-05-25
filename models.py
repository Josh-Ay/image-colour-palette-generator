from app import db
from flask_login import UserMixin
from sqlalchemy.orm import relationship


class Colors(db.Model):
    __tablename__ = "colors"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    colors = relationship("User", back_populates="saved_colors")


class ColorPalettes(db.Model):
    __tablename__ = "colorpalettes"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    palettes = relationship("User", back_populates="saved_palettes")


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True)
    display_name = db.Column(db.String(250), nullable=False)
    saved_colors = relationship("Colors", back_populates="colors")
    saved_palettes = relationship("ColorPalettes", back_populates="palettes")

    def get_user_id(self):
        return self.id


def initialize_db():
    db.create_all()


if __name__ == "main":
    initialize_db()
