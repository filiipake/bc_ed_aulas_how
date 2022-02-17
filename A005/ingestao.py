# %%
from abc import ABC, abstractmethod
import datetime
import json
import os
import time
from typing import List, Union
import requests
import logging
import schedule
import ratelimit
from backoff import on_exception, expo

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

    @on_exception(expo, ratelimit.RateLimitException, max_tries=10)
    @ratelimit.limits(calls=29, period=30)
    @on_exception(expo, requests.exceptions.HTTPError, max_tries=10)
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
# %%


class DataTypeNotSupportedForIngestionException(Exception):
    def __init__(self, data) -> None:
        self.data = data
        self.message = f"Data type {type(data)} is not supported for ingestion."
        super().__init__(self.message)
# %%


class DataWriter():

    def __init__(self, coin: str, api: str) -> None:
        self.api = api
        self.coin = coin
        self.fileName = f"{self.api}/{self.coin}/{datetime.datetime.now()}.json"

    def _write_row(self, row: str) -> None:
        os.makedirs(os.path.dirname(self.fileName), exist_ok=True)
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
class DataIngestor(ABC):

    @property
    def _checkpointFileName(self) -> str:
        return f"{self.__class__.__name__}.checkpoint"

    def __init__(self, writer: DataWriter, coins: List[str], default_start_date: datetime.datetime) -> None:
        self.writer = writer
        self.coins = coins
        self.default_start_date = default_start_date
        self._checkpoint = self._loadCheckpoint()

    def _writeCheckpoint(self):
        with open(self._checkpointFileName, 'w') as f:
            f.write(f"{self._getCheckpoint()}")

    def _loadCheckpoint(self) -> datetime:
        try:
            with open(self._checkpointFileName, 'r') as f:
                return datetime.datetime.strptime(f.read(), "%Y-%m-%d").date()
        except FileNotFoundError:
            return None

    def _getCheckpoint(self):
        if not self._checkpoint:
            return self.default_start_date
        else:
            return self._checkpoint

    def _updateCheckpoint(self, value):
        self._checkpoint = value
        self._writeCheckpoint()

    @abstractmethod
    def ingest(self) -> None:
        pass

# %%


class DaySummaryIngestor(DataIngestor):

    def ingest(self) -> None:
        date = self._getCheckpoint()

        print(date)

        if (date < datetime.datetime.today()):
            for coin in self.coins:
                api = DaySummaryApi(coin=coin)
                data = api.getData(date=date)
                self.writer(coin=coin, api=api.type).write(data)
            self._updateCheckpoint(
                date + datetime.timedelta(days=1))


# %%
ingestor = DaySummaryIngestor(writer=DataWriter, coins=[
    "BTC", "ETH", "LTC"], default_start_date=datetime.datetime(2021, 6, 1))


# %%
@schedule.repeat(schedule.every(1).seconds)
def job():
    ingestor.ingest()


# %%
while True:
    schedule.run_pending()
    time.sleep(0.5)
