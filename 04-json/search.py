import sys
import sqlite3
import json

database = "04-json/scorelib.dat"

name = sys.argv[1]

def create_print(print_number, con):
    cur = con.cursor()
    composers = cur.execute("SELECT person.name, person.born, person.died FROM 'print' JOIN edition ON print.edition = edition.id JOIN score ON edition.score = score.id JOIN score_author ON score_author.score = score.id JOIN person ON score_author.composer = person.id where print.id = ?", (7,))
    editors = cur.execute("SELECT person.name, person.born, person.died FROM 'print' JOIN edition ON print.edition = edition.id JOIN edition_author ON edition_author.edition = edition.id JOIN person ON edition_author.editor = person.id where print.id = ?", (373,))
    tmp = cur.fetchall()
    res = {}
    res["Composer"] = ""
    res["Editor"] = ""
    res["Voices"] = ""
    return res

con = sqlite3.connect(str(database))

cur = con.cursor()

query = cur.execute("SELECT * FROM person JOIN score_author on score_author.composer = person.id JOIN score ON score.id = score_author.score JOIN edition ON edition.score = score.id JOIN print ON print.edition = edition.id where person.name like ?", ("%" + name + "%",))
#tmp = cur.fetchall()

res = {}
for r in query:
    if not res.__contains__(r[3]):
        res[r[3]] = []
        create_print(r[17], con)
    res[r[3]].append({
        "Print Number": r[17],
        "Composer": [],
        "Title": r[8],
        "Genre": r[9],
        "Key": r[10],
        "Composition Year": r[12],
        "Edition": r[15],
        "Editor": [],
        "Voices": [],
        "Partiture": False if r[18] == "N" else True,
        "Incipit": r[11]
    })

print(json.dumps(res, indent=4, ensure_ascii=False))