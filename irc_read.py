import sys
import socket
import string

from irc import *

s = connect()
readbuffer = ""

while 1:
	readbuffer = readbuffer + s.recv(1024).decode()
	temp = readbuffer.split('\n')
	readbuffer = temp.pop( )

	for line in temp:
		parts = line.split(' ')
		server = parts[0][1:]
		prefix_len = len(parts[0]) + 1
		if len(parts) > 1:
			prefix_len += len(parts[1]) + 1
		if len(parts) > 2:
			prefix_len += len(parts[2]) + 1

		if parts[0] == 'PING':
			s.send(('PONG ' + line[4:] + '\r\n').encode())
			continue
		elif 'PRIVMSG ' in line and '!' in line:
			prefix_len = len(parts[0]) + 1 + len(parts[1]) + 1 + len(parts[2]) + 2
			user = line[1:line.index('!')]
			print("<%s> %s" % (user, line[prefix_len:]))
			continue

		if parts[1] == 'MODE':
			print(parts[0][1:] + " mode set to " + parts[3][1:])
		elif parts[1] == 'JOIN':
			name = parts[0][1:]
			name = name[0:name.index('~')]
			end_of_name = len(name) - 1
			name = name[0:end_of_name]
			print(name + " has joined #" + parts[2][1:])

		try:
			code = int(parts[1])
		except:
			continue
		body_text = line[prefix_len:]

		# https://www.alien.net.au/irc/irc2numerics.html
		if code == 1 or code == 2 or code == 3:
			print(body_text[1:])
		elif code == 4:
			continue
		elif code == 5:
			continue
		elif code == 251 or code == 252 or code == 253 or code == 254 or code == 255 or code == 266 or code == 250:
			print(body_text[1:])
		elif code == 375 or code == 372:
			print(body_text[1:])