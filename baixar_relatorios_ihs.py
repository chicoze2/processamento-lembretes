import selenium
import json
import time
import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

load_dotenv()
LOGIN_URL = os.getenv('LOGIN_URL')

# Diretório de downloads
download_path = os.path.abspath("downloads")

# Configuração do Selenium para download automático
options = webdriver.ChromeOptions()
prefs = {
    "download.default_directory": download_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
}
options.add_experimental_option("prefs", prefs)

# Carregar dados de login
with open('auth.json', 'r') as file:
    auth_data = json.load(file)

for empresa in auth_data:
    driver = webdriver.Chrome(options=options)
    driver.get(LOGIN_URL)

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "empresa_login"))).send_keys(auth_data[empresa]["codigo"])
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username_login"))).send_keys("IHSMASTER")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "password_login"))).send_keys(auth_data[empresa]["password"])

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login_btn"))).click()

    xpath_hondaMotocicletas = '//*[@id="menuBar"]/ul/li[1]/a/span[1]'
    xpath_servicos2W = '//*[@id="menuBar"]/ul/li[1]/ul/li[4]/a/span'
    
    # Interagir com o dropdown
    menu_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_hondaMotocicletas)))
    ActionChains(driver).move_to_element(menu_element).perform()

    time.sleep(1)  # Pausa para garantir que o dropdown abra

    dropdown_element = WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, xpath_servicos2W)))
    dropdown_element.click()

    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tree:0:j_idt29"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tree:0_2:j_idt29"]'))).click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="tree:0_2_1"]/span/span[3]/a'))).click()

    # Aguardar nova janela
    time.sleep(2)

    # Trocar para a nova janela
    janela_principal = driver.current_window_handle
    janelas = driver.window_handles
    for janela in janelas:
        if janela != janela_principal:
            driver.switch_to.window(janela)
            break

    # Selecionar o segundo valor no select
    select_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tipoRevisao"]')))
    select = Select(select_element)
    select.select_by_index(1)

    # Clicar no botão de download
    download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/form/input[8]")))
    download_button.click()

    # Aguardar download ser concluído
    timeout = 30
    start_time = time.time()
    while time.time() - start_time < timeout:
        arquivos = os.listdir(download_path)
        if arquivos:
            print(f"Download concluído: {arquivos[0]}")
            break
        time.sleep(1)
    else:
        print("Erro: Nenhum arquivo foi baixado dentro do tempo limite.")

    # Fechar pop-up e retornar à janela principal
    driver.close()
    driver.switch_to.window(janela_principal)

driver.quit()
