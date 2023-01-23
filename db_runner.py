import sqlite3
from sqlite3 import Cursor


def get_connection():
    conn = sqlite3.connect("/home/HARM/shopsite/data.db")
    cur = Cursor(conn)
    return conn, cur

def exec(command):
    conn, cur = get_connection()
    res = cur.execute(command)
    conn.commit()
    res = res.fetchall()
    conn.close()
    return res