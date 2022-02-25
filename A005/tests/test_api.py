import datetime

from apis import DaySummaryApi


def test_get_endpoint_BTC():
    date = datetime.date(2021, 6, 21)
    api = DaySummaryApi(coin="BTC")
    actual = api._get_endpoint(date=date)
    expected = "https://www.mercadobitcoin.net/api/BTC/day-summary/2021/6/21"
    assert actual == expected

def test_get_endpoint_ETH():
    date = datetime.date(2021, 6, 21)
    api = DaySummaryApi(coin="ETH")
    actual = api._get_endpoint(date=date)
    expected = "https://www.mercadobitcoin.net/api/ETH/day-summary/2021/6/21"
    assert actual == expected
