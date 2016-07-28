from Translator import FreeTranslations

tr = FreeTranslations("chrome")
translate = tr.translate

output = open("important_words_ar.txt", "a+").write

for line in input("Enter words: ").split():
    output(translate(line) + '\n')
