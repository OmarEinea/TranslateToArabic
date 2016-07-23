from Translator import FreeTranslations
import codecs, csv, sys, os

number = str(sys.argv[1]) if len(sys.argv) > 1 else '1'
tr = FreeTranslations()
translate = tr.translate
done, count = 0, 0
divider = ["(@)", "(#)", "(%)", "(&)", "(|)"]

if os.path.exists("Reviews_arabic%s.csv" % number):
    output = open("Reviews_arabic%s.csv" % number)
    done = len(output.readlines())
    output.close()

output = codecs.open("Reviews_arabic%s.csv" % number, "a+", "utf-8").write
input_ = csv.reader(open("Reviews%s.csv" % number))

for i in range(done): input_.__next__()

for line in input_:
    loop = 0
    while True:
        try:
            summary, text = translate("%s %s %s" % (line[8], divider[count], line[9])).split(divider[count], 1)
            break
        except ValueError:
            count = (count + 1) % 5
            print("Switching to %s" % divider[count])
            loop += 1
            if loop > 3:
                raise ValueError
    print(("Summary: %s    Text: %s" % (summary, text))[:155])
    output('\t'.join(line[:8] + [summary.strip(), text.strip()]) + '\n')
