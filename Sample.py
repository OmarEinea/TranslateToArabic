from Translator import FreeTranslations
import codecs, csv, sys, os

number = str(sys.argv[1]) if len(sys.argv) > 1 else '1'
user_en, user_ar = None, None
tr = FreeTranslations()
translate = tr.translate
done = 0

if os.path.exists("amazon_baby_arabic%s.csv" % number):
    output = open("amazon_baby_arabic%s.csv" % number)
    done = len(output.readlines())
    output.close()

output = codecs.open("amazon_baby_arabic%s.csv" % number, "a+", "utf-8").write
input_ = csv.reader(open("amazon_baby%s.csv" % number))

for i in range(done): input_.__next__()

for line in input_:
    if line[0] != user_en:
        user_en = line[0]
        user_ar = translate(user_en)
    name = user_ar
    review = translate(line[1])
    print(("Name: " + name + "\tReview: " + review)[:150])
    output(name + '\t' + review + '\t' + line[2] + '\n')

print("Time: %d" % tr.execution_time())
tr.close()
