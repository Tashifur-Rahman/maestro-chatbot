import json
import os

from config import *
import sqlite3

from config import DATABASE


def create_database():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS messages(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            role TEXT NOT NULL,

            content TEXT NOT NULL

        )
        """
    )

    connection.commit()

    connection.close()


def load_memory():
    connection=sqlite3.connect(DATABASE)
    cursor=connection.cursor()
    cursor.execute("SELECT role,content FROM messages ORDER BY id ASC")
    rows=cursor.fetchall()
    connection.close()
    messages=[]
    for row in rows:
        messages.append({"role":row[0],"content":row[1]})
    return messages


def save_memory(role,content):
    connection=sqlite3.connect(DATABASE)
    cursor=connection.cursor()
    cursor.execute("INSERT INTO messages (role,content) VALUES (?,?)",(role,content))
    connection.commit()
    connection.close()

def clear_memory():
    connection=sqlite3.connect(DATABASE)
    cursor=connection.cursor()
    cursor.execute("DELETE FROM messages")
    connection.commit()
    connection.close()

def show_history(messages):

    print("\n========== Chat History ==========")

    for msg in messages:

        if msg["role"] == "user":

            print(
                f"\033[32mYou      : {msg['content']}\033[0m"
            )

        else:

            print(
                f"\033[33mMaestro  : {msg['content']}\033[0m"
            )

