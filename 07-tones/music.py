import sys
from math import *
from peaks import *
from numpy import sort

pitch_dic = {
    0: "c",
    1: "cis",
    2: "d",
    3: "es",
    4: "e",
    5: "f",
    6: "fis",
    7: "g",
    8: "gis",
    9: "a",
    10: "bes",
    11: "b"
}


class Octav_Diff:
    def __init__(self, upper, diff):
        self.upper = upper
        self.diff = diff


def octav_diff(num):
    diff = 0
    if round(num) >= 0 and round(num) <= 11:
        return 0
    elif round(num) < 0:
        while round(num) < 0:
            num += 12
            diff -= 1
        return diff
    elif round(num) > 11:
        while round(num) > 11:
            num -= 12
            diff += 1
        return diff


def octav_gen(octav_diff):
    upper = True if octav_diff < -1 else False
    if upper:
        return Octav_Diff(upper, (octav_diff + 2) * (-1))
    else:
        return Octav_Diff(upper, octav_diff + 1)


def to_upper(note):
    note = str(note)
    return note[0].upper() + note[1:]


def f_to_pitch(freq, base):
    pitch = 9 + 12 * log2(freq / base)
    diff = octav_diff(pitch)
    absolut_part = pitch + ((-1) * diff * 12)
    whole_part = round(absolut_part)

    octav = octav_gen(diff)

    octave_str = pitch_dic[whole_part]
    if octav.upper:
        octave_str = to_upper(octave_str) + "," * octav.diff
    else:
        octave_str = octave_str + "'" * octav.diff

    cents = round((absolut_part - whole_part) * 100)
    cents_str = ("+" if cents >= 0 else "") + str(cents)
    return octave_str + cents_str


base_freq = int(sys.argv[1])
wav_file = sys.argv[2]

audio = wave.open(wav_file, "r")

audio_arr = list(wav_to_arr(audio))
fr = audio.getframerate()


a_arr = [audio_arr[x:x+fr] for x in range(0, len(audio_arr), fr // 10)]
a_filter = filter(lambda a: len(a) == fr, a_arr)
a_map = list(map(lambda c: list(find_peak(fft(c), fr)), a_filter))

chunks = list(map(lambda e: [f_to_pitch(x, base_freq) for x in sorted(e)], filter(lambda q: q is not None, a_map)))

tmp = None
start_time = 0.0
time = 0.0
for i, c in enumerate(chunks):
    time = round(time + 1 / 10, 1)
    if tmp == c and i != chunks.__len__() - 1:
        continue
    tmp = c
    arr_print = ""
    print(str(start_time) + "-" + str(time) + " " + " ".join(c))
    start_time = time
