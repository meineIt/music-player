from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

user_playlists = db.Table('user_playlists', db.Model.metadata,
                          db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                          db.Column('playlist_id', db.Integer, db.ForeignKey('playlist.id'), primary_key=True)
                          )


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)
    password_hash = db.Column(db.String(100))
    playlists = db.relationship('Playlist', secondary=user_playlists, back_populates='users')
    
    def __repr__(self): return '{}'.format(self.name)
  
    def set_password(self, password):
      self.password_hash = generate_password_hash(password)

    def check_password(self, password):
      return check_password_hash(self.password_hash, password)


class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=False, index=True)
    users = db.relationship('User', secondary=user_playlists, back_populates='playlists')
    songs = db.relationship('Song', backref='playlist', lazy='dynamic', cascade='all, delete, delete-orphan')
    def __repr__(self): return '{}'.format(self.name)


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=False, index=True)
    artist = db.Column(db.String(50), unique=False, index=True)
    url = db.Column(db.String, unique=True, index=True)
    grade = db.Column(db.Integer, unique=False, index=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlist.id'))
    def __repr__(self): return '{t} ({a})'.format(a=self.artist, t=self.title)
