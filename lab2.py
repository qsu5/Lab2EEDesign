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
UDP_IP = "2620::e50:1400:64f3:9ac8:f4bd:fbd3"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
audio = pyaudio.PyAudio()
stream = audio.open(format = FORMAT, channels = CHANNELS, rate=RATE, input = True, frames_per_buffer = INPUT_FRAMES_PER_BLOCK)
streamout = audio.open(format = FORMAT, channels = CHANNELS, rate= RATE,output=True, frames_per_buffer = INPUT_FRAMES_PER_BLOCK)
# enc = Encoder(RATE,CHANNELS,constants.APPLICATION_VOIP)
# dec = Decoder(RATE,CHANNELS,)


errorCount = 0
i = 0
while(1):
	try:
		raw_data = stream.read(INPUT_FRAMES_PER_BLOCK)
		serial = struct.pack('q',i)
		sock.sendto(serial+raw_data,(UDP_IP,UDP_PORT))
		i+=1
		# encdata = []
		# for x in data:
		# 	encdata.append(Encoder.encode(enc,x,INPUT_BLOCK_TIME))
		# decdata = ''
		# for x in encdata:
		# 	decdata += Decoder.decode(dec,x,INPUT_BLOCK_TIME)

		# streamout.write(decdata)
		streamout.close()
		stream.close()
	except IOError, e:
		errorCount += 1
		print("(%d) Error recording: %s" %(errorCount, e))




