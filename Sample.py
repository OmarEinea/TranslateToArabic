from Translator import *
import codecs
import csv

count = 0

tr = Systran()
file = csv.reader(open("amazon_baby.csv", "r"))
output = csv.writer(codecs.open("amazon_baby_systran.csv", "w", "utf-8"))

translated = {}

for line in file:
    if line[0] in translated:
        name = translated[line[0]]
    else:
        name = tr.translate(line[0])
        translated[line[0]] = name
    review = tr.translate(line[1])
    print(("Name: " + name + "\tReview: " + review)[:150])
    output.writerow([name, review, line[2]])
    count += len(line[0]) + len(line[1])
    if count > 100000:
        print("Time: " + str(tr.execution_time()))
        break

tr.close()