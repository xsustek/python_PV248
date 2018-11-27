import csv

key_selector = {
    "dates": lambda e: str(e).split("/")[0],
    "exercises": lambda e: str(e).split("/")[1],
    "deadlines": lambda e: e
}


def load(file, mode):
    with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        dic = {}
        for i, row in enumerate(reader):
            id = row["student"]
            for field in reader.fieldnames:
                if field == "student":
                    continue
                if not dic.__contains__(id):
                    dic[id] = {}
                key = key_selector[mode](field)
                if not dic[id].__contains__(key):
                    dic[id][key] = []
                point = float((row[field]))
                dic[id][key].append(point)
        return dic


def date_dic(dic):
    res = {}
    for k, e in dic.items():
        for ik, ie in e.items():
            if not res.__contains__(ik):
                res[ik] = []
            res[ik].append(sum(ie))
    return res

def exercises_dic(dic):
    res = {}
    for k, e in dic.items():
        for ik, ie in e.items():
            if not res.__contains__(ik):
                res[ik] = []
            res[ik].append(sum(ie))
    return res

def exercises_dic_stud(dic):
    res = {}
    for k, e in dic.items():
            if not res.__contains__(k):
                res[k] = []
            res[k].append(sum(e))
    return res