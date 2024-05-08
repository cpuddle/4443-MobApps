import json
from rich import print
import pymysql.cursors

artists = [
    ("AC/DC", "Heavy Metal"),
    ("Arcade Fire", "Indie Rock"),
    ("Arctic Monkeys", "Indie Rock"),
    ("Ben Harper", "Folk Rock"),
    ("Bill Withers", "Soul"),
    ("Billy Bragg & Wilco", "Alternative Rock"),
    ("Black Sabbath", "Hard Rock"),
    ("Blitzen Trapper", "Alternative Country"),
    ("Bob Dylan", "Folk Rock"),
    ("Bob Marley", "Reggae"),
    ("Bryan Adams", "Rock"),
    ("Cat Stevens", "Folk"),
    ("Chvrches", "Synthpop"),
    ("Coldplay", "Alternative Rock"),
    ("Conor Oberst", "Indie Folk"),
    ("Dave Matthews", "Rock"),
    ("David Bowie", "Rock"),
    ("DeVotchKa", "Indie Folk"),
    ("Dispatch", "Indie Folk"),
    ("Don McLean", "Folk Rock"),
    ("Donovan", "Folk"),
    ("Elton John", "Pop Rock"),
    ("Elvis Perkins", "Folk"),
    ("Emmylou Harris", "Country"),
    ("Father John Misty", "Indie Folk"),
    ("First Aid Kit", "Folk"),
    ("Florence + The Machine", "Indie Pop"),
    ("Fun", "Indie Pop"),
    ("Gin Blossoms", "Alternative Rock"),
    ("Guns N Roses", "Hard Rock"),
    ("Harry Chapin", "Folk Rock"),
    ("Jack Johnson", "Folk Rock"),
    ("Jason Mraz", "Pop"),
    ("Jimmy Buffett", "Country Rock"),
    ("John Lennon", "Rock"),
    ("John Mellencamp", "Rock"),
    ("Johnny Cash", "Country"),
    ("Journey", "Rock"),
    ("Keane", "Alternative Rock"),
    ("Led Zeppelin", "Rock"),
    ("Lynyrd Skynyrd", "Southern Rock"),
    ("Mason Jennings", "Folk"),
    ("Metallica", "Heavy Metal"),
    ("Michael Jackson", "Pop"),
    ("Miley Cyrus", "Pop"),
    ("Neil Young", "Rock"),
    ("Nirvana ", "Grunge"),
    ("OAR", "Rock"),
    ("Oasis", "Britpop"),
    ("Of Monsters and Men", "Indie Folk"),
    ("Paul Simon", "Folk Rock"),
    ("Pink Floyd", "Rock"),
    ("Queen", "Rock"),
    ("Radiohead", "Alternative Rock"),
    ("Red Hot Chili Peppers", "Alternative Rock"),
    ("Refused", "Hardcore Punk"),
    ("Regina Spektor", "Indie Pop"),
    ("Ricky Nelson", "Rock and Roll"),
    ("She & Him", "Indie Pop"),
    ("Stealers Wheel", "Rock"),
    ("Sublime", "Ska Punk"),
    ("Taylor Swift", "Pop"),
    ("The Avett Brothers", "Folk Rock"),
    ("The Band", "Rock"),
    ("The Beatles ", "Rock"),
    ("The Black Keys", "Rock"),
    ("The Byrds", "Rock"),
    ("The Church", "Alternative Rock"),
    ("The Clash ", "Punk"),
    ("The Cure ", "Post-Punk"),
    ("The Doors ", "Psychedelic Rock"),
    ("The Eagles", "Rock"),
    ("The Killers", "Indie Rock"),
    ("The Kinks", "Rock"),
    ("The Lumineers", "Indie Folk"),
    ("The Ramones ", "Punk"),
    ("The Rolling Stones ", "Rock"),
    ("The Shins", "Indie Rock"),
    ("The Smiths ", "post-Punk"),
    ("The Stooges ", "proto-Punk"),
    ("The Strokes", "Indie Rock"),
    ("The Tallest Man on Earth", "Folk"),
    ("The Velvet Underground ", "Art Rock"),
    ("The White Stripes", "Alternative Rock"),
    ("The Who ", "Hard Rock"),
    ("The Zombies", "Rock"),
    ("Tom Petty", "Rock"),
    ("Tom Waits", "Folk"),
    ("Train", "Pop Rock"),
    ("Vampire Weekend", "Indie Rock"),
    ("Van Morrison", "Rock"),
    ("Violent Femmes", "Alternative Rock"),
    ("Weezer", "Alternative Rock"),
    ("Whitesnake", "Hard Rock"),
    ("Wilco", "Alternative Rock"),
]

# Database connection parameters
db_config = {
    "host": "localhost",
    "user": "musicApp",
    "password": "musicMakesYouWannaDance",
    "db": "musicApp",  # Replace with your actual database name
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor,
}


# Database interaction class
class MysqlDb:
    def __init__(self, **config):
        if not config:
            config = db_config
        self.config = config

    def get_connection(self):
        return pymysql.connect(**self.config)

    def fetch_all(self, table, where=1):
        query = f"SELECT * FROM {table} WHERE {where};"
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    def fetch_by_id(self, table, key, record_id):
        query = f"SELECT * FROM {table} WHERE {key} = {record_id};"
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                return result
        finally:
            connection.close()

    def post_data(self, table, data):
        """
        Inserts data into the specified table.

        Parameters:
        - table (str): The table name.
        - data (dict): A dictionary where keys are column names and values are the data to insert.
        """
        if not data:
            return "No data provided", False

        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        values = tuple(data.values())

        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders});"

        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, values)
                connection.commit()
                return f"Record inserted successfully into {table}.", True
        except pymysql.Error as e:
            return f"An error occurred: {e}", False
        finally:
            connection.close()

    def get_max_id(self, table, idFieldKey="id"):
        """
        Fetches the maximum ID from the specified table.

        Parameters:
        - table (str): The table name.

        Returns:
        - int: The maximum ID found in the table. Returns 0 if the table is empty.
        """

        query = f"SELECT MAX({idFieldKey}) AS max_id FROM {table};"
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                if result["max_id"] is not None:
                    return result["max_id"]
                else:
                    return 0
        except pymysql.Error as e:
            print(f"An error occurred while fetching the max ID: {e}")
            return None
        finally:
            connection.close()


if __name__ == "__main__":
    db = MysqlDb()
    with open("artists2.sql", "w") as f:
        for artist in artists:
            genre = artist[1].replace("-", " ").strip().title()
            result = db.fetch_all("Genre", f"name LIKE '{genre}'")
            # print(f"artist: {artist[0]} genre: {genre} result:{result[0]['genre_id']}")
            query = f"INSERT INTO `Artist` (`name`, `genre_id`) VALUES ('{artist[0]}','{result[0]['genre_id']}');\n"
            f.write(query)
            db.post_data(
                "Artist", {"name": artist[0], "genre_id": result[0]["genre_id"]}
            )
