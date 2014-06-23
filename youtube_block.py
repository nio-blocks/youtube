from datetime import datetime
from nio.common.discovery import Discoverable, DiscoverableType
from .http_blocks.rest.rest_block import RESTPolling
from nio.metadata.properties.string import StringProperty
from nio.metadata.properties.timedelta import TimeDeltaProperty
from nio.metadata.properties.int import IntProperty
from nio.metadata.properties.list import ListProperty
from nio.common.signal.base import Signal


class YouTubeSignal(Signal):
    def __init__(self, data):
        for k in data:
            setattr(self, k, data[k])


@Discoverable(DiscoverableType.block)
class YouTube(RESTPolling):
    
    URL_FORMAT = ("https://www.googleapis.com/youtube/v3/"
                  "search?order=date&part=snippet&q={0}&"
                  "&type=video&maxResults={1}&key={2}")

    dev_key = StringProperty(default='')
    lookback = TimeDeltaProperty()
    limit = IntProperty(default=20)
    exclude = ListProperty(str)

    def __init__(self):
        super().__init__()
        self._paging_field = 'nextPageToken'
        self._created_field = 'publishedAt'
        self._page_token = None

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
            excl_str = '-'.join(self.exclude)
            query_str = '-'.join([query_str, excl_str])
        self.queries = [query_str]
        self._n_queries = 1

    def _process_response(self, resp):
        signals = []
        paging = False
        status = resp.status_code
        if status == 304:
            return [], paging

        resp = resp.json()
        fresh_posts = posts = [i['snippet'] for i in resp.get('items', [])]
        self._page_token = resp.get(self._paging_field)
        self._logger.debug("YouTube response contains %d posts" % len(posts))
        
        if len(posts) > 0:
            self.update_freshness(posts)
            fresh_posts = self.find_fresh_posts(posts)
            paging = len(fresh_posts) == len(posts)

        signals = [YouTubeSignal(p) for p in fresh_posts]
        self._logger.debug("Found %d fresh posts" % len(signals))

        return signals, paging

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
