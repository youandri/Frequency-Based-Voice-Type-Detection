from tkinter import *
import pyaudio
import wave
import numpy as np
from pydub import AudioSegment
import threading as tr

class Nlp():
    def __init__(self, master):
        self.recordBtn = PhotoImage(file='mic.gif')
        self.stopBtn = PhotoImage(file='stop.gif')
        self.status = False
        self.recordTrigger = Button(main,image=self.recordBtn)
        self.recordTrigger.image=self.recordBtn
        self.recordTrigger.grid(row=1,column=1)
        self.recordTrigger.bind("<Button-1>", self.Rekam)

    def Rekam(self, event):
        self.CHUNK = 2048
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 11000
        self.RECORD_SECONDS = 10
        self.WAVE_OUTPUT_FILENAME = "output.wav"
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        self.recordTrigger.bind("<Button-1>", self.Berhenti)
        self.status = True
        t = tr.Thread(target=self._Rekam)
        t.start()

    def Berhenti(self, event):
        self.status = False
        self.recordTrigger.bind("<Button-1>", self.Rekam)

    def _Rekam(self):
        self.frames = []
        while self.status:
            self.data = self.stream.read(self.CHUNK)
            self.frames.append(self.data)
            print("Recording")

main = Tk()
nlp = Nlp(main)
main.config(bg='#3498db')
main.geometry('500x130')
main.title('Frequency Based Voice Type Detection')
main.mainloop()
