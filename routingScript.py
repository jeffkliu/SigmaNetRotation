### Re-doing the lab from scratch
#!/usr/bin/env python

import sys
import json
import types
import device
import xmltodict
import collections
from device import *
#import cli
#from cli import *

#Can take arguments
args = sys.argv

globaltable = []

def router_list():

	"""This method returns three dicts that contain attributes of a specific/
	router"""

	router1 = dict(os_version = '3.1.1.1', hostname = 'sf_router', model = 'nexus 9396',
	domain = 'cisco.com', mgmt_ip = '10.1.50.11' )

	router2 = dict(os_version = '3.1.1.1', hostname = 'nyc_router', model = 'nexus 9396',
	domain = 'cisco.com', mgmt_ip = '10.2.50.11' )

	router3 = dict(os_version = '3.1.1.1', hostname = 'sjc_router', model = 'nexus 9396',
	domain = 'cisco.com', mgmt_ip = '10.3.50.11' )

	router4 = dict(os_version = '3.1.1.1', hostname = 'sd_router', model = 'nexus 9396',
	domain = 'cisco.com', mgmt_ip = '10.4.50.11' )

	router5 = dict(os_version = '3.1.1.1', hostname = 'la_router', model = 'nexus 9396',
	domain = 'cisco.com', mgmt_ip = '10.5.50.11' )

	router6 = dict(os_version = '3.1.1.1', hostname = 'oc_router', model = 'nexus 9396',
	domain = 'cisco.com', mgmt_ip = '10.6.50.11' )

	neighbors = [router4, router6, router6]

	router1['neighbors'] = neighbors

	allrouter = [router1, router2, router3]

	print isinstance(router1, dict)
	return allrouter

def getRouter(rtr, list_router ):

	"""This method returns a specific router in the dict/
	given the hostname of router"""
	
	allrouter = list_router

	for router in allrouter:
		for key, value in router.iteritems():
			if key == 'neighbors':
				for each in value:
					if each['hostname'] == rtr:
						return each
			else: 
				if value == rtr:
					return router

	return "No such router"

def print_in_json(dict):
	""" print in json """
	print json.dumps(dict, indent = 4)

def get_os_version(rtr, router_list):

	"""This method returns a specific os_version of a router in the dict/
	given the hostname of router"""

	for router in router_list:
		if router['hostname'] == rtr:
			return router['os_version']
	return "no such router"

def get_model(rtr, router_list):

	"""This method returns a specific model of a router in the dict/
	given the hostname of router"""

	for router in router_list:
		if router['hostname'] == rtr:
			return router['model']
	return "no such router"

def get_domain(rtr, router_list):

	"""This method returns a specific domain of a router in the dict/
	given the hostname of router"""

	for router in router_list:
		if router['hostname'] == rtr:
			return router['domain']
	return "no such router"

def get_mgmt_ip(rtr, router_list):

	"""This method returns a specific mgmt_ip of a router in the dict/
	given the hostname of router"""

	for router in router_list:
		if router['hostname'] == rtr:
			return router['mgmt_ip']
	return "no such router"

def open_switch(ip_addr = None, username= None, password=None):
	
	"""this method opens switch with three params"""
	if ip_addr is None and username is None and password is None:
		ip_addr = '172.31.217.142'
		username = 'admin'
		password = 'cisco123'


	sw1 = Device(ip = ip_addr,username = username,password = password)
	sw1.open()

	return sw1

def show_cmd(sw, port = None, vlan = None, show_cmd = None):
	""" show cmds table in json """
	table = {}

	if port is not None:
		if port.startswith('Ethernet'):
			command = sw.show('show interface ' + port)
			table = xmltodict.parse(command[1])
	elif vlan is not None:
		if isinstance(vlan, int):
			table = xmltodict.parse(sw.show('show vlan ' + str(vlan))[1])
		else:
			table = xmltodict.parse(sw.show('show vlan')[1])
	elif show_cmd is not None:
		table = xmltodict.parse(sw.show(show_cmd)[1])
	else:
		table = xmltodict.parse(sw.show('show interface')[1])

	#print_in_json(table)
	return table

def learning_generator():
	""" just learning generator so I can parse through a dictionary """
	mylist = range(3)
	for i in mylist:
		yield i*i

### size of dict choose greatest
size_of_list = 0

def parse_dict(table):
	""" this function parses through dicts and finds the right element"""
	global size_of_list
	global globaltable

	if type(table) == list:
		globaltable = table
		return table

	for key, value in table.iteritems():
		if len(value) >= 1 and type(value) is collections.OrderedDict:
			parse_dict(value)
		elif type(value) is list:
			if(len(value[0]) > size_of_list):
				size_of_list = len(value[0])
				parse_dict(value)

	return globaltable

def list_table_options(table):
	"""takes in a list and gives"""




if __name__ == "__main__":

	flag = False
	table = show_cmd(open_switch(), show_cmd = 'show vlan')
	print table
	final_table = parse_dict(table)



	for each in final_table:
		print 'VLAN ID: ', each['vlanshowbr-vlanid-utf']
		print 'VLAN NAME: ', each['vlanshowbr-vlanname']
		print '=' * 25





	if flag == True:
		if args[1] == 'False':
			show_cmd(open_switch(), show_cmd = 'show vlan')
		else:
			if len(args) == 1:
					print "Enter at least one argument. Try again"
					exit()
			else:
				for i in range (0, len(args)):
					if(i != 0):
						print getRouter(args[i], router_list())	

				
		

