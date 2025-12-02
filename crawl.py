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
                {"name": "created_timestamp", "type": "attribute", "attribute": "created-timestamp"},
            ],
            "fields": []
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
        text_mode=True, 
    )
    
    strategy = JsonCssExtractionStrategy(schema, verbose=True)
    
    async with AsyncWebCrawler(config=browser_conf) as redditcrawler:
        run_config = CrawlerRunConfig(
            virtual_scroll_config=reddit_scroll_config,
            extraction_strategy=strategy,
            excluded_tags=["img", "video", "source", "picture", "iframe", "svg"]
        )
        result = await redditcrawler.arun(url=subreddit_url, config=run_config)
        if not result.success:
            return {"error": f"Failed to scrape {subreddit_url}", "status": 500}


        posts = json.loads(result.extracted_content) if result.extracted_content else []

        return {
                "status": "success",
                "source_url": subreddit_url,
                "post_count": len(posts),
                "posts": posts,
        }

async def postcrawl(post_link, comment_limit=10):
    if "?" in post_link:
        post_link += "&sort=top"
    else:
        post_link += "?sort=top"

    flatten_shadow_dom_js = """
    (async function() {
        // First, scroll down to trigger lazy-loading of comments
        console.log('Scrolling to trigger comment loading...');
        window.scrollTo(0, document.body.scrollHeight);
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Scroll back up a bit to ensure comment tree is in viewport
        window.scrollTo(0, document.body.scrollHeight / 2);
        await new Promise(resolve => setTimeout(resolve, 500));

        // Now flatten Shadow DOM
        function getShadowDomHtml(shadowRoot) {
            let shadowHTML = '';
            for (const el of shadowRoot.childNodes) {
                shadowHTML += el.nodeValue || el.outerHTML || '';
            }
            return shadowHTML;
        }

        function replaceShadowDomsRecursively(rootElement) {
            const elements = rootElement.querySelectorAll('*');
            for (const el of elements) {
                if (el.shadowRoot) {
                    replaceShadowDomsRecursively(el.shadowRoot);
                    el.innerHTML += getShadowDomHtml(el.shadowRoot);
                }
            }
        }

        replaceShadowDomsRecursively(document.body);
        console.log('Shadow DOM flattened successfully');
    })();
    """

    schema = {
            "name": "Reddit Comments",
            "baseSelector": "shreddit-comment[depth='0']",
            "baseFields": [
                {"name": "author", "type": "attribute", "attribute": "author"},
                {"name": "upvotes", "type": "attribute", "attribute": "score"},
                {"name": "created_timestamp", "type": "attribute", "attribute": "created-timestamp"},
            ],
            "fields": [
                {"name": "body", "selector": "div[slot='comment']", "type": "text"},
            ]
    }

    reddit_scroll_config = VirtualScrollConfig(
        scroll_count=math.ceil(comment_limit / 5),
        wait_after_scroll=2.0,
        scroll_by="page_height",
        container_selector="shreddit-comment-tree",
    )

    browser_conf = BrowserConfig(
        headless=True,
        verbose=True,
        proxy_config=os.getenv("PROXY_API_KEY"),
        text_mode=True,  
    )
    
    strategy = JsonCssExtractionStrategy(schema, verbose=True)

    # Wait for ANY Reddit element to load - whichever appears first
    wait_condition = """() => {
        return document.querySelector('shreddit-post') ||
               document.querySelector('shreddit-comment-tree') ||
               document.querySelector('shreddit-comment');
    }"""

    async with AsyncWebCrawler(config=browser_conf) as redditcrawler:
        run_config = CrawlerRunConfig(
            virtual_scroll_config=reddit_scroll_config,
            extraction_strategy=strategy,
            js_code=flatten_shadow_dom_js,
            wait_for=f"js:{wait_condition}",
            wait_for_timeout=20000,  # 20s timeout
            page_timeout=30000,
            excluded_tags=["img", "video", "source", "picture", "iframe", "svg"]
        )

        try:
            result = await redditcrawler.arun(url=post_link, config=run_config)


            if not result.success or not result.extracted_content:
                return {
                    "status": "success",
                    "source_url": post_link,
                    "comment_count": 0,
                    "comments": [],
                    "note": "Post may not exist or failed to load"
                }

         
            comments = json.loads(result.extracted_content) if result.extracted_content else []

            return {
                "status": "success",
                "source_url": post_link,
                "comment_count": len(comments),
                "comments": comments,
            }
        except Exception as e:
            return {
                "status": "success",
                "source_url": post_link,
                "comment_count": 0,
                "comments": [],
                "note": f"Failed to load post: {str(e)}"
            }
