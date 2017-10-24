import pyaudio
import struct
import socket
from opuslib.api import constants, decoder, encoder
from opuslib.exceptions import OpusError
from opuslib.api import ctl as opus_ctl

FORMAT = pyaudio.paInt16 
CHANNELS = 1
RATE = 48000
INPUT_BLOCK_TIME = 0.02
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
UDP_IP = "2620:0:e50:1400:5588:5e9d:39dc:f170"
UDP_PORT = 8000

sock = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
audio = pyaudio.PyAudio()
stream = audio.open(format = FORMAT, channels = CHANNELS, rate=RATE, input = True, frames_per_buffer = 50*INPUT_FRAMES_PER_BLOCK)
#streamout = audio.open(format = FORMAT, channels = CHANNELS, rate= RATE,output=True, frames_per_buffer = INPUT_FRAMES_PER_BLOCK)
enc = encoder.create(RATE,CHANNELS,constants.APPLICATION_VOIP)
# disable variable bitrate (VBR)
encoder.ctl(enc,opus_ctl.set_vbr,0)


errorCount = 0
i = 0
while(1):
	try:
		raw_data = stream.read(INPUT_FRAMES_PER_BLOCK)
		
		i+=1
		print i
		encdata = ""
		#for x in raw_data:
		print "The length of the raw_data"
		print len(raw_data)
		encdata = encoder.encode(enc,raw_data,INPUT_FRAMES_PER_BLOCK, 128)
		serial = struct.pack('q',i)
		print len(encdata)

		sock.sendto(serial+encdata,(UDP_IP,UDP_PORT))

		#stream.close()
	except IOError, e:
		errorCount += 1
		print("(%d) Error recording: %s" %(errorCount, e))




