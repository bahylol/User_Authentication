import socket
import pickle

SERVER_IP = '192.168.1.14'
SERVER_PORT = 5678

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # Connect to the server
    s.connect((SERVER_IP, SERVER_PORT))
    data = s.recv(1024)
    print(pickle.loads(data))
    # Take the desired data from the user
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    signInOrUp = ''
    while signInOrUp != '1' and signInOrUp != '0':
        signInOrUp = input("Enter 0 if You want to sign up or Enter 1 if you want to sign in: ")
    # Sends data to server
    s.send(pickle.dumps([username, password, signInOrUp]))
    # Takes the response of the server and prints it to the user
    data = s.recv(1024)
    print(pickle.loads(data))
