import requests

from nio.properties import VersionProperty

from .youtube_channel_block import YouTubeChannel


class YouTubeUser(YouTubeChannel):

    USER_CHANNEL_URL = ("https://www.googleapis.com/youtube/v3/"
                        "channels?part=id&forUsername={}&key={}")
    version = VersionProperty("1.0.1")

    def configure(self, context):
        super().configure(context)
        self.queries = [self._get_user_channel_id(u) for u in self.queries]
        self.queries = [q for q in self.queries if q is not None]
        self._update_internal_data()

    def stop(self):
        super().stop()

    def persisted_values(self):
        """ Return a list containing the values to be persisted.
        This function should be overriden in a Block that wishes to use
        persistence. Return a list of the names of the instance level variables
        to save.
        For example, if your block class has an instance level attribute called
        `_values` and you wish to save it, you would return this list:
            ["_values"]
        """
        return ["_id"]

    def _get_user_channel_id(self, username):
        _id = username
        if _id is None:
            headers = {"Content-Type": "application/json"}
            url = self.USER_CHANNEL_URL.format(username, self.dev_key())
            response = requests.get(url, headers=headers, auth=self._auth)
            response = response.json()
            if response.get('error') is not None:
                self.logger.error(
                    "YouTube channel list request failed: {}, "
                    "reasons: {}".format(
                        response['error']['code'],
                        [e['reason'] for e in response['error']['errors']]
                    )
                )
                _id = None
            else:
                channels = response.get('items')
                _id = channels[0].get('id') if len(channels) > 0 else None
        return _id

    def _update_internal_data(self):
        self._n_queries = len(self.queries)
        self._etags = self._etags[:self._n_queries]
        self._modifieds = self._modifieds[:self._n_queries]
        self._prev_freshest = self._prev_freshest[:self._n_queries]
        self._prev_stalest = self._prev_stalest[:self._n_queries]
