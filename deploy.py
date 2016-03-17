import os
import sys
hostname = sys.argv[1]
passwd = sys.argv[2]

def peer_generation(input):
	if input=="" : return ""
	return input.replace(",",":8088,")+":8088,"
	
def onedragon(hostname,done_list,ip_list):
	IpList = ip_list.split(",")
	ip_peer = peer_generation(done_list)
	for ip in IpList:
		cmd = ""
		# install
		###cmd += "cd /tmp/Package;"
		###cmd += "echo '"+passwd+"' | sudo -S pip install influxdb;"
		cmd += "wget https://s3.amazonaws.com/influxdb/influxdb_0.9.6.1_amd64.deb;"
		cmd += "echo '"+passwd+"' | sudo -S dpkg -i influxdb_0.9.6.1_amd64.deb;"
		
		# config
		cmd += "echo '"+passwd+"' | sudo -S sed -i 's/localhost/"+ip+"/g' /etc/influxdb/influxdb.conf;"
		cmd += "sudo sed -i 's/\":8088\"/\""+ip+":8088\"/g' /etc/influxdb/influxdb.conf;"
		cmd += "echo '"+passwd+"' | sudo -S sed -i 's/start-stop-daemon --chuid/start-stop-daemon --background --chuid/g' /etc/init.d/influxdb;"
	
		# set peers
		if ip_peer != "":
			peers = ip_peer[:len(ip_peer)-1]
			OPTS = "INFLUXD_OPTS=\\\"-hostname "+ip+" -join "+peers+"\\\""
			cmd += "echo '"+OPTS+"' > influxdb;"
			cmd += "echo '"+passwd+"' | sudo -S mv influxdb /etc/default;"
			
		# start influx
		cmd += "sudo /etc/init.d/influxdb start;"
		cmd += "sudo rm /var/run/influxdb/influxd.pid;"
		cmd += "sudo /etc/init.d/influxdb restart;"
		os.system("sshpass -p '"+passwd+"' ssh -o StrictHostKeyChecking=no "+hostname+"@"+ip+" -t \""+cmd+"\"")
		ip_peer += ip+":8088,"
	
os.system("echo '"+passwd+"' | sudo -S apt-get install sshpass -y")

try:
	onedragon(sys.argv[1],sys.argv[3],sys.argv[4])
	IpList = sys.argv[4].split(",")
	for x in IpList:
		os.system("echo '"+x+"' >> servers")
	
except:
	IpList = sys.argv[3].split(",")
	os.system("echo '"+IpList[0]+"' > master")
	os.system("rm -rf servers")
	for x in IpList:
		os.system("echo '"+x+"' >> servers")
	onedragon(sys.argv[1],"",sys.argv[3])