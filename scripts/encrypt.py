from cryptography.fernet import Fernet

def loadKey():
    key = open("./data/universal.key","rb").read()
    return key

def Encrypt(secret):
    key = loadKey()
    encodeSecret = secret.encode()
    fer  = Fernet(key)
    return fer.encrypt(encodeSecret)
