import csv
import sys
import pandas as pd
import numpy as np
import json

file = sys.argv[1]
mode = sys.argv[2]

key_selector = {
    "dates": lambda e: str(e).split("/")[0],
    "exercises": lambda e: str(e).split("/")[1],
    "deadlines": lambda e: e
}

with open(file) as csvfile:
    reader = csv.DictReader(csvfile)
    dic = {}
    for i, row in enumerate(reader):
        id = row["student"]
        for field in reader.fieldnames:
            if field == "student":
                continue
            if not dic.__contains__(id):
                dic[id] = {}
            key = key_selector[mode](field)
            if not dic[id].__contains__(key):
                dic[id][key] = []
            point = float((row[field]))
            dic[id][key].append(point)


def date_dic(dic):
    res = {}
    for k, e in dic.items():
        for ik, ie in e.items():
            if not res.__contains__(ik):
                res[ik] = []
            for iie in ie:
                res[ik].append(iie)
    return res

def exercises_dic(dic):
    res = {}
    for k, e in dic.items():
        for ik, ie in e.items():
            if not res.__contains__(ik):
                res[ik] = []
            res[ik].append(max(ie))
    return res

if mode == "exercises":
    data = exercises_dic(dic)
else:
    data = date_dic(dic)


res = {}
for k, e in data.items():
    arr = np.array(e)
    res[k] = {
        "mean": np.mean(arr),
        "median": np.median(arr),
        "first": np.percentile(arr, 25),
        "last": np.percentile(arr, 75),
        "passed": np.count_nonzero(arr > 0)
    }

print(json.dumps(res, indent=4, ensure_ascii=False))
