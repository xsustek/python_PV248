import sys
import sqlite3
import json

database = "scorelib.dat"

print_number = sys.argv[1]

con = sqlite3.connect(str(database))

cur = con.cursor()

query = cur.execute("SELECT person.name, person.born, person.died FROM 'print' JOIN 'edition' ON print.edition = edition.id JOIN 'score' ON edition.score = score.id JOIN 'score_author' ON score.id = score_author.score JOIN 'person' ON score_author.composer = person.id where print.id = ?", (print_number,))

res = list(map(lambda c: {"name": c[0], "born": c[1], "died": c[2]}, query))

print(json.dumps(res, indent=4))