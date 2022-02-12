#%%
#imports
import requests
import json

#%%
url = 'https://economia.awesomeapi.com.br/json/last/USD-BRL'
ret = requests.get(url)

# %%
if ret:
    print(ret)
else:
    print('Falhou')

# %%
ret.text
dolar = json.loads(ret.text)['USDBRL']
print( f"20 Dólares hoje custam {float(dolar['bid']) * 20 } reais")

# %%
def cotacao(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-', '')]
    print( f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor } {moeda[-3:]}")

#%%
cotacao(20, 'USD-BRL')

#%%
try:
    cotacao(20, 'Rafael')
except Exception as e:
    print(e)
else:
    print('OK')
        
#%%
lst_money = [
        "USD-BRL",
        "EUR-BRL",
        "BTC-BRL",
        "JPY-BRL",
        "RPL-BRL"
]

multi_moedas(20, "USD-BRL")

#%%
def error_check(func):
    
    def inner_func(*args, **kargs):
        try:
            func(*args, **kargs)
        except:
            print(f"{func.__name__} falhou")
    
    return inner_func

@error_check
def multi_moedas(valor, moeda):
    url = f'https://economia.awesomeapi.com.br/json/last/{moeda}'
    ret = requests.get(url)
    dolar = json.loads(ret.text)[moeda.replace('-', '')]
    print( f"{valor} {moeda[:3]} hoje custam {float(dolar['bid']) * valor } {moeda[-3:]}")

#%%
multi_moedas(20,"USD-BRL")
multi_moedas(20,"EUR-BRL")
multi_moedas(20,"BTC-BRL")
multi_moedas(20,"JPY-BRL")
multi_moedas(20,"RPL-BRL")

#%%
import backoff
