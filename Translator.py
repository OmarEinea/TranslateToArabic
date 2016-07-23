from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import PhantomJS, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from microsofttranslator import Translator as MicrosoftTranslator
from requests.exceptions import ConnectionError
from urllib.parse import quote
from bs4 import BeautifulSoup
import requests, time


class Translator:
    _start_time = None

    def translate(self, string):
        self._start_time = time.time()
        self.translate = self.__translate
        return self.__translate(string)

    def __translate(self, string):
        for i in range(3):
            try:
                return self._translate(string.replace("\\", ''))
            except AttributeError as e:
                print(e)
                time.sleep(2)
            except TimeoutException as e:
                print(e)
                string = string.replace("...", ' ')
            except (ConnectionError, NoSuchElementException) as e: print(e)
        raise ConnectionAbortedError

    def _translate(self, string):
        pass

    def close(self):
        pass

    def execution_time(self):
        if self._start_time:
            return time.time() - self._start_time


class SDL(Translator):
    def __init__(self):
        self.url = "https://lc-api.sdl.com/translate"
        self.headers = {
            "Content-type": "application/json",
            "Authorization": "LC apiKey=4lzNWfvaFHpwiaNRNrhSaA%3D%3D",
        }
        self.data = '{"text": "%s", "from": "eng", "to": "ara"}'

    def _translate(self, string):
        return requests.post(self.url, self.data % string.replace('"', '').replace('%', ''),
                             headers = self.headers).json()["translation"] if string.strip() != '' else ''


class Bing(Translator):
    def __init__(self):
        self.__tr = MicrosoftTranslator("TranslateToArabic", "m7ojVbqDptFtr4MbWc718YpNIw6IVyJ5FzQMOXsrcxE=")

    def _translate(self, string):
        return self.__tr.translate(string, "ar")


class Selenium:
    def __init__(self, browser):
        if browser == "chrome":
            self._br = Chrome("./chromedriver")
        elif browser == "phantom":
            self._br = PhantomJS("./phantomjs")
        self._br.set_page_load_timeout(15)

    @staticmethod
    def _insert_string(source, string):
        source.send_keys(Keys.CONTROL + "a")
        source.send_keys(Keys.DELETE)
        source.send_keys(string)

    def close(self):
        self._br.close()


class Systran(Selenium, Translator):
    def __init__(self):
        Selenium.__init__(self, "chrome")
        self._br.get("http://www.systranet.com/translate")
        self._br.find_element_by_xpath("//select[@id='src_lang']/option[@value='en']").click()
        self._br.find_element_by_xpath("//select[@id='tgt_lang']/option[@value='ar']").click()

    def _translate(self, string):
        self._br.switch_to.default_content()
        self._insert_string(self._br.find_element_by_id("edit_src"), string)
        self._br.find_element_by_id("tb_tr_btn").click()
        WebDriverWait(self._br, 10).until(ec.invisibility_of_element_located((By.ID, "processing")))
        self._br.switch_to.frame("edit_tgt")
        return self._br.find_element_by_id("tgt").text


class FreeTranslations(Selenium, Translator):
    def __init__(self, browser="phantom"):
        Selenium.__init__(self, browser)
        self._br.get("https://www.freetranslations.org/english-to-arabic-translation.html")

    def _translate(self, string):
        self._insert_string(self._br.find_element_by_id("InputText"), string)
        self._br.find_element_by_class_name("translate-form-control").click()
        WebDriverWait(self._br, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "mttextarea")))
        return self._br.find_element_by_xpath("//*[@id='TranslationOutput']/div").text


class Babylon(Selenium, Translator):
    def __init__(self):
        Selenium.__init__(self, "phantom")
        self._br.get("http://translation.babylon-software.com/english/to-arabic/")
        self._br.find_element_by_class_name("popup-closeButton").click()
        WebDriverWait(self._br, 10).until(ec.invisibility_of_element_located((By.ID, "popup-wrapper")))

    def _translate(self, string):
        self._insert_string(self._br.find_element_by_id("translationSourceTextarea"), string.replace("'", ""))
        self._br.find_element_by_id("btnTranslate").click()
        return self._br.find_element_by_id("resltext").text.replace('\n', ' ')


# >>> Below are currently not working <<<
# Needs a premium key!
class Frengly(Translator):
    def _translate(self, string):
        r = requests.get("http://frengly.com/?src=en&dest=ar&email=eineao@ymail.com&password=translate&text=" + quote(string))
        return BeautifulSoup(r.text, "lxml").translation.get_text()


# Not working properly
class BabelFish(Selenium, Translator):
    def __init__(self):
        Selenium.__init__(self, "chrome")
        self._br.get("http://www.babelfish.fr/dict?src=en&dst=ar&query=+")

    def _translate(self, string):
        result = ''
        for substring in [string[i:i + 999] for i in range(0, len(string), 999)]:
            self._insert_string(self._br.find_element_by_id("txtSource"), substring)
            self._br.find_element_by_class_name("submit").click()
            result += self._br.find_element_by_class_name("row_first").text
        return result.replace('\n', ' ')
