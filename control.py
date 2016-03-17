import os
import sys
hostname = sys.argv[1]
passwd = sys.argv[2]
ips = sys.argv[3]
passwd = 'kuan23028004052260'
def GetServerList():
	try:
		f = open('servers','r')
	except:
		return ""
	Slist = list()
	X = ""
	while True:
		line = f.readline()
		if not line:
			break
		Slist.append(line.replace("\n",""))
		X += line.replace("\n","")+","
	return X[:len(X)-1]
	
servers = GetServerList()
if servers == "":
	os.system("python deploy.py "+hostname+" "+passwd+" "+ips)
else:
	os.system("python deploy.py "+hostname+" "+passwd+" "+servers+" "+ips)