import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, storeName text)")
cursor.execute("CREATE TABLE IF NOT EXISTS stores (store_id INTEGER PRIMARY KEY, ownerName text, storeName text)")
cursor.execute("CREATE TABLE IF NOT EXISTS items (item_id INTEGER PRIMARY KEY,storeName text,itemName text,price text)")

connection.commit()
connection.close()
