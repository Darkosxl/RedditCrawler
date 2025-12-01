import asyncio
import json
import math
import os

import dotenv
import requests
from crawl4ai import (
    AdaptiveConfig,
    AdaptiveCrawler,
    AsyncWebCrawler,
    BrowserConfig,
    CacheMode,
    CrawlerRunConfig,
    LLMConfig,
    VirtualScrollConfig,
    JsonCssExtractionStrategy
)
from scrapeops_python_requests.scrapeops_requests import ScrapeOpsRequests

scrapeops_logger = ScrapeOpsRequests(
    scrapeops_api_key="c05e7246-4ab0-4d43-9457-c80e85631786",
    spider_name="Scraping Amazon",
    job_name="Clothing Section",
)

request = scrapeops_logger.RequestsWrapper()
dotenv.load_dotenv()


async def subredditcrawl(subreddit_url, num_posts):
    
    schema = {
            "name": "Reddit Posts",
            "baseSelector": "shreddit-post",
            "baseFields": [
                {"name": "title", "type": "attribute", "attribute": "post-title"},
                {"name": "author", "type": "attribute", "attribute": "author"},
                {"name": "score", "type": "attribute", "attribute": "score"},
                {"name": "comment_count", "type": "attribute", "attribute": "comment-count"},
                {"name": "permalink", "type": "attribute", "attribute": "permalink"},
                {"name": "content_href", "type": "attribute", "attribute": "content-href"},
            ]
    }
        
    reddit_scroll_config = VirtualScrollConfig(
        scroll_count=math.ceil(num_posts / 2),
        wait_after_scroll=2.0,
        scroll_by="page_height",
        container_selector="shreddit-feed",
    )

    browser_conf = BrowserConfig(
        headless=True,
        verbose=True,
        proxy_config=os.getenv("PROXY_API_KEY"),
        text_mode=True,  # Tells crawl4ai to skip loading images/media
    )
    
    strategy = JsonCssExtractionStrategy(schema, verbose=True)
    
    async with AsyncWebCrawler(config=browser_conf) as redditcrawler:
        run_config = CrawlerRunConfig(virtual_scroll_config=reddit_scroll_config, extraction_strategy=strategy)
        result = await redditcrawler.arun(url=subreddit_url, config=run_config)
        if not result.success:
            return {"error": f"Failed to scrape {subreddit_url}", "status": 500}

        # Parse JSON string to list
        posts = json.loads(result.extracted_content) if result.extracted_content else []

        return {
                "status": "success",
                "source_url": subreddit_url,
                "post_count": len(posts),
                "posts": posts,
        }
