import sqlite3
from pathlib import Path

#Sets the relative path of the database
DATA_DIR = Path(__file__).parent
DB_PATH = DATA_DIR / "gig_organiser.db"

#SQL commands to create database tables if they do not already exist
CREATE_ARTISTS = '''
CREATE TABLE IF NOT EXISTS artists (
    id INTEGER PRIMARY KEY, 
    name text NOT NULL, 
    no_members INT NOT NULL
);
'''
CREATE_USERS = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username text NOT NULL,
    role text NOT NULL,
    password_hash text NOT NULL
);
'''
CREATE_VENUES = '''
CREATE TABLE IF NOT EXISTS venues (
    id INTEGER PRIMARY KEY,
    name text NOT NULL,
    capacity INT NOT NULL
);
'''


def load_database(): #Creates the database and tables if it does not already exist
    with sqlite3.connect(DB_PATH) as conn:
        print("Opened database succesfully")
        cursor = conn.cursor()
        cursor.execute(CREATE_ARTISTS)
        cursor.execute(CREATE_USERS)
        cursor.execute(CREATE_VENUES)
        conn.commit()

    print("Database successfully loaded")