import socket
import threading
import json
import getpass
import os
from database import add_contact, get_contacts, remove_contact

import json

# Load config
with open("config.json") as f:
    config = json.load(f)

HOST = config["host"]
PORT = config["port"]

def receive_messages(sock):
    while True:
        try:
            metadata = sock.recv(1024).decode()
            if not metadata:
                break

            data = json.loads(metadata)

            if data["type"] == "text":
                print(f"\n{data['from']}: {data['content']}")

            elif data["type"] == "file":
                print(f"\nReceiving file '{data['filename']}' from {data['from']}...")

                file_data = b''
                remaining = data["filesize"]
                while remaining > 0:
                    chunk = sock.recv(min(1024, remaining))
                    if not chunk:
                        break
                    file_data += chunk
                    remaining -= len(chunk)

                with open("received_" + data["filename"], "wb") as f:
                    f.write(file_data)
                print(f"File saved as 'received_{data['filename']}'")

        except Exception as e:
            print("Connection error:", e)
            break

def send_messages(sock, username):
    while True:
        msg = input()
        if msg.lower() == "exit":
            print("Exiting...")
            sock.close()
            break

        elif msg.startswith("/sendfile"):
            parts = msg.split(" ", 2)
            if len(parts) < 3:
                print("Usage: /sendfile <recipient> <filepath>")
                continue

            to_user = parts[1]
            filepath = parts[2]

            if not os.path.exists(filepath):
                print("File does not exist.")
                continue

            with open(filepath, "rb") as f:
                file_data = f.read()

            filename = os.path.basename(filepath)
            metadata = {
                "type": "file",
                "filename": filename,
                "from": username,
                "to": to_user,
                "filesize": len(file_data)
            }

            sock.send(json.dumps(metadata).encode())
            sock.sendall(file_data)
            print(f"Sent file '{filename}' to {to_user}.")

        elif msg.startswith("/addcontact"):
            parts = msg.split()
            if len(parts) != 2:
                print("Usage: /addcontact <username>")
                continue
            contact_user = parts[1]
            success, message = add_contact(username, contact_user)
            print(message)

        elif msg.startswith("/listcontacts"):
            contacts = get_contacts(username)
            print("\n📋 Your contacts:")
            for c in contacts:
                print(" -", c)

        elif msg.startswith("/removecontact"):
            parts = msg.split()
            if len(parts) != 2:
                print("Usage: /removecontact <username>")
                continue
            remove_contact(username, parts[1])
            print("✅ Contact removed.")

        else:
            message = {
                "type": "text",
                "content": msg
            }
            sock.send(json.dumps(message).encode())

def authenticate():
    while True:
        choice = input("Do you want to [login] or [register]? ").lower().strip()
        if choice not in ["login", "register"]:
            print("Choose 'login' or 'register'")
            continue

        username = input("Username: ").strip()
        password = getpass.getpass("Password: ").strip()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        auth_data = {
            "action": choice,
            "username": username,
            "password": password
        }

        sock.send(json.dumps(auth_data).encode())
        response = sock.recv(1024).decode()
        result = json.loads(response)

        if result["status"] == "ok":
            print(result["message"])
            return sock, username
        else:
            print("❌", result["message"])
            sock.close()

if __name__ == "__main__":
    client_socket, username = authenticate()
    threading.Thread(target=receive_messages, args=(client_socket,), daemon=True).start()
    send_messages(client_socket, username)
# This code implements a simple client for a chat application that allows users to send text messages and files.
# It connects to a server, handles user authentication, and provides a command-line interface for sending messages and files.
# The client uses threads to handle incoming messages while allowing the user to send messages concurrently.        
# The client also supports adding and removing contacts, listing contacts, and sending files to other users.
# The user can exit the application by typing "exit". The client uses JSON for message formatting and handles file transfers by reading the file in binary mode and sending it over the socket.
# The client runs indefinitely until the user decides to exit, allowing for continuous communication with the server and other users.
# The client also uses the `getpass` module to securely handle password input without echoing it to the console.
# The client connects to the server at the specified host and port, and it uses a simple command-line interface for user interaction.
# The client handles various commands such as sending text messages, sending files, adding contacts, listing contacts, and removing contacts.
# The client also handles errors gracefully, providing feedback to the user when actions fail or when the