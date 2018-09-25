import re
import sys
from datetime import datetime
from collections import Counter


def composer(file):
    r = re.compile(r"Composer: (.*)")
    counter = Counter()

    for line in file:
        m = r.match(line)
        if m is not None and m.group(1):
            names = re.sub(r"\(.*\)", "", m.group(1))
            for name in names.split(";"):
                counter[name.strip()] += 1

    return counter


def extract_century(date_str):
    date_str = date_str.strip()
    date_m = re.match(r"[0-9]*. [0-9]*. [0-9]*", date_str)
    span_m = re.match(r"([0-9]*)-[0-9]*", date_str)
    year_m = re.match(r"([0-9]*)", date_str)
    if date_m is not None:
        return int(str(datetime.strptime(date_str, "%d. %m. %Y").year)[:2]) + 1
    elif span_m is not None and span_m.group(1):
        return int(span_m.group(1)[:2]) + 1
    elif year_m is not None and year_m.group(1):
        return int(year_m.group(1)[:2]) + 1


def century(file):
    r = re.compile(r"Composition Year: (.*)")
    counter = Counter()

    for line in file:
        m = r.match(line)
        if m is not None and m.group(1):
            year = extract_century(m.group(1))
            counter[year] += 1
    return counter


file = open(sys.argv[1], 'r', encoding='utf8')

if sys.argv[2] == "composer":
    for k, v in composer(file).items():
        if k is not None:
            print(k, v)
elif sys.argv[2] == "century":
    for k, v in century(file).items():
        if k is not None:
            print(k, v)
