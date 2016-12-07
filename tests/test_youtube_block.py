from unittest.mock import patch
from requests import Response
from ..youtube_block import YouTube
from nio.testing.block_test_case import NIOBlockTestCase
from threading import Event


class YTTestBlk(YouTube):
    def __init__(self, event):
        super().__init__()
        self._event = event

    def _paging(self):
        self._event.set()


class TestYouTube(NIOBlockTestCase):

    @patch("requests.get")
    @patch("requests.Response.json")
    @patch.object(YouTube, 'created_epoch')
    def test_process_responses(self, mock_epoch, mock_json, mock_get):
        mock_get.return_value = Response()
        mock_get.return_value.status_code = 200
        mock_epoch.return_value = 23
        mock_json.return_value = {
            'items': [
                {'snippet': {'key': 'val'}}
            ]
        }
        e = Event()
        blk = YTTestBlk(e)
        self.configure_block(blk, {
            "log_level": "DEBUG",
            "polling_interval": {
                "seconds": 1
            },
            "retry_interval": {
                "seconds": 1
            },
            "queries": [
                "foobar"
            ],
            "limit": 2,
        })
        blk._freshest = [22]

        blk.start()
        e.wait(2)

        self.assertEqual(blk._freshest, [23])
        self.assert_num_signals_notified(1)

        blk.stop()
