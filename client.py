#!/usr/bin/env python

############################
## Remove *.pyc files
############################
import os

def remove_pyc(dir = '.'):
	directory = os.listdir(dir)
	for file in directory:
		path = dir + '/' + file
		if os.path.isdir(path) and file not in ['.', '..']:
			remove_pyc(path)
		elif file[-4:] == '.pyc':
			os.remove(path)

############################
## MAIN
############################

import optparse
from src.sessionmanager import SessionManager
#from src.sessionmanager import *

op = optparse.OptionParser(version="%prog 0.1")
op.add_option("-u", "--username", help="spotify username")
op.add_option("-p", "--password", help="spotify password")
(options, args) = op.parse_args()

if not options.username or not options.password:
	op.print_help()
	remove_pyc()
	raise SystemExit
	
s = SessionManager(options.username, options.password)
s.connect()

remove_pyc()
