from scorelib import Print
from scorelib import load
import sys

prints = load(sys.argv[1])

for p in prints:
    p.format()
    print()