from selenium.webdriver import PhantomJS, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
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
                return self._translate(string)
            except AttributeError:
                time.sleep(2)
            except (ConnectionError, TimeoutException, NoSuchElementException) as e: print(e)
        raise ConnectionAbortedError

    def _translate(self, string):
        pass

    def execution_time(self):
        return time.time() - self._start_time


class Frengly(Translator):
    def _translate(self, string):
        r = requests.get("http://frengly.com/?src=en&dest=ar&email=eineao@ymail.com&password=translate&text=" + quote(string))
        soup = BeautifulSoup(r.text, "lxml").translation.get_text()
        return soup


class BabelFish(Translator):
    def _translate(self, string):
        r = requests.get("http://www.babelfish.fr/dict?src=en&dst=ar&query=" + quote(string))
        r.encoding = "UTF-8"
        return BeautifulSoup(r.text, "lxml").find(class_="source_url_spacer").previous_sibling.strip()


class SLD(Translator):
    def _translate(self, string):
        headers = {
            "Content-type": "application/json",
            "Authorization": "LC apiKey=4lzNWfvaFHpwiaNRNrhSaA%3D%3D",
        }
        data = '{"text": "' + string + '", "from": "eng", "to": "ara"}'
        return requests.post("https://lc-api.sdl.com/translate", headers=headers, data=data).json()["translation"]


class Bing(Translator):
    def __init__(self):
        self.__tr = MicrosoftTranslator("TranslateToArabic", "m7ojVbqDptFtr4MbWc718YpNIw6IVyJ5FzQMOXsrcxE=")

    def _translate(self, string):
        return self.__tr.translate(string, "ar")


class Systran(Translator):
    def __init__(self):
        self._br = Chrome("./chromedriver")
        self._br.set_page_load_timeout(15)

    def _translate(self, string):
        self._br.get("http://www.systranet.com/translate")
        self._br.find_element_by_xpath("//select[@id='src_lang']/option[@value='en']").click()
        self._br.find_element_by_xpath("//select[@id='tgt_lang']/option[@value='ar']").click()
        self._br.find_element_by_id("edit_src").send_keys(string)
        self._br.find_element_by_id("tb_tr_btn").click()
        WebDriverWait(self._br, 10).until(ec.invisibility_of_element_located((By.ID, "processing")))
        self._br.switch_to.frame("edit_tgt")
        return self._br.find_element_by_class_name("systran_seg").text


class FreeTranslations(Translator):
    def __init__(self):
        self._br = PhantomJS("./phantomjs")
        self._br.set_page_load_timeout(15)

    def _translate(self, string):
        self._br.get("https://www.freetranslations.org/english-to-arabic-translation.html")
        self._br.find_element_by_id("InputText").send_keys(string)
        self._br.find_element_by_class_name("translate-form-control").click()
        WebDriverWait(self._br, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "mttextarea")))
        return self._br.find_element_by_xpath("//*[@id='TranslationOutput']/div").get_attribute("innerHTML")


class Babylon(Translator):
    def __init__(self):
        self._br = PhantomJS("./phantomjs")
        self._br.set_page_load_timeout(15)

    def _translate(self, string):
        self._br.get("http://translation.babylon-software.com/english/to-arabic/")
        try:
            self._br.find_element_by_class_name("popup-closeButton").click()
            WebDriverWait(self._br, 10).until(ec.invisibility_of_element_located((By.ID, "popup-wrapper")))
        except ElementNotVisibleException: pass
        self._br.find_element_by_id("translationSourceTextarea").send_keys(string.replace("'", ""))
        self._br.find_element_by_id("btnTranslate").click()
        return self._br.find_element_by_id("resltext").get_attribute("innerHTML")
