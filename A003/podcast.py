#%%
from os import sep
from re import U
import requests
from bs4 import BeautifulSoup as bs
import logging
import pandas as pd

#%%
url = 'https://portalcafebrasil.com.br/todos/podcasts/'

#%%
ret = requests.get(url)

ret.text

#%%
soup = bs(ret.text)

#%%
soup.find('h5').a['href']

#%%
lst_podcast = soup.find_all('h5')

for it in lst_podcast:
    print(f"EP: {it.text}")
    print(f"Link: {it.a['href']}")

#%%
url = 'https://portalcafebrasil.com.br/todos/podcasts/page/{}/?ajax=true'

#%%
url.format(5)

#%%
log = logging.getLogger()
log.setLevel(logging.DEBUG)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
log.addHandler(ch)
#%%
def get_podcast(url):
    ret = requests.get(url)
    soup = bs(ret.text)
    return soup.find_all('h5')

#%%
get_podcast(url)

#%%
i = 1
lst_podcast = []
lst_get = get_podcast(url.format(i))
log.debug(f"Coletado {lst_get} episódios do link: {url.format(i)}")
while (len(lst_get) > 0):
    lst_podcast = lst_podcast + lst_get
    i += 1
    lst_get = get_podcast(url.format(i))
    log.debug(f"Coletado {lst_get} episódios do link: {url.format(i)}")
#%%
len(lst_podcast)

#%%
df = pd.DataFrame(columns=['nome', 'link'])

#%%
for it in lst_podcast:
    df.loc[df.shape[0]] = [it.text, it.a['href']]
#%%
df.shape
df
df.to_csv('banco_de_podcast.csv', sep=';', index=False)