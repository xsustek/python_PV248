import sqlite3
import sys

import os   
from scorelib import load

input = sys.argv[1]
output = sys.argv[2]

os.remove(output)
con = sqlite3.connect(output)
cur = con.cursor()
cur.executescript(open("scorelib.sql").read())


prints = load(input)

for p in prints:
    p.save(con)

con.commit()