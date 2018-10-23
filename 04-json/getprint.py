import sys
import sqlite3
import json

def create_composer(row):
    res = {}
    res["name"] = row[0]
    if row[1] is not None:
        res["born"] = row[1]
    if row[2] is not None:
        res["died"] = row[2]
    return res

database = "scorelib.dat"

print_number = sys.argv[1]

con = sqlite3.connect(str(database))

cur = con.cursor()

query = cur.execute("SELECT person.name, person.born, person.died FROM 'print' JOIN 'edition' ON print.edition = edition.id JOIN 'score' ON edition.score = score.id JOIN 'score_author' ON score.id = score_author.score JOIN 'person' ON score_author.composer = person.id where print.id = ?", (print_number,))

res = list(map(create_composer, query))

print(json.dumps(res, indent=4, ensure_ascii=False))