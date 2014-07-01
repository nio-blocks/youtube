from datetime import datetime
from nio.common.discovery import Discoverable, DiscoverableType
from .youtube_block import YouTube
from nio.metadata.properties.list import ListProperty


@Discoverable(DiscoverableType.block)
class YouTubeSearch(YouTube):

    URL_FORMAT = ("https://www.googleapis.com/youtube/v3/"
                  "search?order=date&part=snippet&q={0}&"
                  "type=video&maxResults={1}&key={2}")

    exclude = ListProperty(str)

    def configure(self, context):
        super().configure(context)
        self._smash_queries()
        lb = self._unix_time(datetime.utcnow() - self.lookback)
        self._freshest = [lb] * self._n_queries

    def _smash_queries(self):
        """ Helper method to take advantage of the YouTube API's multi-
        query support, avoiding unnecessary HTTP requests.

        """
        query_str = '|'.join(self.queries)
        if len(self.exclude) > 0:
            excl_str = ' -'.join(self.exclude)
            query_str = ' -'.join([query_str, excl_str])
        self.queries = [query_str]
        self._n_queries = 1

    def _prepare_url(self, paging=False):
        headers = {"Content-Type": "application/json"}
        if self.etag is not None:
            headers['If-None-Match'] = self.etag
        if self.modified is not None:
            headers['If-Modified-Since'] = self._modified

        self.url = self.URL_FORMAT.format(
            self.current_query,
            self.limit,
            self.dev_key
        )
        if paging:
            self.url = "%s&pageToken=%s" % (self.url, self._page_token)

        return headers
