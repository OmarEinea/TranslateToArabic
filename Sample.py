from Translator import Translator

# Create headless translator
tr = Translator(True)

# Open English input text file and Arabic output text file
english_input = open("english.txt")
arabic_output = open("arabic.txt", "w+", encoding="utf-8")

# Loop over every English line
for line in english_input:
    # Translate line to Arabic
    translation = tr.translate(line)
    # Write Translation to Arabic file
    arabic_output.write(translation + "\n")
