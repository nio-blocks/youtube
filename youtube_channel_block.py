from nio.common.discovery import Discoverable, DiscoverableType
from .youtube_block import YouTube
from nio.metadata.properties.string import StringProperty


@Discoverable(DiscoverableType.block)
class YouTubeChannel(YouTube):
    
    URL_FORMAT = ("https://www.googleapis.com/youtube/v3/"
                  "search?order=date&part=snippet&q={0}&"
                  "type=video&maxResults={1}&channelId={2}&"
                  "key={3}")

    channel_id = StringProperty(default='')

    def _prepare_url(self, paging=False):
        headers = {"Content-Type": "application/json"}
        if self.etag is not None:
            headers['If-None-Match'] = self.etag
        if self.modified is not None:
            headers['If-Modified-Since'] = self._modified

        self.url = self.URL_FORMAT.format(
            self.current_query,
            self.limit,
            self.channel_id,
            self.dev_key
        )
        if paging:
            self.url = "%s&pageToken=%s" % (self.url, self._page_token)
            
        return headers
