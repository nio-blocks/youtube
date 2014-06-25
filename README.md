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
