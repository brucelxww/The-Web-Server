import sys
import socket
import os
import codecs
import gzip

def main():
	# missing file argument
	if (len(sys.argv)!=2):
		print("Missing Configuration Argument")
		sys.exit()
	try:
		configfile=open(sys.argv[1],'r')
	except FileNotFoundError:   # file not found
		print("Missing Field From Configuration File")
		sys.exit()
	# read config content
	line=configfile.readline().strip('\n')
	staticfiles=""
	cgibin=""
	port=""
	exec=""
	count=0
	while line:
		if(line[0:3]=="sta"):
			staticfiles=line.split("=./")[1]
		if(line[0:3]=="cgi"):
			cgibin=line.split("=./")[1]
		if(line[0:3]=="por"):
			port=line.split("=")[1]
		if(line[0:3]=="exe"):
			exec=line.split("=")[1]
		line=configfile.readline().strip('\n')
		count+=1
	# miss content in config file
	if count!=4 or staticfiles=="" or cgibin=="" or port=="" or exec=="":
		print("Missing Field From Configuration File")
		sys.exit()
	# create socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	sock.bind(('', int(port)))
	sock.listen()
	# continusly accept connection
	while True:
		conn, addr = sock.accept()
		# parse request
		data = conn.recv(1024) 
		string=data.decode()
		split=string.split( )
		if(split!=[]):
			count=0
			a=split[0]+split[1]
			html=a.split("GET")[1]
			i=0
			while(i<len(html)):
				if html[i]=="/":
					count+=1
				i+=1
		# some basic variable for after coding
		header="empty"
		contype="empty"
		senddata="empty"
		Gzip=False
		# special situation: ask for gzip file
		for line in split:
			if "gzip" in line:
				Gzip=True
		# request static file
		if count<=1: 
			try:
				# special case
				if html=="/":
					html="/index.html"
				header="HTTP/1.1 200 OK".encode()
				# check content type
				if "txt" in html:
					contype="Content-Type: text/plain"
				if "html" in html:
					contype="Content-Type: text/html"
				if "js" in html:
					contype="Content-Type: application/javascript"
				if "css" in html:
					contype="Content-Type: text/css"
				if "png" in html:
					contype="Content-Type: image/png"
				if "jpg" in html or "jpeg" in html:
					contype="Content-Type: image/jpeg"
				if "xml" in html:
					contype="Content-Type: text/xml"
				# check gzip 
				if Gzip==True:
					contype="Content-Type: gzip"
				contypesend=(contype).encode()
			    # normal file
				if not "image" in contype:
					if Gzip==False:
						f=open(staticfiles+html, 'r')
						senddata=(f.read().encode())
					else:
						f=open(staticfiles+html, 'r')
						binarydata=(bytes(f.read(), 'UTF-8'))
						senddata=gzip.compress(binarydata)
				# image file
				else:
					f=open(staticfiles+html, 'rb')
					senddata=f.read()
			# file not found ,send 404 html
			except FileNotFoundError:
				header="HTTP/1.1 404 File not found".encode()
				contypesend=(contype).encode()
				senddata=("<html>\n<head>\n\t<title>404 Not Found</title>\n</head>\n<body bgcolor=\"white\">\n<center>\n\t<h1>404 Not Found</h1>\n</center>\n</body>\n</html>\n".encode())
		# request cgi program 
		if count==2:
			# set environment variables
			os.environ["SERVER_ADDR"]=addr[0]
			os.environ["SERVER_PORT"]=split[4].split(":")[1]
			os.environ["REQUEST_METHOD"]=split[0]
			os.environ["REQUEST_URI"]=split[1]
			if "?" in html:
				os.environ["QUERY_STRING"]=html.split("?")[1]
			# set variables for piping
			STDIN=0
			STDOUT=1
			STDERR=2
			html="/"+html.split("/")[2]
			# piping and fork
			reading, writing=os.pipe()
			pid=os.fork() 
			if pid==0:
				# child process
				os.close(reading)
				os.dup2(writing,STDOUT)
				try:
					if not "?" in html:
						os.execle(exec,"python3",cgibin+html,os.environ)
					else:
						os.execle(exec,"python3",cgibin+html.split("?")[0],os.environ)
				except:
					os._exit(1)
			elif pid==-1:
				sys.exit(1)
			else:
				# parent process
				wval=os.wait()
				os.close(writing)
				os.dup2(reading,STDIN)
			# some boolean variable for checking data
			havecontenttype=False
			customstatus=False
			# all goes well
			if(wval[1]==0):
				# read data
				f = open(reading)
				data= f.read().strip("\n")
				split=data.split()
				statuscode="statuscode"
				for line in split:
					if "Content-Type" in line:
						havecontenttype=True
					if "Status-Code" in line:
						customstatus=True
						statuscode=split[split.index(line)+1]
						split.remove(line)
				# check gzip
				if Gzip==False:
					senddata=data.encode()
				else:
					binarydata=(bytes(data, 'UTF-8'))
					senddata=gzip.compress(binarydata)
			# some error happens when exec the file
			else:
				senddata=("<html>\n<head>\n\t<title>505 Not Found</title>\n</head>\n<body bgcolor=\"white\">\n<center>\n\t<h1>505 Not Found</h1>\n</center>\n</body>\n</html>\n".encode())
		if senddata=="empty":
			break
		# send static file data to client
		if count<=1:
			conn.sendall(header)
			conn.sendall("\n".encode())
			conn.sendall(contypesend)
			conn.sendall("\n\n".encode())
			conn.sendall(senddata)
		# send cgi program data to client
		if count==2:
			# no error when exec the file
			if(wval[1]==0):
				if customstatus==False:
					conn.sendall("HTTP/1.1 200 OK\n".encode())
				else:
					header="HTTP/1.1 {} Custom Status\n".format(statuscode)
					conn.sendall(header.encode())
				# check whether the content type is gzip
				if havecontenttype==False and Gzip==False:
					conn.sendall("Content-Type: text/html".encode())
					conn.sendall("\n\n".encode())
				elif havecontenttype==False and Gzip==True:
					conn.sendall("Content-Type: gzip".encode())
					conn.sendall("\n\n".encode())
				conn.sendall(senddata)
				conn.sendall("\n".encode())
			# error happens when exec the file
			if(wval[1]!=0):
				conn.sendall("HTTP/1.1 500 Internal Server Error\n".encode())
				conn.sendall("Content-Type: text/html\n\n".encode())
				conn.sendall(senddata)
		# close connection
		conn.close()

	pass



if __name__ == '__main__':
	main()