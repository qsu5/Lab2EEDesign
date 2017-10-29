import pyaudio
import struct
import socket
from opuslib.api import constants,decoder
from opuslib.exceptions import OpusError
import threading
import Queue
import heapq
import time
import sys

###############receiving################
class recvAndDecode(threading.Thread): 
	def __init__(self, sock, dec,buf):
		threading.Thread.__init__(self)
		self.sock = sock
		self.dec = dec
		self.buf = buf

	def run(self):	
		while True:
			data = sock.recvfrom(INPUT_FRAMES_PER_BLOCK) # buffer size is 1024 bytes
			try:
				assert len(data[0]) == 136
				(serial,)=struct.unpack('q',data[0][:8])
				raw_audio = decoder.decode(dec,data[0][8:],len(data[0][8:]),INPUT_FRAMES_PER_BLOCK, False, 1)
				#try:
				if len(buf)<MAX_BUFF_SIZE:
					heapq.heappush(buf,((serial,raw_audio)))
				else:
					heapq.heappop(buf)
					heapq.heappush(buf,((serial,raw_audio)))
				print "receiving and push to jb",serial
				#print len(buf)
				#except 

				#print "Raw Data: ",raw_audio
				
			except AssertionError:
				print 'Didn\'t get full packet!'
				sys.exit(1)
class playOut(threading.Thread):
	def __init__(self,streamout,buf):
		threading.Thread.__init__(self)
		self.streamout=streamout
		self.buf = buf

	def run(self):
		while True:
			currentSerial = 0
			if len(buf)>0:
				(serial,raw_audio) = heapq.heappop(buf)
				if currentSerial < serial:
					print "getting from", serial
					currentSerial = serial
					streamout.write(raw_audio)


FORMAT = pyaudio.paInt16 
CHANNELS = 1
RATE = 48000
INPUT_BLOCK_TIME = 0.02
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
UDP_IP = ""
UDP_PORT = 8001
MAX_BUFF_SIZE = 5

sock = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
sock.bind(("",UDP_PORT))
audio = pyaudio.PyAudio()
streamout = audio.open(format = FORMAT, channels = CHANNELS, rate= RATE, output=True, frames_per_buffer = INPUT_FRAMES_PER_BLOCK*5)
dec = decoder.create(RATE,CHANNELS)

buf=[]
# heapq.heapify(buf)
# heapq._heapify_max(buf)

a=recvAndDecode(sock,dec,buf)
a.daemon = True
b=playOut(streamout,buf)
b.daemon = True
a.start()
b.start()

while True:
    time.sleep(1)
	