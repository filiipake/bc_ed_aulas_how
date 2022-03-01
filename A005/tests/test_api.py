import datetime
from unittest.mock import patch
import pytest
from apis import MercadoBitcoinApi
from apis import TradesApi
from apis import DaySummaryApi
import requests


class TestDaySummaryApi:

    @pytest.mark.parametrize(
        "coin, date, expected",
        [
            ("BTC", datetime.date(2021, 6, 21),
             "https://www.mercadobitcoin.net/api/BTC/day-summary/2021/6/21"),
            ("ETH", datetime.date(2021, 6, 22),
             "https://www.mercadobitcoin.net/api/ETH/day-summary/2021/6/22"),
            ("ETH", datetime.date(2019, 6, 22),
             "https://www.mercadobitcoin.net/api/ETH/day-summary/2019/6/22")
        ]
    )
    def test_get_endpoint(self, coin, date, expected):
        api = DaySummaryApi(coin=coin)
        actual = api._get_endpoint(date=date)
        assert actual == expected


class TestTradesApi:

    @pytest.mark.parametrize(
        "coin, date_from, date_to, expected",
        [
            ("TEST", datetime.datetime(2019, 1, 1), datetime.datetime(
                2019, 1, 2), "https://www.mercadobitcoin.net/api/TEST/trades/1546308000/1546394400"),
            ("TEST", datetime.datetime(2021, 6, 12), datetime.datetime(
                2021, 6, 15), "https://www.mercadobitcoin.net/api/TEST/trades/1623466800/1623726000"),
            ("TEST", None, None,
             "https://www.mercadobitcoin.net/api/TEST/trades"),
            ("TEST", datetime.datetime(2021, 6, 12), None,
             "https://www.mercadobitcoin.net/api/TEST/trades/1623466800"),
            ("TEST", None, datetime.datetime(
                2021, 6, 15),
             "https://www.mercadobitcoin.net/api/TEST/trades")
        ]
    )
    def test_get_endpoint(self, coin, date_from, date_to, expected):
        api = TradesApi(coin=coin)
        actual = api._get_endpoint(date_from=date_from, date_to=date_to)
        assert actual == expected

    def test_get_endpoint_date_from_grater_than_date_to(self):
        with pytest.raises(RuntimeError):
            TradesApi(coin="TEST")._get_endpoint(
                date_from=datetime.datetime(2021, 1, 4),
                date_to=datetime.datetime(2021, 1, 2)
            )

    @pytest.mark.parametrize(
        "date, expected",
        [
            (datetime.datetime(2019, 1, 1), 1546308000),
            (datetime.datetime(2019, 1, 2), 1546394400),
            (datetime.datetime(2021, 6, 12), 1623466800),
            (datetime.datetime(2021, 6, 12, 0, 0, 5), 1623466805),
            (datetime.datetime(2021, 6, 15), 1623726000)
        ]
    )
    def test_get_unix_epoch(self, date, expected):
        actual = TradesApi(coin="TEST")._get_unix_epoch(date)
        assert actual == expected


@pytest.fixture
@patch("apis.MercadoBitcoinApi.__abstractmethods__", set())
def fixture_mercado_bitcoin_api():
    return MercadoBitcoinApi(coin="test")


def mocked_request_get(*args, **kwargs):
    class MockResponse(requests.Response):
        def __init__(self, json_data, status_code) -> None:
            super().__init__()
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if(args[0] == "ValidEndpoint"):
        print(args[0])
        return MockResponse(json_data={"foo": "bar"}, status_code=200)
    else:
        print('kkkk')
        return MockResponse(json_data=None, status_code=404)


@patch("apis.MercadoBitcoinApi._get_endpoint", return_value="ValidEndpoint")
class TestMercadoBitcoinApi:

    @patch("requests.get")
    def test_get_data(self, mock_requests, mock_get_endpoint, fixture_mercado_bitcoin_api):
        fixture_mercado_bitcoin_api.get_data()
        mock_requests.assert_called_once_with("ValidEndpoint")

    @patch("requests.get", side_effect=mocked_request_get)
    def test_get_data_with_valid_endpoint(self, mock_requests, mock_get_endpoint, fixture_mercado_bitcoin_api):
        actual = fixture_mercado_bitcoin_api.get_data()
        expected = {"foo": "bar"}

        assert actual == expected
