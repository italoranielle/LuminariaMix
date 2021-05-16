# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 20:57:44 2021

@author: pc_lab
"""
import numpy as np
import wave
import pyaudio
import socket
import threading



class ToRGB:
    
    def __init__(self):
        self.RATE=22000
        self.CHUNKSIZE = 256
        self.ip = '192.168.4.1'
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.p = pyaudio.PyAudio()
        self.playing = False
        
    
    def sendUDP(self,msg,host):
        dstHost = (host, 3333)
        self.udp.sendto(msg.encode(), dstHost)
        
    
    def Dfft(self,s):
        fft = np.fft.fft(s)
        N = int(s.size/2)
        absFFT = np.abs(fft)
        
        r = "{:03.0f}".format( (np.average(absFFT[5:int(N/3)]) *255)/160000 )
        g = "{:03.0f}".format( (np.average(absFFT[int(N/3):int((N/3)*2)]) *255)/160000 )
        b = "{:03.0f}".format( (np.average(absFFT[int((N/3)*2):N]) *255)/160000 )
        
        self.sendUDP(r+g+b,self.ip)
    
    

    def readMic(self):
        self.playing = True
        stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True, frames_per_buffer=self.CHUNKSIZE)
        while(True):
            data = stream.read(self.CHUNKSIZE)
            data = np.fromstring(data, dtype=np.int16)
            self.Dfft(data)
            if not self.playing:
                break
            
        stream.start_stream() 
        stream.close()
        self.playing= False
        
    
    def readFile(self,arquivo):
        self.playing = True
        wf = wave.open(arquivo, 'rb' )
        stream  = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                         channels=wf.getnchannels(),
                         rate=wf.getframerate(),
                         output=True
                         )
        data = wf.readframes(self.CHUNKSIZE)
        while data != '':
            stream.write(data)
            self.Dfft(np.fromstring(data, dtype=np.int16))
            data = wf.readframes(self.CHUNKSIZE)
            if  not self.playing:
                break
        stream.start_stream()
        stream.close()
        self.playing = False
    
    def setPause(self):
        self.playing = False
    
    def playMic(self):
        if self.playing:
            self.setPause()
        else:
            t = threading.Thread(target=self.readMic)
            t.start()

    def playFile(self,arquivo):
        if self.playing:
            self.setPause()
        else:
            t = threading.Thread(target=self.readFile,args=(arquivo,))
            t.start()
    
        
    
#a = ToRGB()
#a.readMic()