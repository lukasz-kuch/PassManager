from cryptography.fernet import Fernet

def loadKey():
    key = open("./data/universal.key","rb").read()
    return key

def Decrypt(encryptSecret):
    key = loadKey()
    fer  = Fernet(key)
    decryptSecret = fer.decrypt(encryptSecret)
    return decryptSecret.decode()
