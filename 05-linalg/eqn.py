import sys
import re
import string
from numpy import linalg
from numpy import array
from numpy import nditer

class Eq:
    def __init__(self, left, right, eq):
        self.left = left
        self.right = int(right)
        self.eq = eq

    def to_string(self):
        return self.eq


input = sys.argv[1]

f = open(input)


def line_into_list(line):
    line = line.strip()
    splits = str(line).split(" = ")
    m = sorted(re.findall(r"[+-]? ?\d?[a-z]", splits[0]), key=lambda f: f[f.__len__() - 1])

    dic = dict.fromkeys(list(string.ascii_lowercase), 0)
    for c in m:
        coef = c[:-1].replace(' ', '')
        if not re.match(r"[+-]?\d", coef):
            coef += str(1)
        dic[c[c.__len__() - 1]] = int(coef)
    return Eq(dic, splits[1].strip(), line)

def find_end(arrs):
    lens = []
    for arr in arrs:
        for i in range(arr.__len__() - 1, 0, -1):
            if arr[i] != 0:
                lens.append(i)
    return max(lens)

def slice_arr(arr, max):
    res = []
    for a in arr:
        res.append(a[:max + 1])
    return res


eqs = list(map(line_into_list, f))

arr = []
vals = []
for i in eqs:
    vals.append(i.right)
    arr.append(list(i.left.values()))

m = find_end(arr)
w = slice_arr(arr, m)

narr = array(w)
nvals = array(vals)

res = linalg.solve(narr, nvals)

for eq in eqs:
    print(eq.to_string())


solution = ""
for i, e in enumerate(nditer(res.T)):
    keys = list(eqs[0].left.keys())
    solution += str(keys[i]) + " = " + str(e) + ", "


print("solution: " + solution.strip(", "))
