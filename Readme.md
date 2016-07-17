# English to Arabic Translators

This is a python 3 web scraping script to translate English text to Arabic,             <br>
using the web browser automation tool Selenium, or python requests and BeautifulSoup.

The translation is done through one of several translation services
(e.g. Bing, Google Translation, etc...)

### Contents

- Translator.py: A collection of translator classes for each of the supported services
- Sample.py: A sample script showing the steps for translating 100k chars of a file

### Supported Services

|Name|Time (100k chars)|Price|Terms of Use|Used Libraries|
|----|-----------------|-----|------------|--------------|
|[Bing (Microsoft)](https://www.bing.com/translator)|5.8 minutes|[Free for 2000k chars/month](https://datamarket.azure.com/dataset/bing/microsofttranslator)|Commercial Use|[MicrosoftTranslator](https://github.com/fulfilio/Microsoft-Translator-Python-API)|
|[FreeTranslations](https://www.freetranslations.org)|6.2 minutes|Completely Free|Not Specified|[Selenium](http://www.seleniumhq.org)|
|[Systran](http://www.systranet.com/translate)|6.7 minutes|Completely Free|[Commercial Use](http://www.systransoft.com/systran/corporate-profile/policies/terms-of-service)|[Selenium](http://www.seleniumhq.org)|
|[SDL](http://www.sdl.com/languagecloud/machine-translation)|7.7 minutes|[Trial for 1000k chars only](http://www.sdl.com/languagecloud/machine-translation/pricing.html)|[Subject to Terms](http://www.sdl.com/about/terms.html)|[Python Requests](https://github.com/kennethreitz/requests)|
|[Babylon](http://translation.babylon-software.com)|11.1 minutes|Completely Free|Personal Use Only!|[Selenium](http://www.seleniumhq.org)|

### Unsupported Services (Yet!)

These aren't supported yet because even their trial subscription needs a credit card.

|Name|Price|Terms of Use|
|----|-----|------------|
|[Google Translate](https://translate.google.com/)|[$20 / 1000k chars](https://cloud.google.com/translate/v2/pricing)|[Seems ok for Commercial Use](https://cloud.google.com/translate/v2/terms)|
|[WorldLingo](http://www.worldlingo.com/en/products_services/worldlingo_translator.html)|[$4.95 / month](http://www.worldlingo.com/en/mywl)|[Seems ok for Commercial Use](http://www.worldlingo.com/en/company/terms_conditions.html)|