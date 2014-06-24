from nio.common.discovery import Discoverable, DiscoverableType
from .youtube_block import YouTube
from nio.metadata.properties.string import StringProperty


@Discoverable(DiscoverableType.block)
class YouTubeChannel(YouTube):
    
    URL_FORMAT = ("https://www.googleapis.com/youtube/v3/"
                  "search?order=date&part=snippet&"
                  "type=video&maxResults={0}&channelId={1}&"
                  "key={2}")

    def _prepare_url(self, paging=False):
        headers = {"Content-Type": "application/json"}
        if self.etag is not None:
            headers['If-None-Match'] = self.etag
        if self.modified is not None:
            headers['If-Modified-Since'] = self._modified

        self.url = self.URL_FORMAT.format(
            self.limit,
            self.current_query,
            self.dev_key
        )
        if paging:
            self.url = "%s&pageToken=%s" % (self.url, self._page_token)
            
        return headers
