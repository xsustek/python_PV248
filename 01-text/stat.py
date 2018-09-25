import sys
import re
from collections import Counter
f = open(sys.argv[1], 'r', encoding='utf8')
r = re.compile(r"Composer: (.*).*\(?.*\)?")



def composer():
    counter = Counter()

    for line in f:
        m = r.match(line)
        if m is not None and m.group(1):
            names = re.sub(r"\(.*\)", "", m.group(1))
            for name in names.split(";"):
                counter[name.strip()] += 1

    for k, v in sorted(counter.items(), key=lambda kv: kv[1]):
        print(k, v)

composer()