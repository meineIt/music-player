import logging.config
from app import app, login
from models import Playlist, Song, User
from flask import render_template, url_for, redirect, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from forms import AddPlaylistForm, AddSongForm, DeleteForm, RegistrationForm, LoginForm
from helper import *
from urllib.parse import urlparse as url_parse
import logging

logging.basicConfig(level=logging.INFO)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('player'))
  
  login_form = LoginForm()
  
  if login_form.validate_on_submit():
    
    user = User.query.filter_by(name=login_form.name.data).first()  
    if user is None:
      flash('Username not exists')
      logging.info('Username not exists')
      return redirect(url_for('login'))
    
    if not user.check_password(login_form.password.data):
      flash('Invalid password')
      logging.info('Invalid password')
      return redirect(url_for('login'))
    
    login_user(user, remember=login_form.remember_me.data)

    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('player')
    
    logging.info('Logged in')
    return redirect(next_page)
    
  return render_template('login.html', title='Sign In', login_form=login_form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
      return redirect(url_for('player'))
    
    register_form = RegistrationForm()
    
    if register_form.validate_on_submit():
        register_new_user(name=register_form.name.data, email=register_form.email.data, password=register_form.password.data)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', register_form=register_form)


@app.route('/player', methods=['GET', 'POST'])
@login_required
def player():
    users = User.query.all()
    playlists = Playlist.query.all()
    songs = Song.query.all()
    return render_template('player.html', 
                           users=users,
                           playlists=playlists, 
                           songs=songs)


@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():

    add_playlist_form = AddPlaylistForm()
    add_song_form = AddSongForm()

    add_playlist_form.users_field.query = User.query.all()
    
    choices = [(playlist.id, playlist.name) for playlist in Playlist.query.all()]
    add_song_form.playlist_field.choices = choices

    if request.method=='POST':
        if add_song_form.validate_on_submit():
            new_artist = add_song_form.artist_field.data
            new_title = add_song_form.title_field.data
            new_url = add_song_form.url_field.data
            new_grade = add_song_form.grade_field.data
            choosen_playlist = add_song_form.playlist_field.data
            add_song_to_database(artist=new_artist, title=new_title, url=new_url, grade=new_grade, playlist_id=choosen_playlist)
        elif add_playlist_form.validate_on_submit():
            new_playlist_name = add_playlist_form.playlist_name_field.data
            choosen_users = add_playlist_form.users_field.data
            add_playlist_to_database(new_playlist_name=new_playlist_name, choosen_users=choosen_users)
        return redirect(url_for('add'))
    
    return render_template('add.html',
                           add_song_form=add_song_form,
                           add_playlist_form=add_playlist_form)


@app.route('/delete', methods=['GET', 'POST'])
@login_required
def delete():
    delete_form = DeleteForm()
    song_id_to_delete = request.form.get('song_id')
    playlist_id_to_delete = request.form.get('playlist_id')

    if request.method=='POST':
        if song_id_to_delete: 
            delete_song_from_database(song_id_to_delete)
        elif playlist_id_to_delete: 
            delete_playlist_from_database(playlist_id_to_delete)
        return redirect(url_for('delete'))

    return render_template('delete.html',
                            playlists=Playlist.query.all(), 
                            songs=Song.query.all(),
                            delete_form=delete_form)


@app.errorhandler(404) 
def not_found(e): 
  logging.info(f'Error occured: {e}')
  return render_template('error404.html') 


@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('login'))