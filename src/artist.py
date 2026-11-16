from data import database

class Artist:
    def __init__(self, id, name):
        self.__id = id
        self.__name = name
        self.__nomembers = database.read_record("artists", "id", id)[0][2]

def create_artist(name:str, no_members:int):
    exists = len(database.read_record("artists", "name", name))
    
    if not exists:
        database.write_record("artists", name=name, no_members=no_members)
    else:
        raise Exception("Artist name already exists")


def link_user(user_id:int, artist_id:int):
    duplicate = False
    existing = database.read_record("artistUsers", "artist_id", artist_id)
    for record in existing:
        if record[1] == user_id:
            duplicate = True

    if not duplicate:
        database.write_record("artistUsers", artist_id=artist_id, user_id=user_id)