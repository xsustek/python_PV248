import re
import sys
import math
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


def extract_year(date_str):
    date_str = date_str.strip()
    date_m = re.match(r"[0-9]*. [0-9]*. [0-9]*", date_str)
    span_m = re.match(r"([0-9]*)-[0-9]*", date_str)
    century_m = re.match(r"([0-9]+)th century", date_str)
    year_m = re.match(r".*?([0-9]+)", date_str)

    if date_m is not None:
        return int(datetime.strptime(date_str, "%d. %m. %Y").year)
    elif span_m is not None and span_m.group(1):
        return int(span_m.group(1))
    elif century_m is not None and century_m.group(1):
        return int(century_m.group(1)) * 100
    elif year_m is not None and year_m.group(1):
        return int(year_m.group(1))


def extract_century(date_str):
    year = extract_year(date_str)
    if year is None:
        return None
    if year <= 100:
        return 1
    if year % 100 == 0:
        return year // 100
    else:
        return year // 100 + 1


def century(file):
    r = re.compile(r"Composition Year: (.*)")
    counter = Counter()

    for line in file:
        m = r.match(line)
        if m is not None and m.group(1):
            year = extract_century(m.group(1))
            if year is not None:
                counter[year] += 1
    return counter


file = open(sys.argv[1], 'r', encoding='utf8')

if sys.argv[2] == "composer":
    for k, v in sorted(composer(file).items(), key=lambda kv: kv[0]):
        if k is not None:
            print(k + ": " + str(v))
elif sys.argv[2] == "century":
    for k, v in sorted(century(file).items(), key=lambda kv: kv[0]):
        if k is not None:
            print(str(k) + "th century: " + str(v))
