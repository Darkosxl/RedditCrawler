# Reddit Crawler

Scrape Reddit posts and comments using FastAPI endpoints

## Setup

1. Clone and install dependencies:
```bash
git clone https://github.com/Darkosxl/RedditCrawler.git
cd RedditCrawler
pip install -r requirements.txt
playwright install chromium
```

2. Get a free residential proxy from [ScrapeOps](https://scrapeops.io/) (they have a free trial)

3. Create a `.env` file:
```

ENDPOINT_PASSWORD=your_secret_password (for using this  in a vps)
PROXY_API_KEY=your_scrapeops_proxy_url
```

4. Run the server:
```bash
uvicorn fastapi_endpoints:app --reload
```

## API Endpoints

All endpoints require `Authorization: Bearer your_secret_password` header.

### GET /crawlsubreddit

Scrape posts from a subreddit.

```bash
curl "http://localhost:8000/crawlsubreddit?subreddit=https://reddit.com/r/programming&num_posts=10" \
  -H "Authorization: Bearer your_secret_password"
```

**Response:**
```json
{
  "status": "success",
  "source_url": "https://reddit.com/r/programming",
  "post_count": 10,
  "posts": [
    {
      "title": "Post title",
      "author": "username",
      "score": "1234",
      "comment_count": "56",
      "permalink": "/r/programming/comments/...",
      "created_timestamp": "2024-01-01T12:00:00Z"
    }
  ]
}
```

### GET /crawlpostcomments

Scrape comments from a specific post.

```bash
curl "http://localhost:8000/crawlpostcomments?post_link=https://reddit.com/r/programming/comments/abc123/some_post&comment_limit=20" \
  -H "Authorization: Bearer your_secret_password"
```

**Response:**
```json
{
  "status": "success",
  "source_url": "https://reddit.com/r/programming/comments/...",
  "comment_count": 20,
  "comments": [
    {
      "author": "username",
      "upvotes": "123",
      "body": "Comment text here",
      "created_timestamp": "2024-01-01T12:00:00Z"
    }
  ]
}
```

### GET /health

Health check endpoint (no auth required).

```bash
curl http://localhost:8000/health
```

## Apify

This crawler is also available on [Apify](https://apify.com/dark_warro/reddit-crawler). Check `.actor/README.md` for Apify-specific usage.
