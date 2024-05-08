import pymysql.cursors

from log_config import setup_logging

from rich.console import Console
from rich.traceback import install

install()
console = Console()

# Customize traceback
install(show_locals=True)  # Show local variables in tracebacks


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

    def fetch_all(self, table):
        query = f"SELECT * FROM {table};"
        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    def fetch_one(self, table):
        query = f"SELECT * FROM {table};"
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
        values = list(data.values())
        val_params = ""
        for val in values:
            val_params += f"'{val}',"
        val_params = val_params[:-1]

        query = f"INSERT INTO {table} ({columns}) VALUES {values};"
        print(f"Query: {query}")

        connection = self.get_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                return {
                    "success": True,
                    "query": query,
                    "Rows Affected": cursor.rowcount,
                }
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
    conn = MysqlDb(db_config)
    print(conn.fetch_all("Album"))
    print(conn.get_max_id("Album", "AlbumId") + 1)
