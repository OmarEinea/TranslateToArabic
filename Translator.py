from selenium.webdriver import Chrome, PhantomJS
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import requests, time
from requests.exceptions import ConnectionError
from urllib.parse import quote
from bs4 import BeautifulSoup
from datetime import datetime


class MyTranslator:
    def translate(self, string):
        pass


class Bing(MyTranslator):
    def __init__(self):
        from microsofttranslator import Translator
        self.tr = Translator("TranslateToArabic", "m7ojVbqDptFtr4MbWc718YpNIw6IVyJ5FzQMOXsrcxE=")

    def translate(self, string):
        for i in range(3):
            try:
                return self.tr.translate(string, "ar")
            except ConnectionError: pass
        raise ConnectionAbortedError


class Frengly(MyTranslator):
    def translate(self, string):
        for i in range(3):
            try:
                r = requests.get("http://frengly.com/?src=en&dest=ar&email=eineao@ymail.com&password=translate&text=" + quote(string))
                soup = BeautifulSoup(r.text, "lxml").translation.get_text()
                return soup
            except AttributeError:
                time.sleep(2)
            except ConnectionError: pass
        raise ConnectionAbortedError


class BabelFish(MyTranslator):
    def translate(self, string):
        for i in range(3):
            try:
                r = requests.get("http://www.babelfish.fr/dict?src=en&dst=ar&query=" + quote(string))
                r.encoding = "UTF-8"
                return BeautifulSoup(r.text, "lxml").find(class_="source_url_spacer").previous_sibling.strip()
            except (ConnectionError, AttributeError): pass
        raise ConnectionAbortedError


class FreeTranslations(MyTranslator):
    def __init__(self):
        self.__br = PhantomJS("./phantomjs")
        self.__br.set_page_load_timeout(15)

    def translate(self, string):
        for i in range(3):
            try:
                self.__br.get("https://www.freetranslations.org/english-to-arabic-translation.html")
                self.__br.find_element_by_id("InputText").send_keys(string)
                self.__br.find_element_by_class_name("translate-form-control").click()
                WebDriverWait(self.__br, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "mttextarea")))
                return self.__br.find_element_by_xpath("//*[@id='TranslationOutput']/div").get_attribute("innerHTML")
            except (TimeoutException, NoSuchElementException): pass
        raise ConnectionAbortedError


class SLD(MyTranslator):
    def translate(self, string):
        headers = {
            "Content-type": "application/json",
            "Authorization": "LC apiKey=4lzNWfvaFHpwiaNRNrhSaA%3D%3D",
        }
        data = '{"text": "' + string + '", "from": "eng", "to": "ara"}'
        return requests.post("https://lc-api.sdl.com/translate", headers=headers, data=data).json()["translation"]


class Babylon(MyTranslator):
    def __init__(self):
        self.__br = Chrome("./chromedriver")
        self.__br.set_page_load_timeout(15)

    def translate(self, string):
        for i in range(3):
            try:
                self.__br.get("http://translation.babylon-software.com/english/to-arabic/")
                self.__br.find_element_by_class_name("popup-closeButton").click()
                WebDriverWait(self.__br, 10).until(ec.invisibility_of_element_located((By.ID, "popup-wrapper")))
                self.__br.find_element_by_id("translationSourceTextarea").send_keys(string)
                self.__br.find_element_by_id("btnTranslate").click()
                return self.__br.find_element_by_id("resltext").get_attribute("innerHTML")
            except TimeoutException: pass
        raise ConnectionAbortedError


class Systran(MyTranslator):
    def __init__(self):
        self.__br = Chrome("./chromedriver")
        self.__br.set_page_load_timeout(15)

    def translate(self, string):
        for i in range(3):
            try:
                self.__br.get("http://www.systranet.com/translate")
                self.__br.find_element_by_xpath("//select[@id='src_lang']/option[@value='en']").click()
                self.__br.find_element_by_xpath("//select[@id='tgt_lang']/option[@value='ar']").click()
                self.__br.find_element_by_id("edit_src").send_keys(string)
                self.__br.find_element_by_id("tb_tr_btn").click()
                WebDriverWait(self.__br, 10).until(ec.invisibility_of_element_located((By.ID, "processing")))
                self.__br.switch_to.frame("edit_tgt")
                return self.__br.find_element_by_class_name("systran_seg").text
            except TimeoutException: pass
        raise ConnectionAbortedError
