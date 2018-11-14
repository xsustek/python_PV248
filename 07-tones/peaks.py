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
    fil = numpy.where(arr > p)
    peak_val = arr[fil]
    top_peaks = peak_val[peak_val.argsort()[-3:][::-1]]
    res = numpy.where(numpy.isin(arr, top_peaks))

    if res[0].size == 0:
        return []
    return res[0]

def fft(c):
    avg = list(map(cal_avg, c))
    abs_val = abs(rfft(numpy.array(avg)))
    return abs_val
