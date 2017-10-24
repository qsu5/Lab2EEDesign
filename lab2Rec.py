import pyaudio
import struct
import socket
from opuslib.api import constants,decoder
from opuslib.exceptions import OpusError
import sys

FORMAT = pyaudio.paInt16 
CHANNELS = 1
RATE = 48000
INPUT_BLOCK_TIME = 0.02
INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)
UDP_IP = ""
UDP_PORT = 8000

sock = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
sock.bind(("",UDP_PORT))
audio = pyaudio.PyAudio()

streamout = audio.open(format = FORMAT, channels = CHANNELS, rate= RATE, output=True, frames_per_buffer = INPUT_FRAMES_PER_BLOCK*50)

dec = decoder.create(RATE,CHANNELS)

###############receiving################
    
while True:
	data = sock.recvfrom(136) # buffer size is 1024 bytes
	print len(data)
	try:
		assert len(data) == 136
	except AssertionError:
		print 'Didn\'t get full packet!'
		#sys.exit(1)
	(serial,)=struct.unpack('q',data[:8])
	raw_audio = decoder.decode(dec,data[8:],INPUT_FRAMES_PER_BLOCK)
	print "Raw Data: ",raw_audio
	streamout.write(raw_audio)

	