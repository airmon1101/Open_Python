#!/usr/bin/env python3

import bcrypt
import os
import sys
import getpass
from pathlib import Path

DB_FILE = Path("users.db")
BCRYPT_ROUNDS = 12


# ---------------- SECURITY HELPERS ---------------- #

def secure_db_permissions():
    if DB_FILE.exists():
        os.chmod(DB_FILE, 0o600)
    else:
        DB_FILE.touch(mode=0o600)


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    )


def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed)


# ---------------- USER MANAGEMENT ---------------- #

def user_exists(username: str) -> bool:
    with DB_FILE.open("r") as f:
        for line in f:
            if line.split(":", 1)[0] == username:
                return True
    return False


def register_user(username: str, password: str):
    if user_exists(username):
        print("❌ User already exists")
        return

    hashed = hash_password(password)

    with DB_FILE.open("a") as f:
        f.write(f"{username}:{hashed.decode()}\n")

    print("✅ User registered successfully")


def authenticate_user(username: str, password: str):
    with DB_FILE.open("r") as f:
        for line in f:
            stored_user, stored_hash = line.strip().split(":", 1)
            if stored_user == username:
                if verify_password(password, stored_hash.encode()):
                    print("✅ Authentication successful")
                    return True
                else:
                    print("❌ Authentication failed")
                    return False

    print("❌ User not found")
    return False


# ---------------- CLI INTERFACE ---------------- #

def prompt_register():
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    confirm = getpass.getpass("Confirm Password: ")

    if password != confirm:
        print("❌ Passwords do not match")
        return

    register_user(username, password)


def prompt_login():
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")
    authenticate_user(username, password)


def main():
    secure_db_permissions()

    while True:
        print("\n1) Register")
        print("2) Login")
        print("3) Exit")

        choice = input("Select: ").strip()

        if choice == "1":
            prompt_register()
        elif choice == "2":
            prompt_login()
        elif choice == "3":
            sys.exit(0)
        else:
            print("❌ Invalid option")


if __name__ == "__main__":
    main()
