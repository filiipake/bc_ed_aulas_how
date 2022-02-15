# %%
from abc import ABC, abstractmethod
import datetime
import json
from typing import List, Union
import requests
import logging

# %%
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
# %%


class MercadoBitcoinApi(ABC):

    def __init__(self, coin: str) -> None:
        self.coin = coin
        self.baseEndpoint = 'https://www.mercadobitcoin.net/api'
        pass

    @abstractmethod
    def _getEndpoint(self, **kwargs) -> str:
        pass

    def getData(self, **kwargs) -> dict:
        response = requests.get(self._getEndpoint(**kwargs))
        logger.info(
            f"Getting data from endpoint: {self._getEndpoint(**kwargs)}")
        response.raise_for_status
        return response.json()

# %%


class DaySummaryApi(MercadoBitcoinApi):

    type = "day-summary"

    def _getEndpoint(self, date: datetime.date) -> str:
        return f"{self.baseEndpoint}/{self.coin}/{self.type}/{date.year}/{date.month}/{date.day}"

# %%


class TradesApi(MercadoBitcoinApi):
    type = "trades"

    def getUnixEpoch(self, date: datetime) -> int:
        return int(date.timestamp())

    def _getEndpoint(self, dateFrom: datetime = None, dateTo: datetime = None) -> str:
        if (dateFrom and not dateTo):
            unixDateFrom = self.getUnixEpoch(dateFrom)
            endpoint = f"{self.baseEndpoint}/{self.coin}/{self.type}/{unixDateFrom}"
        elif (dateFrom and dateTo):
            unixDateFrom = self.getUnixEpoch(dateFrom)
            unixDateTo = self.getUnixEpoch(dateTo)
            endpoint = f"{self.baseEndpoint}/{self.coin}/{self.type}/{unixDateFrom}/{unixDateTo}"
        else:
            endpoint = f"{self.baseEndpoint}/{self.coin}/{self.type}"

        return endpoint
#%%
class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data) -> None:
        self.data = data
        self.message = f"Data type {type(data)} is not supported for ingestion."
        super().__init__(self.message)
# %%

class DataWriter():

    def __init__(self, fileName: str) -> None:
        self.fileName = fileName

    def _write_row(self, row: str) -> None:
        with open(self.fileName, 'a') as f:
            f.write(row)

    def write(self, data: Union[List, dict]):

        if(isinstance(data, dict)):
            self._write_row(json.dumps(data) + "\n")
        
        elif(isinstance(data, List)):
            for it in data:
                self.write(it)
        else:
            raise DataTypeNotSupportedForIngestionException(data)


# %%
data = DaySummaryApi(coin="BTC").getData(date=datetime.date(2022, 2, 14))
writer = DataWriter('day_summary.json')
writer.write(data)
# %%
data = TradesApi(coin="BTC").getData()
writer = DataWriter('trades.json')
writer.write(data)