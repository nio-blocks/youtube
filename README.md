YouTube Blocks
=============

There are two YouTube blocks. The basic YouTube block searches for all videos with a given string of words. The YouTubeChannel block will search only the specified channels and will return all videos on that channel.

-   [YouTube](https://github.com/nio-blocks/youtube#youtube)
-   [YouTubeChannel](https://github.com/nio-blocks/youtube#youtubechannel)

***
***

YouTube
==============

Create a signal for each new video post for a given query. Official documentation [here](https://developers.google.com/youtube/v3/docs/search).

Properties
--------------

-   **queries**: List of queries to search for.
-   **dev_key**: API credentials.
-   **polling_interval**: How often API is polled.
-   **retry_interval**: When a url request fails, how long to wait before attempting to try again.
-   **retry_limit**: When a url request fails, number of times to attempt a retry before giving up.
-   **lookback**: On block start, look back this amount of time to grab old posts.
-   **limit**: Number of posts to come back on each url request.

Commands
----------------
None

Input
-------
None

Output
---------
Creates a new signal for each Video. Every field on the Video will become a signal attribute. The following is a list of commonly include attributes, but note that not all will be included on every signal:

-   id['videoId']
-   snippet['channelTitle']
-   snippet['title']
-   snippet['description']
-   snippet['thumbnails']['high']['url']
-   snippet['publishedAt']


***
***


YouTubeChannel
==============

Create a signal for each new video post, given a channel ID. Official documentation [here](https://developers.google.com/youtube/v3/docs/search).

Properties
--------------

-   **queries**: List of channel IDs to query.
-   **dev_key**: API credentials.
-   **polling_interval**: How often API is polled.
-   **retry_interval**: When a url request fails, how long to wait before attempting to try again.
-   **retry_limit**: When a url request fails, number of times to attempt a retry before giving up.
-   **lookback**: On block start, look back this amount of time to grab old posts.
-   **limit**: Number of posts to come back on each url request.

Commands
----------------
None

Input
-------
None

Output
---------
Creates a new signal for each Video. Every field on the Video will become a signal attribute. The following is a list of commonly include attributes, but note that not all will be included on every signal:

-   id['videoId']
-   snippet['channelTitle']
-   snippet['title']
-   snippet['description']
-   snippet['thumbnails']['high']['url']
-   snippet['publishedAt']
