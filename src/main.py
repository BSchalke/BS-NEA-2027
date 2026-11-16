from data import database
import user, venue, artist

database.load_database()
try:
    user.create_account("Ben", "ThisIsAPassword!")
    user.create_account("test_user", "12345")
except Exception:
    pass

current_user = user.load_user("Ben")
print(current_user.get_status())
current_user.login("ThisIsAPassword!")
print(current_user.get_status())

"""
password1 = "hello123"
password2 = "different456"
test_salt = "ExampleSalt12345"

hash1, _ = user.myhash(password1, salt=test_salt)
hash2, _ = user.myhash(password2, salt=test_salt)

print("Hash 1:", hash1)
print("Hash 2:", hash2)
print("Collision:", hash1 == hash2)
"""