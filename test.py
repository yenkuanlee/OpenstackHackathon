import os
import random
import time
#for i in range(60):
while True:
	os.system("python influx.py "+str(random.randint(10,20))+" &")
	time.sleep(5)