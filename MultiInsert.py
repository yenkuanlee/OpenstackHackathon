from influxdb import InfluxDBClient
import random
import sys
from multiprocessing import Pool

number = int(sys.argv[1])

f = open('servers','r')
client = dict()
servers = list()
cnt = 0
while True:
	line = f.readline()
	if not line:
		break
	cnt += 1
	sip = line.replace("\n","")
	servers.append(sip)

def DataGeneration(id):
	measurement = 'cpu'
	tags = dict()
	fields = dict()
	tags['id'] = str(id)
	fields['value'] = random.uniform(0, 1)
	return {"measurement":measurement,"tags":tags,"fields":fields}

def GetJsonArray(num):
	l = list()
	for i in range(num):
		l.append(DataGeneration(i))
	return l

def chunks(l, n):
	tmp = list()
	for i in xrange(0, len(l), n):
		tmp.append(l[i:i+n])
	return tmp
	
def InfoGeneration():
	L = list()
	J = GetJsonArray(number)
	size = number/cnt
	if number%cnt != 0:
		size += 1
	a = chunks(J,size)
	for i in range(len(a)):
		L.append([servers[i],a[i]])
	return L
	
def ParallelInsert(info):
	server = info[0]
	J = info[1]
	client = InfluxDBClient(server, 8086, 'root', 'root', 'example')
	try:
		client.create_database('example')
	except:
		pass
	client.write_points(J)

infoList = InfoGeneration()
p = Pool(cnt)
p.map(ParallelInsert,infoList)