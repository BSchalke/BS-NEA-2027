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
    password_hash INT NOT NULL,
    salt text NOT NULL
);
'''
CREATE_VENUES = '''
CREATE TABLE IF NOT EXISTS venues (
    id INTEGER PRIMARY KEY,
    name text NOT NULL,
    capacity INT NOT NULL
);
'''
CREATE_ARTISTUSERS = '''
CREATE TABLE IF NOT EXISTS artistUsers (
    artist_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artists (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
);
'''
CREATE_VENUEUSERS = '''
CREATE TABLE IF NOT EXISTS venueUsers (
    venue_id INT NOT NULL,
    user_id INT NOT NULL,
    FOREIGN KEY (venue_id) REFERENCES venues (id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
);
'''
CREATE_EVENTS = '''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    venue_id INT NOT NULL,
    date text NOT NULL,
    door_time text NOT NULL,
    FOREIGN KEY (venue_id) REFERENCES venues (id) ON DELETE CASCADE ON UPDATE CASCADE
);
'''
CREATE_EVENTARTISTS = '''
CREATE TABLE IF NOT EXISTS eventArtists (
    artist_id INT NOT NULL,
    event_id INT NOT NULL,
    FOREIGN KEY (artist_id) REFERENCES artists (id) ON DELETE CASCADE ON UPDATE CASCADE
    FOREIGN KEY (event_id) REFERENCES events (id) ON DELETE CASCADE ON UPDATE CASCADE
);
'''

def load_database(): #Creates the database and tables if it does not already exist
    with sqlite3.connect(DB_PATH) as conn:
        print("Opened database succesfully")
        cursor = conn.cursor()

        #Create all tables
        cursor.execute(CREATE_ARTISTS)
        cursor.execute(CREATE_USERS)
        cursor.execute(CREATE_VENUES)
        cursor.execute(CREATE_ARTISTUSERS)
        cursor.execute(CREATE_VENUEUSERS)
        cursor.execute(CREATE_EVENTS)
        cursor.execute(CREATE_EVENTARTISTS)

        conn.commit()

    print("Database successfully loaded")

#Executes any SQL query passed in, with error handling
def execute_query(query:str):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            execute = cursor.execute(query)
            return execute
    except Exception as e:
        raise e

#Write a new record to a table in the database
def write_record(table:str, **data:str): #Uses **kwargs to take in all the data needed for the record with column names and values
    #Splits the data into columns and values, formating each one as a tuple
    columns = str(tuple(data.keys()))
    values = str(tuple(data.values()))
    execute_query(f'''
            INSERT INTO {table}{columns}
            VALUES{values};
            ''')

#Removes a specific record or group of records based on an identifier using a WHERE statement
def remove_record(table:str, id_name:str, id_value):
    execute_query(f'''
            DELETE FROM {table}
            WHERE {id_name} = {id_value};
            ''')

def edit_record(table:str, id_name:str, id_value, column_name:str, new_value):
    execute_query(f'''
            UPDATE {table}
            SET {column_name} = {new_value}
            WHERE {id_name} = {id_value};
            ''')

def read_record(table:str, id_name:str, id_value):
    result = list(execute_query(f'''
            SELECT *
            FROM {table}
            WHERE {id_name} = "{id_value}";
            '''))

    return result