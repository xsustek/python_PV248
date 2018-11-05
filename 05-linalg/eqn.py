import sys
import re
import string
from numpy import linalg
from numpy import array
from numpy import nditer
from numpy import column_stack

class Eq:
    def __init__(self, left, right, eq):
        self.left = left
        self.right = int(right)
        self.eq = eq

    def to_string(self):
        return self.eq
    
    def aug(self):
        return self.left.append(self.right)


input = sys.argv[1]

f = open(input)


def line_into_list(line):
    line = line.strip()
    splits = str(line).split(" = ")
    m = sorted(re.findall(r"[+-]? ?\d?[a-z]", splits[0]), key=lambda f: f[f.__len__() - 1])

    dic = {}
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

def find_start(arrs):
    lens = []
    for arr in arrs:
        for i in range(0, arr.__len__() - 1):
            if arr[i] != 0:
                lens.append(i)
    return min(lens)

def slice_arr(arr, min, max):
    res = []
    for a in arr:
        res.append(a[min:max + 1])
    return res

def print_eqs(eqs):
    for eq in eqs:
        print(eq.to_string())


eqs = list(map(line_into_list, f))

arr = []
vals = []
key_set = set()

for i in eqs:
    for k in i.left.keys():
        key_set.add(k)

key_set = list(sorted(key_set))

for i in eqs:
    vals.append(i.right)
    eq_arr = []
    for k in key_set:
        if i.left.__contains__(k):
            eq_arr.append(i.left[k])
        else:
            eq_arr.append(0)
    arr.append(eq_arr)

narr = array(arr)
nvals = array(vals)

aug_rank = linalg.matrix_rank(column_stack((narr, nvals)))
coef_rank = linalg.matrix_rank(narr)

num_of_var = key_set.__len__()

if coef_rank < aug_rank:
    print_eqs(eqs)
    print("no solution")
elif coef_rank == aug_rank and coef_rank == num_of_var:
    print_eqs(eqs)
    res = linalg.solve(narr, nvals)
    solution = ""
    for i, e in enumerate(nditer(res.T)):
        keys = list(eqs[i].left.keys())
        solution += str(key_set[i]) + " = " + str(e) + ", "
    
    print("solution: " + solution.strip(", "))
else:
    print_eqs(eqs)
    print("solution space dimension:", num_of_var - coef_rank)
