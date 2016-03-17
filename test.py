from influxdb import InfluxDBClient
import os
client = InfluxDBClient('172.16.8.5', 8086, 'root', 'root', 'example')
try:
	client.create_database('example')
except:
	pass
	
def ServerInfo():
	result = client.query("show servers")
	for x in result:
		for y in x:
			print y['cluster_addr'].split(":")[0],y['id']
			
def GetServerID(ip):
	result = client.query("show servers")
	for x in result:
		for y in x:
			if y['cluster_addr'].split(":")[0] == ip:
				return str(y['id'])
	return "Null"
	
def DropServer(ip):
	os.system("sed -i '/"+ip+"/d' servers")
	sid = GetServerID(ip)
	if sid == "Null" :
		return "No Such Server"
	result = client.query("drop server "+sid+" force")
	return sid
			
#ServerInfo()

#print GetServerID("172.16.8.7")
print DropServer("172.16.8.7")