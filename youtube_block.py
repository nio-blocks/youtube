from .http_blocks.rest.rest_block import RESTPolling
from nio.metadata.properties.string import StringProperty
from nio.metadata.properties.timedelta import TimeDeltaProperty
from nio.common.signal.status import BlockStatusSignal
from nio.common.block.controller import BlockStatus
from nio.metadata.properties.int import IntProperty
from nio.common.signal.base import Signal


class YouTubeSignal(Signal):
    def __init__(self, data):
        super().__init__()
        for k in data:
            setattr(self, k, data[k])


class YouTube(RESTPolling):

    dev_key = StringProperty(default='', title='Developer Key')
    lookback = TimeDeltaProperty(title='Lookback Period')
    limit = IntProperty(default=20, title='Limit')

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
        fresh_posts = posts = resp.get('items', [])
        self._page_token = resp.get(self._paging_field)
        self._logger.debug("YouTube response contains %d posts" % len(posts))

        if len(posts) > 0:
            self.update_freshness(posts)
            fresh_posts = self.find_fresh_posts(posts)
            paging = len(fresh_posts) == len(posts)

        signals = [YouTubeSignal(p) for p in fresh_posts]
        self._logger.debug("Found %d fresh posts" % len(signals))

        return signals, paging

    def created_epoch(self, post):
        """ Overriden from base class.

        Args:
            post (dict): YouTube post.
        Returns:
            seconds (int): publishedAt in seconds since epoch.

        """
        dt = self._parse_date(post.get('snippet', {}).get(self._created_field, ''))
        return self._unix_time(dt)

    def _validate_response(self, resp):

        # Unauthorized errors come back as 400 with a reason in the response
        # body, so let's check for that and log an Invalid Creds error.
        try:
            error = resp.json().get('error')
            errors = error.get('errors') if error is not None else []
            if resp.status_code == 400 and \
               'keyInvalid' in [err.get('reason') for err in errors]:
                status_signal = BlockStatusSignal(
                    BlockStatus.error, 'Invalid Credentials')

                # Leaving source for backwards compatibility
                # In the future, you will know that a status signal is a block
                # status signal when it contains service_name and name
                #
                # TODO: Remove when source gets added to status signals in nio
                setattr(status_signal, 'source', 'Block')

                self.notify_management_signal(status_signal)
                return False
        except:
            pass

        # Otherwise, just do the normal response validation
        return super()._validate_response(resp)
            
