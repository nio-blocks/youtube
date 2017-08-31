YouTubeChannel
==============
Create a signal for each new video post, given a channel ID. When you view the source code of a channel page on YouTube, the channel ID is found by searching for 'channelId'.

Properties
----------
- **dev_key**: Youtube API credentials.
- **include_query**: Whether to include queries in request to facebook.
- **limit**: Number of posts to come back on each url request to Facebook.
- **lookback**: On block start, look back this amount of time to grab old posts.
- **polling_interval**: How often Youtube is polled. When using more than one query. Each query will be polled at a period equal to the *polling interval* times the number of queries.
- **queries**: Queries to include on request to Youtube
- **retry_interval**: When a url request fails, how long to wait before attempting to try again.
- **retry_limit**: Number of times to retry on a poll.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: Creates a new signal for each Video. Every field on the Video will become a signal attribute.

Commands
--------
None

Output Example
--------------
The following is a list of commonly include attributes, but note that not all will be included on every signal:
```
{
  id: {
    videoId: int
  },
  snippet: {
    channelTitle: string,
    title: string,
    description: string,
    thumbnails: {
      high: {
        url: string
      }
    },
    publishedAt: datetime
  }
}
```

YouTubeSearch
=============
Search Youtube for specified query.

Properties
----------
- **dev_key**: Youtube API credentials.
- **exclude**: List of terms to exclude from results.
- **include_query**: Whether to include queries in request to facebook.
- **limit**: Number of posts to come back on each url request to Facebook.
- **lookback**: On block start, look back this amount of time to grab old posts.
- **polling_interval**: How often Youtube is polled. When using more than one query. Each query will be polled at a period equal to the *polling interval* times the number of queries.
- **queries**: Queries to include on request to Youtube
- **retry_interval**: When a url request fails, how long to wait before attempting to try again.
- **retry_limit**: Number of times to retry on a poll.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: Creates a new signal for each Video. Every field on the Video will become a signal attribute.

Commands
--------
None

Output Example
--------------
The following is a list of commonly include attributes, but note that not all will be included on every signal:
```
{
  id: {
    videoId: int
  },
  snippet: {
    channelTitle: string,
    title: string,
    description: string,
    thumbnails: {
      high: {
        url: string
      }
    },
    publishedAt: datetime
  }
}
```

YouTubeUser
===========
Search Youtube for specified user videos.

Properties
----------
- **dev_key**: Youtube API credentials.
- **include_query**: Whether to include queries in request to facebook.
- **limit**: Number of posts to come back on each url request to Facebook.
- **lookback**: On block start, look back this amount of time to grab old posts.
- **polling_interval**: How often Youtube is polled. When using more than one query. Each query will be polled at a period equal to the *polling interval* times the number of queries.
- **queries**: Queries to include on request to Youtube
- **retry_interval**: When a url request fails, how long to wait before attempting to try again.
- **retry_limit**: Number of times to retry on a poll.

Inputs
------
- **default**: Any list of signals.

Outputs
-------
- **default**: Creates a new signal for each Video. Every field on the Video will become a signal attribute.

Commands
--------
None

Output Example
--------------
The following is a list of commonly include attributes, but note that not all will be included on every signal:
```
{
  id: {
    videoId: int
  },
  snippet: {
    channelTitle: string,
    title: string,
    description: string,
    thumbnails: {
      high: {
        url: string
      }
    },
    publishedAt: datetime
  }
}
```

