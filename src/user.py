import secrets
import string
from data import database

class User:
    def __init__(self, id, username):
        self.__id = id
        self.__username = username
        self.__loggedin = False

    #Verifies a user to be logged in, returns True or False if they can be logged in
    def login(self, password):
        user_data = database.read_record("users", "username", self.__username)
        exists = len(user_data)
        user_data = user_data[0]
    
        if exists:
            entered_password_hash = myhash(password, salt=user_data[3])[0] #Given password is hashed with the salt stored in the database record
            if entered_password_hash == user_data[2]: #If hash matches the hash stored in the database
                self.__loggedin = True
                return True
            else:
                return False
        else:
            raise Exception("Username does not exist, enter existing username or create an account")

    def get_status(self):
        return self.__loggedin

#Algorithm I made to demonstrate a couple different techniques used in hashing algorithms, used for passwords in this project, NOT SECURE FOR REAL USES
def myhash(plaintext, salt_size = 16, repeats = 1000, salt = None) -> (int):
    if salt == None:
        salt = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(salt_size)) #Generates a salt containing ascii letters and digits as a string

    input_bytes = plaintext.encode("utf-8") + salt.encode("utf-8") #Combines the bytes of the user password and the salt

    state = 0
    for num in range(repeats): #Repeats a number of times defined in the arguments
        for byte in input_bytes:
            state ^= byte
            #This line with the constant caused an interesting bug, before it had a value of 56 which is divisible by 8 (bits in a byte) which caused collisions when a key was above a certain length. The constant is now prime.
            state = (state * 37) & 0xFFFFFFFF #Multiplied by arbetrary constant and constrained to 32 bits
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

def remove_user(username):
    exists = len(database.read_record("users", "username", username))

    if exists:
        database.remove_record("users", "username", username)
    else:
        raise Exception("User does not exist")


def load_user(username):
    exists = len(database.read_record("users", "username", username)) == 1

    if exists:
        user_id = database.read_record("users", "username", username)[0][0]
        current_user = User(user_id, username)
        return current_user
    else:
        raise Exception("No such username exists")