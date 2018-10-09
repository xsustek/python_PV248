import re

def value_or_nothing(val):
        return str(val) if val is not None else ""

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
            if "yes" in g :
                return True
            else:
                return False

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
        self.name = self.load_name(data)

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


class Composition:
    def __init__(self, data):
        self.name = self.load_name(data)
        self.incipit = self.load_incipit(data)
        self.genre = self.load_genre(data)
        self.year = self.load_year(data)
        self.key = self.load_key(data)
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
        groups = re.findall(r"Voice [0-9]+: (.*)", data)
        return list(map(lambda v: Voice(v), groups))

    def load_authors(self, data):
        s = re.search(r"Composer: (.*)", data)
        if s is not None:
            m = s.group(1)
            if m is not None:
                return list(map(lambda v: Person(v), m.split(";")))


class Voice:
    def __init__(self, data):
        self.name = self.load_name(data)
        self.range = self.load_range(data)

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


class Person:
    def __init__(self, data):
        self.name = self.load_name(data)
        self.born = self.load_born(data)
        self.died = self.load_died(data)

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


def parse(data, regex):
    m = re.search(regex, data)
    if m and m.group(1):
        return m.group(1)


def load(filename):
    with open(filename, encoding="utf8") as file:
        file_str = file.read().split("\n\n")
        return sorted(list(map(lambda f: Print(f), file_str)), key=lambda i: i.print_id)
