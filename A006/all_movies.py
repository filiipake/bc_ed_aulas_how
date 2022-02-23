# %%
import time
import pandas
from selenium import webdriver

# %%
driver = webdriver.Chrome("./src/chromedriver")
time.sleep(5)
driver.get('https://pt.wikipedia.org/wiki/Nicolas_Cage')
table = driver.find_element_by_xpath(
    '//*[@id="mw-content-text"]/div[1]/table[2]')

# %%
print(table.get_attribute('innerHTML'))

#%%
df = pandas.read_html('<table>' + table.get_attribute('innerHTML') + '</table>')[0]
df.to_csv('filmes_nicolas_cage.csv', sep = ";", index=False)