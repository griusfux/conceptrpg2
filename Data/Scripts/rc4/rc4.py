#!/usr/bin/env python
"""Implementation of RC4 with drop[(nbytes)] improvement

By using a class, the inital expense of generating the key-stream and drop bytes
is only incurred on startup.  This means a much stronger 'good enough'
encryption is available with zero extra overhead.  Default usage has a keystream
byte drop of 768 as recommended after crypto-analysis*.  Also makes use of
base64 de/encoding to make streaming the data easier across languages &
platforms.  Tested in Python 3.1

More information can be found at http://en.wikipedia.org/wiki/RC4.
*http://www.users.zetnet.co.uk/hopwood/crypto/scan/cs.html#RC4-drop 

--------------------------------------------------------------------------------
Copyright (C)2010 BitFlip Games
Written by Delaney Gillilan delaney@bitflipgames.com

I, the copyright holder of this work, hereby release it into the public domain.
This applies worldwide.  In case this is not legally possible, I grant any
entity the right to use this work for any purpose, without any conditions,
unless such conditions are required by law.

Modified by Mitchell Stokes to work with pure byte data
--------------------------------------------------------------------------------
"""

import struct,unittest

class rc4(object):
	def __init__(self,key,drop_n_bytes=768):
		self.ksa = self.make_key(key,drop_n_bytes)

	def encrypt_byte(self, i,j,S):
		i = (i+1) % 256
		j = (j+S[i]) % 256
		S[i], S[j] = S[j],S[i]
		K = S[(S[i] + S[j])%256]
		return (i,j,K)

	def make_key(self, key, drop_n_bytes):
		#The key-scheduling algorithm (KSA)
		S = [i for i in range(256)]
		j = 0
		for i in range(256):
			j = (j + S[i] + ord(key[i % len(key)])) % 256
			S[i], S[j] = S[j],S[i]

		self.i = 0
		self.j = 0
		#Do the RC4-drop[(nbytes)]
		if drop_n_bytes:
			#i = j = 0
			for dropped in range(drop_n_bytes):
				self.i,self.j,K = self.encrypt_byte(self.i,self.j,S)
		return S

	def __crypt(self, message):
		#The pseudo-random generation algorithm (PRGA)
		S = list(self.ksa)  #make a deep copy of you KSA array, gets modified
		combined = []
		counter = 0
		i,j = self.i, self.j
		for c in message:
			i,j,K = self.encrypt_byte(i,j,S)
			combined.append(K ^ c)

		crypted = bytearray(combined)
		return crypted

	def encode(self,message,encodeBase64=False):
		crypted = self.__crypt(message)
		if encodeBase64:
			crypted = base64.urlsafe_b64encode(crypted)
		return crypted

	def decode(self,message,encodedBase64=False):
		if encodedBase64:
			message = base64.urlsafe_b64decode(message.encode())
		return self.__crypt(message)

class TestEncryption(unittest.TestCase):
	def setUp(self):
		self.key = "This is a test"
		self.rc4 = rc4(self.key,0)
		self.rc4d = rc4(self.key)
		self.message = b"Attack at dawn!"

	def test_encode(self):
		print("test_encode")
		encoded = self.rc4.encode(self.message)
		self.assertEqual(encoded,b'\xe3\x16w\xa6\x06\\\xf5~\x014\xbeP\x8fcC')
		
		self.rc4.decode(encoded)

	def test_encode_drop(self):
		print("test_encode_drop")
		encoded_drop = self.rc4d.encode(self.message)
		self.assertEqual(encoded_drop,b'M\\\x0e\xea\x8b\x99!\xcf\x1d\xd8X\xcb\xe6W\xfc')

	def test_decode(self):
		print("test_decode")
		e = self.rc4.encode(self.message)
		decoded = self.rc4.decode(e)
		self.assertEqual(decoded,self.message)

	def test_decode_drop(self):
		print("test_decode_drop")
		e = self.rc4d.encode(self.message)
		decoded = self.rc4d.decode(e)
		self.assertEqual(decoded,self.message)

if __name__ == '__main__':
	unittest.main()