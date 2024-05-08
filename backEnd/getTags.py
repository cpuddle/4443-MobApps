from mutagen.id3 import ID3
import glob
from initScripts.mysqlDb import MysqlDb
from mutagen.mp3 import MP3

# Instantiate the database helper
db = MysqlDb()


# albums = glob.glob('musicApi/data/albums/*')

# Replace 'example.mp3' with the path to your MP3 file
file_path = "./data/Refused-The_Shape_Of_Punk_To_Come"
tracks = glob.glob(file_path + "/*.mp3")
# Loading the file

for track in tracks:
    # if "06" in track:
    audio = ID3(track)
    # print(dir(audio))
    print("Track Title:", audio.get("TIT2").text[0])
    print("Artist:", audio.get("TPE1").text[0])
    print("Album:", audio.get("TALB").text[0])
    print("Track Number:", audio.get("TRCK").text[0])
    print("Year:", audio.get("TDRC").text[0])
    # print("Genre:", audio.get("TCON").text[0])
    # if "TLEN" in audio:
    #    print("Duration:", audio.get("TLEN").text[0])
    print("File Path:", track)
    # print("")
    mp3data = MP3(track)
    # Audio length in seconds
    print("Duration:", mp3data.info.length)

# audio = ID3(file_path)

# # Accessing tags
# print("Track Title:", audio.get("TIT2").text[0])
# print("Artist:", audio.get("TPE1").text[0])
# print("Album:", audio.get("TALB").text[0])
