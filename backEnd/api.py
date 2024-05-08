from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import RedirectResponse
import pymysql.cursors
import uvicorn
from initScripts.mysqlDb import MysqlDb
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse

from log_config import setup_logging

from rich.console import Console
from rich.traceback import install

from secrets import token_hex

import hashlib


install()
console = Console()

import os
os.chdir("...")

# Customize traceback
install(show_locals=True)  # Show local variables in tracebacks


"""
Track Title: New Noise
Artist: Refused
Album: The Shape Of Punk To Come
Track Number: 6
Year: 1998
File Path: ./data/Refused-The_Shape_Of_Punk_To_Come/Refused - The Shape Of Punk To Come - 06 New Noise.mp3

- Check if album exists.
- If album does not exist, create album and get album id.
- Check if artist exists.
- If artist does not exist, create artist and get artist id.- Check if track exists.
- If track does not exist, create track and get track id.

"""


# Optional[str] = None


class Album(BaseModel):
    title: str
    artist_id: int
    genre_id: Optional[int] = None
    release_date: int


class Artist(BaseModel):
    name: str
    genre_id: Optional[int] = None


class Playlist(BaseModel):
    user_id: int
    title: str
    creation_date: Optional[int] = None


class PlayListSongs(BaseModel):
    play_list_id: int
    track_id: int


class Track(BaseModel):
    title: Optional[str] = None
    artist_id: int
    album_id: int
    duration: Optional[int] = 0
    release_date: Optional[int] = None


class User(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    username: Optional[str] = None
    email: str
    password: str

class Login(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: str

db_config = {
    "host": "localhost",
    "user": "musicApp",
    "password": "musicMakesYouWannaDance",
    "db": "musicApp",  # Replace with your actual database name
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}

# conn = pymysql.connect(**db_config)

"""
methods to do checks for dependancy's

since both Albums and Tracks require artistId we should start by getting artistId
then do albums since tracks require albumId

def insert_artist(self, name, genre):
        max_artist_id = get_max_id("Album", AlbumId)
        artist_id = max_artist_id + 1
        query = f"INSERT INTO Artist (ArtistID, Name, Genre) VALUES ('{artist_id}', '{name}', '{genre}');"
        self.cursor.execute(query)
        self.connection.commit()
        print("Artist inserted successfully!")
        return artist_id

def insert_album(self, title, artist_id, genre, release_date):
        query = f"INSERT INTO Album (Title, ArtistID, Genre, ReleaseDate) VALUES ('{title}', '{artist_id}', '{genre}', '{release_date}');"
        cursor.execute(query)
        connection.commit()
        print("Album inserted successfully!")

def insert_track(self, title, artist_id, album_id, duration, release_date):
        query = f"INSERT INTO Track (Title, ArtistID, AlbumID, Duration, ReleaseDate) VALUES ('{title}', '{artist_id}', '{album_id}', '{duration}', '{release_date}');"
        self.cursor.execute(query)
        self.connection.commit()
        print("Track inserted successfully!")

"""


def check_Exists(table, key, value):
    global conn
    query = f"SELECT * FROM '{table}' WHERE '{key}' = ''{value}'';"
    print(query)

    try:
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            return cursor.rowcount
    finally:
        conn.close()
        return 0


# Initialize the FastAPI app
app = FastAPI()

# Setup logging
logger = setup_logging()


# Instantiate the database helper
db = MysqlDb()


@app.get("/")
async def docs_redirect():
    """Api's base route that displays the information created above in the ApiInfo section."""
    return RedirectResponse(url="/docs")

@app.get("/test_exists")
def test_exists(table: str, key: str, value: str):
    """Fetch a single artist by their ID, or all artists if no ID is provided."""
    result = check_Exists(table, key, value)

    if result > 0:
        return f"'{key}' '{value}' exists in '{table}'"
    else:
        return f"'{key}' '{value}' does not exist in '{table}'"


# Define routes for each table
@app.get("/albums/'{album_id}'", tags=["Album"])
def get_album(album_id: int = None):
    """Fetch a single album by its ID, or all albums if no ID is provided."""
    if album_id:
        album = db.fetch_by_id("Album", album_id)
        if album:
            return album
        raise HTTPException(status_code=404, detail="Album not found")
    return db.fetch_all("Album")


@app.get("/artists/", tags=["Artist"])
def get_artist(artist_id: int = None):
    """Fetch a single artist by their ID, or all artists if no ID is provided."""
    if artist_id:
        artist = db.fetch_by_id("Artist", "ArtistID", artist_id)
        if artist:
            return artist
        raise HTTPException(status_code=404, detail="Artist not found")
    return db.fetch_all("Artist")


@app.get("/playlists/'{playlist_id}'", tags=["Playlist"])
def get_playlist(playlist_id: int = None):
    """Fetch a single playlist by its ID, or all playlists if no ID is provided."""
    if playlist_id:
        playlist = db.fetch_by_id("Playlist", playlist_id)
        if playlist:
            return playlist
        raise HTTPException(status_code=404, detail="Playlist not found")
    return db.fetch_all("Playlist")


@app.get("/tracks/'{track_id}'", tags=["Track"])
def get_track(track_id: int = None):
    """Fetch a single track by its ID, or all tracks if no ID is provided."""
    if track_id:
        track = db.fetch_by_id("Track", track_id)
        if track:
            return track
        raise HTTPException(status_code=404, detail="Track not found")
    return db.fetch_all("Track")


@app.get("/users/", tags=["User"])
def get_user(user_id: int = None):
    """Fetch a single user by their ID, or all users if no ID is provided."""
    if user_id:
        user = db.fetch_by_id("User", user_id)
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")
    return db.fetch_all("User")

@app.get("/searchTrack")
def search(key:str):
    query = f"SELECT * FROM `Track` WHERE name LIKE '%{key}%';"
    response = db.run_query(query, True)

    return response

@app.get("/searchAlbum")
def search(key:str):
    query = f"SELECT * FROM `Album` WHERE name LIKE '%{key}%';"
    response = db.run_query(query, True)

    return response

@app.get("/searchArtist")
def search(key:str):
    query = f"SELECT * FROM `Artist` WHERE name LIKE '%{key}%';"
    print(query)
    response = db.run_query(query, True)

    return response

@app.get("/stream/{filename}")
async def stream_music(filename: str):
    file_path = os.path.join("assets", "music", filename)
    
    # Ensure the file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine the content type based on the file extension
    content_type = "audio/mpeg"  # Default for MP3 files
    if filename.lower().endswith(".flac"):
        content_type = "audio/flac"

    def iterfile():
        with open(file_path, "rb") as file:
            while chunk := file.read(1024 * 1024):  # Read in chunks of 1 MB
                yield chunk

    return StreamingResponse(iterfile(), media_type=content_type)


@app.get("/image/{filename}")
async def stream_image(filename: str):
    file_path = os.path.join("assets", "albumCovers", filename)
    
    # Ensure the file exists
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    # Determine the content type based on the file extension
    content_type = "image/jpeg"  # Default for JPG files
    if filename.lower().endswith(".png"):
        content_type = "image/png"

    def iterfile():
        with open(file_path, "rb") as file:
            while chunk := file.read(1024 * 1024):  # Read in chunks of 1 MB
                yield chunk

    return StreamingResponse(iterfile(), media_type=content_type)


#########################
# POST METHODS
#########################

"""
@app.post("/album", tags=["Album"])
def post_album(self, album: Album, data):
    Insert a new album into the database.
    max_album_id = self.get_max_id("Album", "AlbumID")
    album_id = max_album_id + 1
    query = f"INSERT INTO Album (AlbumID, Title, ArtistID, Genre, ReleaseDate) VALUES ('{album_id}', '{album.title}', '{album.artist_id}', '{album.genre}', '{album.release_date}');"
    self.cursor.execute(query)
    self.connection.commit()
    # print("Album inserted successfully!")
    if self.cursor.rowcount > 0:
        return {"success": True}
    else:
        return {"success": False}
    # return db.post_data("Album", data)
"""


@app.post("/album", tags=["Album"])
def post_album(album: Album):

    album = {
       "title": album.title,
       "artist_id": album.artist_id,
       "genre_id": album.genre_id,
       "release_date": album.release_date,
    }

    result = db.post_data("Album", album)

    return result

"""
@app.post("/track", tags=["Track"])
def insert_track(self, track: Track):
    # check for artist and check for album
    artist_exists = conn.fetch_by_id("Artist", "ArtistID", track.artist_id)
    album_exists = conn.fetch_by_id("Album", "AlbumID", track.album_id)
    max_track_id = self.get_max_id("Track", "TrackID")
    track_id = max_track_id + 1

    query = f"INSERT INTO Track (TrackID, Title, ArtistID, AlbumID, Duration, ReleaseDate) VALUES ('{track.title}', '{track_id}', '{track.album_id}', '{track.duration}', '{track.release_date}');"
    self.cursor.execute(query)
    self.connection.commit()
    print("Track inserted successfully!")
    if self.cursor.rowcount > 0:
        return {"success": True}
    else:
        return {"success": False}
"""
@app.post("/track", tags=["Track"])
def insert_track(track: Track):
    
    track = {
        "title": track.title,
        "artist_id": track.artist_id,
        "album_id": track.album_id,
        "duration": track.duration,
        "release_date": track.release_date
    }

    result = db.post_data("Track", track)

    return result


# @app.post("/artist", tags=["Artist"])
# def insert_artist(artist: Artist):
#     max_artist_id = self.get_max_id("Artist", "ArtistID")
#     artist_id = max_artist_id + 1
#     query = f"INSERT INTO Artist (ArtistID, Name, Genre) VALUES ('{artist_id}', '{artist.name}', '{artist.genre}');"
#     print(query)
#     self.cursor.execute(query)
#     self.connection.commit()
#     if self.cursor.rowcount > 0:
#         return {"success": True}
#     else:
#         return {"success": False}


@app.post("/artist", tags=["Artist"])
def insert_artist(artist: Artist):

    # max_artist_id = db.get_max_id("Artist", "ArtistID")
    # artist_id = max_artist_id + 1

    artist = {
        "name": artist.name,
        "genre_id": artist.genre_id,
    }

    result = db.post_data("Artist", artist)

    return result


@app.post("/playlist", tags=["Playlist"])
def insert_playlist(playlist: Playlist):
    max_playlist_id = db.get_max_id("Playlist", "PlaylistID")
    play_list_id = max_playlist_id + 1
    query = f"INSERT INTO Playlist (PlaylistID ,UserID, Title, Genre) VALUES ('{play_list_id}', '{playlist.artist_id}', '{playlist.name}', '{playlist.genre}');"

# @app.post("/user")
#   user_id: int
#  username: str
# email: str
# password: str


@app.post("/register", tags=["User"])
def post_user(user: User):
    """
        Insert a new user into the database.
    ```
    {
      "first_name": "",
      "last_name": "",
      "username": "",
      "email": "",
      "password": ""
    }
    ```
    """
    # logger("running register")
    max_user_id = db.get_max_id("User", "user_id")
    if not max_user_id:
        max_user_id = 0
    print(f"max user id: {max_user_id}")
    print(f"user: {user}")
    user_id = int(max_user_id) + 1
    encrypted = hashlib.sha256(user.password.encode()).hexdigest()

    query = f"INSERT INTO `User` (`user_id`, `first_name`, `last_name`, `user_name`, `email`, `password`) VALUES ('{user_id}', '{user.first_name}', '{user.last_name}', '{user.username}', '{user.email}', '{encrypted}');"
    # query = f"INSERT INTO Album (AlbumID, Title, ArtistID, Genre, ReleaseDate) VALUES ('{album_id}', '{album.title}', '{album.artist_id}', '{album.genre}', '{album.release_date}');"
    print(query)
    response = db.run_query(query, True)

    return response

@app.post("/login", tags=["User"])
def post_login(login: Login):
    """
        Insert a new user into the database.
    ```
    {
      "username": "lucygirl",
      "password": "lucy"
    }
    or
       {
      "email": "lucy@bob.com",
      "password": "lucy"
    }
    angel@badill.com
    passwordpasswordpassword

    hash_result = hashlib.sha256('lucy'.encode()).hexdigest() = dc99e9aa86fab83a062cff5e0808391757071a3d5dbb942802d5f923aaead3b4
    SELECT SHA2('lucy', 256); = 'dc99e9aa86fab83a062cff5e0808391757071a3d5dbb942802d5f923aaead3b4'
    UPDATE `users` SET `password` = SHA2('bob', 256) WHERE `user_id` = 52;
    ```
    """
    info = dict(login)
    email = info.get("email", None)
    username = info.get("user_name", None)
    password = info.get("password", None)

    password = hashlib.sha256(password.encode()).hexdigest()

    print(f"{email}:{username}:{password}")

    if email:
        user_exists = db.exists("User", "email", email)
    else:
        user_exists = db.exists("User", "user_name", username)

    if user_exists:
        query = f"SELECT * FROM `User` WHERE `password` = '{password}';"
        print(query)
        response = db.run_query(query, False)
        print(response)

        print(f"inpassword: {password} == {response['data'][0]['password']}")
        if response["success"] and response["data"][0]["password"] == password:
            return {"success": True}

    return {"success": False}

@app.post("/uploadAlbumCover")
async def upload(file:UploadFile = File(...)):
    allowed_extensions = {'png', 'jpg'}
    file_ext = file.filename.split(".")[-1]
    if file_ext.lower() not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Only PNG and JPG file formats are allowed.")
    
    file_name = token_hex(10)
    file_path = f"assets/albumCovers/{file_name}.{file_ext}"
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    return JSONResponse(content={"success": True, "file_path": file_path, "message": "File Uploaded Successfully"})

@app.post("/uploadSong")
async def upload(file:UploadFile = File(...)):
    allowed_extensions = {'mp3', 'flac'}
    file_ext = file.filename.split(".")[-1]
    if file_ext.lower() not in allowed_extensions:
        raise HTTPException(status_code=400, detail="Only MPG and FLAC file formats are allowed.")
    
    file_name = token_hex(10)
    file_path = f"assets/music/{file_name}.{file_ext}"
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    return JSONResponse(content={"success": True, "file_path": file_path, "message": "File Uploaded Successfully"})

if __name__ == "__main__":
    # gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:main --bind 0.0.0.0:8000 --keyfile=./key.pem --certfile=./cert.pem

    # uvicorn.run("api:app", host="kidsinvans.fun", port=8080, log_level="debug", reload=True)

    uvicorn.run(
        "api:app",
        host="0.0.0.0",  # Use 0.0.0.0 to bind to all network interfaces
        #port=443,  # Standard HTTPS port
        port=8889,  # Standard HTTPS port
        log_level="debug",
        # ssl_keyfile="/etc/letsencrypt/archive/kidsinvans.fun/privkey1.pem",
        # ssl_certfile="/etc/letsencrypt/archive/kidsinvans.fun/fullchain1.pem",
        reload=True,
    )


# def fill_Artist(self, name, genre):
#     max_artist_id = self.get_max_id("Album", AlbumID)
#     artist_id = max_artist_id + 1
#     query = f"INSERT INTO Artist (ArtistID, Name, Genre) VALUES ('{artist_id}', '{name}', '{genre}');"
#     self.cursor.execute(query)
#     self.connection.commit()
#     print("Artist inserted successfully!")
#     return artist_id


# fill_Artist("Refused", "Hardcore Punk")
