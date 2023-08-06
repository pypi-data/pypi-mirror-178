import random
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ß!"§$%&/()=?+*~#-_.:,;öäüy<>|^° '
alphabet_len = len(alphabet)

def verschlüsseln(string, keyFile):
    key = open(f"{keyFile}", "r").read().split()
    new_string = ""
    for i in range(len(string)):
        position = alphabet.find(string[i])
        neuePosition = (position + int(f"{key[i]}")) % alphabet_len
        neuesZeichen = alphabet[neuePosition]
        new_string += neuesZeichen
    return new_string
def entschlüsseln(string, keyFile):
    key = open(f"{keyFile}", "r").read().split()
    new_string = ""
    for i in range(len(string)):
        position = alphabet.find(string[i])
        neuePosition = (position + int(f"-{key[i]}")) % alphabet_len
        neuesZeichen = alphabet[neuePosition]
        new_string += neuesZeichen
    return new_string
def generate_key(keyFile):
    key_string = ""
    for i in range(1, 9999):
        key_string += f"{random.randint(1, 9999)} "
    with open(f"{keyFile}", "w") as key:
        key.write(f"{key_string}")

if __name__ == "__main__":
    print("Crypti v1\n\n")
    print("Die folgenden Modi existieren:\n1. Schlüssel generieren \n2. Nachrichten verschlüsseln \n3. Nachrichten entschlüsseln")
    mode = input("Welchen Modus wählst du (1, 2 oder 3)?: ")
    if mode == "1":
        keyFile = input("Schlüsseldatei-Name: ")
        generate_key(keyFile)
        print(f"Key generated!\nFilename: {keyFile}")
    elif mode == "2":
        keyFile = input("Schlüsseldatei-Name: ")
        message = input("Zu verschlüsselnde Nachricht:")
        new_message = verschlüsseln(message, keyFile)
        print(f"Deine verschlüsselte Nachricht lautet: {new_message}")
    elif mode == "3":
        keyFile = input("Schlüsseldatei-Name: ")
        message = input("Zu entschlüsselnde Nachricht: ")
        new_message = entschlüsseln(message, keyFile)
        print(f"Deine entschlüsselte Nachricht lautet: {new_message}")
