import sqlite3
import sys

import os   
from scorelib import load
from pathlib import Path

input = sys.argv[1]
output = Path(str(sys.argv[2]))

if output.is_file:
    os.remove(output)


con = sqlite3.connect(output)
cur = con.cursor()
cur.executescript(open("scorelib.sql").read())


prints = load(input)

for p in prints:
    p.save(con)

con.commit()
