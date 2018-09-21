import sys
import re
from collections import Counter
f = open(sys.argv[1], 'r', encoding='utf8')
r = re.compile(r"Composer: (.*)")

counter = Counter()

for line in f:
    m = r.match(line)
    if m is not None:
        counter[m.group(1)] += 1

for k, v in counter.items():
    print(k, v)
