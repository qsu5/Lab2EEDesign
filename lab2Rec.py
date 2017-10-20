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
sock.bind((UDP_IP,UDP_PORT))
audio = pyaudio.PyAudio()

streamout = audio.open(format = FORMAT, channels = CHANNELS, rate= RATE, output=True, frames_per_buffer = INPUT_FRAMES_PER_BLOCK)

###############receiving################3
sock.bind((UDP_IP, UDP_PORT))
    
while True:
	data, addr = sock.recvfrom(INPUT_FRAMES_PER_BLOCK*2) # buffer size is 1024 bytes
	print data
	while len(data) > 0:
		streamout.write(data)
	