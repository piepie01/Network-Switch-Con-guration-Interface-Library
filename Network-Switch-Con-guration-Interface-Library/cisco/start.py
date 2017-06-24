#!/usr/bin/env python3
from pexpect import pxssh
from getpass import getpass
from cisco.lib import cli
from cisco.lib import hpshell
import sys
import time
import socket

# def checkArgument(address):
# 	print (len(address))
# 	if len(address) != 12:
# 		print("http - Connect a switch through HTTP protocal")
# 		print("Usage: http [user@]host")
# 		print("(If not specified, username is admin.)")
# 		sys.exit(0)
def parseArgument(address):
	if '@' in address:
		return address.split('@')
	else:
		return '',address
def testConnect(host):
	print ("Try ssh to ",host)
	con = socket.socket()
	con.settimeout(5)
	try:
		con.connect((host,22))
		print("Success!")
		con.close()
	except:
		print("can't connect to ",host," with ssh.")
		con.close()
		sys.exit(0)
def sshcisco(address):
	# if __name__ == "__main__":
	# 	print ("ssh")
	# checkArgument(address)
	user, host = parseArgument(address)
	if user == '':
		user = input("Username:")
	testConnect(host)
	for count in range(1,4):
		ssh = pxssh.pxssh()
		password = getpass('password :')
		if password:
			try:
				ssh.login(sys.argv[1],user,password,auto_prompt_reset=False)
				break
			except:
				ssh.close()
				print ("incorrect password")
		if count==3:
			print ("incorrect password")
			sys.exit(0)

	ssh.sendline("terminal length 0")
	SwitchName = cli.getSwitchName(ssh)
	hpshell.run(ssh,password,SwitchName)
