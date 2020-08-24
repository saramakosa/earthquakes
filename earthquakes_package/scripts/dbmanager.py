import sqlite3
import argparse
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
    # Create table with usernam, password and salt
    cursor.execute('''CREATE TABLE users
                   (username CHARACTER(256) NOT NULL,
                    password CHARACTER(256) NOT NULL,
                    salt CHARACTER(256) NOT NULL,
                    PRIMARY KEY (username))''')
    
    
def parse_arguments():
    parser = argparse.ArgumentParser(description="Add users / Remove users")
    parser.add_argument("-a", help="Add username '-u' with password '-p'",
                        action="store_true")
    parser.add_argument("-r", help="Remove username '-u' with password '-p'",
                        action="store_true")
    parser.add_argument('-username', help="add a username name",
                        required=True, default=None)
    parser.add_argument('-password', help="the username password",
                        required=False, default=None)
    parser.add_argument("--version", action="version", version="1.0")
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    # get the correct path based on the folder where the script is invoked in
    db_path = os.path.abspath(os.path.join(os.getcwd(), db_abs_path))
    open_and_create(db_path)
    args = parse_arguments()
    print(args)