from datetime import datetime
from nio.util.discovery import discoverable
from .youtube_block import YouTube


@discoverable
class YouTubeChannel(YouTube):

    URL_FORMAT = ("https://www.googleapis.com/youtube/v3/"
                  "search?order=date&part=snippet&"
                  "type=video&maxResults={0}&channelId={1}&"
                  "key={2}")

    def configure(self, context):
        super().configure(context)
        lb = self._unix_time(datetime.utcnow() - self.lookback())
        self._freshest = [lb] * self._n_queries

    def _prepare_url(self, paging=False):
        headers = {"Content-Type": "application/json"}
        if self.etag is not None:
            headers['If-None-Match'] = self.etag
        if self.modified is not None:
            headers['If-Modified-Since'] = self._modified

        self.url = self.URL_FORMAT.format(
            self.limit(),
            self.current_query,
            self.dev_key()
        )
        if paging:
            self.url = "%s&pageToken=%s" % (self.url, self._page_token)

        return headers
