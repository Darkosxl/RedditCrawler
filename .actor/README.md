# Reddit Crawler

Scrape posts from any subreddit or grab comments from specific Reddit posts. No API keys needed.

## What it does

- **Subreddit mode**: Give it a subreddit name, get back posts with titles, authors, scores, and URLs
- **Post mode**: Give it one or more post URLs, get back the top comments

## How to use

### Crawl posts from a subreddit

```json
{
  "subreddit": "programming",
  "num_posts": 10
}
```

### Crawl comments from posts

```json
{
  "post_urls": [
    "https://www.reddit.com/r/programming/comments/abc123/some_post/",
    "https://www.reddit.com/r/webdev/comments/xyz789/another_post/"
  ],
  "comment_limit": 20
}
```

## Inputs

| Field | Type | Description |
|-------|------|-------------|
| `subreddit` | string | Subreddit name (without r/) |
| `num_posts` | number | How many posts to grab (default: 10) |
| `post_urls` | array | List of Reddit post URLs to scrape comments from |
| `comment_limit` | number | Max comments per post (default: 10) |
| `proxy_config` | string | Optional proxy URL (recommended for heavy use) |

## Output

Posts include: title, author, score, comment count, permalink, timestamp

Comments include: author, upvotes, body text, timestamp
