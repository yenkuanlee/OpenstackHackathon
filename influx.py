from influxdb import InfluxDBClient
import random
import sys
client = InfluxDBClient('172.16.8.5', 8086, 'root', 'root', 'example')
try:
	client.create_database('example')
except:
	pass

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

	
#print GetJsonArray(10)
#print DataGeneration(1)

J = GetJsonArray(int(sys.argv[1]))
client.write_points(J)
print J

#client.write_points([DataGeneration(5)])


'''
l = list()
	
tags = dict()
tags['host'] = 'server04'
tags['region'] = 'taiwan'
fields = dict()
fields['values'] = 0.01
record1 = {"measurement":"cpu_load_short","tags":tags,"fields":fields}
l.append(record1)

tags = dict()
tags['host'] = 'server05'
tags['region'] = 'taiwan'
fields = dict()
fields['values'] = 0.01
record2 = {"measurement":"cpu_load_short","tags":tags,"fields":fields}
l.append(record2)

#json_body=[{"measurement":"cpu_load_short","tags":tags,"fields":fields}]
client.write_points(l)
'''