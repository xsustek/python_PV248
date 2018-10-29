import re


def value_or_nothing(val):
    return str(val) if val is not None else ""


def strip_if_not_none(val):
    if val is not None:
        return val.strip()
    else:
        return val


def to_int_if_not_none(val):
    if val is not None and val:
        return int(val)
    else:
        return val

def dic_equals(dic, arr):
    for k, e in dic.items():
        if array_equal(e, arr):
            return k


def array_equal(arr1, arr2):
    if arr1 == arr2:
        return True
    if arr1 is None or not arr1:
        return False
    if arr2 is None or not arr2:
        return False
    for a in arr1:
        res = False
        for b in arr2:
            res = res or a == b
        if not res:
            return False
    return True

def group_by(key_selector, result_selector, array):
    dic = {}
    for a in array:
        key = key_selector(a)
        if not dic.__contains__(key):
            dic[key] = []
        dic[key].append(result_selector(a))
    return dic

class Print:
    def __init__(self, data):
        self.edition = self.load_edition(data)
        self.print_id = self.load_print_id(data)
        self.partiture = self.load_partiture(data)

    def load_edition(self, data):
        return Edition(data)

    def load_print_id(self, data):
        return int(parse(data, r"Print Number: ([0-9]+)"))

    def load_partiture(self, data):
        reg = re.compile(r"Partiture: (.*)")
        m = reg.search(data)
        if m is not None and m.group(1):
            g = m.group(1)
            if "yes" in g:
                return True
        else:
            return False

    def save(self, connection):
        ed_id = self.edition.save(connection)
        self.save_print(connection, ed_id)

    def save_print(self, connection, ed_id):
        cur = connection.cursor()
        cur.execute("Select * FROM print where id = ?", (self.print_id,))
        data = cur.fetchone()
        if data is None:
            cur.execute("INSERT INTO print (id, partiture, edition) VALUES (?, ?, ?)",
                        (self.print_id, "Y" if self.partiture else "N", ed_id))
            return cur.lastrowid
        else:
            return data[0]

    def format(self):
        print("Print Number:", self.print_id)
        print("Composer:", self.format_persons(self.composition().authors))
        print("Title:", value_or_nothing(self.composition().name))
        print("Genre:", value_or_nothing(self.composition().genre))
        print("Key:", value_or_nothing(self.composition().key))
        print("Composition Year:", value_or_nothing(self.composition().year))
        print("Edition:", value_or_nothing(self.edition.name))
        print("Editor:", self.format_persons(self.edition.authors))

        i = 1
        for voice in self.composition().voices:
            print("Voice " + str(i) + ":", voice.format())
            i += 1

        print("Partiture:", "yes" if self.partiture else "no")
        print("Incipit:", value_or_nothing(self.composition().incipit))

    def format_persons(self, persons):
        if persons is None:
            return ""
        res = ""
        for p in persons:
            res += p.format() + ";"
        return res.strip(";")

    def composition(self):
        return self.edition.composition


class Edition:
    def __init__(self, data):
        self.composition = self.load_composition(data)
        self.authors = self.load_authors(data)
        self.name = strip_if_not_none(self.load_name(data))

    def load_composition(self, data):
        return Composition(data)

    def load_authors(self, data):
        s = re.search(r"Editor: (.*)", data)
        if s is not None:
            m = s.group(1)
            if m is not None:
                return list(map(lambda v: Person(v), m.split(";")))

    def load_name(self, data):
        return parse(data, r"Edition: (.*)")

    def save(self, connection):
        com_id = self.composition.save(connection)
        ed_id = self.save_edition(connection, com_id)
        self.save_authors(connection, ed_id)
        return ed_id

    def save_authors(self, connection, ed_id):
        if self.authors is None:
            return
        for a in self.authors:
            aut_id = a.save(connection)
            self.save_edition_author(connection, ed_id, aut_id)

    def save_edition(self, connection, com_id):
        cur = connection.cursor()
        cur.execute(
            "Select * FROM edition where name IS ? AND score IS ?", (self.name, com_id))

        data = cur.fetchone()
        if data is None or not data:
            cur.execute(
                "INSERT INTO edition (name, score) VALUES (?, ?)", (self.name, com_id))
            return cur.lastrowid
        else:
            return data[0]

    def save_edition_author(self, connection, edition_id, author_id):
        if author_id is None:
            return
        cur = connection.cursor()
        cur.execute(
            "Select * FROM edition_author where edition = ? AND editor = ?", (edition_id, author_id))
        data = cur.fetchone()
        if data is None:
            cur.execute(
                "INSERT INTO edition_author (edition, editor) VALUES (?, ?)", (edition_id, author_id))
            return cur.lastrowid
        else:
            return data[0]


class Composition:
    def __init__(self, data):
        self.name = strip_if_not_none(self.load_name(data))
        self.incipit = strip_if_not_none(self.load_incipit(data))
        self.genre = strip_if_not_none(self.load_genre(data))
        self.year = strip_if_not_none(self.load_year(data))
        self.key = strip_if_not_none(self.load_key(data))
        self.voices = self.load_voices(data)
        self.authors = self.load_authors(data)

    def load_name(self, data):
        return parse(data, r"Title: (.*)")

    def load_incipit(self, data):
        return parse(data, r"Incipit: (.*)")

    def load_genre(self, data):
        return parse(data, r"Genre: (.*)")

    def load_key(self, data):
        return parse(data, r"Key: (.*)")

    def load_year(self, data):
        return parse(data, r"Composition Year: (.*)")

    def load_voices(self, data):
        groups = re.findall(r"Voice ([0-9]+): (.*)", data)
        return list(map(lambda v: Voice(v), groups))

    def load_authors(self, data):
        s = re.search(r"Composer: (.*)", data)
        if s is not None:
            m = s.group(1)
            if m is not None:
                return list(map(lambda v: Person(v), m.split(";")))

    def save(self, connection):
        com_id = self.save_composition(connection)
        self.save_authors(connection, com_id)
        self.save_voices(connection, com_id)
        return com_id

    def save_authors(self, connection, com_id):
        for a in self.authors:
            aut_id = a.save(connection)
            self.save_score_author(connection, com_id, aut_id)

    def save_voices(self, connection, com_id):
        for v in self.voices:
            v.save(connection, com_id)

    def save_composition(self, connection):
        cur = connection.cursor()
        cur.execute("SELECT score.id, person.name FROM score join score_author on score.id = score_author.score join person on score_author.composer = person.id where score.name IS ? and score.genre IS ? AND score.key IS ? AND score.incipit IS ? and score.year IS ?",
                    (self.name, self.genre, self.key, self.incipit, self.year))
        data = cur.fetchall()
        g = group_by(lambda e: e[0], lambda e: e[1], data)
        eq = dic_equals(g, map(lambda e: e.name, self.authors))

        cur.execute("SELECT score.id, voice.number, voice.range, voice.name FROM score join voice on score.id = voice.score where score.name IS ? and score.genre IS ? AND score.key IS ? AND score.incipit IS ? and score.year IS ?",
                    (self.name, self.genre, self.key, self.incipit, self.year))
        data = cur.fetchall()
        g = group_by(lambda e: e[0], lambda e: [e[1], e[2], e[3]], data)
        eqv = dic_equals(g, map(lambda e: [e.number, e.range, e.name], self.voices))

        cur.execute("Select * FROM score where name IS ? and genre IS ? AND key IS ? AND incipit IS ? and year IS ?",
                    (self.name, self.genre, self.key, self.incipit, self.year))
        data = cur.fetchone()
        if data is None or eq != eqv:
            cur.execute("INSERT INTO score (name, genre, key, incipit, year) VALUES (?, ?, ?, ?, ?)",
                        (self.name, self.genre, self.key, self.incipit, self.year))
            return cur.lastrowid
        elif eqv:
            return eqv       
        else:
            return data[0]

    def save_score_author(self, connection, composition_id, author_id):
        if author_id is None:
            return
        cur = connection.cursor()
        cur.execute("Select * FROM score_author where score = ? AND composer = ?",
                    (composition_id, author_id))
        data = cur.fetchone()
        if data is None:
            cur.execute("INSERT INTO score_author (score, composer) VALUES (?, ?)",
                        (composition_id, author_id))
            return cur.lastrowid
        else:
            return data[0]


class Voice:
    def __init__(self, data):
        self.name = strip_if_not_none(self.load_name(data[1]))
        self.range = strip_if_not_none(self.load_range(data[1]))
        self.number = self.load_number(data[0])

    def load_number(self, data):
        return int(data)

    def load_name(self, data):
        if "--" in data:
            return re.sub(r"(.*--.*?)[,;]", "", data)
        return str(data).strip()

    def load_range(self, data):
        if "--" in data:
            if "," in data:
                return data.split(",")[0]
            elif ";" in data:
                return data.split(";")[0]

    def format(self):
        if self.range is not None:
            return str(self.range) + ", " + str(self.name)
        return str(self.name)

    def save(self, connection, com_id):
        cur = connection.cursor()
        cur.execute("Select * FROM voice where number IS ? AND score IS ? AND range IS ? AND name IS ?",
                    (self.number, com_id, self.range, self.name))
        data = cur.fetchone()
        if data is None:
            cur.execute("INSERT INTO voice (number, score, range, name) VALUES (?, ?, ?, ?)",
                        (self.number, com_id, self.range, self.name))
            return cur.lastrowid
        else:
            return data[0]


class Person:
    def __init__(self, data):
        self.name = strip_if_not_none(self.load_name(data))
        self.born = to_int_if_not_none(self.load_born(data))
        self.died = to_int_if_not_none(self.load_died(data))

    def load_name(self, data):
        return re.sub(r"\(([0-9]{4}|[0-9]{0})-{1,2}([0-9]{4}|[0-9]{0})\)", "", data).strip()

    def load_born(self, data):
        res = re.search(
            r"\(([0-9]{4}|[0-9]{0})-{1,2}([0-9]{4}|[0-9]{0})\)", data)
        if res is not None:
            return res.group(1).strip()
        if "*" in data:
            res = re.search(r"\*([0-9]{4})", data)
            if res is not None:
                return res.group(1).strip()

    def load_died(self, data):
        res = re.search(
            r"\(([0-9]{4}|[0-9]{0})-{1,2}([0-9]{4}|[0-9]{0})\)", data)
        if res is not None:
            return res.group(2).strip()
        if "+" in data:
            res = re.search(r"\+([0-9]{4})", data)
            if res is not None:
                return res.group(1).strip()

    def format(self):
        if self.name is None:
            return ""
        res = str(self.name)
        if self.born is None and self.died is None:
            return res
        if self.born is not None:
            res += " " + str(self.born)
        res += "--"
        if self.died is not None:
            res += str(self.died)
        return res

    def save(self, connection):
        if not self.name:
            return
        cur = connection.cursor()
        cur.execute("Select * FROM person where name IS ?", (self.name,))
        data = cur.fetchone()
        if data is None:
            cur.execute("INSERT INTO person (born, died, name) VALUES (?, ?, ?)",
                        (self.born, self.died, self.name))
            return cur.lastrowid
        else:
            if self.born is not None:
                cur.execute("UPDATE person SET born = ? where id = ?",
                            (self.born, data[0]))
            if self.died is not None:
                cur.execute("UPDATE person SET died = ? where id = ?",
                            (self.died, data[0]))

            return data[0]


def parse(data, regex):
    m = re.search(regex, data)
    if m and m.group(1):
        return m.group(1)


def load(filename):
    with open(filename, encoding="utf8") as file:
        file_str = file.read().split("\n\n")
        return sorted(list(map(lambda f: Print(f), file_str)), key=lambda i: i.print_id)
