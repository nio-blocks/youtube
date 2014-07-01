from .http_blocks.rest.rest_block import RESTPolling
from nio.metadata.properties.string import StringProperty
from nio.metadata.properties.timedelta import TimeDeltaProperty
from nio.metadata.properties.int import IntProperty
from nio.common.signal.base import Signal


class YouTubeSignal(Signal):
    def __init__(self, data):
        for k in data:
            setattr(self, k, data[k])


class YouTube(RESTPolling):

    dev_key = StringProperty(default='')
    lookback = TimeDeltaProperty()
    limit = IntProperty(default=20)

    def __init__(self):
        super().__init__()
        self._paging_field = 'nextPageToken'
        self._created_field = 'publishedAt'
        self._page_token = None

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
