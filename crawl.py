import asyncio

from crawl4ai import AsyncWebCrawler, BrowserConfig, CacheMode, CrawlerRunConfig


async def main():
    browser_conf = BrowserConfig(headless=True)
    run_conf = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun(url="", config=run_conf)


if __name__ == "__main__":
    asyncio.run(main())
