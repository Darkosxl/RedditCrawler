import asyncio
from apify import Actor
from crawl import subredditcrawl, postcrawl


async def main():
    async with Actor:
        input = await Actor.get_input() or {}
        
        post_urls = input.get("post_urls", [])
        subreddit = input.get("subreddit")

        # Auto-detect mode: if post_urls are provided, crawl comments; otherwise crawl subreddit posts
        if post_urls:
            for post_url in post_urls:
                Actor.log.info(f"Crawling comments from: {post_url}")
                result = await postcrawl(
                    post_url,
                    input.get("comment_limit", 10)
                )
                for comment in result.get("comments", []):
                    await Actor.push_data(comment)
        elif subreddit:
            url = f"https://www.reddit.com/r/{subreddit}/"
            result = await subredditcrawl(url, input.get("num_posts", 10))
            for post in result.get("posts", []):
                await Actor.push_data(post)
        else:
            Actor.log.error("Please provide either a 'subreddit' name or 'post_urls'")


asyncio.run(main())
