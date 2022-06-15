import os
import sys
import tempfile
import queue
from gpiozero import Button
from pydub import AudioSegment
from pydub.playback import play
import sounddevice as sd
import soundfile as sf
import numpy
assert numpy

hook = Button(19)
ringback = AudioSegment.from_wav(os.getcwd() + '/assets/ringback_tone.wav')
greeting = AudioSegment.from_wav(os.getcwd() + '/assets/StarWars3.wav')
beep = AudioSegment.from_wav(os.getcwd() + '/assets/answering_machine_beep.wav')
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())

while True:
    if hook.is_pressed:
        play(ringback)
        play(greeting)
        play(beep)
        try:
            filename = tempfile.mkstemp(prefix='message_', suffix='.wav', dir=os.getcwd() + '/messages')
            while hook.is_pressed:
                with sf.SoundFile(filename[1], mode='w', samplerate=48000, channels=2, format='WAV') as file:
                    with sd.InputStream(samplerate=48000, channels=2, callback=callback):
                        while hook.is_pressed:
                            file.write(q.get())
            os.chmod(filename[1], 0o0777)
        except Exception as e:
            print(e)