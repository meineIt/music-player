from app import app, db
from models import Playlist, Song, User
import logging

logging.basicConfig(level=logging.INFO)


def register_new_user(name, email, password):
    
    with app.app_context():
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)

        try:    
            db.session.commit()
            logging.info('user registered successfully')
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error occured while registering new user: {e}')
        finally:
            db.session.close()


def add_playlist_to_database(new_playlist_name, choosen_users):

    with app.app_context():
        new_playlist = Playlist(name=new_playlist_name)
        db.session.add(new_playlist)

        for user in choosen_users:
            user_in_session = db.session.query(User).get(user.id)
            if user_in_session:
                user_in_session.playlists.append(new_playlist)
            else: 
                db.session.add(user)
                user_in_session.playlists.append(new_playlist)
        
        try:    
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error occured while adding playlist: {e}')
        finally:
            db.session.close()


def add_song_to_database(artist, title, url, grade, playlist_id):
    
    with app.app_context():
        new_song = Song(artist=artist, title=title, url=url, grade=grade, playlist_id=playlist_id)
        db.session.add(new_song)
        try:    
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error occured while adding song: {e}')
        finally:
            db.session.close()


def delete_song_from_database(song_id_to_delete):
    song_to_delete = Song.query.get(song_id_to_delete)
    
    if song_to_delete:
        db.session.delete(song_to_delete)
    
    try: 
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error occured while deleting song from database: {e}')
    finally:
        db.session.close()


def delete_playlist_from_database(playlist_id_to_delete):
    playlist_to_delete = Playlist.query.get(playlist_id_to_delete)

    if playlist_to_delete:
        db.session.delete(playlist_to_delete)
    
    try: 
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logging.error(f'Error while deleting playlist from database: {e}')
    finally:
        db.session.close()