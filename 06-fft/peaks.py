import wave
import sys
import struct
import numpy
from numpy.fft import rfft

def cal_avg(tuple):
    if list(tuple).__len__() == 1:
        return tuple[0]
    else:
        return (tuple[0] + tuple[-1]) // 2

def wav_to_arr(audio):
    while audio.tell() < audio.getnframes():
        frame = audio.readframes(1)
        if audio.getnchannels() == 1:
            decoded = struct.unpack("<h", frame)
        if audio.getnchannels() == 2:
            decoded = struct.unpack("<hh", frame)
        yield decoded

def find_peak(arr, fr):
    avg = numpy.average(arr)
    p = 20 * avg
    fil = numpy.where(arr >= p)
    if fil[0].size == 0:
        return None
    return (numpy.min(fil), numpy.max(fil))

def fft(c):
    avg = list(map(cal_avg, c))
    abs_val = abs(rfft(numpy.array(avg)))
    return abs_val

input = sys.argv[1]

audio = wave.open(input, "r")

audio_arr = list(wav_to_arr(audio))
fr = audio.getframerate()

chunks = list(filter(lambda e: e is not None, map(lambda c: find_peak(fft(c), fr), filter(lambda a: len(a) == fr, [audio_arr[x:x+fr] for x in range(0, len(audio_arr), fr)]))))
if len(chunks) == 0:
    print("no peaks")
else:
    print("low = " + str(min(x[0] for x in chunks)) + ", high = " + str(max(x[1] for x in chunks)))