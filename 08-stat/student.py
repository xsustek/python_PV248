import sys
import json
from stat_utils import *
import numpy as np
import scipy.optimize as ss
import datetime
from dateutil.parser import parse


def flatten(l): return [item for sublist in l for item in sublist]


base_time = parse("2018-09-17")


def cumulation(dic_to_trans):
    res = []
    for k, e in dic_to_trans.items():
        d = parse(k) - base_time
        res.append((d.days, (res[-1][1] if res else 0) + sum(e)))
    return res


def get_slope(data):
    s = sum(map(lambda e: e[0] * e[1], data))
    s2 = sum(map(lambda e: e[0]**2, data))
    return s / s2


def prediction(points, slope):
    return datetime.timedelta(points / slope) + base_time


def to_avg_dic(dic):
    res = {}
    for k, e in dic.items():
        res[k] = [np.mean(np.array(e))]
    return res


file = sys.argv[1]
id = sys.argv[2]

dic = load(file, "exercises")


res = {}
if id == "average":
    dic_date = load(file, "deadlines")
    dic_date = exercises_dic(dic_date)
    dic_date = to_avg_dic(dic_date)
    cum = cumulation(dic_date)
    slope = get_slope(cum)
    val = list(dic_date.values())
    arr = np.array(val)
    res = {
        "mean": np.mean(arr),
        "median": np.median(arr),
        "total": np.sum(arr),
        "passed": np.count_nonzero(arr > 0),
        "regression slope": slope,
        "date 16": "inf" if slope == 0 else prediction(16, slope).strftime("%Y-%m-%d"),
        "date 20": "inf" if slope == 0 else prediction(20, slope).strftime("%Y-%m-%d")
    }
else:
    dic_date = load(file, "dates")
    if dic_date.__contains__(id):
        cum = cumulation(dic_date[id])
        slope = get_slope(cum)
        stud = dic[id]
        stud = exercises_dic_stud(stud)
        val = list(flatten(stud.values()))
        arr = np.array(val)
        res = {
            "mean": np.mean(arr),
            "median": np.median(arr),
            "total": np.sum(arr),
            "passed": np.count_nonzero(arr > 0),
            "regression slope": slope,
            "date 16": "inf" if slope == 0 else prediction(16, slope).strftime("%Y-%m-%d"),
            "date 20": "inf" if slope == 0 else prediction(20, slope).strftime("%Y-%m-%d")
        }

if res:
    print(json.dumps(res, indent=4, ensure_ascii=False))
