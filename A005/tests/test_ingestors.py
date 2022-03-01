import datetime
from importlib.resources import path
from pickletools import read_string1
from unittest.mock import mock_open, patch

import pytest
from writers import DataWriter
from ingestors import DataIngestor


@pytest.fixture
@patch("ingestors.DataIngestor.__abstractmethods__", set())
def data_ingestor_fixture():
    return DataIngestor(
        writer=DataWriter,
        coins=["TEST", "HOW"],
        default_start_date=datetime.date(2021, 6, 21)
    )


@patch("ingestors.DataIngestor.__abstractmethods__", set())
class TestIngestors:

    def test_checkpoint_filename(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._checkpoint_filename
        expected = "DataIngestor.checkpoint"
        assert expected == actual

    def test_load_checkpoint_no_checkpoint(self, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()
        expected = datetime.date(2021, 6, 21)
        assert actual == expected

    @patch("builtins.open", new_callable=mock_open, read_data="2021-06-25")
    def test_load_checkpoint_existing_checkpoint(self, _mock, data_ingestor_fixture):
        actual = data_ingestor_fixture._load_checkpoint()
        expected = datetime.date(2021, 6, 25)
        assert actual == expected

    @patch("ingestors.DataIngestor._write_checkpoint", return_value=None)
    def test_update_checkpoint_checkpoint_updated(self, mock, data_ingestor_fixture):
        data_ingestor = data_ingestor_fixture
        data_ingestor._update_checkpoint(value=datetime.date(2019, 1, 1))
        actual = data_ingestor._checkpoint
        expected = datetime.date(2019, 1, 1)
        assert actual == expected

    @patch("ingestors.DataIngestor._write_checkpoint", return_value=None)
    def test_update_checkpoint_checkpoint_written(self, mock, data_ingestor_fixture):
        data_ingestor = data_ingestor_fixture
        data_ingestor._update_checkpoint(value=datetime.date(2019, 1, 1))
        mock.assert_called_once()

    @patch("builtins.open", new_callable=mock_open, read_data="2021-06-25")
    @patch("ingestor.DataIngestor._checkpoint_filename", return_value="foobar.checkpoint")
    def write_checkpoint(self, mock_checkpoint_filename, mock_open_file, data_ingestor_fixture):
        data_ingestor = data_ingestor_fixture
        data_ingestor._write_checkpoint()
        mock_open_file.assert_called_with(mock_checkpoint_filename, "w")
