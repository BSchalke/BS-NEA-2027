import secrets
import string

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