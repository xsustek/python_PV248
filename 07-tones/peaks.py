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
    return cluster(peak_val, fil[0])
    top_peaks = peak_val[peak_val.argsort()][-1]
    res = numpy.where(numpy.isin(arr, top_peaks))

    if res[0].size == 0:
        return []
    return res[0]

def cluster(arr, peak):
    i = 0
    res = []
    while i < 3 and arr.size > 0:
        max = numpy.argmax(arr)
        max_val = peak[max]
        res.append(max_val)
        cluster = find_cluster(max, peak)
        arr = numpy.delete(arr, cluster)
        peak = numpy.delete(peak, cluster)
        i += 1
    return res

def find_cluster(index, peaks):
    val = peaks[index]
    to_remove = set()
    i = index
    while i < peaks.size and abs(peaks[i] - val) <= 1:
        to_remove.add(int(i))
        val = peaks[i]
        i += 1
    val = peaks[index]
    i = index
    while i >= 0 and abs(peaks[i] - val) <= 1:
        to_remove.add(int(i))
        val = peaks[i]
        i -= 1
    return list(to_remove)


def fft(c):
    avg = list(map(cal_avg, c))
    abs_val = abs(rfft(numpy.array(avg)))
    return abs_val
