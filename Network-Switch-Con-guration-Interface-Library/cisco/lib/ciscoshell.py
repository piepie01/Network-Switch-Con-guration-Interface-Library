from pexpect import pxssh
import time
from getpass import getpass
import sys
from cmd import Cmd
from cisco.lib import cli

class Prompt(Cmd):
	def do_showarp(self, args):
		cli.showArp(ssh,SwitchName)
	def do_forceexit(self, args):
		"""Quit the program without logout."""
		raise SystemExit

	def do_EOF(self, args):
		"""Logout current switch and exit."""
		ssh.logout()
		raise SystemExit

	def do_exit(self, args):
		"""Logout current switch and exit."""
		ssh.logout()
		raise SystemExit

	def do_showrun(self, args):
		"""Show switch dashboard information."""
		cli.showrun(ssh,SwitchName)

	def do_showintstat(self, args):
		"""Show port packet statistics."""
		cli.showintstat(ssh,SwitchName)

	def do_showint(self, args):
		"""Show interfaces status."""
		cli.showint(ssh,SwitchName)

	def do_showportchannel(self, args):
		"""Show port channel information."""
		cli.showportchannel(ssh,SwitchName)

	def do_showvlan(self, args):
		"""Show interface VLAN membership."""
		cli.showvlan(ssh,SwitchName)

	def do_showvlanid(self, args):
		"""Show VLAN id status."""
		vlan_id = input("vlan id(1-4094)?")
		cli.showvlanid(ssh,SwitchName,vlan_id)

	def do_showmac(self, args):
		"""Show mac address table."""
		cli.showmac(ssh,SwitchName)

	def do_setinfo(self, args):
		"""Set switch name, Location, contact."""
		global SwitchName
		ChangeName = input("Switch name:")
		cli.setinfo(ssh,ChangeName)
		prompt.prompt = ChangeName + '>'
		SwitchName = ChangeName
	def do_write(self, args):
		"""Save configuration."""
		cli.write(ssh)

	def do_setaccount(self, args):
		"""Modify administrative account."""
		cli.setaccount(ssh,SwitchName)
		print ("login again")
		raise SystemExit

	def do_setnetwork(self, args):
		"""Set switch IP, subnet, gateway, management vlan."""
		manage_vlan_id = input("management vlan id? (empty = 1)")
		manage_vlan_id = '1' if manage_vlan_id == '' else manage_vlan_id
		mode = input("dhcp or static?")
		while mode != "static" and mode != "dhcp":
			mode = input("dhcp or static?")
		cli.setnetwork(ssh,manage_vlan_id, mode)
	def do_settime(self, args):
		"""Set SNTP server IP and timezone (support GMT+8 TPE only)."""
		cli.settime(ssh)

	def do_vlanadd(self, args):
		"""Add a new vlan interface."""
		vlan_id = input("vlan id(1-4094)?")
		cli.vlanadd(ssh,vlan_id)

	def do_vlandel(self, args):
		"""Delete a new vlan interface."""
		vlan_id = input("vlan id(1-4094)?")
		cli.vlandel(ssh,vlan_id)

	def do_vlanset(self, args):
		"""Set interfaces vlan membership."""
		mode = input("trunk[t] or access[a]?")
		while mode not in "ta":
			mode = input("trunk[t] or access[a]?")
		if mode == "t":
			cli.trunk(ssh)
		else:
			cli.vlanset(ssh)

	def do_uploadconfig(self,args):
		"""Upload a config file to switch."""
		cli.uploadconfig(ssh)

	def do_downloadconfig(self,args):
		"""Download a config file to local."""
		cli.downloadconfig(ssh)

	def do_setportchannel(self,args):
		"""Configure port channel settings."""
		cli.setportchannel(ssh)

	def do_clearportchannel(self,args):
		"""Clear port channel settings."""
		cli.clearportchannel(ssh)

	def do_setportstatus(self,args):
		"""Enable or disable ports."""
		available_mode = {'e':'enabled', 'd':'disabled'}
		mode = input("enable or disable a port(e/d)?")
		while mode not in available_mode:
			mode = input("enable or disable a port(e/d)?")
		cli.setportstatus(ssh,mode)

	def do_ping(self, args):
		"""Ping an IP through the switch"""
		ipAddr, count, interval, size = input("IP address: "), input("Count (1-15): "), input("Interval (1-60 Seconds): "), input("Size (40-1000Bytes): ")
		cli.ping(ssh, ipAddr, count, interval, size, SwitchName)

	def do_loopprotection(args):
		"""loop protection on all interface"""

	def do_setmgmtvlan(self, args):
		"""change management vlan id"""
		pre_vlan = input("Original vlan manager:")
		if cli.VlanHasIP(ssh,pre_vlan):
			vlan_id, ip, mask = input("Vlan ID(1-4094)?: "), input("IP:"), input("Mask(a.b.c.d):")
			if vlan_id == pre_vlan:
				print ("same vlan as before, you can use setnetwork.")
			else:
				cli.setmgmtvlan(ssh,vlan_id,ip,mask,pre_vlan)
		else:
			print("incorrect original vlan manager, see showrun")

	def do_showntp(self, args):
		cli.showntp(ssh,SwitchName)

	def do_ntpenable(self,args):
		cli.ntpenable(ssh)

	def do_ntpdisable(self,args):
		cli.ntpdisable(ssh)

	def do_setntpserver(self,args):
		if 'not enabled.' not in cli.showntp(ssh,SwitchName):
			mode = input("add or delete a server(a/d)?")
			while mode not in 'ad':
				mode = input("add or delete a server(a/d)?")
			ntp_server = input("ntp server(ip)?")
			cli.setntpserver(ssh,mode,ntp_server)

	def do_showclock(self,args):
		cli.showclock(ssh,SwitchName)

prompt = Prompt()
ssh = None
password = ''
SwitchName = ''
def run(_ssh,_password,_SwitchName):
	global ssh
	global password
	global SwitchName
	ssh = _ssh
	password = _password
	SwitchName = _SwitchName
	prompt.prompt = SwitchName + '>'
	print (prompt.prompt)
	while True:
		try:
			prompt.cmdloop("Type exit/forceexit to quit, help for help.")
		except KeyboardInterrupt:
			pass
