# Lab2
# Ahmed Elmaleh, Qingyang Su
# See LICENSE for details
# 2017-10-16

"""Transmit Audio"""
import pyaudio
import opuslib
import audioop
import wave


chunk = 1920
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000
RECORD_SECONDS = 120
WAVE_OUTPUT_FILENAME = "./a_test_2.wav"

p = pyaudio.PyAudio()


s = p.open(format = FORMAT,
       channels = CHANNELS,
       rate = RATE,
       input = True,
       frames_per_buffer = chunk)
print s


print("---recording---")

d = []

print((RATE / chunk) * RECORD_SECONDS)

for i in range(0, (RATE // chunk * RECORD_SECONDS)):
    print s.read(chunk)
    data = s.read(chunk)
    d.append(data)
    mx = audioop.max(data, 2)
    print mx
    #s.write(data, chunk)

print("---done recording---")

s.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(d))
wf.close()