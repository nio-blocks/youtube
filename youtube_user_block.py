from datetime import datetime
import requests
from nio.common.discovery import Discoverable, DiscoverableType
from .youtube_channel_block import YouTubeChannel


@Discoverable(DiscoverableType.block)
class YouTubeUser(YouTubeChannel):

    USER_CHANNEL_URL = ("https://www.googleapis.com/youtube/v3/"
                        "channels?part=id&forUsername={}&key={}")

    def configure(self, context):
        super().configure(context)
        self.queries = [self._get_user_channel_id(u) for u in self.queries]
        self.queries = [q for q in self.queries if q is not None]
        self._update_internal_data()

    def _get_user_channel_id(self, username):
        headers = {"Content-Type": "application/json"}
        url = self.USER_CHANNEL_URL.format(username, self.dev_key)
        response = requests.get(url, headers=headers, auth=self._auth)
        response = response.json()
        if response.get('error') is not None:
            self._logger.error(
                "YouTube channel list request failed: {}: {}".format(
                    [e['reason'] for e in response['error']['errors']]
                )
            )
            json().get('items')[0].get('id')
        channels = response.get('items')
        return channels[0].get('id') if len(channels) == 1 else None

    def _update_internal_data(self):
        self._n_queries = len(self.queries)
        self._etags = self._etags[:self._n_queries]
        self._modifieds = self._modifieds[:self._n_queries]
        self._prev_freshest = self._prev_freshest[:self._n_queries]
        self._prev_stalest = self._prev_stalest[:self._n_queries]
