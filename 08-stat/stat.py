import csv
import sys

file = sys.argv[1]

with open(file) as csvfile:
     reader = csv.DictReader(csvfile)
     res = []
     for row in reader:
         dic = {}
         for field in reader.fieldnames:
             dic[field] = (row[field])
         res.append(dic)

print(res)
