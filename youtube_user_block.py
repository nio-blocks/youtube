from datetime import datetime
from nio.common.discovery import Discoverable, DiscoverableType
from .youtube_channel_block import YouTubeChannel


@Discoverable(DiscoverableType.block)
class YouTubeUser(YouTubeChannel):

    USER_CHANNEL_URL = ("https://www.googleapis.com/youtube/v3/"
                        "channels?part=id&forUsername={}&key={}")

    def configure(self, context):
        super().configure(context)
        for idx, q in enumerate(self.queries):
            self.queries[idx] = self._get_user_channel_id(q)

    def _get_user_channel_id(self, username):
        headers = {"Content-Type": "application/json"}
        url = self.USER_CHANNEL_URL.format(username, self.dev_key)
        response = requests.get(url, headers=headers, auth=self._auth)
        print(response.json())
        return response.json().get('items')[0].get('id')
        
