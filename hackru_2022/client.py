from network import Network
import time

n = Network()

n.connect()
while 1:
	n.send("Get fucked")
	print("sent")
	time.sleep(10)