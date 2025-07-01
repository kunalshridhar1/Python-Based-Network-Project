import sqlite3
import bcrypt  # type: ignore

# Initialize database and create users & contacts tables
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash BLOB NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            owner TEXT,
            contact TEXT,
            FOREIGN KEY(owner) REFERENCES users(username),
            FOREIGN KEY(contact) REFERENCES users(username)
        )
    ''')

    conn.commit()
    conn.close()

# Register new user
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
    conn.commit()
    conn.close()
    return True

# Verify login credentials
def verify_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    if result is None:
        return False
    stored_hash = result[0]
    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode()
    return bcrypt.checkpw(password.encode(), stored_hash)

# Get all users
def get_all_users():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users")
    users = [row[0] for row in cursor.fetchall()]
    conn.close()
    return users

# Delete user
def delete_user(username):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE username = ?", (username,))
    conn.commit()
    conn.close()

# Update password
def update_password(username, new_password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    new_password_hash = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())
    cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (new_password_hash, username))
    conn.commit()
    conn.close()

# ===================== CONTACT MANAGEMENT =====================

# Add a contact
def add_contact(owner, contact):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (contact,))
    if cursor.fetchone() is None:
        conn.close()
        return False, "Contact user does not exist."

    cursor.execute("SELECT * FROM contacts WHERE owner = ? AND contact = ?", (owner, contact))
    if cursor.fetchone():
        conn.close()
        return False, "Contact already exists."

    cursor.execute("INSERT INTO contacts (owner, contact) VALUES (?, ?)", (owner, contact))
    conn.commit()
    conn.close()
    return True, "Contact added successfully."

# Get contacts for a user
def get_contacts(owner):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT contact FROM contacts WHERE owner = ?", (owner,))
    contacts = [row[0] for row in cursor.fetchall()]
    conn.close()
    return contacts

# Remove a contact
def remove_contact(owner, contact):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM contacts WHERE owner = ? AND contact = ?", (owner, contact))
    conn.commit()
    conn.close()

# Initialize database
init_db()       
# This code implements a simple user management system using SQLite and bcrypt for password hashing.
# It includes functions to initialize the database, register new users, verify login credentials,   

# Example usage
if __name__ == "__main__":
    if register_user("testuser", "password123"):
        print("User registered successfully.")
    else:
        print("User already exists.")

    if verify_user("testuser", "password123"):
        print("Login successful.")
    else:
        print("Login failed.")

    users = get_all_users()
    print("Registered users:", users)

    update_password("testuser", "newpassword123")
    print("Password updated successfully.")

    delete_user("testuser")
    print("User deleted successfully.")
# This code implements a simple user management system using SQLite and bcrypt for password hashing.
# It includes functions to initialize the database, register new users, verify login credentials, retrieve all          
# registered users, delete a user, and update a user's password.
# The database is initialized with a users table, and the bcrypt library is used to securely hash       
# passwords before storing them in the database.
# The example usage at the end demonstrates how to use these functions to manage users.         
# This code implements a simple chat client that connects to a chat server.
# It allows users to register or log in, send messages, and receive messages from other users