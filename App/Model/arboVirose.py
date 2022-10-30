import os
import urllib.request
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.utils import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def initDriver(name):
    if name == ("google-chrome.desktop" or "brave-browser.desktop" or "chromium_chromium.desktop"):
        options = ChromeOptions()
        options.add_argument("--headless")

        if name == "google-chrome.desktop":
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        elif name == "brave-browser.desktop":
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()), options=options)
        elif name == "chromium_chromium.desktop":
            driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()), options=options)

    elif (name == "firefox.desktop"):
        options = FirefoxOptions()
        options.add_argument("--headless")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install(), log_path=os.devnull), options=options)

    return driver

class arboVirose():
    def __init__(self, arbo_v):
        os.environ['WDM_LOG_LEVEL'] = '0'
        self.arbo_v = arbo_v
        self.obterInfo()
    
    def obterUrl(self):
        if self.arbo_v == 'Dengue':
            return "http://www3.saude.ba.gov.br/cgi/deftohtm.exe?sinan/deng.def"
        elif self.arbo_v == 'Chikungunya':
            return "http://www3.saude.ba.gov.br/cgi/deftohtm.exe?sinan/chikun.def"
        elif self.arbo_v == 'Zika':
            return "http://www3.saude.ba.gov.br/cgi/deftohtm.exe?sinan/zika.def"
    
    def obterInfo(self):
        html = urllib.request.urlopen(self.obterUrl())
        soup = BeautifulSoup(html, 'html5lib')

        linha = soup.find("div", {"class": "linha"}).find("select").select("option")
        linha = list(map(lambda tmp: tmp.get_text().strip(), linha))

        coluna = soup.find("div", {"class": "coluna"}).find("select").select("option")
        coluna = list(map(lambda tmp: tmp.get_text().strip(), coluna))

        periodo = soup.find("div", {"class": "periodo"}).find("select").select("option")
        periodo = list(map(lambda tmp: tmp.get_text().strip(), periodo))
        
        self.linha, self.coluna, self.periodo = linha, coluna, periodo
    
    def obterDf(self, linha_valor, coluna_valor, periodo_valor):
        browser_name = ["google-chrome.desktop", "brave-browser.desktop", "chromium_chromium.desktop"]
        
        for item in browser_name:
            try:
                driver = initDriver(item)
                break
            except:
                pass

        driver.set_page_load_timeout(100)
        driver.get(self.obterUrl())

        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CLASS_NAME, 'mostra')))

        if self.arbo_v == "Dengue" or self.arbo_v == "Chikungunya":
            # Linha
            driver.find_element(By.XPATH, f'/html/body/div/center/div/form/div[2]/div/div[1]/select/option[{self.linha.index(linha_valor)+1}]').click()
            # Coluna
            driver.find_element(By.XPATH, f'/html/body/div/center/div/form/div[2]/div/div[2]/select/option[{self.coluna.index(coluna_valor)+1}]').click()
            # Periodo
            driver.find_element(By.XPATH, '/html/body/div/center/div/form/div[3]/div/select/option[1]').click()
            for i, item in enumerate(self.periodo):
                if item in periodo_valor:
                    driver.find_element(By.XPATH, f'/html/body/div/center/div/form/div[3]/div/select/option[{i+1}]').click()
            # Mostra
            driver.find_element(By.XPATH, '/html/body/div/center/div/form/div[4]/div[2]/div[2]/input[1]').click()
        else:
            # Linha
            driver.find_element(By.XPATH, f'/html/body/center/div/form/div[2]/div/div[1]/select/option[{self.linha.index(linha_valor)+1}]').click()
            # Coluna
            driver.find_element(By.XPATH, f'/html/body/center/div/form/div[2]/div/div[2]/select/option[{self.coluna.index(coluna_valor)+1}]').click()
            # Periodo
            driver.find_element(By.XPATH, '/html/body/center/div/form/div[3]/div/select/option[1]').click()
            for i, item in enumerate(self.periodo):
                if item in periodo_valor:
                    driver.find_element(By.XPATH, f'/html/body/center/div/form/div[3]/div/select/option[{i+1}]').click()

            # Mostra
            driver.find_element(By.XPATH, '/html/body/center/div/form/div[4]/div[2]/div[2]/input[1]').click()

        html = driver.page_source
        driver.quit()
        
        soup = BeautifulSoup(html, 'html.parser')
        tabdados = soup.select(".tabdados tbody tr td ")
        tabdados = list(map(lambda tmp: tmp.get_text().strip(), tabdados))
        col_tabdados = soup.select(".tabdados th ")
        col_tabdados = list(map(lambda tmp: tmp.get_text().strip(), col_tabdados))
        
        tam_lin = int(len(tabdados)/len(col_tabdados))
        tam_col = len(col_tabdados)

        aux = []
        for i in range (tam_lin):
            aux_2 = []
            for j in range (tam_col):  
                aux_2.append(tabdados.pop(0))
            aux.append(aux_2)

        df = pd.DataFrame(aux, columns=col_tabdados)
        df = df.drop(columns=['Total'])
        df = df.drop(0)
        df = df.reset_index()
        df = df.drop(columns=['index'])
        
        aux = []
        for item in df.iloc[:, 0]:
            aux.append(item.split(" ", 1))

        aux = pd.DataFrame(aux)

        df["Código"] = aux[0]
        df["Município"] = aux[1]

        aux = list(df.columns)
        aux.insert(0, aux.pop())
        df = df[aux]
        
        df.iloc[:, 2:] = df.iloc[:, 2:].astype('str').replace('\.', '', regex=True)
        df.iloc[:, 2:] = df.iloc[:, 2:].astype('str').replace('-', '0')
        
        return df