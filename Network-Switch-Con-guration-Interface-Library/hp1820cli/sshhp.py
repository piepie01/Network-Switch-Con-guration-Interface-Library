#!/usr/bin/env python3
import sys
from getpass import getpass
from hp1820cli.lib import cli
from hp1820cli.lib import hpshell
from hp1820cli.lib.cli import Cli

# def checkArgument(address):
#     print (len(address))
#     if len(address) != 11:
#         print("http - Connect a switch through HTTP protocal")
#         print("Usage: http [user@]host")
#         print("(If not specified, username is admin.)")
#         sys.exit(0)

def parseArgument(address):
    if '@' in address:
        return address.split('@')
    else:
        return "admin", address

def execPrompt(cli):
    hpshell.run(cli)

def hpswitch(address):
# if __name__ == "__main__":
    # checkArgument(address)
    user, host = parseArgument(address)

    # Always try https first!
    if Cli.testConnection('https', host):
        cli = Cli('https', host)
        print("Connect through HTTPS successfully")
        print("Note: This program will NOT verify the SSL certificate.")
    else:
        print("HTTPS failed. Try HTTP...")
        if Cli.testConnection('http', host):
            cli = Cli('http', host)
            print("*****************************************")
            print("*Warning: Connect through HTTP protocal.*")
            print("*****************************************")
        else:
            print("Error: Cannot connect to remote host through HTTP and HTTPS.")
            sys.exit(0)

    wrong_times = 0
    while wrong_times < 3:
        password = getpass('Password: ')
        if cli.login(user, password):
            break
        wrong_times += 1

    if wrong_times >= 3:
        print("3 incorrect password attempts")
        sys.exit(0)

    execPrompt(cli)
