from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), unique=True)
  password = db.Column(db.String(64))
  notes = db.relationship('Note')

class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  content = db.Column(db.String(8192))
  date = db.Column(db.DateTime(timezone=True), default=func.now())
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))