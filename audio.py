# Credit for setting values of constants and basic functions : https://gist.github.com/mabdrabo/8678538
import pyaudio
import wave
import numpy as np
import keyboard

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS =  10

def init_audio():
    audio = pyaudio.PyAudio()
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)
    return audio, stream

def close_audio(stream, audio):
    stream.stop_stream()
    stream.close()
    audio.terminate()

def audio_to_amp(stream, max_val):
    data = stream.read(CHUNK)
    data2 = np.fromstring(data,dtype=np.int16)
    peak = np.average(np.abs(data2))*2
    rounded = min(peak/2**11, 1)*max_val
    return rounded
