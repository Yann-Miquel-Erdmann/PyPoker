import hashlib

def encrypt(text): # Fonction qui va servir à crypter les mots de passes
    return hashlib.sha256(text.encode("utf-8")).hexdigest() # Crypte le text en sha256
