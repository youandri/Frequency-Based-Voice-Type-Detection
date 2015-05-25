# Warning! Pseudo-OOP, Procedural with OOP Style ^_^, honestly i'm not expert with Object Oriented Programming

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
        self.recordTrigger.config(image=self.stopBtn)
        self.recordTrigger.image=self.stopBtn
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
        self.recordTrigger.config(image=self.recordBtn)
        self.recordTrigger.image=self.recordBtn
        self.recordTrigger.bind("<Button-1>", self.Void)
        self.recordTrigger.config(state=DISABLED)
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        self.wf.setnchannels(self.CHANNELS)
        self.wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        self.wf.setframerate(self.RATE)
        self.wf.writeframes(b''.join(self.frames))
        self.wf.close()
        self.process()
       
    def sr_(self):
        #Silence Removal
        def detect_leading_silence(sound):
            chunk_size=0.1
            silence_threshold=-25.0
            trim_ms = 0
            while sound[trim_ms:trim_ms + chunk_size].dBFS < silence_threshold:
                trim_ms += chunk_size
            return trim_ms
        sound = AudioSegment.from_file("output.wav", format="wav")
        start_trim = detect_leading_silence(sound)
        end_trim = detect_leading_silence(sound.reverse())
        duration = len(sound)
        trimmed_sound = sound[start_trim:duration - end_trim]
        trimmed_sound.export("output.wav", format="wav")

    def play_(self):
        print('Playing')
        wf = wave.open('output.wav', 'rb')
        chunk = 2048
        swidth = wf.getsampwidth()
        RATE = wf.getframerate()
        window = np.blackman(chunk)
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=RATE, output=True)
        data = wf.readframes(chunk)
        thefreq = []
        while len(data) == chunk * swidth:
            stream.write(data)
            indata = np.array(wave.struct.unpack("%dh" % (len(data) / swidth), data)) * window
            fftData = abs(np.fft.rfft(indata)) ** 2
            which = fftData[1:].argmax() + 1
            if which != len(fftData) - 1:
                y0, y1, y2 = np.log(fftData[which - 1:which + 2:])
                x1 = (y2 - y0) * .5 / (2 * y1 - y2 - y0)
                thefreq.append((which + x1) * RATE / chunk)
            else:
                thefreq.append(which * RATE / chunk)
            data = wf.readframes(chunk)
        if data:
            stream.write(data)
        stream.close()
        p.terminate()
        
    def process(self):
        self.sr_()
        self.play_()
    def Void(self,event):
        pass
    
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
