import sys
import sqlite3
import json

database = "scorelib.dat"

name = sys.argv[1]

def create_person(row):
    res = {}
    res["name"] = row[0]
    if row[1] is not None:
        res["born"] = row[1]
    if row[2] is not None:
        res["died"] = row[2]
    return res


def create_voice(data):
    res = {}
    for r in data:
        res[r[1]] = {
            "name": r[3],
            "range": r[2]
        }
    return res


def create_print(print_number, con):
    cur = con.cursor()
    res = {}
    
    composers = cur.execute("SELECT person.name, person.born, person.died FROM 'print' JOIN edition ON print.edition = edition.id JOIN score ON edition.score = score.id JOIN score_author ON score_author.score = score.id JOIN person ON score_author.composer = person.id where print.id = ?", (print_number,))
    res["Composer"] = list(map(create_person, composers))

    editors = cur.execute("SELECT person.name, person.born, person.died FROM 'print' JOIN edition ON print.edition = edition.id JOIN edition_author ON edition_author.edition = edition.id JOIN person ON edition_author.editor = person.id where print.id = ?", (print_number,))
    res["Editor"] = list(map(create_person, editors))
    
    voices = cur.execute("SELECT voice.id, voice.number, voice.range, voice.name FROM 'print' JOIN edition ON print.edition = edition.id JOIN score ON edition.score = score.id JOIN voice on voice.score = score.id where print.id = ?", (print_number,))
    res["Voices"] = create_voice(voices)
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
    prints = create_print(r[17], con)
    res[r[3]].append({
        "Print Number": r[17],
        "Composer": prints["Composer"],
        "Title": r[8],
        "Genre": r[9],
        "Key": r[10],
        "Composition Year": r[12],
        "Edition": r[15],
        "Editor": prints["Editor"],
        "Voices": prints["Voices"],
        "Partiture": False if r[18] == "N" else True,
        "Incipit": r[11]
    })

print(json.dumps(res, indent=4, ensure_ascii=False))