import sys
import socket
import string

def read_args():
	arg_map = {}
	args = sys.argv
	i = 1

	while i < len(args):
		name = args[i]
		if name.startswith("--"):
			name = name[2:]
			value = args[i + 1]
			arg_map[name] = value
			i += 2
		else:
			i += 1

	return arg_map

def connect():
	args = read_args()
	try:
		host = args['host']
	except:
		host = "irc.freenode.net"
	try:
		port = int(args['port'])
	except:
		port = 6667
	nick = args['nick']
	try:
		ident = args['ident']
	except:
		ident = nick
	try:
		realname = args['realname']
	except:
		realname = ident
	channel = args['channel']
	try:
		password = args['pass']
	except:
		password = None

	s = socket.socket()
	s.connect((host, port))
	s.send(('USER %s %s Server %s\r\n' % (ident, host, realname)).encode())
	s.send(('NICK %s\r\n' % nick).encode())
	s.send(('JOIN #%s\r\n' % channel).encode())
	if not password == None:
		s.send(('/msg nickserv identify %s\r\n' % password).encode())

	return s