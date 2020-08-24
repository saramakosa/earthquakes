import sqlite3
import argparse
import os
import random
import hashlib

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


def add_user(u, p):
    """Add a new user to the database

    :param u: username
    :type u: string
    :param p: password
    :type p: string
    """

    global conn
    global cursor
    salt = random.randint(1, 10000)
    p = str(salt) + p
    digest = hashlib.sha256(p.encode('utf-8')).hexdigest()
    # if the user already exists, replace its password and salt
    cursor.execute("INSERT OR REPLACE INTO users VALUES (?,?,?)",
                   (u, digest, salt))
    conn.commit()


def remove_user(u):
    """Remove a user from the database

    :param u: username
    :type u: string
    """
    global conn
    global cursor
    cursor.execute("DELETE FROM users WHERE username = ?", (u,))
    conn.commit()


def get_users():
    """Get all the existing users

    :return: list of existing users
    :rtype: list of existing users
    """
    global conn
    global cursor
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    if len(users) > 0:
        return users
    return False


def parse_arguments():
    parser = argparse.ArgumentParser(description="Add users / Remove users")
    parser.add_argument("-a", help="Add username '-u' with password '-p'",
                        action="store_true")
    parser.add_argument("-r", help="Remove username '-u' with password '-p'",
                        action="store_true")
    parser.add_argument("-show", help="Show all existing users",
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
    # If the user tries to add and remove at the same time
    if args.a and args.r:
        print("Incompatible actions, please choose only one!")
        exit()
    # If the user wants to add another user
    if args.a:
        # if the password is not given
        if not args.password:
            print("Please choose a password as well!")
            exit()
        else:
            add_user(args.username, args.password)
    # If the user wants to remove another user
    if args.r:
        remove_user(args.username)
    # Show all the users in the database if needed
    if args.show:
        print('Retrieving all existing users...')
        users = get_users()
        if users:
            for i in range(len(users)):
                print('username: ' + users[i][0], '\tpassword: ' + users[i][1])
        else:
            print("No users found")
