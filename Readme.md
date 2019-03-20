# English to Arabic Translators

This is a python 3 web scraping script to translate English text to Arabic,  
using the web browser automation tool Selenium.

The translation is done using the service provided by freetranslations.org


### How to Use?

Instantiate a Translator object, then call `translate(text)` on it like so:

```python
from Translator import Translator

tr = Translator()

text = input("Type Something: ")
print(tr.translate(text))
```

Note: you could pass `True` to Translator to make it headless.


### Installation

Install Selenium using:

```
pip install selenium
```

Then download Chrome WebDriver from
[here](https://chromedriver.storage.googleapis.com/index.html?path=2.46/),
then extract and place it in the same folder.


### Contents

- Translator.py: A class which opens the browser and provide a function to translate text.
- Sample.py: A simple script that demonstrates the use of Translator on a text file.


### References

- [Translation Service](https://www.freetranslations.org/english-to-arabic-translation.html)
- [Selenium WebDriver](https://selenium-python.readthedocs.io)