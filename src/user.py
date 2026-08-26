import secrets
import string
from data import database

#Algorithm I made to demonstrate a couple different techniques used in hashing algorithms, used for passwords in this project, NOT SECURE FOR REAL USES
def myhash(plaintext, salt_size = 16, repeats = 1000, salt = None):
    if salt == None:
        salt = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(salt_size)) #Generates a salt containing ascii letters and digits as a string

    input_bytes = plaintext.encode("utf-8") + salt.encode("utf-8") #Combines the bytes of the user password and the salt

    state = 0
    for num in range(repeats): #Repeats a number of times defined in the arguments
        for byte in input_bytes:
            state ^= byte
            state = (state * 56) & 0xFFFFFFFF #Multiplied by arbetrary constant and constrained to 32 bits
        state ^= num

    return state, salt

#Creates a user account and stores data in users table in database
def create_account(username, password):
    exists = len(database.read_record("users", "username", username))

    #If there is no existing user with that username, a new account is created
    if not exists:
        password_hash, salt = myhash(password)
        database.write_record("users", username=username, password_hash=password_hash, salt=salt)
    else:
        raise Exception("Username already exists")

#Verifies a user to be logged in, returns True or False if they can be logged in
def login(username, password):
    user_data = database.read_record("users", "username", username)
    exists = len(user_data)
    user_data = user_data[0]

    if exists:
        entered_password_hash = myhash(password, salt=user_data[3])[0] #Given password is hashed with the salt stored in the database record
        if entered_password_hash == user_data[2]: #If hash matches the hash stored in the database
            return True
        else:
            return False
    else:
        raise Exception("Username does not exist, enter existing username or create an account")
