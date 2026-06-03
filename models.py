from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

Db = SQLAlchemy()

class User(Db.Model):
    __tablename__ = 'users'
    Id = Db.Column(Db.Integer, primary_key=True)
    Username = Db.Column(Db.String(80), unique=True, nullable=False, index=True)
    PasswordHash = Db.Column(Db.String(255), nullable=False)
    HighestStreak = Db.Column(Db.Integer, default=0)
    TotalWins = Db.Column(Db.Integer, default=0)
    TotalGames = Db.Column(Db.Integer, default=0)

    def set_password(self, password):
        self.PasswordHash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.PasswordHash, password)

class Word(Db.Model):
    __tablename__ = 'words'
    Id = Db.Column(Db.Integer, primary_key=True)
    TargetWord = Db.Column(Db.String(100), nullable=False)
    Category = Db.Column(Db.String(50), nullable=False, index=True)
