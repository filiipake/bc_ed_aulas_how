# %%
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
# %%
url = 'https://www.vivareal.com.br/aluguel/parana/curitiba/apartamento_residencial/?pagina={}'

# %%
i = 1
ret = requests.get(url.format(i))
soup = bs(ret.text)
#%%
soup
# %%
houses = soup.find_all(
    'a', {'class': 'property-card_content-link js-card-title'})
#%%
houses