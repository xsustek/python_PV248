import sys
import numpy as np
import json
from stat_utils import *
import collections

file = sys.argv[1]
mode = sys.argv[2]

dic = load(file, mode)

data = date_dic(dic)
data = collections.OrderedDict(sorted(data.items(), key=lambda e: e[0]))

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
