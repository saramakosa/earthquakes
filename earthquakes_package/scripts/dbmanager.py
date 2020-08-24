import sqlite3
import os

conn = None
cursor = None
db_abs_path = 'earthquakes_package/scripts/database.db'


def open_and_create(db_path):
    """Connect to sqlite database given the path
    
    :param db_path: The path to the database file
    :type db_path: string
    """
    global conn
    global cursor
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users")
    # if the table does not exist create one
    except sqlite3.OperationalError:
        create_users_table()


def create_users_table():
    """Create table for users according to the defiend schema"""

    global conn
    global cursor
    # Create table, allow user names for max 20 chars and passwords 32 (hash)
    cursor.execute('''CREATE TABLE users
                   (username CHARACTER(20) NOT NULL,
                    password CHARACTER(32) NOT NULL,
                    salt SMALLINT NOT NULL,
                    PRIMARY KEY (username))''')
    

if __name__ == "__main__":
    # get the correct path based on the folder where the script is invoked in
    db_path = os.path.abspath(os.path.join(os.getcwd(), db_abs_path))
    open_and_create(db_path)