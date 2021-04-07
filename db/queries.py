import sqlite3

def get_connection():
	con = sqlite3.connect("./rsa.db")
	return con

def insert_encryption(e, n, text):
	con = get_connection()
	cur = con.cursor()

	cur.execute("INSERT INTO encryptions (public_key, sum, text) VALUES (?, ?, ?)", (e, n, text))
	con.commit()

def get_encryptions():
	con = get_connection()
	cur = con.cursor()

	return cur.execute("SELECT * FROM encryptions")