#!/usr/local/bin/python

'''
ALL THE FILES MUST BE IN THE SAME DIRECTORY.

password_manager.py creates a master password to store in files accounts with
their encrypted password. You can add and view accounts and their passwords
only if you know the master password. If no accounts have been stored yet, the
first master password entered will be the one decrypting the accounts's
passwords if at least one is added with this new password.

#TODO ADD CONFIRMATION OF FIRST TIME WRITING MASTER PASSWORD
'''

import base64
import fileinput
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)


def load_key():
    file = open("key.key", "rb")
    key = file.read()
    file.close()
    return key


def write_salt():
    salt = os.urandom(16)
    with open("salt.txt", "wb") as salt_file:
        salt_file.write(salt)


def load_salt():
    file_salt = open("salt.txt", "rb")
    salt = file_salt.read()
    file_salt.close()
    return salt


def view(fernet):
    with open("password.txt", "r") as f:
        for line in f.readlines():
            data = line.rstrip()
            user, passw = data.split("|")
            print("User:", user, "| Password:",
                  (fernet.decrypt(passw.encode())).decode())


def verif(fernet):
    with open("password.txt", "r") as f:
        for line in f.readlines():
            data = line.rstrip()
            passw = data.split("|")[1]
            fernet.decrypt(passw.encode()).decode()
        return


def add(fernet):
    name = input("Username: ")
    with open("password.txt", "r") as f:
        for line in f.readlines():
            data = line.rstrip()
            user = data.split("|")[0]
            if name == user:
                print('This username already exists.')
                print('Please enter another username.')
                add(fernet)
                return
    pwd = input("Password: ")

    # "a" add to the end of the existing line or create a new file if it doesn't exist
    with open("password.txt", "a") as f:
        f.write(name + "|" + fernet.encrypt(pwd.encode()).decode() + "\n")


def find_key(pwd):
    salt = load_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(pwd.encode()))
    return key


def change(fernet, user_input):
    print("not done yet")
    # with open("password.txt", "r") as f:
    #     for line in f.readlines():
    #         data = line.rstrip()
    #         user = data.split("|")[0]
    #         if user == user_input:
    #             print("EVERYTHING GOOD HERE")
    #             change_pass(fernet, user_input)
    #             return
    # answer = input('Please enter a valid username here or type "stop": ')
    # if answer == "stop":
    #     return
    # else:
    #     change(fernet, answer)


# TODO: get lines from file, then reopen and write without the one line
# Need to rewrite this function because its not doing anything properly
# def change_pass(fernet, user_input):
#     for line in fileinput.input("password.txt", inplace=True):
#         line_encoded = line.split("|")
#         print(line_encoded)
#         if user_input == line_encoded[0]:
#             pass_decoded = fernet.decrypt(line_encoded[1].encode()).decode()
#             pass_input = input("Please enter the new password for user " + str(user_input) + ": ")
#             while pass_input == pass_decoded:
#                 pass_input = input("Please enter a new password for user " + str(user_input) + ": ")
#             print('{} {} {}'.format(line_encoded, '|', pass_input), end='')
#             return
#         else:
#             print('{}'.format(line), end='')


def change_pass(fernet, user_input):
    with fileinput.FileInput("password.txt", inplace=True) as f:
        for line in f:
            line_encoded = line.split("|")
            print(line_encoded)
            if user_input == line_encoded[0]:
                pass_decoded = fernet.decrypt(line_encoded[1].encode()).decode()
                pass_input = input("Please enter the new password for user " + str(user_input) + ": ")
                while pass_input == pass_decoded:
                    pass_input = input("Please enter a new password for user " + str(user_input) + ": ")
                print('{} {} {}'.format(line_encoded, '|', pass_input), end='')
                return
            else:
                print('{}'.format(line), end='')
        

#TODO MAKE DEF RESET TO DELETE PASSWORD.TXT  (DEV TOOL)


def main():

    if os.stat("password.txt").st_size < 1:
        write_salt()

    master_pwd = input("What is the master password? ")
    # Fernet algorithm
    salt = load_salt()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(master_pwd.encode()))
    fer = Fernet(key)

    while True:
        mode = input(
            "Would you like to add a new password or view existing ones (view, add, change), press q to quit? ").lower()
        if mode == "q" or mode == "quit":
            quit()
        elif mode == "view":
            try:
                view(fer)
            except:
                print("You entered the wrong master password.")
                m_pwd = input("What is the master password? ")
                fer = Fernet(find_key(m_pwd))
                continue
        elif mode == "add":
            try:
                verif(fer)
                add(fer)
            except:
                print("You entered the wrong master password.")
                m_pwd = input("What is the master password? ")
                fer = Fernet(find_key(m_pwd))
                continue
        elif mode == "change":
            try:
                verif(fer)
            except:
                print("You entered the wrong master password.")
                m_pwd = input("What is the master password? ")
                fer = Fernet(find_key(m_pwd))
                continue
            username_input = input(
                "Who is the user you want to change the password? ")
            change(fer, username_input)
        else:
            print("Invalid mode.")
            continue


if __name__ == "__main__":
    main()
