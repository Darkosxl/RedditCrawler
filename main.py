import asyncio
import os

from apify import Actor
from crawl import subredditcrawl, postcrawl


async def main() -> None:
    async with Actor:
        actor_input = await Actor.get_input() or {}
        
        # Set proxy config as environment variable for crawl.py to use
        proxy_config = actor_input.get("proxy_config")
        if proxy_config:
            os.environ["PROXY_API_KEY"] = proxy_config
            Actor.log.info("Using provided proxy configuration")
        
        post_urls = actor_input.get("post_urls", [])
        subreddit = actor_input.get("subreddit")
        
        # Auto-detect mode: if post_urls are provided, crawl comments; otherwise crawl subreddit posts
        if post_urls:
            Actor.log.info(f"Starting Reddit crawler in 'post' mode - crawling {len(post_urls)} post(s)")
            
            comment_limit = actor_input.get("comment_limit", 10)
            
            for post_url in post_urls:
                Actor.log.info(f"Crawling post: {post_url} for up to {comment_limit} comments")
                
                result = await postcrawl(post_url, comment_limit)
                
                for comment in result.get("comments", []):
                    await Actor.push_data({
                        "type": "comment",
                        "source_url": result.get("source_url", post_url),
                        **comment
                    })
                
                Actor.log.info(f"Successfully extracted {result.get('comment_count', 0)} comments from {post_url}")
                
        elif subreddit:
            url = f"https://www.reddit.com/r/{subreddit}/"
            num_posts = actor_input.get("num_posts", 10)
            
            Actor.log.info(f"Starting Reddit crawler in 'subreddit' mode")
            Actor.log.info(f"Crawling subreddit: {subreddit} for {num_posts} posts")
            
            result = await subredditcrawl(url, num_posts)
            
            if "error" in result:
                Actor.log.error(result["error"])
                raise RuntimeError(result["error"])
            
            for post in result.get("posts", []):
                await Actor.push_data({
                    "type": "post",
                    "source_url": result.get("source_url", url),
                    **post
                })
            
            Actor.log.info(f"Successfully extracted {result.get('post_count', 0)} posts")
            
        else:
            raise ValueError("Please provide either a 'subreddit' name or 'post_urls'")


if __name__ == "__main__":
    asyncio.run(main())