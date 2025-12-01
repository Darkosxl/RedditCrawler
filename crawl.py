import asyncio
import requests
from crawl4ai import LLMConfig, AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig, AdaptiveCrawler, AdaptiveConfig, VirtualScrollConfig
import dotenv
import os
import math
from scrapeops_python_requests.scrapeops_requests import ScrapeOpsRequests

scrapeops_logger =  ScrapeOpsRequests(
                      scrapeops_api_key= 'c05e7246-4ab0-4d43-9457-c80e85631786', 
                      spider_name='Scraping Amazon',
                      job_name='Clothing Section',
                    )

request = scrapeops_logger.RequestsWrapper()
dotenv.load_dotenv()

async def subredditcrawl(subreddit_url, num_posts):
    reddit_scroll_config = VirtualScrollConfig(
         scroll_count=math.ceil(num_posts / 4),
         wait_after_scroll=2.0,
         scroll_by="page_height",
         container_selector = "shreddit-feed"
    )
    
    browser_conf = BrowserConfig(
            headless=True,
            verbose=True,
            proxy_config=os.getenv("PROXY_API_KEY"),
            text_mode=True,   # Tells crawl4ai to skip loading images/media
    )
        
    async with AsyncWebCrawler(config=browser_conf) as redditcrawler:
        run_config = CrawlerRunConfig(
            virtual_scroll_config=reddit_scroll_config
        )
        
        result = await redditcrawler.arun(url=subreddit_url, config=run_config)
        if not result.success:
                    return {"error": f"Failed to scrape {subreddit_url}", "status": 500}
        return {
                    "status": "success",
                    "source_url": subreddit_url,
                    "character_count": len(result.markdown),
                    "content": result.markdown  # <--- THIS is what your LLM needs
                }

if __name__ == "__main__":
    # Example usage
    data = asyncio.run(subredditcrawl(
        subreddit_url="https://www.reddit.com/r/smallbusiness/", 
        num_posts=10, 
    ))
    
    # Prove that we got the data back
    print(f"Returned data length: {len(data['content'])}")