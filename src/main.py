from data import database
import user, venue, artist

#database.load_database()
#user.create_account("Ben", "ThisIsAPassword!")
print(user.login("Ben", "ThisIsAPassword!"))

#venue.create_venue("New Cross Inn", 250, 1.23, 2.34)
venue.link_user(1, 1)

#artist.create_artist("Gutalax", 4)
#artist.create_artist("Party Cannon", 5)
artist.link_user(1, 2)