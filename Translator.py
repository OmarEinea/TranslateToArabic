from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome
from time import sleep


class Translator:
    def __init__(self, headless=False):
        options = Options()
        if headless: options.headless = True
        self._br = Chrome(chrome_options=options)
        self._br.get("https://www.freetranslations.org/english-to-arabic-translation.html")
        # self._br.set_page_load_timeout(25)

    def translate(self, string):
        for i in range(3):
            try: return self._translate(string.replace("\\", ''))
            except Exception as e:
                print(e)
                sleep(2)
        raise ConnectionAbortedError

    def _translate(self, string):
        tag = self._br.find_element_by_id("InputText")
        tag.send_keys(Keys.CONTROL + "a")
        tag.send_keys(Keys.DELETE)
        tag.send_keys(string)
        self._br.find_element_by_class_name("translate-form-control").click()
        WebDriverWait(self._br, 10).until(ec.presence_of_element_located((By.CLASS_NAME, "mttextarea")))
        return self._br.find_element_by_xpath("//*[@id='TranslationOutput']/div").text

    def close(self):
        self._br.close()
