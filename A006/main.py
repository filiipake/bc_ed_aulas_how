# %%
import sys
from selenium import webdriver

#%%
cep = sys.argv[1]

if cep:
    # %%
    driver = webdriver.Chrome("./src/chromedriver")
    driver.get('https://buscacepinter.correios.com.br/app/endereco/index.php?t')
    # %%
    cepElement = driver.find_element_by_name('endereco')
    cepTypeElement = driver.find_element_by_name('tipoCEP')
    # %%
    cepElement.clear()
    cepElement.send_keys(cep)
    cepTypeElement.click()
    driver.find_element_by_xpath(
        '//*[@id="formulario"]/div[2]/div/div[2]/select/option[6]').click()

    driver.find_element_by_id('btn_pesquisar').click()

    #%%
    address = driver.find_element_by_xpath('/html/body/main/form/div[1]/div[2]/div/div[3]/table/tbody/tr/td[1]').text
    neighborhood = driver.find_element_by_xpath('/html/body/main/form/div[1]/div[2]/div/div[3]/table/tbody/tr/td[2]').text
    city = driver.find_element_by_xpath('/html/body/main/form/div[1]/div[2]/div/div[3]/table/tbody/tr/td[3]').text
    zipcode = driver.find_element_by_xpath('/html/body/main/form/div[1]/div[2]/div/div[3]/table/tbody/tr/td[4]').text
    driver.close()

    #%%
    print("""
    Para o CEP {} temos:

    Endereço: {}
    Bairro: {}
    Localidade: {}
    """.format(
        cep,
        address.split(' - ')[0],
        neighborhood,
        city
    ))