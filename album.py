import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    '''Описывает структуру таблиц album для хранения музыкальной библиотеки'''
    __tablename__ = "album"
    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    '''Устанавливает соединение к БД, создает таблицы если их нет, возвращает объект сессии'''
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find(artist):
    '''Находит все альбомы по заданному artist'''
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def save_album(album_data):
    '''Сохраняет в БД полученные данные'''
    session = connect_db()
    album = Album(year=int(album_data["year"]), artist=album_data["artist"], genre=album_data["genre"], album=album_data["album"])
    session.add(album)
    session.commit()

def find_conflict(album_data):
    '''Ищет в БД одноименные альбомы, критерий совпадения: по артисту и названию альбома'''
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == album_data["artist"] and Album.album == album_data["album"]).all()
    if len(albums) > 0:
        return False
    else:
        return True
