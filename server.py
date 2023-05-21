import socket
import secrets
import pickle
import hashlib
import csv
import os
import pandas as pd

# Create the file for the first time only
if not os.path.isfile('data.csv'):
    # Create data.csv file to store usernames and passwords and their salts
    with open('data.csv', 'w', newline='') as file:
        writer = csv.writer(file)

    # Write the coloumn names to the data.csv file
    with open("data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Usernames", "Passwords", "Salts"])


# Method to read the data.csv file and checks weather the user is in the file or not in case of sign up
# In case of login it checks if the user exists and return the user salt and hash to check password of the user
def checkUsername(newUser):
    if os.stat("data.csv").st_size != 0:
        storedData = pd.read_csv('data.csv')
        usernames = storedData.iloc[:, 0]
        passwords = storedData.iloc[:, 1]
        salts = storedData.iloc[:, 2]
        for i in range(0, len(usernames)):
            if usernames[i] == newUser:
                return [False, passwords[i], salts[i]]
    return [True, 0, 0]


SERVER_IP = '192.168.1.14'
SERVER_PORT = 5678

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Server Opens Connection
    s.bind((SERVER_IP, SERVER_PORT))
    print('Server is listening')
    s.listen(1)
    conn, addr = s.accept()
    print(f'Connection accepted from :{addr}')
    with conn:
        while True:
            conn.send(pickle.dumps("You Are Now Connected to The Server"))
            data = conn.recv(1024)
            data = pickle.loads(data)
            # Sign Up case
            if data[2] == '0':
                # Check if user is already registered
                if checkUsername(data[0])[0]:
                    # Generate salt and appends it to the password
                    salt = secrets.token_hex(16)
                    data[1] += salt
                    message = data[1].encode()
                    # create a SHA512 hash object and update the hash object with the message
                    sha512 = hashlib.sha512()
                    sha512.update(message)
                    # Stores the hashed password and the salt in the data object
                    data[1] = sha512.hexdigest()
                    data[2] = salt
                    # Store the data object in the data.csv file
                    with open("data.csv", "a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(data)

                    conn.send(pickle.dumps("Your Account Has Been Registered Successfully"))
                else:
                    conn.send(pickle.dumps("Username Already Exists"))
            # Sign in case
            else:
                # Check if the user exist and return it's Hashed password and salt
                notExists, hashedPass, salt = checkUsername(data[0])
                if not notExists:
                    # Generate the hash again from the password and the salt
                    data[1] += salt
                    message = data[1].encode()
                    sha512 = hashlib.sha512()
                    sha512.update(message)
                    data[1] = sha512.hexdigest()
                    # Check if the Hashes Match
                    if hashedPass == data[1]:
                        conn.send(pickle.dumps("You have logged in Successfully"))
                    else:
                        conn.send(pickle.dumps("You entered a wrong password"))

                else:
                    conn.send(pickle.dumps("Username does not Exists please Sign Up"))
            print(data)
            break
