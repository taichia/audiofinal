import pyaudio
import wave

old = ""

def play(file_):
        wf = wave.open(file_, 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=2,
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(1024)

        while data != '':
            stream.write(data)
            data = wf.readframes(1024)

        stream.stop_stream()
        stream.close()

        p.terminate()

import serial
import sys
import time
from struct import pack
from math import sin, pi
import wave
port = '/dev/serial/by-id/usb-SEGGER_J-Link_000760008519-if00'
deca = serial.Serial(port,115200,timeout=5)

def read_serial():
    deca.reset_output_buffer()
    deca.readline()
    deca.readline()
    deca.readline()
    deca.readline()
    return deca.readline()

def audio(left, right, file_name):
    RATE=44100
    maxVol=32767.0 #maximum amplitude
    freq = 2000
    wv = wave.open(file_name, 'w')
    wv.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
    avg = (left + right)/2
    delta = abs(left - right)
    if left < avg:
        left -= delta
        right += delta
    else:
        left += delta
        right -= delta
    if left < 1:
        left = 1.0
    if right < 1:
        right = 1.0
    wvData=""
    for i in range(0, int(RATE/4)):
        wvData+=pack('h', (maxVol/(right**2))*sin(i*freq/RATE)) #500Hz left
        wvData+=pack('h', (maxVol/(left**2))*sin(i*freq/RATE)) #200Hz right
    wv.writeframes(wvData)
    wv.close()

while(True):
    d = read_serial()
    while old == d:
        d = read_serial()
    old = d
    d = d.decode("utf-8")
    d = d.rstrip()
    print(d)
    d1, d2 = d.split(" ")
    _,d1 = d1.split(":")
    _,d2 = d2.split(":")
    d1 = float(d1)
    d1 *= 2
    print(d1)
    d2 = float(d2)
    d2 *= 2
    print(d2)
    if d1 < 1:
        d1 = 1.0
    if d2 < 1:
        d2 = 1.0
    audio(d1, d2, 'test.wav')
    play('test.wav')
