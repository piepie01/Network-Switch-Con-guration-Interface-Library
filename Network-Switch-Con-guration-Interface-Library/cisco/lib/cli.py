from pexpect import pxssh
import time
import sys
from getpass import getpass

def showArp(ssh,SwitchName):
	s = 'show arp'
	ssh.sendline(s)
	ssh.prompt(timeout = 1)
	output = ssh.before.decode('ascii')
	ssh.expect (r'.+')
	output = delete(output,s)
	output = delete(output,SwitchName+'#')
	print (output)
def showrun(ssh,SwitchName):
	s = 'show ru'
	ssh.sendline(s)
	ssh.prompt(timeout = 1)
	output = ssh.before.decode('ascii')
	ssh.expect (r'.+')
	output = delete(output,s)
	output = delete(output,SwitchName+'#')
	print (output)
def showintstat(ssh,SwitchName):
	s = 'show interface status'
	trunk = getTrunk(ssh)
	ssh.sendline(s)
	ssh.prompt(timeout = 1)
	output = ssh.before.decode('ascii')
	ssh.expect (r'.+')
	output = delete(output,s)
	output = delete(output,SwitchName+'#')
	output_list = output.split('\n')
	output_list[1] = output_list[1][:-1]
	output_list[1] = output_list[1] + "                Trunk "
	index = 0
	for element in output_list:
		element = element[:-1]
		if len(trunk)>0:
			if trunk[index].split(' ')[0] == element.split(' ')[0]:
				element = element + '   ' + trunk[index].split(' ')[-1]
				index = index + 1
		print (element)

def showint(ssh,SwitchName):
	s = 'show interface'
	ssh.sendline(s)
	ssh.prompt(timeout = 1)
	output = ssh.before.decode('ascii')
	ssh.expect (r'.+')
	output = delete(output,s)
	output = delete(output,SwitchName+'#')
	print (output)
def showportchannel(ssh,SwitchName):
	s = 'show etherchannel port-channel'
	ssh.sendline(s)
	ssh.prompt(timeout = 1)
	output = ssh.before.decode('ascii')
	ssh.expect (r'.+')
	output = delete(output,s)
	output = delete(output,SwitchName+'#')
	print (output)
def showvlan(ssh,SwitchName):
	s = 'show vlan'
	ssh.sendline(s)
	ssh.prompt(timeout = 1)
	output = ssh.before.decode('ascii')
	ssh.expect (r'.+')
	output = delete(output,s)
	output = delete(output,SwitchName+'#')
	output_list = output.split('\r\n')
	final = ''
	line = "=>"
	output_list_len = len(output_list)
	index = 0
	judge = 0
	for element in output_list:
		print (line+str(index/output_list_len)[2:4]+'%', end='\r')
		index = index + 1
		line = '=' + line
		if judge == 1 and element.split(' ')[0] != '1' and element.split(' ')[0].isdigit():
			port = getPort(ssh,element.split(' ')[0])
			element = element + "   " + port	
			port = ''
		elif "VLAN Type  SAID       MTU   Parent RingNo BridgeNo Stp  BrdgMode Trans1 Trans2" in element:
			element = element + " port"
		elif "---- ----- ---------- ----- ------ ------ -------- ---- -------- ------ ------" in element:
			element = element + " ----"
			judge = 1
		final = final + element + '\n'
	print('')
	print(final)
def showvlanid(ssh,SwitchName,vlan_id):
	s = 'show vlan id '+vlan_id
	ssh.sendline(s)
	ssh.prompt(timeout = 1)
	output = ssh.before.decode('ascii')
	ssh.expect (r'.+')
	output = delete(output,s)
	output = delete(output,SwitchName+'#')
	print (output)
def showmac(ssh,SwitchName):
	s = 'show mac address-table'
	ssh.sendline(s)
	ssh.prompt(timeout = 1)
	output = ssh.before.decode('ascii')
	ssh.expect (r'.+')
	output = delete(output,s)
	output = delete(output,SwitchName+'#')
	print (output)
def setinfo(ssh,ChangeName):
	list_s = ['config term','hostname '+ChangeName,'exit']
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1])
	ssh.sendline(list_s[2])
	ssh.prompt(timeout = 1)
	ssh.expect (r'.+')
def settime(ssh):
	s = 'clock set '
	hh = input('hour(0-23):')
	mm = input('minute(0-59):')
	ss = input('second(0-59):')
	day = input('day(1-31):')
	month = input('month(Jan-Dec):')
	year = input('year(1993-2035):')
	ssh.sendline(s+hh+':'+mm+':'+ss+' '+day+' '+month+' '+year)
	ssh.prompt(timeout=1)
	if output.find('Unrecognized')!=-1 or output.find('Invalid')!=-1:
		print ("Invalid input")
	ssh.expect(r'.+')
def vlanadd(ssh,vlan_id):
	list_s = ['config term','vlan ','exit','exit']
	if int(vlan_id) < 1 or int(vlan_id) > 4094:
		print ("Invalid id")
		return
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1]+vlan_id)
	ssh.sendline(list_s[2])
	ssh.sendline(list_s[3])
	ssh.prompt(timeout=1)
	ssh.expect(r'.+')
def vlandel(ssh,vlan_id):
	list_s = ['config term','no vlan ','exit']
	if int(vlan_id) < 2 or int(vlan_id) > 4094:
		print ("Invalid id")
		return
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1]+vlan_id)
	ssh.sendline(list_s[2])
	ssh.prompt(timeout=1)
	ssh.expect(r'.+')
def vlanset(ssh):
	interface = input("Interface(1-24):")
	vlan_id = input("vlan_id(1-4094):")
	list_s = ['config term','interface Gi0/'+interface,'switchport mode access','switchport access vlan ','end']
	if int(vlan_id) < 1 or int(vlan_id) > 4094:
		print ("Invalid id")
		return
	if int(interface) < 1 or int(interface) > 24:
		print ("Invalid interface")
		return
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1])
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	if output.find("Incomplete") != -1 or output.find("Invalid") != -1:
		print ("Invalid interface")
		ssh.sendline(list_s[4])
		ssh.expect(r'.+')
		return
	ssh.sendline(list_s[2])
	ssh.sendline(list_s[3]+vlan_id)
	ssh.sendline(list_s[4])
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	#print(output)
	ssh.expect(r'.+')
def trunk(ssh):
	list_s = ['config t','interface Gi0/','switchport mode trunk','switchport trunk allowed vlan add ','end']
	interface = input("Interface(1-24):")
	mode = input("add or remove(a/r)?")
	while mode not in 'ar':
		mode = input("add or remove(a/r)?")
	if mode == 'r':
		list_s[3] = 'switchport trunk allowed vlan remove '
	vlan_id = input("vlan_id(1-4094):")
	if int(vlan_id) < 1 or int(vlan_id) > 4094:
		print ("Invalid id")
		return
	if int(interface) < 1 or int(interface) > 24:
		print ("Invalid interface")
		return
	list_s[1] = list_s[1]+interface
	list_s[3] = list_s[3]+vlan_id
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1])
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	if output.find("Incomplete") != -1 or output.find("Invalid") != -1:
		print ("Invalid interface")
		ssh.sendline(list_s[4])
		ssh.expect(r'.+')
		return
	ssh.sendline(list_s[2])
	ssh.sendline(list_s[3])
	ssh.sendline(list_s[4])
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	ssh.expect(r'.+')
def setaccount(ssh,SwitchName):
	ChangeName = input("Username:")
	ChangePassword = getpass('Password:')
	list_s = ['sh ru | i user','configure term','username '+ChangeName+' priv 15 password '+ChangePassword,'no ','exit']
	ssh.sendline(list_s[0])
	ssh.prompt(timeout=1)
	user = ssh.before.decode('ascii')
	user = delete(user,'root')
	user = delete(user,list_s[0])
	user = delete(user,SwitchName)
	user = user.split('\n')[0]
	ssh.sendline(list_s[1])
	ssh.sendline(list_s[2])
	ssh.sendline(list_s[3]+user)
	ssh.sendline(list_s[4])
	ssh.prompt(timeout=1)
	ssh.expect(r'.+')
	ssh.logout()
def write(ssh):
	list_s = ['show boot','copy system:running-config ']
	ssh.sendline(list_s[0])
	ssh.prompt(timeout=1)
	fileName = ssh.before.decode('ascii')
	list_file = fileName.split('\n')
	for element in list_file:
		if element.find('Config file') != -1:
			fileName = element[22:]
			break
	#print (fileName)
	list_s[1]=list_s[1]+fileName
	ssh.sendline(list_s[1])
	ssh.sendline('')
	ssh.sendline('')
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	ssh.expect(r'.+')
def ping(ssh, ipAddr, count, interval, size, SwitchName):
	list_s = ['ping ip '+ipAddr+' repeat '+count+' timeout '+interval+' size '+size]
	ssh.sendline(list_s[0])
	output = ""
	index = 1
	while "Success" not in output and "%" not in output:
		if index % 2:
			print ("            ",end='\r')
			print ("ping....",end='\r')
		else:
			print ("pinging....",end='\r')
		index = index + 1
		ssh.prompt(timeout=0.5)
		output = ssh.before.decode('ascii')
	output = delete(output,list_s[0])
	output = delete(output,SwitchName)
	print (output)
	ssh.expect(r'.+')
def setportchannel(ssh):
	interfacerange_start = input("Configure interface from:")
	interfacerange_end = input("to:")
	channel = input("Assign the ports to a channel group (For channel group number, the range is 1 to 6):")
	list_s = ['config t','interface range Gi0/'+interfacerange_start+'-'+interfacerange_end, 'channel-group '+channel+' mode active','end']
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1])
	ssh.sendline(list_s[2])
	ssh.sendline(list_s[3])
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	#print(output)
	ssh.expect(r'.+')
def clearportchannel(ssh):
	channel = input("Enter port channel number:")
	list_s = ['config t','no interface Port-channel '+channel, 'exit']
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1])
	ssh.sendline(list_s[2])
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	if 'Invalid' in output:
		print ("Invalid port channel")
	#print(output)
	ssh.expect(r'.+')
def setportstatus(ssh,mode):
	interface = input("Enter the port number: ")
	list_s = ['config t','interface Gi0/'+interface,'shutdown','no shutdown','end']
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1])
	if mode == "d" :
		ssh.sendline(list_s[2])
	if mode == "e" :
		ssh.sendline(list_s[3])
	ssh.sendline(list_s[4])
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	#print(output)
	ssh.expect(r'.+')
def uploadconfig(ssh):
	username = input("Username:")
	password = getpass("Password:")
	host = input("Host:")
	filename = input("Filename:")
	if filename[:1] != '/':
		filename = '/' + filename
	list_s = ['copy ftp://'+username+':'+password+'@'+host+filename+' system:running-config','']
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1])
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	#print(output)
	ssh.expect(r'.+')
def downloadconfig(ssh):
	username = input("Username:")
	password = getpass("Password:")
	host = input("Host:")
	filename = input("Filename:")
	if filename[:1] != '/':
		filename = '/' + filename
	list_s = ['copy system:running-config ftp://'+username+':'+password+'@'+host+filename,'']
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1])
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	#print(output)
	ssh.expect(r'.+')
def setmgmtvlan(ssh,vlan_id,ip,mask,pre_vlan):
	list_s = ['configure term','interface vlan '+vlan_id,'ip address '+ip+' '+mask,'no shutdown','end']
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1])
	ssh.sendline(list_s[2])
	ssh.sendline(list_s[3])
	ssh.sendline(list_s[4])
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	ssh.expect(r'.+')
	if "Invalid" in output:
		print ("Invalid input")
	elif "overlaps" in output:
		print ("overlap with origin.")
	else:
		ssh.sendline("configure term")
		ssh.sendline("interface vlan "+pre_vlan)
		ssh.sendline("no ip address")
		ssh.close()
		sys.exit(0)

def showntp(ssh,SwitchName):
	list_s = ['show ntp status','show ntp associations']
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1])
	ssh.prompt(timeout = 1)
	output = ssh.before.decode('ascii')
	ssh.expect (r'.+')
	output = delete(output,list_s[0])
	output = delete(output,list_s[1])
	output = delete(output,SwitchName+'#')
	print (output)
	return output
def ntpenable(ssh):
	list_s = ['configure term','ntp authenticate','exit']
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1])
	ssh.sendline(list_s[2])
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	#print (output)
	ssh.expect(r'.+')
def ntpdisable(ssh):
	list_s = ['configure term','no ntp authenticate','exit']
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1])
	ssh.sendline(list_s[2])
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	#print (output)
	ssh.expect(r'.+')
def setntpserver(ssh,mode,ntp_server):
	list_s = ['configure term','ntp server '+ntp_server,'exit']
	if mode == 'd':
		list_s[1] = 'no '+list_s[1]
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1])
	ssh.sendline(list_s[2])
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	#print (output)
	ssh.expect(r'.+')
def showclock(ssh,SwitchName):
	s = 'show clock'
	ssh.sendline(s)
	ssh.prompt(timeout = 1)
	output = ssh.before.decode('ascii')
	ssh.expect (r'.+')
	output = delete(output,s)
	output = delete(output,SwitchName+'#')
	print (output)
def setnetwork(ssh, mgmt, mode):
	ip = ''
	if mode == 'static':
		ip = input('IP:')
	mask = input("subnet mask:")
	gateway = input("gateway:")
	list_s = ['configure term','ip default-gateway '+gateway,'interface vlan '+mgmt]
	ssh.sendline(list_s[0])
	ssh.sendline(list_s[1])
	ssh.sendline(list_s[2])
	if mode == 'dhcp':
		ssh.sendline("ip address dhcp")
	else:
		ssh.sendline("ip address "+ip+' '+mask)
	ssh.sendline("end")
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	ssh.expect(r'.+')
	print (output)
def delete(s,goal):
	temp_list = s.split('\n')
	str_out = ''
	for element in temp_list:
		if element.find(goal) == -1 and element != '\n':
			str_out = str_out + element
			str_out = str_out + '\n'
	return str_out
def getSwitchName(ssh):
	s = 'show ru'
	ssh.sendline(s)
	ssh.prompt(timeout = 1.5)
	output = ssh.before.decode('ascii')
	ssh.expect (r'.+')
	temp_list = output.split('\n')
	switchname=''
	for element in temp_list:
		if element.find('hostname') != -1:
			switchname = element[9:]
			break
	return switchname[:len(switchname)-1]
def VlanHasIP(ssh,vlan_id):
	ssh.sendline('show interface vlan '+vlan_id)
	ssh.prompt(timeout=1)
	output = ssh.before.decode('ascii')
	ssh.expect(r'.+')
	if 'Internet address is' in output:
		return 1
	else:
		return 0
def getTrunk(ssh):
	s = 'show interface trunk'
	ssh.sendline(s)
	ssh.prompt(timeout = 1)
	output = ssh.before.decode('ascii')
	ssh.expect (r'.+')
	output = delete(output,s)
	list_output = output.split('\n')
	final_list = []
	start = 1
	for element in list_output:
		if "spanning tree" in element:
			break
		elif start == 2:
			final_list.append(element)
		elif "allowed and active" in element:
			start = 2
	return final_list
def getPort(ssh,vlan_id):
	ssh.sendline("show vlan id "+vlan_id)
	ssh.prompt(timeout=0.5)
	output = ssh.before.decode('ascii')
	output_list = output.split('\r\n')
	ssh.expect(r'.+')
	judge = 1
	for element in output_list:
		if judge == 2:
			return element.split(' ')[-1]
			judge = 3
		elif "---- -------------------------------- --------- -------------------------------" in element:
			judge = 2
	#print(output)
