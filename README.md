Python-Based Messaging Application

A comprehensive messaging application using Python and a client-server architecture that supports real-time text messaging, secure file transfers, user authentication, and contact management.

🚀 Features

Real-time text communication

File and photo transfer between users

Secure user registration and login (bcrypt + SQLite)

Contact management (add/list/remove)

Configuration via config.json

Modular and maintainable codebase

📁 Project Structure

├── client.py          # Client-side logic and command-line interface
├── server.py          # Server handling client connections and routing
├── database.py        # User authentication and contact management
├── config.json        # Configuration file (host and port)
├── README.md          # Project overview and instructions

⚙️ Requirements

Python 3.10+

bcrypt

SQLite3 (built-in with Python)

Install bcrypt:

pip install bcrypt

🔧 Setup Instructions

1. Clone the Repository

git clone https://github.com/kunalshridhar1/B206-Operating-Systems.git
cd messaging-app

2. Configure Host and Port

Edit config.json:

{
  "host": "127.0.0.1",
  "port": 5000
}

3. Run the Server

python server.py

4. Run the Client (in a new terminal)

python client.py

🧪 Sample Commands (Client)

/addcontact <username> – Add a contact

/listcontacts – Show saved contacts

/removecontact <username> – Remove contact

/sendfile <username> <filepath> – Send a file

exit – Disconnect from the server

📦 Functional Overview

Authentication: Passwords are hashed with bcrypt before storing in SQLite.

Messaging: JSON-based protocol over TCP sockets.

File Transfer: Sends metadata + binary stream to the server.

Contact List: SQLite-based, linked to the user account.

Config Management: Easily switch between localhost or LAN IP.

📌 Future Enhancements

GUI with Tkinter or PyQt

End-to-end encryption (RSA/AES)

Offline message support

Group chats

Dockerized deployment

📄 License

This project is for educational and demonstration purposes only.

✍️ Author
Kunal Shridhar
Mail id: shridharkunal2005@gmail.com

