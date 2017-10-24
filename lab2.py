import pyaudio
import struct
import socket
from opuslib import Encoder, Decoder
from opuslib.api import constants
from opuslib.exceptions import OpusError

FORMAT = pyaudio.paInt16 
CHANNELS = 1
RATE = 48000
INPUT_BLOCK_TIME = 0.02
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
UDP_IP = "2620:0:e50:1400:70cf:621c:8b4c:7bd9"
UDP_PORT = 8000

sock = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
audio = pyaudio.PyAudio()
stream = audio.open(format = FORMAT, channels = CHANNELS, rate=RATE, input = True, frames_per_buffer = 50*INPUT_FRAMES_PER_BLOCK)
#streamout = audio.open(format = FORMAT, channels = CHANNELS, rate= RATE,output=True, frames_per_buffer = INPUT_FRAMES_PER_BLOCK)
enc = Encoder(RATE,CHANNELS,constants.APPLICATION_VOIP)



errorCount = 0
i = 0
while(1):
	try:
		raw_data = stream.read(INPUT_FRAMES_PER_BLOCK)
		
		i+=1
		print i
		encdata = ""
		for x in raw_data:
			encdata += Encoder.encode(enc,x,INPUT_FRAMES_PER_BLOCK)
		serial = struct.pack('q',i)
		print len(encdata)

		sock.sendto(serial+encdata,(UDP_IP,UDP_PORT))

		#stream.close()
	except IOError, e:
		errorCount += 1
		print("(%d) Error recording: %s" %(errorCount, e))




