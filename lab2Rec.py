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
UDP_IP = ""
UDP_PORT = 8000

sock = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
sock.bind(("",UDP_PORT))
audio = pyaudio.PyAudio()

streamout = audio.open(format = FORMAT, channels = CHANNELS, rate= RATE, output=True, frames_per_buffer = INPUT_FRAMES_PER_BLOCK*50)
dec = Decoder(RATE,CHANNELS)

###############receiving################
    
while True:
	data, addr = sock.recvfrom(INPUT_FRAMES_PER_BLOCK) # buffer size is 1024 bytes
	print "Raw Data: ",data
	while len(data) > 0:
		print "data"
		decdata = []
		for x in data:
			decdata.append(Decoder.decode(dec,x,INPUT_FRAMES_PER_BLOCK))
		streamout.write(decdata)
		data = []
	