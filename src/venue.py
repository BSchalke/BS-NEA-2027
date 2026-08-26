from data import database

def create_venue(name:str, capacity:int, lat_coord:float, long_coord:float):
    exists = len(database.read_record("venues", "name", name))

    if not exists:
        database.write_record("venues", name=name, capacity=capacity, lat_coord=lat_coord, long_coord=long_coord)
    else:
        raise Exception("Venue name already exists")


def link_user(user_id:int, venue_id:int):
    duplicate = False
    existing = database.read_record("venueUsers", "venue_id", venue_id)
    for record in existing:
        if record[1] == user_id:
            duplicate = True

    if not duplicate:
        database.write_record("venueUsers", venue_id=venue_id, user_id=user_id)