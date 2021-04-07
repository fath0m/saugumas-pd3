import math
import random
import sqlite3
import os
from db.queries import insert_encryption, get_encryptions

"""
Helper functions
"""
def is_prime(a):
	for i in range(2, a):
		if(a % i ==0):
			return False
	return True

def inverse(a, m):
	m0 = m
	y = 0
	x = 1

	if (m == 1):
		return 0

	while (a > 1):
		q = a // m
		t = m
		m = a % m
		a = t
		t = y

		y = x - q * y
		x = t

	if (x < 0):
		x = x + m0
	
	return x

"""
RSA specific functions
"""
def keygen(p, q, phi, n):
	# Choose a random exponential, try until GCD = 1
	e = random.randrange(2, phi)
	g = math.gcd(e, phi)

	while g != 1:
		e = random.randrange(2, phi)
		g = math.gcd(e, phi)

	# Extended Euclid's algorithm to generate private key (d)
	# As we already have public key (e)
	d = inverse(e, phi)
	
	# (Public key, Private key)
	return ((e, n), (d, n))

def gen_public_key(p, q, phi, n):
	e = random.randrange(2, phi)
	g = math.gcd(e, phi)

	while g != 1:
		e = random.randrange(2, phi)
		g = math.gcd(e, phi)

	return (e, n)

def gen_private_key(e, phi, n):
	# Extended Euclid's algorithm to generate private key (d)
	# As we already have public key (e)
	d = int(inverse(e, phi))

	return (d, n)

def decrypt(key, encrypted_text):
	x, y = key
	p = [chr((char ** x) % y) for char in encrypted_text]

	return ''.join(p)

def encrypt(key, text):
	x, y = key
	c = [(ord(char) ** x) % y for char in text]

	return c


"""
Application
"""
def ui_clear():
	os.system('clear')

def ui_hr():
	print("----------------------------------------------")

def ui_br():
	print()

def ui_continue():
	input("Press ENTER to continue")
	ui_clear()

def do_encrypt():
	ui_clear()

	print("Provide encryption parameters")
	ui_hr()

	p = 0
	q = 0

	while True:
		p = int(input("p = "))
		q = int(input("q = "))

		if (is_prime(p) == False):
			ui_clear()
			print("Number p is not a prime")
			continue

		if (is_prime(q) == False):
			ui_clear()
			print("Number q is not a prime")
			continue

		break

	ui_hr()
	print("Enter text to encrypt")

	text = input("> ")

	ui_hr()
	print("CALCULATIONS")
	ui_hr()

	n = p * q
	print("n = " + str(n))

	phi = (p - 1) * (q - 1)
	print("phi = " + str(phi))

	e, _ = gen_public_key(p, q, phi, n)
	print("e = " + str(e) + " (public key)")

	ui_hr()
	print("ENCRYPTED RESULT")
	ui_hr()

	encrypted = encrypt((e, n), text)
	print(encrypted)
	ui_br()

	insert_encryption(e, n, ','.join(map(str, encrypted)))
	ui_continue()

def do_decrypt():
	ui_clear()
	encryptions = get_encryptions()
	available = []

	for row in get_encryptions():
		available.append(row)

	if (len(available) == 0):
		print("No existing encryptions exist")
		ui_hr()
		ui_continue()
		return

	print("Choose which text you want to decrypt")
	ui_hr()

	i = 1
	for row in available:
		_id, e, n, encrypted_text = row

		print("%d) e = %d, n = %d, encrypted text = %s" % (i, e, n, encrypted_text))
		i += 1

	x = 0

	while True:
		x = int(input("> "))

		if (x < 1 or x > len(available) + 1):
			print("Invalid selection, please try again")
		else:
			break

	choice = available[x - 1]
	_id, e, n, encrypted_text = choice

	# str[] -> int[]
	encrypted = [int(numeric_string) for numeric_string in encrypted_text.split(",")]

	ui_hr()
	print("CALCULATIONS")
	ui_hr()

	p = 2
	q = 0

	while (n % p > 0):
		p += 1

	print("p = " + str(p))

	q = n / p
	print("q = " + str(q))

	phi = (p - 1) * (q - 1)
	print("phi = "+ str(phi))

	private_key = gen_private_key(e, phi, n) 
	pk_e, _ = private_key

	print("d = " + str(private_key) + " (private key)")

	ui_hr()
	print("DECRYPTED RESULT")
	ui_hr()

	decrypted = decrypt(private_key, encrypted)
	print(decrypted)

	ui_br()
	ui_continue()



def main():
	# p = 179
	# q = 1229

	# if is_prime(q) == False or is_prime(q) == False:
	# 	print("Please provide prime numbers")
	# 	return

	# n = p * q
	# phi = (p - 1) * (q - 1)

	# public_key = gen_public_key(p, q, phi, n)

	# e, n = public_key
	
	# print(public_key)
	# text = "Jonas"

	# # Try and get private key
	# new_p = 2
	# new_q = 0

	# while (n % new_p > 0):
	# 	new_p += 1

	# new_q = n / new_p

	# new_phi = (new_p - 1) * (new_q - 1)

	# private_key = gen_private_key(e, new_phi, n)

	# encrypted = encrypt(public_key, text)
	# decrypted = decrypt(private_key, encrypted)

	# print(encrypted)
	# print(decrypted)

	ui_clear()

	while True:
		ui_br()
		print("RSA Encryption / Decryption")
		ui_hr()
		print("1 - Encrypt a text")
		print("2 - Decrypt a text")
		print("0 - Exit")
		ui_hr()

		print(get_encryptions())

		x = int(input("> "))

		if (x == 0):
			break
		elif (x == 1):
			do_encrypt()
		elif (x == 2):
			do_decrypt()
		else:
			ui_clear()
			print("ERROR: Invalid option, please select again")

if __name__ == "__main__":
	main()