import socket
import select
import json
from database import init_db, register_user, verify_user

with open("config.json") as f:
    config = json.load(f)

HOST = config["host"]
PORT = config["port"]
init_db()


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()

sockets_list = [server_socket]
clients = {}  # {socket: username}

def receive_message(client_socket):
    try:
        message = client_socket.recv(1024).decode()
        if not message:
            return None
        return json.loads(message)
    except:
        return None

print(f"Server listening on {HOST}:{PORT}")

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            auth_data = receive_message(client_socket)

            if auth_data is None:
                continue

            if auth_data["action"] == "register":
                success = register_user(auth_data["username"], auth_data["password"])
                if success:
                    client_socket.send(json.dumps({"status": "ok", "message": "Registration successful."}).encode())
                else:
                    client_socket.send(json.dumps({"status": "fail", "message": "Username already exists."}).encode())
                client_socket.close()

            elif auth_data["action"] == "login":
                if verify_user(auth_data["username"], auth_data["password"]):
                    client_socket.send(json.dumps({"status": "ok", "message": "Login successful."}).encode())
                    sockets_list.append(client_socket)
                    clients[client_socket] = auth_data["username"]
                    print(f"User '{auth_data['username']}' logged in.")
                else:
                    client_socket.send(json.dumps({"status": "fail", "message": "Invalid credentials."}).encode())
                    client_socket.close()

        else:
            try:
                message = receive_message(notified_socket)

                if message is None:
                    raise Exception("Disconnected")

                if message["type"] == "text":
                    sender = clients[notified_socket]
                    print(f"{sender}: {message['content']}")

                    for client_socket in clients:
                        if client_socket != notified_socket:
                            client_socket.send(json.dumps({
                                "type": "text",
                                "from": sender,
                                "content": message["content"]
                            }).encode())

                elif message["type"] == "file":
                    print(f"Receiving file from {clients[notified_socket]}: {message['filename']}")

                    file_data = b''
                    remaining = message["filesize"]
                    while remaining > 0:
                        chunk = notified_socket.recv(min(1024, remaining))
                        if not chunk:
                            break
                        file_data += chunk
                        remaining -= len(chunk)

                    for client_socket in clients:
                        if clients[client_socket] == message["to"]:
                            client_socket.send(json.dumps(message).encode())
                            client_socket.sendall(file_data)
                            print(f"Forwarded file to {message['to']}")
            except:
                user = clients.get(notified_socket, "Unknown")
                print(f"{user} disconnected.")
                sockets_list.remove(notified_socket)
                clients.pop(notified_socket, None)

    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        clients.pop(notified_socket, None)
server_socket.close()
print("Server shutting down.")          
# This code implements a simple chat server that handles user registration and login, as well as message and file transfer.
# It uses sockets for communication and JSON for message formatting.            
# The server listens for incoming connections, allowing users to register or log in.
# Once authenticated, users can send text messages and files to each other.
# The server handles multiple clients using the `select` module to manage I/O operations efficiently.
# The server also manages user sessions and broadcasts messages to all connected clients.
# The server runs indefinitely, accepting new connections and processing messages until it is manually stopped. 