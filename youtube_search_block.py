from datetime import datetime

from nio.properties import ListProperty, VersionProperty
from nio.types import StringType

from .youtube_block import YouTube


class YouTubeSearch(YouTube):

    URL_FORMAT = ("https://www.googleapis.com/youtube/v3/"
                  "search?order=date&part=snippet&q={0}&"
                  "type=video&maxResults={1}&key={2}")

    exclude = ListProperty(
        list_obj_type=StringType, title="Terms to Exclude", default=[])
    version = VersionProperty("1.0.0")

    def configure(self, context):
        super().configure(context)
        self._smash_queries()
        lb = self._unix_time(datetime.utcnow() - self.lookback())
        self._freshest = [lb] * self._n_queries

    def _smash_queries(self):
        """ Helper method to take advantage of the YouTube API's multi-
        query support, avoiding unnecessary HTTP requests.

        """

        self.queries = self._quote_multi_word_queries(self.queries)
        query_str = '|'.join(self.queries)

        if len(self.exclude) > 0:
            self.exclude = self._quote_multi_word_queries(self.exclude)
            query_str += ' -' + ' -'.join(self.exclude)

        if len(query_str):
            self.queries = [query_str]
            self._n_queries = 1

    def _quote_multi_word_queries(self, queries):
        single_word = [q for q in queries if len(q.split(' ')) == 1]

        # quote the multi-word queries so that whitespace is not treated
        # as a boolean AND of low precedence.
        # NOTA BENE: Neither the treatment of whitespace nor quotation is
        # documented by Google. This functionality could change at ANY TIME
        multi_word = ['"{}"'.format(q) for q in queries
                      if len(q.split(' ')) > 1]

        return single_word + multi_word

    def _prepare_url(self, paging=False):
        headers = {"Content-Type": "application/json"}
        if self.etag is not None:
            headers['If-None-Match'] = self.etag
        if self.modified is not None:
            headers['If-Modified-Since'] = self._modified

        self.url = self.URL_FORMAT.format(
            self.current_query,
            self.limit(),
            self.dev_key()
        )
        if paging:
            self.url = "%s&pageToken=%s" % (self.url, self._page_token)

        return headers
