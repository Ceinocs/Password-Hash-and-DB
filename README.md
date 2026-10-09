# Secure Authentication System & SQLite Database Exporter

A console-based Python application designed for secure user registration and authentication, featuring automated database backups.

## Features

* **Secure Password Hashing:** User passwords are encrypted using the cryptographically strong **Scrypt** key derivation function along with a unique salt (`os.urandom`) for every user.
* **Database Management:** Uses **SQLite** for lightweight, local storage of user credentials.
* **Automated Data Export:** Every successful login automatically generates or updates a backup of the entire user database in a `.csv` format (pre-configured with a semicolon delimiter for native compatibility with Excel).

## Requirements

Before running the project, you need to install the required dependency for password hashing:

```bash
pip install cryptography
```

## How It Works

1. **Start:** Run `main.py` to open the console menu.
2. **Registration:** Choose option `(2)` to create a new profile. The system ensures unique usernames.
3. **Login:** Choose option `(1)` to sign in. 
4. **Export:** Upon a successful authentication, the script triggers the `export_to_excel()` function, writing the database records into `users_backup.csv`.
